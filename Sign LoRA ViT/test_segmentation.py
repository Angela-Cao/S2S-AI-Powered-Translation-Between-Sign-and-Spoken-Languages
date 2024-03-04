import preprocessing.video_to_csv_asllrp
import preprocessing.pose_to_img_2
from  segmentation_using_classifier import Segmentation
import os
import numpy as np
import timm
from base_vit import ViT
from lora import LoRA_ViT_timm, LoRA_ViT
from nltk.translate.bleu_score import sentence_bleu
import torch
from PIL import Image
import torch
from einops import rearrange
from PIL import Image
import random
from torchvision.transforms import Resize
import matplotlib.pyplot as plt
import random
import shutil
import csv
import pandas as pd

def create_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # Create the folder if it doesn't exist
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")



def preprocess_images(source_dir):    
    id2label = {}
    k = 0        
    for class_folder in os.listdir(source_dir):
        id2label[k] = class_folder                
        k = k+1
    return  id2label

def make_bar_plot(probabilities, names, true_class_label):
    bars = plt.bar(names, probabilities, color='blue')
    plt.xlabel('Categories')
    plt.ylabel('Probabilities')
    plt.title('True class: '+true_class_label)
    for bar, prob in zip(bars, probabilities):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f'{prob:.2f}', ha='center', va='bottom')
    plt.ylim(0, 1.02)
    plt.show()


def randomly_pick_files(folder_path, num_gloss):
    # Get a list of subdirectories (subfolders) in the specified folder
    subfolders = [subfolder for subfolder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subfolder))]
        
    picked_file = np.unique(random.sample(subfolders, num_gloss))

    return picked_file

def copy_and_rename_files(input_folders, output_folder):
    # Ensure the output folder exists or create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    file_path_list = []   
    for input_folder in input_folders:
        # Get the subfolder name
        subfolder_name = os.path.basename(input_folder)

        # Get a list of files in the subfolder
        files = [f.name for f in os.scandir(input_folder) if f.is_file()]

        for file_name in files:
            # Form the new file name based on the format 'old_subfolder_name_original_file_name'
            new_file_name = f"{subfolder_name}_{file_name}"

            # Build the source and destination paths
            source_path = os.path.join(input_folder, file_name)
            destination_path = os.path.join(output_folder, new_file_name)
            file_path_list.append(destination_path)
            # Copy the file to the output folder with the new name
            shutil.copy(source_path, destination_path)
    return file_path_list


model = timm.create_model("vit_base_patch16_224", pretrained=True)
rank = 4
num_classes = 2002
lora_model = LoRA_ViT_timm(model, r=rank, num_classes=num_classes)

lora_path = "../results/20240228_114648_epoch10.safetensors"
lora_model.load_lora_parameters(lora_path)
data_path='../data/WLASL_pngs_organized'


id2label = preprocess_images(data_path)
# Generating label2id from id2label
label2id = {label: id for id, label in id2label.items()}


base_dir =  "../Experiments/100Sentence_Length10_50Particles_Nstep20/"
folder_path = "../data/WLASL_pngs"
create_folder(base_dir)

rows = []
n_sentence = 10

for repeat in range(0,100):
    subfolders  = randomly_pick_files(folder_path, n_sentence)
    subfolder_path_list = [os.path.join(folder_path, item) for item in subfolders]
    gloss_list = subfolders
    out_dir = os.path.join(base_dir, "".join(gloss_list))    
    create_folder(out_dir)
    # Given the video path, export to keypoints csv files
    idx = "".join(gloss_list)
    output_file =out_dir 
    n_class = 2002
    combined_png_temp_dir = os.path.join(out_dir,str(idx)+"_combined_png")
    create_folder(combined_png_temp_dir)
    png_temp_folder = os.path.join(out_dir,str(idx)+"_temp_pngs")
    create_folder(png_temp_folder)
    csv_path = output_file
    png_temp_folder = out_dir 
    num_particles = 50
    n_class = 2002
    png_folder = os.path.join(png_temp_folder,str(idx))
    list_gloss_positive_prob = gloss_list
    list_gloss_positive_prob = [i.lower().split("_")[0] for i in list_gloss_positive_prob]
    png_file_path_list = copy_and_rename_files(subfolder_path_list, png_folder)
    true_label = list_gloss_positive_prob
    nstep = 20
    segmentation_model = Segmentation(lora_model, true_label, csv_path, png_file_path_list, combined_png_temp_dir,n_class,num_particles,id2label, label2id, list_gloss_positive_prob, nstep)
    segmentation_model.segment([0 for i in range(num_particles)])
    print(list_gloss_positive_prob)
    class_label_list, cutoff_list, prob_list = segmentation_model.getResult()
    pred = segmentation_model.pred()
    print(pred)
    print(list_gloss_positive_prob)
    score = sentence_bleu([list_gloss_positive_prob], pred)
    print(score)
    new_row = {'folder':out_dir, 'num_particles':num_particles, 'nstep':nstep, 'list_gloss_positive_prob':",".join(list_gloss_positive_prob), 'pred':",".join(pred), 'bleu':score}
    rows.append(new_row)
    class_label_csv = os.path.join(out_dir,"class_label.csv") 
    with open(class_label_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(class_label_list)
    
    cutoff_list_csv = os.path.join(out_dir,"cutoff_list.csv") 
    with open(cutoff_list_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(cutoff_list)
    
    prob_list_csv = os.path.join(out_dir,"prob_list.csv")     
    with open(prob_list_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(prob_list)
    text_file_path = os.path.join(out_dir, "pred.txt") 
    
    with open(text_file_path, mode='w') as file:
        file.write(','.join(map(str, list_gloss_positive_prob)) + '\n')
        file.write(','.join(map(str, pred)) + '\n')

from datetime import datetime
current_time = datetime.now().strftime("%Y%m%d%H%M%S")
csv_file_path = os.path.join(base_dir, f"pred_true_{current_time}.csv")
df = pd.DataFrame(rows)
df.to_csv(csv_file_path, index=False)
print(f"CSV file '{csv_file_path}' has been created.")
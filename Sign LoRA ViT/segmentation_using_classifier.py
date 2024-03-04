import csv
import math
import os
import random
import numpy as np
import os
from  utils.segmentation_sentence_utils import  frame_list_by_cutpoints, illustrate_propose_next_cutoff_points
from preprocessing.csv2png_asllrp import generate_image_for_frame, combine_images

import torch
from PIL import Image
import os
import numpy as np
import torch
from einops import rearrange
from PIL import Image
import random
from torchvision.transforms import Resize

from nltk.translate.bleu_score import sentence_bleu

import torch
from PIL import Image
from transformers import ViTFeatureExtractor, ViTForImageClassification

import os

from statistics import mode

def find_mode(word_list):
    try:
        # Find the mode of the list
        mode_word = mode(word_list)
        return mode_word
    except StatisticsError:
        # Handle the case where there is no unique mode
        return None
    
# Get a list of all files in the folder
def list_files(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    return files


def list_file_paths(folder_path):
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    return file_paths


def top_k_indices(weight_list, k):
    weight_matrix = np.array(weight_list)
    flat_indices = np.argpartition(weight_matrix.flatten(), -k)[-k:]
    rows, cols = np.unravel_index(flat_indices, weight_matrix.shape)
    indices_with_values = list(zip(rows, cols, weight_matrix[rows, cols]))
    sorted_indices = sorted(indices_with_values, key=lambda x: x[2], reverse=True)
    result_dict = {(row, col): weight for row, col, weight in sorted_indices}
    return result_dict


def sample_from_probability_dict(probability_dict, num_samples=3):
    keys, probabilities = zip(*probability_dict.items())
    probabilities = np.array(probabilities) / np.sum(probabilities)
    sampled_indices = np.random.choice(len(keys), size=num_samples, replace=True, p=probabilities)
    sampled_items = [keys[index] for index in sampled_indices]
    return sampled_items

def weight_list_to_row_col(weight_list, num_samples=1):
    weight_matrix = np.array(weight_list)
    flat_weights = weight_matrix.flatten()
    sampled_indices = np.random.choice(len(flat_weights), size=num_samples, replace=True, p=flat_weights / np.sum(flat_weights))
    rows, cols = np.unravel_index(sampled_indices, weight_matrix.shape)
    indices_with_values = list(zip(rows, cols, weight_matrix[rows, cols]))
    return indices_with_values




class Segmentation:
    # Constructor method
    def __init__(self, model, true_label, csv_path, png_file_path_list, combined_png_temp_dir,n_class,num_particles,id2label, label2id, list_gloss_positive_prob=None, nstep=10):
        self.model = model
        self.true_label = [i for i in true_label], 
        self.csv_path = csv_path
        self.png_file_list = png_file_path_list
        self.combined_png_temp_dir = combined_png_temp_dir
        self.frame_numbers =  range(len(self.png_file_list) ) 
        self.n_class = n_class
        self.num_particles = num_particles
        self.class_label_list = []
        self.cutoff_list = []
        self.prob_list = []
        self.id2label=id2label
        self.label2id=label2id
        self.list_gloss_positive_prob = list_gloss_positive_prob
        self.nstep = nstep
        self.pred_label = []

    # Function to propose the next state and cutoff point
    def propose_next_particles(self):
        return [[next_state, random.randint(3, 5)] for next_state in range(0, self.n_class)]   # replace this proposal to be a two step proposal


    def cutoff_to_probability(self,  previous_cutoff, next_cutoff):
        cutoff_points = [[previous_cutoff[l],next_cutoff[l]] for l in range(0, self.num_particles)]     # cutoff_points defines the video clips for the next gloss. generate num_particles cutoff points        
        out_sample_frames = frame_list_by_cutpoints(self.frame_numbers, cutoff_points)     # get the list of sampled frames between the prevous cutoff point to the next cutoff pont. 
        k = 0
        combined_png_list = []                            # The sampled frames will be combined as one png file and saved in this combined_png_list
        for frameNumber in out_sample_frames:    
            output_image_paths_png = [self.png_file_list[idx] for idx in frameNumber]   # get the pngs for the selected frames. 
            part_name="_".join([str(num) for num in frameNumber])                      
            output_combined_png = os.path.join(self.combined_png_temp_dir, str(previous_cutoff[k])+"combined"+str(k)+part_name+".png")    # combine png file name
            k = k + 1      
            combine_images(output_image_paths_png, output_combined_png)                  # combine the png files and save it to output_combined_png
            combined_png_list.append(output_combined_png)     # add this combined png file to the combined png list. 
        prob_list = []                 # initialize the empty list to save the probabilities 
        for test_image in combined_png_list:    # for each image in the combined png list                   
            resize = Resize([224, 224])
            image = np.array(Image.open(test_image).convert("RGB")).astype(np.float32) / 255.0
            image = rearrange(torch.tensor(image, dtype=torch.float32), 'h w c -> c h w')
            image = resize(image)
            logits = self.model(image.unsqueeze(0))                
            # Apply softmax to get probabilities
            probabilities = torch.nn.functional.softmax(logits, dim=1)                            
            prob_list.append(probabilities[0].tolist())    
        return(prob_list)    
    
    def likelihood_2(self, previous_cutoff_list, cutoff_points):    
        obs_likelihood = []
        for i in range(0, len(cutoff_points)):          
            obs_likelihood.append(self.cutoff_to_probability(previous_cutoff_list[i], cutoff_points[i]))        
        return obs_likelihood
    
    def likelihood(self,previous_cutoff, cutoff_points):                
        return self.cutoff_to_probability(previous_cutoff, cutoff_points)
        
    def segment(self, previous_cutoff):
        number_png = len(self.png_file_list)
        step = max(int(number_png/self.nstep),1)
        # SMC iteration, each one determines one class/gloss            
        # currently maximum 100 iterations. 
        for iter in range(0,100):                          
            print(f"Running iteration {iter}")
            print(f"Proposing the next cutoff point from {step} and {2*step}")
            next_cutoff_points = [point + np.random.randint(step,2*step) for point in previous_cutoff]           
            next_cutoff_points = [min(item,number_png-1) for item in next_cutoff_points]   # to avoid the potential out of range error. TODO: check if this is necessary            
            count_of_reaching_end = len([item for item in next_cutoff_points if item ==(number_png-1)])
            if count_of_reaching_end == self.num_particles:    # count how many proposals have reached the last frame of the video
                break
            weight_list = self.likelihood(previous_cutoff, next_cutoff_points)         # compute the weights for the new cutted video clips 
            samples = weight_list_to_row_col(weight_list, self.num_particles)
            class_label = [self.id2label[onesample[1]] for onesample in samples]
            self.pred_label.append(find_mode(class_label))
            previous_cutoff = [next_cutoff_points[onesample[0]] for onesample in samples]
            probs = [onesample[2] for onesample in samples]            
            self.class_label_list.append(class_label)
            self.cutoff_list.append(previous_cutoff)            
            self.prob_list.append(probs)

    def clean_pred(self):
    # Remove consecutive duplicates
        word_list = self.pred_label
        self.pred_label = [word_list[0]] + [word for prev_word, word in zip(word_list, word_list[1:]) if prev_word != word]
        return self.pred_label


    def showresult(self):
        print(self.class_label_list)
        print(self.cutoff_list)
        print(self.prob_list)

    def bleu(self):
        print(self.true_label)
        print(self.pred_label)        
        score = sentence_bleu([self.true_label], self.pred_label)
        print('BLEU score -> {}'.format(score))    
        self.clean_pred()
        print(self.true_label)
        print(self.pred_label)        
        score = sentence_bleu([self.true_label], self.pred_label)
        print('BLEU score -> {}'.format(score))    
        return score

    def getResult(self):
        return([self.class_label_list, self.cutoff_list, self.prob_list])
    def pred(self):
        self.clean_pred()
        return(self.pred_label)





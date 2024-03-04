import os
import shutil
import random

source_folder_path = "/Users/angelacao/S2S/data/classifier_data"

destination_folder_path = "/Users/angelacao/S2S/data/600"

all_subfolders = [f for f in os.listdir(source_folder_path) if os.path.isdir(os.path.join(source_folder_path, f))]

selected_subfolders = random.sample(all_subfolders, 600)

if not os.path.exists(destination_folder_path):
    os.makedirs(destination_folder_path)

for subfolder in selected_subfolders:
    source_subfolder_path = os.path.join(source_folder_path, subfolder)
    destination_subfolder_path = os.path.join(destination_folder_path, subfolder)
    shutil.copytree(source_subfolder_path, destination_subfolder_path)

print("Folders copied successfully.")

import pandas as pd
import numpy as np
import os
import svgwrite
from PIL import Image
import os
import subprocess

import os
import random
from PIL import Image


def combine_images(image_list, outputfile):

    num_images = len(image_list)
    image1 = Image.open(image_list[0])
    image2 = Image.open(image_list[1])
    image3 = Image.open(image_list[2])
    if num_images>=4:
        image4 = Image.open(image_list[3])
    else:
        image4 = image3

    width, height = image1.size

    combined_width = 2 * width
    combined_height = 2 * height
    combined_image = Image.new('RGBA', (combined_width, combined_height), (255, 255, 255, 0))

    combined_image.paste(image1, (0, 0))
    combined_image.paste(image2, (width, 0))
    combined_image.paste(image3, (0, height))    
    combined_image.paste(image4, (width, height))
    
    directory = os.path.dirname(outputfile)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if combined_image.mode != 'RGB':
        combined_image = combined_image.convert('RGB')
    combined_image.save(outputfile)



import math

def combine_and_save_images(folder_path, output_dir):
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        subfolder_name = os.path.basename(subfolder_path)
        gloss_name = subfolder_name.split("_")[0]
        output_directory = os.path.join(output_dir, gloss_name)
        os.makedirs(output_directory, exist_ok=True)
        
        if os.path.isdir(subfolder_path):
            png_files = [os.path.join(subfolder_path, file) for file in os.listdir(subfolder_path) if file.lower().endswith('.png')]
            n_png_files = len(png_files)  
            if n_png_files >= 2:
                for i in range(4):
                    random_numbers = [random.uniform(0, 0.25), random.uniform(0.25, 0.5), random.uniform(0.5, 0.75), random.uniform(0.75, 1)]                
                    rounded_positions = [math.floor(pos * n_png_files) for pos in random_numbers]
                    selected_files = [png_files[i] for i in rounded_positions]
                    output_filename = f"{subfolder}_sample_{i}.png"
                    output_path = os.path.join(output_directory, output_filename)
                    combine_images(selected_files, output_path)
                



import os
if __name__ == "__main__":    
    
    # # Replace '/path/to/WLASL_pngs' with the actual path to your main folder
    # main_folder_path = '../data/WLASL_pngs'
    # output_dir = '../data/WLASL_pngs_organized'
    # combine_and_save_images(main_folder_path, output_dir)
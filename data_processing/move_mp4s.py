import os
import shutil

def move_mp4_files(source_folder, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".mp4"):
                source_path = os.path.join(root, file)
                target_path = os.path.join(target_folder, file)
                shutil.move(source_path, target_path)
                print(f"Moved: {source_path} to {target_path}")

source_folder = '/Users/angelacao/S2S/data/S2S'
target_folder = '/Users/angelacao/S2S/data/mp4s'

move_mp4_files(source_folder, target_folder)

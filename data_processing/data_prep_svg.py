import os
import shutil

def rename_and_organize(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".svg"):
                subfolder_name = os.path.basename(root)
                path_elements = root.split(os.path.sep)
                
                svg_index = path_elements.index("SVGs")
                
                subfolder_run_frame = path_elements[svg_index + 1]
                
                frame_number = file.split('_')[-1].split('.')[0]

                folder_path = os.path.join(output_folder, subfolder_run_frame)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                subfolder_run_frame = "_".join(path_elements[svg_index+2:])

                new_name = f"{subfolder_run_frame}_frame_{frame_number}.svg"
                new_path = os.path.join(folder_path, new_name)

                old_path = os.path.join(root, file)
                shutil.copy(old_path, new_path)

if __name__ == "__main__":
    input_folder = "/Users/angelacao/S2S/data/SVGs" 
    output_folder = "/Users/angelacao/S2S/data/SVGs_org" 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    rename_and_organize(input_folder, output_folder)

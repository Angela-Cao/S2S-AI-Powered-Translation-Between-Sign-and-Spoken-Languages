import os

def read_expected_folders(expected_folder_path):
    expected_folders = {}

    for subfolder in os.listdir(expected_folder_path):
        subfolder_path = os.path.join(expected_folder_path, subfolder)
        if os.path.isdir(subfolder_path):
            expected_folders[subfolder] = set(os.listdir(subfolder_path))

    return expected_folders

def find_extra_folders(parent_folder, expected_folder_path):
    expected_folders = read_expected_folders(expected_folder_path)
    
    extra_folders = {}
    
    for subfolder, subfolder_expected_folders in expected_folders.items():
        subfolder_path = os.path.join(parent_folder, subfolder)
        
        if os.path.exists(subfolder_path) and os.path.isdir(subfolder_path):
            actual_subfolders = set(os.listdir(subfolder_path))
            
            extra_subfolders = actual_subfolders - subfolder_expected_folders
            if extra_subfolders:
                extra_folders[subfolder] = list(extra_subfolders)

    return extra_folders

if __name__ == "__main__":
    parent_folder = "/Users/angelacao/S2S/data/SVGs"  # Replace this with the actual path to your parent folder
    expected_folder_path = "/Users/angelacao/S2S/data/splits"  # Replace with the actual path to the folder containing subfolders with expected folders

    extra_folders = find_extra_folders(parent_folder, expected_folder_path)

    if not extra_folders:
        print("No extra folders found.")
    else:
        print("Extra folders:")
        for subfolder, extra_subfolders in extra_folders.items():
            print(f"{subfolder}: {', '.join(extra_subfolders)}")

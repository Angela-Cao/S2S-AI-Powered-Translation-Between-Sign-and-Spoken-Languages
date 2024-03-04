import os
import shutil
def remove_subfolders(directory):
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' not found.")
        return

    subfolders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

    for subfolder in subfolders:
        subfolder_path = os.path.join(directory, subfolder)
        try:
            shutil.rmtree(subfolder_path)
            print(f"Removed subfolder: {subfolder_path}")
        except Exception as e:
            print(f"Error removing subfolder {subfolder_path}: {e}")

if __name__ == "__main__":
    target_directory = "/Users/angelacao/S2S/data/top50"

    remove_subfolders(target_directory)

import os
import shutil

def count_items_in_folder(folder_path):
    try:
        item_count = sum([len(files) for _, _, files in os.walk(folder_path)])
        return item_count
    except Exception as e:
        print(f"Error counting items in folder {folder_path}: {e}")
        return 0

def top_subfolders(folder_path, top_count):
    subfolders = [(subfolder, count_items_in_folder(os.path.join(folder_path, subfolder))) for subfolder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subfolder))]
    top_subfolders = sorted(subfolders, key=lambda x: x[1], reverse=True)[:top_count]
    return top_subfolders

def group_top_subfolders(svg_folder, output_folder, top_count):
    top_subfolders_result = top_subfolders(svg_folder, top_count)
    for subfolder, _ in top_subfolders_result:
        src_path = os.path.join(svg_folder, subfolder)
        dest_path = os.path.join(output_folder, subfolder)
        shutil.copytree(src_path, dest_path)

if __name__ == "__main__":
    svg_folder_path = "/Users/angelacao/S2S/data/SVGs_org"  
    top_folder_path = "/Users/angelacao/S2S/data/top50_svg"
    top_count = 50

    if not os.path.exists(top_folder_path):
        os.makedirs(top_folder_path)

    group_top_subfolders(svg_folder_path, top_folder_path, top_count)

    print(f"Top {top_count} subfolders copied to {top_folder_path}.")

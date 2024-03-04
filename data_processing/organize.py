import os
import shutil

input_folder = '/Users/angelacao/S2S/data/csvs_V2'
output_folder = '/Users/angelacao/S2S/data/CSVs'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def format_csv_name(csv_file):
    csv_file = csv_file.replace("_default_id", "")

    parts = csv_file.split()

    if len(parts) > 1:
        return parts[0] + parts[1].capitalize()
    else:
        return csv_file

csv_files = [file for file in os.listdir(input_folder) if file.endswith(".csv")]

for i, csv_file in enumerate(csv_files):
    base_name = format_csv_name(csv_file[:-4])  
    new_name = f"{base_name}.csv" 
    destination_path = os.path.join(output_folder, new_name)
    source_path = os.path.join(input_folder, csv_file)
    shutil.copy(source_path, destination_path)

print("Dataset organized successfully!")

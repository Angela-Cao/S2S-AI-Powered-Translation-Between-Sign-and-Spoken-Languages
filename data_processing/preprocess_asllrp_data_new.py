
import pandas as pd
import os
from video_to_csv_asllrp import video2csv
from pose_to_img_2 import keypoints_to_png


# Read the CSV file
asllrp = pd.read_csv("../data/ASLLRPdataAccess/asllrp_sentence_signs_2023_06_29.csv")


# Get unique utterances
unique_utterance = asllrp['Utterance video filename'].unique()
print(len(unique_utterance))  # Print the number of unique utterances (length)

uniqueGloss = asllrp['Main entry gloss label'].unique()

unique_gloss_list = uniqueGloss.tolist()

# Create a dictionary to store results
result_dict = {}

# Iterate through unique gloss labels
for gloss in unique_gloss_list:
    result = list(asllrp.loc[asllrp['Main entry gloss label'] == gloss, "Sign video filename"].values)
    print(result)
    result_dict[gloss] = result

top_gloss = [key for key in result_dict.keys() if len(result_dict.get(key))>5]


video_dir = "../data/ASLLRPdataAccess/batch_signs_v1_1"
out_dir = "../data/ASLLRP518/keypoints_pngs"
for i in range(0,len(top_gloss)):
    try:
        folder_path = os.path.join(out_dir,top_gloss[i])
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created.")
        for v_f in result_dict.get(top_gloss[i]):         
            try:
                video_path = os.path.join(video_dir, v_f)
                csv_file = os.path.join(folder_path, f"{v_f}_keypoints.csv")   
                video2csv(video_path, csv_file)            # convert the mp4 video file to a csv file
                keypoints_to_png(csv_file, folder_path)
            except Exception as e:
                continue                         
    except Exception as e:
        print(top_gloss[i])        
        # Continue with the next iteration of the loop
        continue

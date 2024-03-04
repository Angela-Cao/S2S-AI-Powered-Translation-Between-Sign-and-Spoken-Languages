import os
import re
import cv2

import subprocess

from peft import PeftModel, PeftConfig
from transformers import AutoModelForSeq2SeqLM, BartTokenizer
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

config = PeftConfig.from_pretrained("angelacao/asl_spoken")

model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large")
model = PeftModel.from_pretrained(model, "angelacao/asl_spoken")
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")



import os
import glob

from moviepy.editor import VideoFileClip, concatenate_videoclips

def concatenate_clips(video_paths, output_path):
    clips = [VideoFileClip(path) for path in video_paths]
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    final_clip.close()


def identify_combined_pairs(folder_path, input_sentence):
    # Get a list of all video files in the folder
    video_files = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]

    # Extract combined pairs and their corresponding two words from the video files
    combined_pairs_and_words = {}
    for video_file in video_files:
        # Check if the file name contains a capitalized letter
        if any(char.isupper() for char in video_file):
            # Extract words from the combined pair
            words = re.findall(r'[A-Za-z][a-z]*', os.path.splitext(video_file)[0])
            combined_pairs_and_words[video_file] = words

    # Use a sliding window to check for combined pairs in the input sentence
    input_words = input_sentence.split()
    identified_pairs = []
    individual_words = []

    i = 0
    while i < len(input_words):
        pair = None
        for j in range(2, 0, -1):
            if i + j <= len(input_words):
                current_pair = ' '.join(input_words[i:i + j])
                if current_pair.lower() in [' '.join(words).lower() for words in combined_pairs_and_words.values()]:
                    identified_pairs.append(current_pair)
                    i += j
                    pair = current_pair
                    break

        if pair is None:
            individual_words.append(input_words[i].lower())
            i += 1

    return combined_pairs_and_words, identified_pairs, individual_words


def play_video(video_file, video_type, folder_path):
    if video_type == 'combined':
        video_files = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]
    elif video_type == 'individual':
        video_name = os.path.splitext(video_file)[0]
        video_files = [f for f in os.listdir(folder_path) if f.startswith(video_name + '_')]

    if not video_files:
        print(f"Video not found for {video_file}.")
        return None

    played_paths = []

    # Assuming you want to play the first video in the list
    video_path = os.path.join(folder_path, video_files[0])
    print(f"Opening video: {video_path}")

    while True:
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow('Video Player', frame)

            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        # Break after playing once for both combined pairs and individual words
        break

    return video_path  # Return the video path

if __name__ == "__main__":
    folder_path = "/Users/angelacao/S2S/data/skeletons"

    user_input_sentence = input("Enter a spoken English sentence: ")

    sample_input_ids = tokenizer.encode(user_input_sentence, return_tensors="pt")
    output_ids = model.generate(input_ids=sample_input_ids)
    user_input_sentence_output = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    combined_pairs_and_words, identified_pairs, individual_words = identify_combined_pairs(folder_path, user_input_sentence_output)

    print(user_input_sentence_output)

    played_paths = []  # Initialize the list here
    captions = []  # Initialize captions list

    for pair in identified_pairs:
        print(pair)
        path = play_video(f"{pair.replace(' ', '_')}.mp4", video_type='combined', folder_path=folder_path)
        if path:
            played_paths.append(path)
            captions.append(pair)

    for word in individual_words:
        print(word)
        path = play_video(f"{word}.mp4", video_type='individual', folder_path=folder_path)
        if path:
            played_paths.append(path)
            captions.append(word)

    print("\nPlayed video paths:")
    for i, path in enumerate(played_paths):
        print(f"{path} - Caption: {captions[i]}")

    # Concatenate video clips
    video_clips = [VideoFileClip(path) for path in played_paths]
    final_clip = concatenate_videoclips(video_clips, method="compose")

    # Add captions to the final video
    current_time = 0

    for i, caption in enumerate(captions):
        # Calculate the width based on text length
        text_width = 150  # Adjust the multiplier as needed
        txt_clip = TextClip(caption, font='Arial', fontsize=24, color='black', bg_color='rgb(211, 211, 211)', size=(text_width, 50))
        txt_clip = txt_clip.set_pos(('center', final_clip.size[1] - 100)).set_duration(video_clips[i].duration).set_start(current_time)
        final_clip = CompositeVideoClip([final_clip, txt_clip])
        current_time += video_clips[i].duration

    # Write the final video to the output path
    final_output_path = "/Users/angelacao/S2S/production/output_video_with_captions3.mp4"
    final_clip.write_videofile(final_output_path, codec="libx264", audio_codec="aac")

    print(f"\nFinal video with captions written to: {final_output_path}")
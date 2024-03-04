import os
import re
import cv2
import streamlit as st
import sounddevice as sd
import numpy as np
import tempfile
import wave
import speech_recognition as sr  
import soundfile as sf

from peft import PeftModel, PeftConfig
from transformers import AutoModelForSeq2SeqLM, BartTokenizer
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips


folder_path = "/Users/angelacao/S2S/data/skeletons"
config_asl = PeftConfig.from_pretrained("angelacao/asl_spoken")
asl_loaded_model = AutoModelForSeq2SeqLM.from_pretrained("angelacao/asl_spoken")

model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large")
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")


config_spoken = PeftConfig.from_pretrained("angelacao/Spoken_to_ASL")
loaded_model_spoken = AutoModelForSeq2SeqLM.from_pretrained("angelacao/Spoken_to_ASL")




st.set_page_config(
    page_title="S2S 🗣",
    layout="wide"
)

def get_translation_model(source_lang):
    if source_lang.lower() == 'asl':
        return tokenizer, asl_loaded_model
    else:
        return tokenizer, loaded_model_spoken


def translate_sentence(sample_input, source_lang, target_lang, prefix=None):
    tokenizer, loaded_model = get_translation_model(source_lang)
    
    if prefix:
        sample_input = prefix + sample_input
    
    print(f"Translating from {source_lang} to {target_lang}")
    
    sample_input_ids = tokenizer.encode(sample_input, return_tensors="pt")
    output_ids = loaded_model.generate(sample_input_ids)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return output_text




def concatenate_clips(video_paths, output_path):
    clips = [VideoFileClip(path) for path in video_paths]
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    final_clip.close()



def identify_combined_pairs(folder_path, input_sentence):
    video_files = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]

    combined_pairs_and_words = {}
    for video_file in video_files:
        if any(char.isupper() for char in video_file):
            words = re.findall(r'[A-Za-z][a-z]*', os.path.splitext(video_file)[0])
            combined_pairs_and_words[video_file] = words

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
        st.error(f"Video not found for {video_file}.")
        return None

    video_path = os.path.join(folder_path, video_files[0])

    return video_path

def add_caption(video_clip, caption_text):
    text_clip = TextClip(caption_text, fontsize=24, color='white', bg_color='black', size=(video_clip.size[0], 50))
    text_clip = text_clip.set_pos(('center', 'bottom')).set_duration(video_clip.duration)
    return CompositeVideoClip([video_clip, text_clip])

def main():
    st.sidebar.title("S2S 🗣")
    st.sidebar.text("Translation Options")

    source_lang = st.sidebar.selectbox("Translate from:", ["ASL", "Spoken English"])
    
    target_lang_options = ["Spoken English", "ASL"]
    target_lang = st.sidebar.selectbox("Translate to:", options=target_lang_options, index=0 if source_lang == "ASL" else 1)

    user_input_sentence_sidebar = st.sidebar.text_area("Enter a sentence:", key="user_input_sidebar", height=300)

    if st.sidebar.button("Translate", key="translate_button_sidebar"):
        translated_sentence = translate_sentence(user_input_sentence_sidebar, source_lang, target_lang, prefix="translate ASL to spoken English: ")
        st.sidebar.write("Translated Sentence:", translated_sentence)
        print(translated_sentence)



        combined_pairs_and_words, identified_pairs, individual_words = identify_combined_pairs(folder_path, translated_sentence)

        played_paths = [] 
        captions = [] 

        for pair in identified_pairs:
            path = play_video(f"{pair.replace(' ', '_')}.mp4", video_type='combined', folder_path=folder_path)
            if path:
                played_paths.append(path)
                captions.append(pair)

        for word in individual_words:
            path = play_video(f"{word}.mp4", video_type='individual', folder_path=folder_path)
            if path:
                played_paths.append(path)
                captions.append(word)

        video_clips = []
        for path, caption_text in zip(played_paths, captions):
            clip = VideoFileClip(path)
            clip_with_caption = add_caption(clip, caption_text)
            video_clips.append(clip_with_caption)

        if video_clips:
            final_clip = concatenate_videoclips(video_clips, method="compose")

            final_output_path = "/Users/angelacao/S2S/production/output_video_with_captions3.mp4"
            final_clip.write_videofile(final_output_path, codec="libx264", audio_codec="aac")

            st.video(final_output_path)

            st.sidebar.write(f"\nFinal video with captions saved to: {final_output_path}")
        else:
            st.sidebar.warning("No video clips to concatenate")


if __name__ == "__main__":
    main()

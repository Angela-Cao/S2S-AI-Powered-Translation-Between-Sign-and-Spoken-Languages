import os
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

input_folder = '/Users/angelacao/S2S/data/mp4s'
output_base_folder = '/Users/angelacao/S2S/data/classifier_data/accent'

if not os.path.exists(output_base_folder):
    os.makedirs(output_base_folder)

def process_video(file):
    video = cv2.VideoCapture(file)
    frame_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    gloss = extract_gloss_from_filename(file)
    output_folder = os.path.join(output_base_folder, gloss)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, os.path.basename(file))
    output = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), video.get(cv2.CAP_PROP_FPS), (int(frame_width), int(frame_height)))

    print("Processing:", file)

    with mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=2,
            enable_segmentation=False,
            refine_face_landmarks=True) as holistic:

        while video.isOpened():
            success, frame = video.read()

            if not success:
                print("Ignoring empty frame")
                break

            results = holistic.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            annotated_frame = np.full((int(frame_height), int(frame_width), 3), 255, dtype=np.uint8)

            if results.face_landmarks:
                mp_drawing.draw_landmarks(
                    annotated_frame,
                    results.face_landmarks,
                    mp_holistic.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    annotated_frame,
                    results.pose_landmarks,
                    mp_holistic.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.
                    get_default_pose_landmarks_style())
            if results.right_hand_landmarks:
                mp_drawing.draw_landmarks(
                    annotated_frame,
                    results.right_hand_landmarks,
                    mp_holistic.HAND_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.
                    get_default_hand_landmarks_style())
            if results.left_hand_landmarks:
                mp_drawing.draw_landmarks(
                    annotated_frame,
                    results.left_hand_landmarks,
                    mp_holistic.HAND_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.
                    get_default_hand_landmarks_style())

            output.write(annotated_frame)

    video.release()
    output.release()

def extract_gloss_from_filename(file):
    filename_without_extension = os.path.splitext(os.path.basename(file))[0]
    gloss = filename_without_extension.split('_')[0]
    return gloss

for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.endswith(".mp4"):
            video_path = os.path.join(root, file)
            process_video(video_path)

print("Processing completed.")

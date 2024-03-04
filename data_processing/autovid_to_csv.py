import os
import cv2
import mediapipe as mp
import pandas as pd

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Set the path to the folder containing MP4 files
input_folder = '/Users/angelacao/S2S/mp42/'
# Set the path to the folder where CSVs will be saved
output_folder = '/Users/angelacao/S2S/data/csvs_V22/'

# Get a list of all MP4 files in the input folder
mp4_files = [file for file in os.listdir(input_folder) if file.endswith('.mp4')]

# Iterate through each MP4 file
for video_file in mp4_files:
    video_path = os.path.join(input_folder, video_file)
    output_csv_path = os.path.join(output_folder, f'{os.path.splitext(video_file)[0]}.csv')

    # Rest of your code remains unchanged
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        cap = cv2.VideoCapture(video_path)

        # Create an empty DataFrame to store the keypoints data
        keypoints_df = pd.DataFrame(columns=['frame_number', 'keypoint_number', 'keypoint_type', 'x', 'y', 'z'])

        frame_number = 0

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # Make Detections
            results = holistic.process(frame)

            # Extract pose landmarks
            if results.pose_landmarks:
                pose_data = [{'frame_number': frame_number,
                              'keypoint_number': idx,
                              'keypoint_type': 'pose',
                              'x': landmark.x,
                              'y': landmark.y,
                              'z': landmark.z,
                              'visibility': landmark.visibility} for idx, landmark in enumerate(results.pose_landmarks.landmark)]

                keypoints_df = pd.concat([keypoints_df, pd.DataFrame(pose_data)])

            if results.face_landmarks:
                face_data = [{'frame_number': frame_number,
                              'keypoint_number': idx,
                              'keypoint_type': 'face',
                              'x': landmark.x,
                              'y': landmark.y,
                              'z': landmark.z,
                              'visibility': landmark.visibility} for idx, landmark in enumerate(results.face_landmarks.landmark)]

                keypoints_df = pd.concat([keypoints_df, pd.DataFrame(face_data)])

            if results.right_hand_landmarks:
                right_data = [{'frame_number': frame_number,
                               'keypoint_number': idx,
                               'keypoint_type': 'right_hand',
                               'x': landmark.x,
                               'y': landmark.y,
                               'z': landmark.z,
                               'visibility': landmark.visibility} for idx, landmark in enumerate(results.right_hand_landmarks.landmark)]

                keypoints_df = pd.concat([keypoints_df, pd.DataFrame(right_data)])

            if results.left_hand_landmarks:
                left_data = [{'frame_number': frame_number,
                              'keypoint_number': idx,
                              'keypoint_type': 'left_hand',
                              'x': landmark.x,
                              'y': landmark.y,
                              'z': landmark.z,
                              'visibility': landmark.visibility} for idx, landmark in enumerate(results.left_hand_landmarks.landmark)]

                keypoints_df = pd.concat([keypoints_df, pd.DataFrame(left_data)])

            frame_number += 1

            # Recolor image back to BGR for rendering
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Draw landmarks
            mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                                      mp_drawing.DrawingSpec(color=(255, 192, 203), thickness=1, circle_radius=1),
                                      mp_drawing.DrawingSpec(color=(255, 192, 203), thickness=1, circle_radius=1))

            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2))

            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2))

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2))

            cv2.imshow('Video Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        keypoints_df.to_csv(output_csv_path, index=False)

        cap.release()
        cv2.destroyAllWindows()

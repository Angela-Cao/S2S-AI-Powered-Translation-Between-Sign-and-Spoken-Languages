import mediapipe as mp
import cv2
import pandas as pd
import random
import os
import csv


def video2csv(video_path,output_file):
    mp_holistic = mp.solutions.holistic
    mp_drawing = mp.solutions.drawing_utils

    mp_drawing.DrawingSpec(color=(240, 240, 240), thickness=2, circle_radius=3)

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        cap = cv2.VideoCapture(video_path)

        keypoints_df = pd.DataFrame(columns=['frame_number', 'keypoint_number', 'keypoint_type', 'x', 'y', 'z'])

        frame_number = 0

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # Recolor Feed
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Make Detections
            results = holistic.process(image)

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
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 1. Draw face landmarks
            mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                                  mp_drawing.DrawingSpec(color=(255, 192, 203), thickness=1, circle_radius=1),
                                  mp_drawing.DrawingSpec(color=(255, 192, 203), thickness=1, circle_radius=1),
                                  )

            # 2. Right hand
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2)
                                  )

            # 3. Left Hand
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2)
                                  )

            # 4. Pose Detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2)
                                  )

            #cv2.imshow('Video Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        keypoints_df.to_csv(output_file, index=False)

    cap.release()
    cv2.destroyAllWindows()

import math

def sample_and_export(csv_path):
    if not os.path.exists(csv_path):
        print("Error: CSV file not found.")
        return

    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')  # Update delimiter if necessary
        rows = list(csv_reader)

    header = rows[0]
    print("CSV Header:", header)
    total_rows = len(rows) - 1  # Exclude the header row
        
    random_numbers = [random.uniform(0, 0.2), random.uniform(0.2, 0.5), random.uniform(0.5, 0.8), random.uniform(0.8, 1)]
    rounded_positions = [math.floor(pos * total_rows) for pos in random_numbers]

    # Extract frame numbers corresponding to the rounded positions
    frame_numbers = [int(rows[position + 1][header.index('frame_number')]) for position in rounded_positions]
    # For your use case, you might want to return the list of frame numbers
    return frame_numbers

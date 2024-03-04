import json
import requests
import os
import mediapipe as mp
import cv2
import pandas as pd

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

mp_drawing.DrawingSpec(color=(240, 240, 240), thickness=2, circle_radius=3)

def find_urls_for_word(sentence, gloss_data):
    sentence = sentence.lower()  # Convert input to lowercase for case-insensitive comparison

    urls = []
    for word in sentence.split():
        for entry in gloss_data:
            if entry["gloss"].lower() == word:
                for instance in entry["instances"]:
                    url = instance["url"]
                    urls.append(url)

    return urls

def test_url(url):
    try:
        response = requests.head(url, timeout=10)  # Increase timeout
        return response.status_code == 200 and response.headers.get('content-type', '').startswith('video/mp4')
    except (requests.ConnectionError, requests.Timeout):
        return False

# Load the gloss data from the provided JSON file
json_path = '/Users/angelacao/S2S/data/WLASL_v0.3 .json'
with open(json_path, "r") as file:
    gloss_data = json.load(file)

# Loop through glosses
for gloss_entry in gloss_data:
    gloss_name = gloss_entry["gloss"]
    print(f"Processing videos for gloss: {gloss_name}")

    # Create a folder for each gloss
    gloss_folder = os.path.join("S2S2", gloss_name)
    os.makedirs(gloss_folder, exist_ok=True)

    # Loop through instances for each gloss
    for idx, instance in enumerate(gloss_entry.get("instances", [])):
        url = instance["url"]

        if not test_url(url):
            print(f"Skipping {url} as it is unreachable or not a valid video.")
            continue

        # Use get method to handle the potential absence of the 'id' key
        video_id = instance.get("id", f"default_id_{idx}")
        video_path = os.path.join(gloss_folder, f"{gloss_name}_{video_id}.mp4")

        # Download video
        try:
            with requests.get(url, stream=True, timeout=30) as response:
                response.raise_for_status()  # Raise an HTTPError for bad responses
                with open(video_path, "wb") as video_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        video_file.write(chunk)
        except requests.RequestException as e:
            print(f"Error downloading {url}: {e}")
            continue

        # Rest of your code for processing video to get keypoints
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            cap = cv2.VideoCapture(video_path)
            keypoints_df = pd.DataFrame(columns=['frame_number', 'keypoint_number', 'keypoint_type', 'x', 'y', 'z'])

            frame_number = 0

            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    break

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = holistic.process(image)

                # Extract keypoints and add to DataFrame
                for landmark_type in ["pose", "face", "right_hand", "left_hand"]:
                    landmarks_attr = getattr(results, f"{landmark_type}_landmarks")

                    if landmarks_attr is not None:
                        num_keypoints = len(landmarks_attr.landmark)
                        landmark_data = [{'frame_number': frame_number,
                                          'keypoint_number': idx,
                                          'keypoint_type': landmark_type,
                                          'x': landmark.x if landmarks_attr.landmark else 'N/A',
                                          'y': landmark.y if landmarks_attr.landmark else 'N/A',
                                          'z': landmark.z if landmarks_attr.landmark else 'N/A',
                                          'visibility': landmark.visibility if landmarks_attr.landmark else 'N/A'} for idx, landmark in
                                         enumerate(landmarks_attr.landmark)]
                    else:
                        # Replace missing landmarks with N/A or any other placeholder
                        num_keypoints = 0
                        landmark_data = [{'frame_number': frame_number,
                                          'keypoint_number': idx,
                                          'keypoint_type': landmark_type,
                                          'x': 'N/A',
                                          'y': 'N/A',
                                          'z': 'N/A',
                                          'visibility': 'N/A'} for idx in range(num_keypoints)]

                    keypoints_df = pd.concat([keypoints_df, pd.DataFrame(landmark_data)])

                    # Drawing part
                    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                                              mp_drawing.DrawingSpec(color=(255, 192, 203), thickness=1, circle_radius=1),
                                              mp_drawing.DrawingSpec(color=(255, 192, 203), thickness=1, circle_radius=1),
                                              )

                    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=4),
                                              mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2)
                                              )

                    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=4),
                                              mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2)
                                              )

                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=4),
                                              mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2)
                                              )

                    cv2.imshow('Video Feed', image)

                    frame_number += 1

            cap.release()

        # Save keypoints CSV file after processing the video
        keypoints_df.to_csv(os.path.join(gloss_folder, f"{gloss_name}_{video_id}.csv"), index=False)

print("Processing complete.")

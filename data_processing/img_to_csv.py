import mediapipe as mp
import cv2
import pandas as pd

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

mp_drawing.DrawingSpec(color=(240, 240, 240), thickness=2, circle_radius=3)

# Path to your image file
image_path = '/Users/angelacao/S2S/female_cousin.png'

# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    # Read the image
    image = cv2.imread(image_path)
    # Recolor image
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Make Detections
    results = holistic.process(image_rgb)

    # Create an empty DataFrame to store the keypoints data
    keypoints_df = pd.DataFrame(columns=['frame_number', 'keypoint_number', 'keypoint_type', 'x', 'y', 'z'])

    if results.right_hand_landmarks:
        right_data = [{'frame_number': 0,
                      'keypoint_number': idx,
                      'keypoint_type': 'right_hand',
                      'x': landmark.x,
                      'y': landmark.y,
                      'z': landmark.z,
                      'visibility': landmark.visibility} for idx, landmark in enumerate(results.right_hand_landmarks.landmark)]

        keypoints_df = pd.concat([keypoints_df, pd.DataFrame(right_data)])

    # Recolor image back to BGR for rendering
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    # 2. Right hand
    mp_drawing.draw_landmarks(image_bgr, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2)
                              )

    cv2.imshow('Image', image_bgr)

    keypoints_df.to_csv('keypointsss.csv', index=False)
 
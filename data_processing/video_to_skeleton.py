## Holistic Solution using Video in Python

import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic


file = '/Users/angelacao/S2S/data/S2S/honey.mp4'
video = cv2.VideoCapture(file)
frame_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("Frame size ", (frame_width, frame_height))

output = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), video.get(cv2.CAP_PROP_FPS), (int(frame_width), int(frame_height)))

print("Video FPS: ", video.get(cv2.CAP_PROP_FPS))
print("Video Frame count:", video.get(cv2.CAP_PROP_FRAME_COUNT))
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

        output.write(annotated_frame)

    video.release()

    output.release()
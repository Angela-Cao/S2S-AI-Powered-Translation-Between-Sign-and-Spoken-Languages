import mediapipe as mp
import cv2

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

mp_drawing.DrawingSpec(color=(240, 240, 240), thickness=2, circle_radius=3)

video_path = '/Users/angelacao/Downloads/raw_videos/_-adcxjm1R4_1-8-rgb_front.mp4'


with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                                  mp_drawing.DrawingSpec(color=(255, 192, 203), thickness=1, circle_radius=1),
                                  mp_drawing.DrawingSpec(color=(255, 192, 203), thickness=1, circle_radius=1),
                                  )

        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=3, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=3, circle_radius=2)
                                  )

        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=3, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=3, circle_radius=2)
                                  )

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2)
                                  )

        cv2.imshow('Video Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

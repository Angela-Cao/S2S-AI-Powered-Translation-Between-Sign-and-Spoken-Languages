POSE_CONNECTIONS = frozenset([(11, 12), (11, 13),
                              (13, 15), 
                              (12, 14), (14, 16),
                                (11, 23), (12, 24), (23, 24), (23, 25),
                              (24, 26), (25, 27), (26, 28), (27, 29), (28, 30),
                              (29, 31), (30, 32), (27, 31), (28, 32)])

POSE_CONNECTION_COLORS = {
    (12, 14): (51, 236, 255), 
    (14, 16): (83, 191, 83),   
    (11, 13): (51, 236, 255),   
    (13, 15): (83, 191, 83),   
}

HAND_PALM_CONNECTIONS = ((0, 1), (0, 5), (9, 13), (13, 17), (5, 9), (0, 17))
HAND_THUMB_CONNECTIONS = ((1, 2), (2, 3), (3, 4))
HAND_INDEX_FINGER_CONNECTIONS = ((5, 6), (6, 7), (7, 8))
HAND_MIDDLE_FINGER_CONNECTIONS = ((9, 10), (10, 11), (11, 12))
HAND_RING_FINGER_CONNECTIONS = ((13, 14), (14, 15), (15, 16))
HAND_PINKY_FINGER_CONNECTIONS = ((17, 18), (18, 19), (19, 20))

HAND_CONNECTIONS = frozenset().union(*[
    HAND_PALM_CONNECTIONS, HAND_THUMB_CONNECTIONS,
    HAND_INDEX_FINGER_CONNECTIONS, HAND_MIDDLE_FINGER_CONNECTIONS,
    HAND_RING_FINGER_CONNECTIONS, HAND_PINKY_FINGER_CONNECTIONS
])
left_hand_colors = {0: (255, 178, 102), 
                    1: (255, 178, 102),
                    2: (102, 178, 255),
                    3: (102, 178, 255),
                    4: (102, 178, 255),
                    5: (255, 178, 102),
                    6: (102, 102, 255),
                    7: (102, 102, 255),
                    8: (102, 102, 255),
                    9: (255, 178, 102),
                    10: (162, 220, 104),
                    11: (162, 220, 104),
                    12: (162, 220, 104),
                    13: (255, 178, 102),
                    14: (255, 102, 178),
                    15: (255, 102, 178),
                    16: (255, 102, 178),
                    17: (255, 178, 102),
                    18: (178, 102, 255),
                    19: (178, 102, 255),
                    20: (178, 102, 255),
                    }
right_hand_colors = {0: (255, 178, 102), 
                    1: (255, 178, 102),
                    2: (102, 178, 255),
                    3: (102, 178, 255),
                    4: (102, 178, 255),
                    5: (255, 178, 102),
                    6: (102, 102, 255),
                    7: (102, 102, 255),
                    8: (102, 102, 255),
                    9: (255, 178, 102),
                    10: (162, 220, 104),
                    11: (162, 220, 104),
                    12: (162, 220, 104),
                    13: (255, 178, 102),
                    14: (255, 102, 178),
                    15: (255, 102, 178),
                    16: (255, 102, 178),
                    17: (255, 178, 102),
                    18: (178, 102, 255),
                    19: (178, 102, 255),
                    20: (178, 102, 255),
                    }
HAND_CONNECTION_COLORS = {
    HAND_PALM_CONNECTIONS: (255, 178, 102), 
    HAND_THUMB_CONNECTIONS: (102, 178, 255),  
    HAND_INDEX_FINGER_CONNECTIONS: (102, 102, 255),
    HAND_MIDDLE_FINGER_CONNECTIONS: (162, 220, 104), 
    HAND_RING_FINGER_CONNECTIONS: (255, 102, 178),
    HAND_PINKY_FINGER_CONNECTIONS: (178, 102, 255)
}



FACEMESH_LIPS = frozenset([(61, 146), (146, 91), (91, 181), (181, 84), (84, 17),
                           (17, 314), (314, 405), (405, 321), (321, 375),
                           (375, 291), (61, 185), (185, 40), (40, 39), (39, 37),
                           (37, 0), (0, 267),
                           (267, 269), (269, 270), (270, 409), (409, 291),
                           (78, 95), (95, 88), (88, 178), (178, 87), (87, 14),
                           (14, 317), (317, 402), (402, 318), (318, 324),
                           (324, 308), (78, 191), (191, 80), (80, 81), (81, 82),
                           (82, 13), (13, 312), (312, 311), (311, 310),
                           (310, 415), (415, 308)])

FACEMESH_LEFT_EYE = frozenset([(263, 249), (249, 390), (390, 373), (373, 374),
                               (374, 380), (380, 381), (381, 382), (382, 362),
                               (263, 466), (466, 388), (388, 387), (387, 386),
                               (386, 385), (385, 384), (384, 398), (398, 362)])

FACEMESH_LEFT_EYEBROW = frozenset([(276, 283), (283, 282), (282, 295),
                                   (295, 285), (300, 293), (293, 334),
                                   (334, 296), (296, 336)])

FACEMESH_RIGHT_EYE = frozenset([(33, 7), (7, 163), (163, 144), (144, 145),
                                (145, 153), (153, 154), (154, 155), (155, 133),
                                (33, 246), (246, 161), (161, 160), (160, 159),
                                (159, 158), (158, 157), (157, 173), (173, 133)])

FACEMESH_RIGHT_EYEBROW = frozenset([(46, 53), (53, 52), (52, 65), (65, 55),
                                    (70, 63), (63, 105), (105, 66), (66, 107)])

FACEMESH_FACE_OVAL = frozenset([(10, 338), (338, 297), (297, 332), (332, 284),
                                (284, 251), (251, 389), (389, 356), (356, 454),
                                (454, 323), (323, 361), (361, 288), (288, 397),
                                (397, 365), (365, 379), (379, 378), (378, 400),
                                (400, 377), (377, 152), (152, 148), (148, 176),
                                (176, 149), (149, 150), (150, 136), (136, 172),
                                (172, 58), (58, 132), (132, 93), (93, 234),
                                (234, 127), (127, 162), (162, 21), (21, 54),
                                (54, 103), (103, 67), (67, 109), (109, 10)])

FACEMESH_CONTOURS = frozenset().union(*[
    FACEMESH_LIPS, FACEMESH_LEFT_EYE, FACEMESH_LEFT_EYEBROW, FACEMESH_RIGHT_EYE,
    FACEMESH_RIGHT_EYEBROW, FACEMESH_FACE_OVAL
])
FACE_CONNECTION_COLORS = {
    frozenset(FACEMESH_LIPS): (0, 0, 153),  
    frozenset(FACEMESH_LEFT_EYE): (64, 64, 64), 
    frozenset(FACEMESH_LEFT_EYEBROW): (64, 76, 153),
    frozenset(FACEMESH_RIGHT_EYE): (64, 64, 64), 
    frozenset(FACEMESH_RIGHT_EYEBROW): (64, 76, 153), 
    frozenset(FACEMESH_FACE_OVAL): (64, 64, 64)
}



import cv2
import pandas as pd
import numpy as np
import os

df = pd.read_csv('/Users/angelacao/S2S/data/CSVs/actor_5.csv')

input_folder_name = os.path.splitext(os.path.basename('/Users/angelacao/S2S/data/CSVs/actor_5.csv'))[0]

output_folder = os.path.join('/Users/angelacao/S2S/data/output_images', f'output_{input_folder_name}')
os.makedirs(output_folder, exist_ok=True)





fps = 30
width, height = 1240, 720

keypoint_positions = {}
for index, row in df.iterrows():
    x, y = int(row['x'] * width), int(row['y'] * height)
    keypoint_positions[(row['frame_number'], row['keypoint_type'], row['keypoint_number'])] = (x, y)

num_images = 10

total_frames = len(df['frame_number'].unique())
frame_interval = total_frames // (num_images - 1) 

current_frame = 0

for frame_number in df['frame_number'].unique():
    frame_data = df[df['frame_number'] == frame_number]

    frame = np.ones((height, width, 3), dtype=np.uint8) * 255

    for index, row in frame_data.iterrows():
        key = (frame_number, row['keypoint_type'], row['keypoint_number'])
        if key in keypoint_positions:
            x, y = keypoint_positions[key]
            keypoint_color = (211, 211, 211)

            if row['keypoint_type'] == 'left_hand' and row['keypoint_number'] in left_hand_colors:
                keypoint_color = left_hand_colors[row['keypoint_number']]

            elif row['keypoint_type'] == 'right_hand' and row['keypoint_number'] in right_hand_colors:
                keypoint_color = right_hand_colors[row['keypoint_number']]

            elif row['keypoint_type'] == 'face' and key in FACEMESH_CONTOURS:
                keypoint_color = (64, 64, 64)

                cv2.circle(frame, (x, y), 3, keypoint_color, -1)

    for connection in POSE_CONNECTIONS:
        start_key = (frame_number, 'pose', connection[0])
        end_key = (frame_number, 'pose', connection[1])

        if connection in POSE_CONNECTION_COLORS:
            color = POSE_CONNECTION_COLORS[connection]
        else:
            color = (64, 64, 64)

        if start_key in keypoint_positions and end_key in keypoint_positions:
            start_point = keypoint_positions[start_key]
            end_point = keypoint_positions[end_key]
            cv2.line(frame, start_point, end_point, color, 5) 


    for connection_set, color in HAND_CONNECTION_COLORS.items():
        for connection in connection_set:
            start_key = (frame_number, 'right_hand', connection[0])
            end_key = (frame_number, 'right_hand', connection[1])
            if start_key in keypoint_positions and end_key in keypoint_positions:
                start_point = keypoint_positions[start_key]
                end_point = keypoint_positions[end_key]
                cv2.line(frame, start_point, end_point, color, 5) 
    for connection_set, color in HAND_CONNECTION_COLORS.items():
        for connection in connection_set:
            start_key = (frame_number, 'left_hand', connection[0])
            end_key = (frame_number, 'left_hand', connection[1])
            if start_key in keypoint_positions and end_key in keypoint_positions:
                start_point = keypoint_positions[start_key]
                end_point = keypoint_positions[end_key]
                cv2.line(frame, start_point, end_point, color, 3) 
    for connection_set, color in FACE_CONNECTION_COLORS.items():
        for connection in connection_set:
            start_key = (frame_number, 'face', connection[0])
            end_key = (frame_number, 'face', connection[1])
            if start_key in keypoint_positions and end_key in keypoint_positions:
                start_point = keypoint_positions[start_key]
                end_point = keypoint_positions[end_key]
                cv2.line(frame, start_point, end_point, color, 3) 

    print(f"Saving image to folder: {output_folder}")


    if current_frame % frame_interval == 0:
        output_filename_with_interval = f'output_image_{current_frame // frame_interval}_frame_{frame_number}.png'
        output_path_with_interval = os.path.join(output_folder, output_filename_with_interval)
        cv2.imwrite(output_path_with_interval, frame)

    current_frame += 1

    if current_frame // frame_interval == num_images:
        break

print(f"{num_images} images generated and saved.")


cv2.destroyAllWindows()
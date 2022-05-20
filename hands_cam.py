# Mediapipe / Hands demo for PC with webcam
# FPS display, gray sclale

import cv2
import mediapipe as mp
from utils import cvfpscalc


mp_drawing = mp.solutions.drawing_utils  # type: ignore
mp_drawing_styles = mp.solutions.drawing_styles  # type: ignore
mp_hands = mp.solutions.hands  # type: ignore

# For webcam input:
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Sorry, no webcam found. Check your connection or privacy settings.")
    exit()

cvFpsCalc = cvfpscalc.CvFpsCalc(buffer_len=60)
with mp_hands.Hands(max_num_hands=2,
                    model_complexity=0,
                    min_detection_confidence=0.35,
                    min_tracking_confidence=0.35) as hands:
    while cap.isOpened():
        display_fps = cvFpsCalc.get()
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)  # Mediapipe is in RGB color space

        # from RGB to Gray to BGR, to make it gray scale
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        # cv2 is in BGR color space.

        image_height, image_width, _ = image.shape

        # Draw the hand annotations on the image.
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                print('Index finger tip coordinates: (',
                      f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width:.1f}, '
                      f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height:.1f})'
                      )
        # Flip the image horizontally for selfie-view.
        image = cv2.flip(image, 1)
        # Draw the title and FPS
        cv2.putText(image, "Mediapipe/Hands demo (Esc to exit)", org=(8, 38),
                    fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, fontScale=1.2,
                    color=(200, 255, 255), thickness=2, lineType=cv2.LINE_8)
        cv2.putText(image, "FPS:" + str(display_fps), org=(520, 68),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8,
                    color=(120, 255, 120), thickness=2, lineType=cv2.LINE_AA)

        cv2.imshow('MediaPipe Hands Demo (press Esc to exit)', image)

        if cv2.waitKey(5) & 0xFF == 27:  # exit if Esc key is pressed
            break
cap.release()

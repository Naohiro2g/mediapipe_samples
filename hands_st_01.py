# Mediapipe / Hands demo with Streamlit
# hands_st_01

import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils  # type: ignore
mp_drawing_styles = mp.solutions.drawing_styles  # type: ignore
mp_hands = mp.solutions.hands  # type: ignore

st.title("MediaPipe Hands Demo")
st.write("Hello")


class VideoProcessor(VideoProcessorBase):
    def __init__(self) -> None:
        self.model_complexity = 1
        self.min_detection_confidence = 0.15
        self.min_tracking_confidence = 0.15

    def recv(self, frame):
        image = frame.to_ndarray(format="bgr24")
        with mp_hands.Hands(model_complexity=self.model_complexity,
                            min_detection_confidence=self.min_detection_confidence,
                            min_tracking_confidence=self.min_tracking_confidence) as hands:

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

#            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())
            image = cv2.flip(image, 1)

        return av.VideoFrame.from_ndarray(image, format="bgr24")


ctx = webrtc_streamer(key="example", video_processor_factory=VideoProcessor)
if ctx.video_processor:
    ctx.video_processor.model_complexity = st.sidebar.selectbox(
        "Model Complexity", [0, 1], index=1)
    ctx.video_processor.min_detection_confidence = st.sidebar.slider(
        "Minimum Detection Confidence", 0.0, 1.0, 0.5)
    ctx.video_processor.min_tracking_confidence = st.sidebar.slider(
        "Minimum Tracking Confidence", 0.0, 1.0, 0.5)

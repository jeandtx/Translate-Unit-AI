import os
import streamlit as st
from utils import (
    get_genai_model,
    get_translation,
    detect_motion,
    translate,
    PROMPT_TRANSLATE,
)
import cv2
from PIL import Image
import io

from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def main():
    model = get_genai_model(GOOGLE_API_KEY, tools=[translate])

    st.title("Translate Unit AI")
    st.write("")
    st.write("This is a simple application to translate any units in images")

    if "camera_active" not in st.session_state:
        st.session_state.camera_active = False
    if "screenshot_buffer" not in st.session_state:
        st.session_state.screenshot_buffer = None
    if "uploaded_file_buffer" not in st.session_state:
        st.session_state.uploaded_file_buffer = None

    uploaded_file = st.file_uploader(
        "Choose an image file", type=["jpg", "jpeg", "png"], accept_multiple_files=False
    )
    if uploaded_file is not None:
        st.session_state.screenshot_buffer = None
        st.session_state.uploaded_file_buffer = uploaded_file

    if st.button("Use Webcam / Restart Camera"):
        st.session_state.screenshot_buffer = None
        st.session_state.uploaded_file_buffer = None
        st.session_state.camera_active = True

        cap = cv2.VideoCapture(0)
        frame_window = st.image([])

        if not cap.isOpened():
            st.write("Error: Could not open webcam.")
        else:
            last_frame = None
            stable_counter = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_window.image(frame_rgb)

                if last_frame is not None:
                    if not detect_motion(last_frame, frame):
                        stable_counter += 1
                        if stable_counter > 50:
                            # Take a screenshot & add the screenshot to the file uploader
                            screenshot = frame_rgb
                            screenshot_buffer = io.BytesIO()
                            Image.fromarray(screenshot).save(
                                screenshot_buffer, format="PNG"
                            )
                            screenshot_buffer.seek(0)
                            st.session_state.screenshot_buffer = screenshot_buffer
                            st.session_state.uploaded_file_buffer = None

                            # Stop the camera feed
                            cap.release()
                            frame_window.empty()
                            st.session_state.camera_active = False
                            break
                    else:
                        stable_counter = 0

                last_frame = frame

    image_to_display = (
        st.session_state.uploaded_file_buffer
        if st.session_state.uploaded_file_buffer
        else st.session_state.screenshot_buffer
    )
    if image_to_display:
        st.image(image_to_display, caption="Image to Translate", use_column_width=True)

    response = ""
    if image_to_display is not None:
        if st.button("Translate"):
            with st.spinner("Translating..."):
                response = get_translation(
                    image=image_to_display,
                    prompt=PROMPT_TRANSLATE,
                    model=model,
                )
            st.success("Translation completed")
    else:
        st.button("Translate", disabled=True)

    st.write(response)


if __name__ == "__main__":
    main()

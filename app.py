import os
import streamlit as st
from utils import (
    get_genai_model,
    get_translation,
    detect_motion,
    translate,
    PROMPT_TRANSLATE,
    get_units_from_country,
)
import cv2
from PIL import Image
import io
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def main():
    model = get_genai_model(GOOGLE_API_KEY, tools=[translate])

    st.title("Translate Unit AI")
    st.write("")
    st.write("This is a simple application to translate any units in images")

    country = st.sidebar.selectbox(
        "Where are you from?",
        [
            "United States",
            "United Kingdom",
            "Canada",
            "Australia",
            "India",
            "China",
            "Japan",
            "South Korea",
            "Russia",
            "Brazil",
        ],
    )

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
        # st.session_state.screenshot_buffer = None
        st.session_state.uploaded_file_buffer = uploaded_file

    if st.button('Clear Image'):
        st.session_state.uploaded_file_buffer = None
        st.session_state.screenshot_buffer = None

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
            st.session_state.uploaded_file_buffer = None

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

    # print('UPLOADER',st.session_state.uploaded_file_buffer)
    # print('CAMERA', st.session_state.screenshot_buffer)
    image_to_display = (
        st.session_state.screenshot_buffer if st.session_state.screenshot_buffer else st.session_state.uploaded_file_buffer
    )
    if image_to_display:
        st.image(image_to_display, caption="Image to Translate", use_column_width=True)

    response = ""
    if image_to_display is not None:
        if st.button("Translate"):
            with st.spinner("Translating..."):
                country_units = get_units_from_country(country)
                response = get_translation(
                    image=image_to_display,
                    prompt=PROMPT_TRANSLATE.format(
                        country=country,
                        price=country_units["price"],
                        distance=country_units["distance"],
                        weight=country_units["weight"],
                        length=country_units["length"],
                        volume=country_units["volume"],
                        temperature=country_units["temperature"],
                        area=country_units["area"],
                        speed=country_units["speed"],
                        footwear=country_units["footwear"],
                    ),
                    model=model,
                )

            st.success("Translation completed")
    else:
        st.button("Translate", disabled=True)

    data = json.dumps(response, indent=4)
    # write data to a json file
    with open('response.json', 'w') as f:
        f.write(json.loads(data))
    
    df = pd.DataFrame(columns=['source', 'target'])

    with open('response.json', 'r') as f:
        data = json.load(f)
        for element in data['args']:
            # print(element)
            # print(data['args'][element])
            for obj in data['args'][element]:
                # print('target', obj['target'])
                # print('source', obj['source'])

                # new_row = {'source': obj['source'], 'target': obj['target']}
                new_row = {'source': str(obj['source']['value']) + ' ' + str(obj['source']['unit']), 'target': str(obj['target']['value']) + ' ' + str(obj['target']['unit'])}

                df = pd.concat([df, pd.DataFrame([new_row])])

    if df is not None:
        st.table(df)

    # st.json(json.loads(json.dumps(response, indent=4)))


if __name__ == "__main__":
    main()

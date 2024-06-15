# Normal imports
import os
import streamlit as st
from utils import get_genai_model, get_translation


# API KEYS
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def main():
    model = get_genai_model(GOOGLE_API_KEY)

    st.title("Translate Unit AI")

    st.write("")
    st.write("This is a simple application to translate any units in images")

    uploaded_file = st.file_uploader(
        "Choose an image file", type=["jpg", "jpeg", "png"], accept_multiple_files=False
    )

    response = ""

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        if st.button("Translate"):
            with st.spinner("Translating..."):
                response = get_translation(
                    image=uploaded_file,
                    prompt="Find the price of this item and convert it to Dollars",
                    model=model,
                )
            st.success("Translation completed")
    else:
        st.button("Translate", disabled=True)

    st.write(response)


if __name__ == "__main__":
    main()

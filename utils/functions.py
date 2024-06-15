"""DECLARE FUNCTIONS HERE"""

import google.generativeai as genai

from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile


def get_genai_model(GOOGLE_API_KEY: str) -> genai.GenerativeModel:
    """Get the GenAI model

    Args:
        GOOGLE_API_KEY (str): The Google API key

    Returns:
        genai.GenerativeModel: The GenAI model
    """
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model


def get_translation(
    image: UploadedFile, prompt: str, model: genai.GenerativeModel
) -> str:
    """Get the translation of the image

    Args:
        image (UploadedFile): The image file
        prompt (str): The prompt to use
        model (genai.GenerativeModel): The GenAI model

    Returns:
        str: The translation of the image
    """
    img = Image.open(image)
    response = model.generate_content([prompt, img])
    return response

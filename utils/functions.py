"""DECLARE FUNCTIONS HERE"""

import google.generativeai as genai

from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile
from google.generativeai.types import content_types


def get_genai_model(
    GOOGLE_API_KEY: str, tools: content_types.FunctionLibraryType = None
) -> genai.GenerativeModel:
    """Get the GenAI model

    Args:
        GOOGLE_API_KEY (str): The Google API key
        tools (content_types.FunctionLibraryType, optional): The tools to use. Defaults to None.

    Returns:
        genai.GenerativeModel: The GenAI model
    """
    genai.configure(api_key=GOOGLE_API_KEY)
    if tools:
        return genai.GenerativeModel(model_name="gemini-1.5-flash", tools=tools)
    return genai.GenerativeModel(model_name="gemini-1.5-flash")


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

"""DECLARE FUNCTIONS HERE"""

import google.generativeai as genai
import numpy as np
import cv2

from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile
from google.generativeai.types import content_types
from utils.constants import UNIT_COUNTRY_MAPPING


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


def detect_motion(
    frame1: np.ndarray, frame2: np.ndarray, threshold: int = 5000
) -> bool:
    """Detect motion between two frames

    Args:
        frame1 (np.ndarray): The first frame
        frame2 (np.ndarray): The second frame
        threshold (int, optional): The threshold. Defaults to 5000.

    Returns:
        bool: True if motion is detected, False otherwise
    """
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    motion = sum(cv2.contourArea(contour) for contour in contours)
    return motion > threshold


def get_units_from_country(country: str) -> dict:
    """Get the units from a country

    Args:
        country (str): The country

    Returns:
        dict: The units from the country
    """
    return UNIT_COUNTRY_MAPPING[country]

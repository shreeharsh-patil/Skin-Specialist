import base64
import mimetypes
import os
from io import BytesIO

import anthropic
from dotenv import load_dotenv
from groq import Groq
from PIL import Image

load_dotenv()

SYSTEM_PROMPT = "You are a careful skin care assistant. Give general information, not a diagnosis."


def _encode_image_for_groq(filepath):
    image = Image.open(filepath)
    image.thumbnail((1024, 1024))
    buffer = BytesIO()
    image.convert("RGB").save(buffer, format="JPEG", quality=75)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def _encode_file(filepath):
    with open(filepath, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def _get_media_type(filepath, fallback):
    media_type, _ = mimetypes.guess_type(filepath)
    return media_type or fallback


def _build_prompt(patient_text, video_provided):
    instructions = (
        "You are a confident, natural doctor specializing in skin care. "
        "Speak with the reassurance, clarity, and authority of a real doctor. "
        "Limit your entire response to two or three sentences maximum. "
        "Do not use any special characters, symbols, asterisks, or markdown formatting "
        "in your response because it will be converted directly to audio.\n\n"
    )

    if video_provided:
        instructions += (
            "The patient uploaded a video in addition to an image. "
            "Explain that you are reviewing the uploaded image as the visual reference. "
            "Provide helpful skin care guidance based on what you observe.\n\n"
        )

    return instructions + f"Patient text: {patient_text}"


def _brain_groq(patient_text, image_filepath, video_filepath):
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("Missing GROQ_API_KEY in .env or environment")

    if not image_filepath:
        raise ValueError("Groq vision requires an image. Please upload a skin image.")

    image_data = _encode_image_for_groq(image_filepath)
    prompt = _build_prompt(patient_text, video_filepath is not None)

    client = Groq(api_key=groq_api_key)
    response = client.chat.completions.create(
        model=os.environ.get("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
        max_completion_tokens=1000,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}",
                        },
                    },
                ],
            },
        ],
    )

    return response.choices[0].message.content


def _brain_minimax(patient_text, image_filepath, video_filepath):
    minimax_api_key = os.environ.get("MINIMAX_API_KEY")
    if not minimax_api_key:
        raise ValueError("Missing MINIMAX_API_KEY in .env or environment")

    prompt = _build_prompt(patient_text, video_filepath is not None)

    if video_filepath:
        media_content = {
            "type": "video",
            "source": {
                "type": "base64",
                "media_type": _get_media_type(video_filepath, "video/mp4"),
                "data": _encode_file(video_filepath),
            },
        }
    elif image_filepath:
        media_content = {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": _get_media_type(image_filepath, "image/png"),
                "data": _encode_file(image_filepath),
            },
        }
    else:
        raise ValueError("Either image_filepath or video_filepath must be provided.")

    client = anthropic.Anthropic(
        api_key=minimax_api_key,
        base_url=os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.io/anthropic"),
    )
    response = client.messages.create(
        model=os.environ.get("MINIMAX_MODEL", "MiniMax-M3"),
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [media_content, {"type": "text", "text": prompt}],
            }
        ],
    )

    return response.content[0].text


def brain_of_the_doctor(patient_text, image_filepath=None, video_filepath=None, provider=None):
    if provider is None:
        provider = os.environ.get("AI_PROVIDER", "groq").lower()

    if provider == "groq":
        return _brain_groq(patient_text, image_filepath, video_filepath)
    elif provider == "minimax":
        return _brain_minimax(patient_text, image_filepath, video_filepath)
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'groq' or 'minimax'.")

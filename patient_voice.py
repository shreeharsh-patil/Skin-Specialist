from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()


def transcribe_patient_voice(audio_filepath):
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError(
            "Missing GROQ_API_KEY in .env or environment. "
            "Transcription requires a valid Groq API key."
        )

    client = Groq(api_key=groq_api_key)
    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model=os.environ.get("WHISPER_MODEL", "whisper-large-v3"),
        )

    return transcription.text

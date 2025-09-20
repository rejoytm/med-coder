import whisperx

from models import transcription_model

def transcribe(audio_path):
    audio = whisperx.load_audio(audio_path)
    result = transcription_model.transcribe(audio)

    full_text = " ".join(segment["text"].strip() for segment in result["segments"])

    return full_text
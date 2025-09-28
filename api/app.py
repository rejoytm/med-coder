import os

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

import src.models
from src.pipeline import transcribe_and_code_soap_note

UPLOAD_FOLDER = "instance/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)

@app.route("/transcribe-and-code", methods=["POST"])
def transcribe_and_code():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400   
    
    file = request.files['audio_file']
    filename = secure_filename(file.filename)

    # Only allow audio formats supported by WhisperX
    allowed_extensions = {'mp3', 'wav', 'm4a', 'flac', 'aac', 'ogg', 'webm'}
    if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({'error': 'Unsupported file type'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        result = transcribe_and_code_soap_note(filepath)
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500
    finally:
        # Delete uploaded file after processing
        if os.path.exists(filepath):
            os.remove(filepath)

    return jsonify(result)

if __name__ == "__main__":
    # Load models at startup to avoid cold starts during API calls
    _ = src.models.transcription_model
    _ = src.models.nlp_model

    app.run()
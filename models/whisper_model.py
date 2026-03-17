import requests

API_URL = "https://crowingly-nomenclatural-samson.ngrok-free.dev/transcribe" # TODO: Thay bằng link ngrok của Colab whisper

def load_whisper():
    """
    Dummy loader to keep pipeline unchanged
    """
    return None

def transcribe(model, audio_path):
    """
    Transcribe audio by calling Colab API.
    """
    with open(audio_path, 'rb') as f:
        # Gửi file audio qua form-data
        response = requests.post(
            API_URL,
            files={"file": f}, # key "file" có thể đổi tùy vào code API trên Colab
            timeout=1200
        )
        
    if response.status_code != 200:
        raise Exception(f"API error: {response.text}")
        
    # Giả định API trả về json giống whisper object nguyên bản: {"text": "...", "segments": [{"start": 0.0, "end": 2.0, "text": "..."}, ...]}
    return response.json()

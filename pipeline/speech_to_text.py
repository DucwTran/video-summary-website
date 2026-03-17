from models.whisper_model import load_whisper, transcribe

# Load model once when module starts
print("Initializing Whisper model...")
model = load_whisper()


def speech_to_text(audio_path, output_path):
    """
    Convert speech in audio file to text and save transcript.
    """

    print("Transcribing audio...")

    result = transcribe(model, audio_path)
    text = result["text"]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print("Transcript saved to:", output_path)

    return result

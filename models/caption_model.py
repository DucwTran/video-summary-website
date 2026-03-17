import requests
import io
import base64

API_URL = "https://crowingly-nomenclatural-samson.ngrok-free.dev/caption" # TODO: Thay bằng link ngrok của Colab caption

def load_caption_model():
    return None, None, None


def generate_caption(model, processor, tokenizer, image):

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    response = requests.post(
        API_URL,
        files={"file": ("image.jpg", buffer, "image/jpeg")},
        timeout=300
    )

    if response.status_code != 200:
        raise Exception(f"API error: {response.text}")

    return response.json()["caption"]
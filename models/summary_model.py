import requests

API_URL = "https://crowingly-nomenclatural-samson.ngrok-free.dev/generate"


def load_summary_model():
    """
    Dummy loader to keep pipeline unchanged
    """
    return None, None


def generate_summary(model, tokenizer, prompt):

    response = requests.post(
        API_URL,
        json={"text": prompt},
        timeout=300
    )

    if response.status_code != 200:
        raise Exception(f"API error: {response.text}")

    result = response.json()["result"]

    # Filter out Qwen ChatML tokens
    result = result.replace("<|im_end|>", "").replace("<|im_start|>", "")
    
    if "<|assistant|>" in result:
        result = result.split("<|assistant|>")[-1]
    if "assistant\n" in result:
        result = result.split("assistant\n")[-1]

    result = result.replace("|improve this answer|", "")

    return result.strip()

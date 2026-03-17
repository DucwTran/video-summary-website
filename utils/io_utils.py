import json
import os


def ensure_dir(path):
    """
    Tạo folder nếu chưa tồn tại
    """

    os.makedirs(path, exist_ok=True)


def save_json(data, path):

    with open(path, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def load_json(path):

    with open(path, "r", encoding="utf-8") as f:

        return json.load(f)


def save_text(text, path):

    with open(path, "w", encoding="utf-8") as f:

        f.write(text)


def load_text(path):

    with open(path, "r", encoding="utf-8") as f:

        return f.read()

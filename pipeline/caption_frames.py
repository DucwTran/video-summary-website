import os
import json
from PIL import Image

from models.caption_model import load_caption_model, generate_caption


print("Loading caption model...")
model, processor, tokenizer = load_caption_model()


def caption_frames(frame_dir, output_path):

    captions = []

    last_caption = None

    files = sorted(os.listdir(frame_dir))

    for f in files:

        img_path = os.path.join(frame_dir, f)

        with Image.open(img_path) as image:

            # resize image to reduce compute
            image = image.resize((224, 224))

            caption = generate_caption(model, processor, tokenizer, image)

        if caption != last_caption:
            captions.append({
                "frame": f,
                "caption": caption
            })

            last_caption = caption

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(captions, f, indent=2, ensure_ascii=False)

    print("Captions saved to:", output_path)

    return captions

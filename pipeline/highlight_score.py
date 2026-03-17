KEYWORDS = [
    "give", "help", "hug", "cry",
    "smile", "laugh", "run",
    "gift", "surprise", "thank",
    "family", "child", "mother",
    "happy", "kind", "share"
]


def keyword_score(caption):

    caption = caption.lower()

    score = 0

    for k in KEYWORDS:
        if k in caption:
            score += 1

    return score / len(KEYWORDS)


def speech_score(scene_text):

    words = scene_text.split()

    return min(len(words) / 40, 1.0)


def duration_score(start, end):

    duration = end - start

    return min(duration / 8, 1.0)


def score_scene(scene_text, caption, start, end):

    s = speech_score(scene_text)
    k = keyword_score(caption)
    d = duration_score(start, end)

    score = (
        0.6 * s +
        0.3 * k +
        0.1 * d
    )

    return score


def rank_scenes(scenes, segments, captions):

    results = []

    for i, (start, end) in enumerate(scenes):

        # gom transcript thuộc scene
        scene_text = ""

        for seg in segments:

            if seg["start"] < end and seg["end"] > start:
                scene_text += " " + seg["text"]

        caption = captions[i]["caption"] if i < len(captions) else ""

        score = score_scene(scene_text, caption, start, end)

        results.append({
            "scene": (start, end),
            "score": score
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    print("Top scene scores:", results[:5])

    return results

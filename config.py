VIDEO_PATH = "data/input/video.mp4"

AUDIO_PATH = "data/output/audio.wav"
TRANSCRIPT_PATH = "data/output/transcript.txt"
CAPTIONS_PATH = "data/output/captions.json"
SUMMARY_PATH = "data/output/summary.txt"

FRAME_DIR = "data/output/frames"

FRAME_STEP = 30
import torch
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

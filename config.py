import os

# Google API key
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyBBtpA1UYjDnDOXFD1fCE3kUUMUpq8p-DY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Default paths
DEFAULT_VIDEO_PATH = "./video_data/"
DEFAULT_OUTPUT_FOLDER = "./mixed_data/"
DEFAULT_AUDIO_PATH = "./mixed_data/output_audio.wav"

# Model settings
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
GEMINI_MODEL_NAME = "models/gemini-2.5-flash"

# LanceDB settings
LANCEDB_URI = "lancedb"
TEXT_TABLE_NAME = "text_collection"
IMAGE_TABLE_NAME = "image_collection"

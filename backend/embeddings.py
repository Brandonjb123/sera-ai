import os
from sentence_transformers import SentenceTransformer

# Cache model di folder yang ter-mount Railway Volume
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "model_cache")
os.makedirs(MODEL_PATH, exist_ok=True)

# Load model sekali saat startup
model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=MODEL_PATH)

def encode(text: str) -> list:
    """Encode text to embedding vector (list of floats)."""
    return model.encode(text).tolist()
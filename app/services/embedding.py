from sentence_transformers import SentenceTransformer


# Load pre-trained model
model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight and fast


# Generate embedding for text
def generate_embedding(text: str) -> list:
    embedding = model.encode(text).tolist()
    return embedding
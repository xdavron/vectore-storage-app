from sentence_transformers import SentenceTransformer


# Load pre-trained model
model = SentenceTransformer("all-MiniLM-L6-v2")
VECTOR_SIZE = model.get_sentence_embedding_dimension()  # Dynamically determine the vector size


# Generate embedding for text
def generate_embedding(text: str) -> list:
    embedding = model.encode(text).tolist()
    return embedding


def generate_embeddings(texts: list) -> list:
    return model.encode(texts).tolist()

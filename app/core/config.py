from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    CHROMADB_HOST: str = "localhost"
    CHROMADB_PORT: int = 8000
    DEFAULT_DB: str = "qdrant"  # Options: 'qdrant' or 'chromadb'
    DEFAULT_COLLECTION: str = "vector_data"

    class Config:
        env_file = ".env"


settings = Settings()
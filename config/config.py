from dotenv import load_dotenv
import os
from pathlib import Path

# Load the .env file from the config directory
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

GENAI_MODEL = os.getenv("GENAI_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FRAUD_API_KEY = os.getenv("FRAUD_API_KEY")

CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME")

FRAUD_API_URL = os.getenv("FRAUD_API_URL")


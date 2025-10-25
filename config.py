import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
    
    # Настройки для обработки текста
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Модель для эмбеддингов (легкая и быстрая)
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Модель для чата
    CHAT_MODEL = "gpt-4-1106-preview"  # Более дешевая и быстрая версия GPT-4

settings = Settings()

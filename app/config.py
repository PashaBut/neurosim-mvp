import os
from dotenv import load_dotenv

load_dotenv()



class Settings:
    # Yandex Cloud settings
    YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
    YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")
    
    # Vector database
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
    
    # Text processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Model settings
    YANDEX_GPT_MODEL = "yandexgpt"
    
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    SECRET_MANAGER_URL = os.getenv("SECRET_MANAGER_URL")  # HashiCorp Vault
    
    # Политики хранения
    DATA_RETENTION_DAYS = 90
    AUTO_DELETION_ENABLED = True
    
    # Yandex Cloud IAM
    SERVICE_ACCOUNT_ID = os.getenv("SERVICE_ACCOUNT_ID")
    
    # Изоляция данных
    VECTOR_NAMESPACE_PREFIX = "user_"  # Префикс для изоляции в векторной БД

settings = Settings()

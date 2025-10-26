from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uuid
import os
from typing import List
from app.services.chat_service import chat_service

from app.config import settings
from app.services.file_processor import FileProcessor
from app.services.vector_store import VectorStore
from app.services.chat_service import ChatService
from app.security.crypto import DataEncryptor
from app.models.schemas import UploadResponse, ChatRequest, ChatResponse, HealthResponse

app = FastAPI(
    title="NeuroSim API",
    version="0.1.0",
    description="Secure AI-powered self-reflection platform with Privacy by Design"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация сервисов
security = HTTPBearer()
file_processor = FileProcessor()
vector_store = VectorStore()
chat_service = ChatService()
encryptor = DataEncryptor()

# Временное хранилище сессий (в продакшене заменить на Redis)
user_sessions = {}

def get_user_id(authorization: str = Depends(security)) -> str:
    """Валидация и получение user_id из токена"""
    # TODO: Реализовать JWT валидацию
    # Пока используем заглушку - возвращаем случайный ID
    return str(uuid.uuid4())

@app.get("/")
async def root():
    return {
        "message": "NeuroSim Secure API is running!", 
        "status": "OK",
        "privacy_level": "encrypted_storage",
        "version": "0.1.0"
    }

@app.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Depends(get_user_id),
    background_tasks: BackgroundTasks = None
):
    """Secure endpoint для загрузки и обработки файлов"""
    try:
        # Валидация типа файла
        if not file.filename.endswith(('.txt', '.pdf')):
            raise HTTPException(400, "Only TXT and PDF files are supported")
        
        # Чтение и шифрование содержимого
        contents = await file.read()
        encrypted_content = encryptor.encrypt_text(contents.decode('utf-8'))
        
        # Создание задачи на обработку в фоне
        file_id = str(uuid.uuid4())
        background_tasks.add_task(
            process_file_background,
            file_id=file_id,
            user_id=user_id,
            encrypted_content=encrypted_content,
            filename=file.filename
        )
        
        return UploadResponse(
            file_id=file_id,
            user_id=user_id,
            filename=file.filename,
            status="processing",
            message="File is being processed securely"
        )
        
    except Exception as e:
        raise HTTPException(500, f"Error processing file: {str(e)}")# В импорты добавить:

@app.post("/chat")
async def chat_with_digital_double(question: str, user_id: str = Depends(get_user_id)):
    """💬 RAG-пайплайн с реальной логикой"""
    try:
        response = chat_service.generate_personalized_response(question, user_id)
        return {
            "question": question,
            "answer": response,
            "user_id": user_id,
            "pipeline": "rag_implemented",
            "sources_used": 3  # TODO: Реальное количество источников
        }
    except Exception as e:
        raise HTTPException(500, f"Error in RAG pipeline: {str(e)}")


@app.delete("/user/{user_id}/data")
async def delete_user_data(user_id: str, auth: str = Depends(security)):
    """Полное удаление всех данных пользователя (GDPR compliance)"""
    try:
        # Удаление из векторной БД
        vector_store.delete_user_data(user_id)
        
        # Удаление зашифрованных файлов (реализовать в FileProcessor)
        file_processor.delete_user_files(user_id)
        
        return {
            "status": "success",
            "message": f"All data for user {user_id} has been permanently deleted",
            "deleted_at": "2024-01-01T00:00:00Z"  # TODO: добавить реальное время
        }
    except Exception as e:
        raise HTTPException(500, f"Error deleting user data: {str(e)}")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Проверка здоровья сервиса и безопасности"""
    security_status = "encryption_active" if encryptor.is_ready() else "encryption_inactive"
    
    return HealthResponse(
        status="healthy",
        model=settings.YANDEX_GPT_MODEL,
        security_level=security_status,
        vector_db_connected=vector_store.is_connected(),
        privacy_features=["data_encryption", "user_isolation", "secure_deletion"]
    )

# Фоновая задача для обработки файлов
async def process_file_background(file_id: str, user_id: str, encrypted_content: bytes, filename: str):
    """Фоновая обработка файла: декрипт -> чанкинг -> векторизация"""
    try:
        # Декрипт содержимого
        decrypted_text = encryptor.decrypt_text(encrypted_content)
        
        # Обработка файла
        chunks = file_processor.process_text(decrypted_text, user_id)
        
        # Сохранение в векторную БД
        vector_store.add_chunks(chunks, user_id)
        
        # Логирование успешной обработки
        print(f"File {filename} processed successfully for user {user_id}")
        
    except Exception as e:
        print(f"Error processing file {filename}: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

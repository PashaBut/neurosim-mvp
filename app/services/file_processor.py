"""
📄 Сервис обработки файлов и текста

ARCHITECTURE:
- Разбивка текста на семантические чанки
- Подготовка данных для векторного поиска
- Обработка различных форматов файлов
"""

import logging
from typing import List, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

class FileProcessor:
    def __init__(self):
        logger.info("FileProcessor initialized")
    
    def process_text(self, text: str, user_id: str) -> List[Dict[str, Any]]:
        """
        Обработка текста: разбивка на чанки и подготовка для векторизации
        
        Args:
            text: Исходный текст
            user_id: ID пользователя для изоляции
            
        Returns:
            Список чанков с метаданными
        """
        try:
            # TODO: Реализовать умное разбиение на чанки
            # Пока просто разбиваем по абзацам
            chunks = self._split_into_chunks(text)
            
            logger.info(f"Processed text into {len(chunks)} chunks for user {user_id}")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing text for user {user_id}: {str(e)}")
            return []
    
    def _split_into_chunks(self, text: str, chunk_size: int = 1000) -> List[Dict[str, Any]]:
        """
        Разбивка текста на чанки фиксированного размера
        
        FUTURE: Реализовать семантическое разбиение по смыслу
        """
        chunks = []
        
        # Простое разбиение по предложениям/абзацам
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        current_chunk = ""
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= chunk_size:
                current_chunk += paragraph + " "
            else:
                if current_chunk:
                    chunks.append({
                        "text": current_chunk.strip(),
                        "metadata": {
                            "chunk_size": len(current_chunk),
                            "type": "text"
                        }
                    })
                current_chunk = paragraph + " "
        
        # Добавляем последний чанк
        if current_chunk:
            chunks.append({
                "text": current_chunk.strip(),
                "metadata": {
                    "chunk_size": len(current_chunk),
                    "type": "text"
                }
            })
        
        return chunks
    
    def process_file(self, file_content: bytes, filename: str, user_id: str) -> List[Dict[str, Any]]:
        """
        Обработка файла в зависимости от формата
        
        FUTURE: Поддержка PDF, DOCX и других форматов
        """
        try:
            # Пока обрабатываем только текстовые файлы
            if filename.endswith('.txt'):
                text = file_content.decode('utf-8')
                return self.process_text(text, user_id)
            else:
                logger.warning(f"Unsupported file format: {filename}")
                return []
                
        except Exception as e:
            logger.error(f"Error processing file {filename} for user {user_id}: {str(e)}")
            return []

# Синглтон экземпляр
file_processor = FileProcessor()

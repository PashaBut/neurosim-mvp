"""
🔐 Сервис шифрования данных

ARCHITECTURE:
- Шифрование пользовательских данных перед сохранением
- Privacy by Design принципы
"""

import os
import logging
from cryptography.fernet import Fernet
from app.config import settings

logger = logging.getLogger(__name__)

class DataEncryptor:
    def __init__(self):
        """
        Инициализация шифровальщика
        
        FUTURE: Интеграция с HashiCorp Vault для управления ключами
        """
        # TODO: Получать ключ из настроек или Vault
        self.key = os.getenv("ENCRYPTION_KEY")
        if not self.key:
            # Временное решение для разработки
            self.key = Fernet.generate_key()
            logger.warning("Using auto-generated encryption key - not for production!")
        
        self.fernet = Fernet(self.key)
        logger.info("DataEncryptor initialized")
    
    def encrypt_text(self, text: str) -> bytes:
        """Шифрование текста"""
        try:
            return self.fernet.encrypt(text.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error encrypting text: {str(e)}")
            raise
    
    def decrypt_text(self, encrypted_data: bytes) -> str:
        """Дешифрование текста"""
        try:
            return self.fernet.decrypt(encrypted_data).decode('utf-8')
        except Exception as e:
            logger.error(f"Error decrypting text: {str(e)}")
            raise
    
    def is_ready(self) -> bool:
        """Проверка готовности шифровальщика"""
        return bool(self.key)

# Синглтон экземпляр
encryptor = DataEncryptor()

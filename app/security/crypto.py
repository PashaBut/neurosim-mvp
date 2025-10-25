from cryptography.fernet import Fernet
import os
import base64

class DataEncryptor:
    def __init__(self):
        # TODO: Интегрировать с HashiCorp Vault
        self.key = os.getenv("ENCRYPTION_KEY")
        if not self.key:
            # Временное решение для разработки
            self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)
    
    def encrypt_text(self, text: str) -> bytes:
        return self.fernet.encrypt(text.encode('utf-8'))
    
    def decrypt_text(self, encrypted_data: bytes) -> str:
        return self.fernet.decrypt(encrypted_data).decode('utf-8')
    
    def is_ready(self) -> bool:
        return bool(self.key)
      

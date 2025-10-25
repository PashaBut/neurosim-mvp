# app/services/chat_service.py
class ChatService:
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm = YandexGPTClient()  # или другой LLM клиент
    
    def generate_personalized_response(self, user_question: str, user_id: str) -> str:
        # 1. Retrieval (Поиск)
        relevant_chunks = self.vector_store.similarity_search(
            query=user_question, 
            user_id=user_id,  # Изоляция по пользователю
            limit=3
        )
        
        # 2. Augmentation (Обогащение контекста)
        context = "\n\n".join([chunk.text for chunk in relevant_chunks])
        
        # 3. Generation (Генерация "от лица")
        prompt = f"""
        Ты - цифровой двойник пользователя. Используй контекст ниже чтобы ответить КАК ОН САМ.
        
        КОНТЕКСТ ИЗ ЗАПИСЕЙ ПОЛЬЗОВАТЕЛЯ:
        {context}
        
        ВОПРОС: {user_question}
        
        ОТВЕТ (от первого лица, в стиле пользователя):
        """
        
        return self.llm.generate(prompt)

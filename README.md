# NeuroSim MVP

> 🧠 AI-powered self-reflection tool that creates your personal digital double.

**⚠️ Status: Early MVP Development**  
This is an experimental minimum viable product. Core functionality is in active development.

## 🎯 Vision

NeuroSim explores a simple but powerful hypothesis: **can we create truly personalized self-analysis by grounding an AI in your own writings?**

Traditional chatbots are generic. Real self-reflection requires context — your past experiences, your unique thoughts, your private worries.

## ✨ MVP Features

- 📁 **Text Upload** (TXT, PDF documents)
- 🧩 **Smart Text Processing** (chunking & semantic embeddings) 
- 🔍 **Context-Aware Search** (vector similarity search)
- 💬 **Personalized Chat** (GPT-4 powered with your context)
- 🎯 **Simple Web Interface** (Streamlit-based)

## 🛠 Tech Stack

**Backend:** Python, FastAPI, LangChain  
**AI:** OpenAI GPT-4, Sentence Transformers  
**Vector DB:** ChromaDB  
**Frontend:** Streamlit  
**Infrastructure:** Docker, Yandex Cloud

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/your-username/neurosim-mvp.git
cd neurosim-mvp

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Run the application
docker-compose up

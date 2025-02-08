# 🎙️ AI Voice Chatbot with Whisper, Ollama & Kokoro

This project is a voice-enabled chatbot that integrates **speech-to-text**, **AI-generated responses**, and **text-to-speech** capabilities. It uses **Whisper ASR** for speech recognition, **Ollama** for AI-powered responses, and **Kokoro** for realistic speech synthesis.

---

##  Features
- 🎤 **Speech-to-Text**: Converts spoken words into text using OpenAI Whisper.
- 🤖 **AI Chatbot**: Generates intelligent responses using Ollama (Llama2 model).
- 🔊 **Text-to-Speech**: Converts responses to speech using Kokoro TTS.
- 💾 **Memory Retention**: Maintains conversation context using LangChain memory.
- 🎧 **Live Audio Playback**: Plays the AI-generated response as audio output.

---

## Installation

### 1 **Clone the Repository**
```bash
git clone https://github.com/your-username/ai-voice-chatbot.git
cd ai-voice-chatbot
```

### 2️ **Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️ **Install Dependencies**
```bash
pip install -r requirements.txt
```

###  **Run the Chatbot**
```bash
python3 chatbot.py
```

###  **Interaction**
1. Type a message or press `Enter` to use voice input.
2. Speak when prompted.
3. AI generates a response and reads it aloud.
4. Type `exit` to quit.

###  DeepSeek API Status
I attempted to integrate DeepSeek for AI responses, but due to temporary payment service issues, it could not be used. The chatbot currently works with llama2 instead. Once DeepSeek's API is available, you can switch by updating the model in generate_response().
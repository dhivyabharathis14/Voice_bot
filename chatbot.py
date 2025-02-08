import numpy as np
import whisper
import ollama
import sounddevice as sd
import soundfile as sf
import asyncio
from langchain.memory import ConversationBufferMemory
from kokoro import KPipeline
from IPython.display import display, Audio

whisper_model = whisper.load_model("base")

tts_pipeline = KPipeline(lang_code="a")

memory = ConversationBufferMemory()

async def speech_to_text(audio_file):
    """Converts speech from an audio file to text asynchronously using Whisper ASR."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, whisper_model.transcribe, audio_file)
    return result["text"]

async def record_audio(duration=15, sample_rate=44100, output_file="live_input.wav"):
    """Records live audio from the microphone asynchronously."""
    print("Recording... Speak now!")
    loop = asyncio.get_event_loop()
    audio_data = await loop.run_in_executor(None, lambda: sd.rec(
        int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16"
    ))
    sd.wait()
    sf.write(output_file, audio_data, sample_rate)
    print("Recording saved.")
    return output_file

async def generate_response(user_text):
    """Generates a chatbot response asynchronously using Ollama (Mistral) with memory."""
    loop = asyncio.get_event_loop()
    conversation_history = ""
    conversation_history += f"User: {user_text}\n"
    response = await loop.run_in_executor(None, lambda: ollama.chat(
        model="llama2", messages=[{"role": "user", "content": conversation_history}]
    ))
    bot_response = response["message"]["content"]
    memory.save_context({"input": user_text}, {"output": bot_response})
    
    return bot_response

async def text_to_speech(response_text, output_file="response.wav"):
    """Converts AI-generated text to speech asynchronously and plays audio."""
    loop = asyncio.get_event_loop()
    generator = tts_pipeline(response_text, voice="af_heart", speed=1)
    
    all_audio = []
    for _, _, audio in generator:
        all_audio.append(audio)
    
    merged_audio = np.concatenate(all_audio, axis=0)
    await loop.run_in_executor(None, sf.write, output_file, merged_audio, 24000)
    
    display(Audio(data=merged_audio, rate=24000, autoplay=True))

async def chatbot():
    """Continuously processes user input asynchronously until exit is typed."""
    while True:
        print("Type your message OR say something (press Enter to use microphone):")
        user_input = input("> ")

        if user_input.lower() == "exit":
            print("Exiting chatbot. Goodbye!")
            break

        elif user_input.strip() == "":
            audio_file = await record_audio(duration=5)
            user_input = await speech_to_text(audio_file)

        print("User:", user_input)
        response_text = await generate_response(user_input)
        print("Bot:", response_text)
        print("Generating speech...")
        await text_to_speech(response_text, output_file="response.wav")

if __name__ == "__main__":
    asyncio.run(chatbot())

import os
import time
import json
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pyttsx3
import pygame
from groq import Groq


# Initialize pyttsx3 TTS engine
tts_engine = pyttsx3.init()

# Initialize Vosk model for speech recognition
model = Model(r"C:\Users\conve\Zexternalpro\local_VA_RAG\free_mdl\vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

def recognize_speech():
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                        channels=1, callback=callback):
        print("Say something...")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                print(f"You said: {text}")
                return text

def generate_response(prompt):
    client = Groq(api_key="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") 
    response = client.chat.completions.create(
    messages=[
            {
                "role": "user",
                "content": f"you are an AI Assistant response to user prompt: {prompt} and the response has to be below 30 words."
            }
        ],
        model="mixtral-8x7b-32768"
    )
    return response.choices[0].message.content.strip()

def play_text_to_speech(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def main():
    while True:
        speech_text = recognize_speech()
        if speech_text.lower() in ["exit", "quit", "stop"]:
            print("Exiting the voice assistant.")
            break
        if speech_text:
            response_text = generate_response(speech_text)
            print(f"Assistant: {response_text}")
            play_text_to_speech(response_text)

if __name__ == "__main__":
    main()

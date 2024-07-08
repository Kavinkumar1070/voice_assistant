import speech_recognition as sr
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

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something, I am Listening...")
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

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

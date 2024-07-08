import speech_recognition as sr
from free_mdl.gt import gTTS
# from pydub import AudioSegment
# from pydub.playback import play
import os
from groq import Groq
import pygame
import time

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


# def text_to_speech(text):
#     tts = gTTS(text=text, lang='en')
#     tts.save("response.mp3")
#     sound = AudioSegment.from_mp3("response.mp3")
#     play(sound)
#     os.remove("response.mp3")


def play_text_to_speech(text, language='en', slow=False):
    tts = gTTS(text=text, lang=language, slow=slow)
    temp_audio_file = "temp_audio.mp3"
    tts.save(temp_audio_file)
    
    pygame.mixer.init()
    pygame.mixer.music.load(temp_audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    time.sleep(3)
    os.remove(temp_audio_file)
    
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

import speech_recognition as sr

fileName = '2.wav'

recoginze = sr.Recognizer()

with sr.AudioFile(fileName) as source:
    audio_data = recoginze.record(source)
    text = recoginze.recognize_google(audio_data)
    print(text)
    
"""    
import whisper

model = whisper.load_model("medium")
result = model.transcribe("2.mp3")
print(result["text"])
"""

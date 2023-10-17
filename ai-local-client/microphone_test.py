#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import whisper
import os
from dotenv import load_dotenv

load_dotenv()

# import openai

# openai.api_key = os.getenv("OPENAI_API_KEY")

import dependency_check

dependency_check.check()


print("################################################################################################")
print("List of microphones")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
print("################################################################################################")


# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone(device_index=1) as source:
    print("Say something!")
    audio = r.listen(source)

##############################################
# # recognize speech using Sphinx
# import torch
# # get a bunch of GPU info
# # comment out if not using Sphinx
# torch.cuda.is_available()
# torch.cuda.device_count()
# torch.cuda.current_device()
# torch.cuda.device(0)
# #torch.cuda.device at 0x7efce0b03be0
# torch.cuda.get_device_name(0)

# try:
#     print("Sphinx thinks you said " + r.recognize_sphinx(audio))
# except sr.UnknownValueError:
#     print("Sphinx could not understand audio")
# except sr.RequestError as e:
#     print("Sphinx error; {0}".format(e))
##############################################

# recognize speech using Google Speech Recognition
print("Google Speech Recognition's turn")
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

# recognize speech using whisper
print("Whisper's turn")
try:
    print("Whisper thinks you said " + r.recognize_whisper(audio, language="english"))
except sr.UnknownValueError:
    print("Whisper could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Whisper")

# # recognize speech using Whisper API
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# try:
#     print(f"Whisper API thinks you said {r.recognize_whisper_api(audio, api_key=OPENAI_API_KEY)}")
# except sr.RequestError as e:
#     print("Could not request results from Whisper API")


#Attempt 1
# import io
# import torch
# from tempfile import NamedTemporaryFile

# model="tiny"
# audio_model = whisper.load_model(model)
# # Use AudioData to convert the raw data to wav data.
# audio_data = sr.AudioData(audio, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
# wav_data = io.BytesIO(audio_data.get_wav_data())

# # Write wav data to the temporary file as bytes.
# with open(temp_file, 'w+b') as f:
#     f.write(wav_data.read())

# # Read the transcription.
# temp_file = NamedTemporaryFile().name
# result = audio_model.transcribe(temp_file, fp16=torch.cuda.is_available())
# text = result['text'].strip()
# print("Whisper2 thinks you said " + text) 
print("Whisper2's turn")
import io
import torch
from tempfile import NamedTemporaryFile
from pydub import AudioSegment

def audio_data_to_wav_bytes(audio_data):
    # Convert AudioData to AudioSegment
    audio_segment = AudioSegment(
        audio_data.frame_data,    # Using frame_data instead of get_raw_data
        sample_width=audio_data.sample_width, 
        frame_rate=audio_data.sample_rate,
        channels=1
    )
    # Export to WAV and get bytes
    with io.BytesIO() as wav_io:
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)
        wav_bytes = wav_io.read()
    return wav_bytes

# Convert your captured audio to WAV bytes
wav_bytes = audio_data_to_wav_bytes(audio)

model="tiny"
audio_model = whisper.load_model(model)

# Create a named temporary file
temp_file = NamedTemporaryFile().name

# Write wav data to the temporary file as bytes.
with open(temp_file, 'wb') as f:
    f.write(wav_bytes)

# Read the transcription.
result = audio_model.transcribe(temp_file, fp16=torch.cuda.is_available())
text = result['text'].strip()
print("Whisper2 thinks you said " + text) 


# Python program to translate
# speech to text and text to speech
#import sys
import os
import speech_recognition as sr
#import pyttsx3
#import args
import io
import torch
from tempfile import NamedTemporaryFile
from pydub import AudioSegment
import whisper

from elevenlabs import set_api_key, voices, generate, stream, play, UnauthenticatedRateLimitError
set_api_key(os.getenv("ELEVENLABS_KEY"))

import subprocess

def is_mpv_installed():
    try:
        # Run the dpkg command to check if mpv is installed.
        result = subprocess.run(['dpkg', '-l', 'mpv'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # If mpv is found in the output, it's installed.
        return 'mpv' in result.stdout.decode('utf-8')
    except Exception as e:
        print(f"Error encountered: {e}")
        return False

if not is_mpv_installed():
    print("mpv is not installed. Please install it using the following command:")
    print("sudo apt install mpv")






microphone_index = int(os.getenv("MICROPHONE_INDEX"))

verbose = False

def set_args(arguments):
    global verbose
    verbose = True if arguments["verbose"] else False

# Function to convert text to speech
def speaktext(command):
    if verbose: print("Verbose", "\n", "speaktext function: ", command)
    audio_stream = generate(
        text=command,
        voice="Bella",
        stream=True
    )

    stream(audio_stream)


r = sr.Recognizer()

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

def record_text():
    # Loop in case of errors
    while(1):
        try:
            # use the microphone as the source for input
            with sr.Microphone(device_index=microphone_index) as source2:
                # Prepare recognizer to recieve input
                #r.adjust_for_ambient_noise(source2, duration=0.2)
                r.adjust_for_ambient_noise(source2)

                print("I'm listening")

                # Listen for user
                audio2 = r.listen(source2)
                if verbose: print("Verbose", "\n", "record_text function: ", "Now deciphering words...")

                # Convert your captured audio to WAV bytes
                wav_bytes = audio_data_to_wav_bytes(audio2)

                model="tiny"
                audio_model = whisper.load_model(model)

                # Create a named temporary file
                temp_file = NamedTemporaryFile().name

                # Write wav data to the temporary file as bytes.
                with open(temp_file, 'wb') as f:
                    f.write(wav_bytes)

                # Read the transcription.
                result = audio_model.transcribe(temp_file, fp16=torch.cuda.is_available())
                MyText = result['text'].strip()

                # # Use Google to recognize audio
                # MyText = r.recognize_google(audio2)

                print("User text: ", "\n", MyText)
                return MyText
            
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occured")
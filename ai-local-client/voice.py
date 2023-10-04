# Python program to translate
# speech to text and text to speech
#import sys
import os
import speech_recognition as sr
#import pyttsx3
#import args


from elevenlabs import set_api_key, voices, generate, stream, play, UnauthenticatedRateLimitError
set_api_key(os.getenv("ELEVENLABS_KEY"))

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


def record_text():
    # Loop in case of errors
    while(1):
        try:
            # use the microphone as the source for input
            with sr.Microphone(device_index=microphone_index) as source2:
                # Prepare recognizer to recieve input
                r.adjust_for_ambient_noise(source2, duration=0.2)

                print("I'm listening")

                # Listen for user
                audio2 = r.listen(source2)
                if verbose: print("Verbose", "\n", "record_text function: ", "Now deciphering words...")
                # Use Google to recognize audio
                MyText = r.recognize_google(audio2)
                print("User text: ", "\n", MyText)
                return MyText
            
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occured")
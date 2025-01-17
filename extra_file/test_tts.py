import re
from deepgram import Deepgram
import requests
from dotenv import load_dotenv
from deepgram.utils import verboselogs
from deepgram import (
    DeepgramClient,
    ClientOptionsFromEnv,
    SpeakOptions,
)
from playsound import playsound
import os
import time
from llm_txt import llm_text
import asyncio
from pydub import AudioSegment
from pydub.playback import play

load_dotenv()



load_dotenv() 
llms = llm_text()

response = asyncio.run(llm_text.llm_response())
# print(response)

# inputText = "Hey how are you doing today? I am doing great. I am just testing out this text to speech feature. I hope it works well. I am excited to see the results."

SPEAK_TEXT = {"text": str(response)}
AUDIO_FILE = "test.mp3"


def main():
    try:
        # STEP 1 Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(
            api_key="", config=ClientOptionsFromEnv(verbose=verboselogs.SPAM)
        )

        # STEP 2 Call the save method on the speak property
        options = SpeakOptions(
            model="aura-asteria-en",
        )

        response = deepgram.speak.rest.v("1").save(AUDIO_FILE, SPEAK_TEXT, options)
        print(response.to_json(indent=4))

    # Ensure the audio file is created
        if os.path.exists(AUDIO_FILE):
            try:
                # Play the audio file
                audio = AudioSegment.from_file(AUDIO_FILE)
                play(audio)

            except Exception as e:
                print(f"Error: Unable to play the audio file. Details: {e}")
        else:
            print(f"Error: The file {AUDIO_FILE} does not exist.")

    except Exception as e:
        print(f"Exception: {e}")

# step play mp3 file
# playsound("test.mp3")

if __name__ == "__main__":
    main()
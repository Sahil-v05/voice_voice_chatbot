
import time
from deepgram.utils import verboselogs
import wave
from dotenv import load_dotenv
from llm_txt import llm_text
import asyncio
from pydub import AudioSegment
from pydub.playback import play

load_dotenv() 
llms = llm_text()

response = asyncio.run(llm_text.llm_response())

  

from deepgram import (
    DeepgramClient,
    SpeakWebSocketEvents,
    SpeakWSOptions,
)

AUDIO_FILE = "output.wav"
# TTS_TEXT = "Hello, this is a text to speech example using Deepgram. How are you doing today? I am fine thanks for asking."

def main():
    try:
        # use default config
        deepgram: DeepgramClient = DeepgramClient()

        # Create a websocket connection to Deepgram
        dg_connection = deepgram.speak.websocket.v("1")

        def on_binary_data(self, data, **kwargs):
            print("Received binary data")
            with open(AUDIO_FILE, "ab") as f:
                f.write(data)
                f.flush()

        dg_connection.on(SpeakWebSocketEvents.AudioData, on_binary_data)

        # Generate a generic WAV container header
        # since we don't support containerized audio, we need to generate a header
        header = wave.open(AUDIO_FILE, "wb")
        header.setnchannels(1)  # Mono audio
        header.setsampwidth(2)  # 16-bit audio
        header.setframerate(16000)  # Sample rate of 16000 Hz
        header.close()

        # connect to websocket
        options = SpeakWSOptions(
            model="aura-stella-en",
            encoding="linear16",
            sample_rate=16000,
        )

        print("\n\nPress Enter to stop...\n\n")
        if dg_connection.start(options) is False:
            print("Failed to start connection")
            return

        # send the text to Deepgram
        dg_connection.send_text(response)
        
        # if auto_flush_speak_delta is not used, you must flush the connection by calling flush()
        dg_connection.flush()

        # Indicate that we've finished
        time.sleep(2)
        print("\n\nPress Enter to stop...\n\n")
        input()

        # Close the connection
        dg_connection.finish()

        print("Finished")

    except ValueError as e:
        print(f"Invalid value encountered:{e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

file_path  = "output.wav"
def play_audio(file_path):
   
    try:
        # Load the audio file
        audio = AudioSegment.from_file(file_path)
        # Play the audio
        play(audio)
    except Exception as e:
        print(f"Error: Unable to play the audio file. Details: {e}")
# play_audio(file_path)

if __name__ == "__main__":
    main()
    play_audio(file_path)
import streamlit as st
import asyncio
# from extra_file.spt_ex import get_transcript
from llm_txt import llm_text
from deepgram import DeepgramClient, SpeakOptions
from pydub import AudioSegment
from pydub.playback import play
import os
from STT import SpeechToTextManager


# Initialize Streamlit app
st.title("Voice-to-Voice Chatbot")

# Button to start recording
if st.button("Start Recording"):
    st.write("Recording... Please speak into the microphone.")
    
    # Get the transcript from the speech-to-text function
    # transcript = asyncio.run(get_transcript())
    # st.write(f"Transcript: {transcript}")
    manager = SpeechToTextManager()
    transcription_response =  asyncio.run(manager.main())
    st.write(f"Transcription Response: {transcription_response}")

    # Get the LLM response
    response = asyncio.run(llm_text.llm_response(transcription_response))
    SPEAK_TEXT = {"text": str(response)}
    st.write(f"LLM Response: {response}")

    # Save the response as an audio file
    AUDIO_FILE = "test.mp3"
    try:
        # Create a Deepgram client
        deepgram = DeepgramClient()

        # Define SpeakOptions
        options = SpeakOptions(
            model="aura-asteria-en",
        )

        # Call the save method on the speak property
        response_audio = deepgram.speak.rest.v("1").save(AUDIO_FILE, SPEAK_TEXT, options)
        st.write("Audio file created succesfully.")

        # Ensure the audio file is created
        if os.path.exists(AUDIO_FILE):
            try:
                # Load and play the audio file using pydub
                audio = AudioSegment.from_file(AUDIO_FILE)
                play(audio)
                # st.write("Playing sound using pydub")
            except Exception as e:
                st.write(f"Error: Unable to play the audio file. Details: {e}")
        else:
            st.write(f"Error: The file {AUDIO_FILE} does not exist.")
    except Exception as e:
        st.write(f"Exception: {e}")

# Run the Streamlit app
# if __name__ == "__main__":
#     st.run()
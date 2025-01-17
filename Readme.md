## Voice-to-Voice Chatbot

This project implements a voice-to-voice chatbot using three models: Speech-to-Text, Language Model (Groq), and Text-to-Speech. The user interacts with the chatbot using their voice, and the chatbot responds with synthesized speech.


## Files Description
app.py
This is the main entry point for the Streamlit application. It initializes the voice-to-voice chatbot and handles user interactions.

STT.py
This file contains the implementation of the Speech-to-Text functionality using Deepgram. It captures audio input, processes it into text, and returns the transcript.

llm_txt.py
This file contains the implementation of the Language Model (Groq) functionality. It takes the transcription response from the Speech-to-Text model and generates a response using the Groq language model.

## How It Works
Speech-to-Text: The user's voice input is captured and transcribed into text using the Deepgram API.

Language Model (Groq): The transcribed text is sent to the Groq language model, which generates a response.

Text-to-Speech: The generated response is converted back into speech and played back to the user.

## 1.Setup
Install the required dependencies
```bash
pip install -r requirements.txt
```


## 2.Set up environment variables

Create a .env file in the root directory.
Add your Deepgram API key, groq api key and other necessary environment variables.

## 3.Run the application
``` bash
streamlit run app.py
```

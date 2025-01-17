import asyncio
from deepgram import DeepgramClient, DeepgramClientOptions, LiveTranscriptionEvents, LiveOptions, Microphone
from dotenv import load_dotenv

load_dotenv()

class TranscriptCollector:
    def __init__(self):
        self.reset()

    def reset(self):
        self.transcript_parts = []

    def add_part(self, part):
        self.transcript_parts.append(part)

    def get_full_transcript(self):
        return ' '.join(self.transcript_parts)

transcript_collector = TranscriptCollector()

async def get_transcript(callback):
    """
    Captures audio input, processes it into text, and returns the transcript.
    """
    transcription_complete = asyncio.Event()  # Event to signal transcription completion

    try:
        # Configure the Deepgram client
        config = DeepgramClientOptions(options={"keepalive": "true"})
        deepgram: DeepgramClient = DeepgramClient("", config)  # Replace with your actual API key

        dg_connection = deepgram.listen.asynclive.v("1")
        print("Listening...")

        async def on_message(self,result, **kwargs):
            """Handles incoming transcription results."""
            sentence = result.channel.alternatives[0].transcript

            if not result.speech_final:
                transcript_collector.add_part(sentence)
            else:
                # This is the final part of the current sentence
                transcript_collector.add_part(sentence)
                full_sentence = transcript_collector.get_full_transcript()
                # Return the complete transcript only if it's not empty
                if len(full_sentence.strip()) > 0:
                    full_sentence = full_sentence.strip()
                    print(f"Human: {full_sentence}")
                    callback(full_sentence)  # Call the callback with the full_sentence
                    transcript_collector.reset()
                    transcription_complete.set()  # Signal to stop transcription

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model="nova-2",
            punctuate=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            endpointing=300,
            smart_format=True,
        )

        await dg_connection.start(options)

        # Open a microphone stream on the default input device
        microphone = Microphone(dg_connection.send)
        microphone.start()

        await transcription_complete.wait()  # Wait for the transcription to complete

        # Clean up resources
        microphone.finish()
        await dg_connection.finish()

    except Exception as e:
        print(f"Error during transcription: {e}")   
        return ""

    return transcript_collector.get_full_transcript()

class SpeechToTextManager:
    def __init__(self):
        self.transcription_response = ""

    async def main(self):
        def handle_full_sentence(full_sentence):
            self.transcription_response = full_sentence

        # Loop indefinitely until "goodbye" is detected
        
        await get_transcript(handle_full_sentence)

            # Print the response
        print(f"Transcript: {self.transcription_response}")

        #     # Exit condition
        # if "goodbye" in self.transcription_response.lower():
        #     print("Goodbye detected. Exiting loop.")
        #     break
        return self.transcription_response


# # Testable entry point
# if __name__ == "__main__":
#     manager = SpeechToTextManager()
#     asyncio.run(manager.main())

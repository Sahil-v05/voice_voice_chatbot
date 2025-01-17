from groq import Groq
from dotenv import load_dotenv

from STT import SpeechToTextManager
import asyncio


load_dotenv()

# respone = SpeechToTextManager()
manager = SpeechToTextManager()
transcription_response =  asyncio.run(manager.main())

class llm_text:
    @staticmethod
    async def llm_response(transcription_response):
        try:
            # full_script = await get_transcript()
            # if not full_script:
            #     print("No transcript received")
            #     return "No transcript available"

            # print(f"Transcript: {full_script}")

            client = Groq()

            stream = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": """You are a conversational assistant named Sahil. User will ask questions mixed with coding and textual content. Answer should be in short , concise and in simple language.""",
                    },
                    {
                        "role": "user",
                        "content": f"Here is the user question: {transcription_response}",
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=100,
                top_p=1,
                stop=None,
                stream=True,
            )

            results = []
            try:
                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        results.append(content)
            except Exception as e:
                print(f"Error while streaming: {e}")
            finally:
                # Ensure the stream is closed
                stream.close()

            thes = ''.join(results)
            print(thes)
            return thes

        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"
        




if __name__ == "__main__":
    response = asyncio.run(llm_text.llm_response(transcription_response))
    print(f"LLM Response: {response}")

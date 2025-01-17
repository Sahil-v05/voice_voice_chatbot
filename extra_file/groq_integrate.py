from groq import Groq
from dotenv import load_dotenv
from speech_to_text import get_transcript
import asyncio


# MODEL_NAME = "llama-3.3-70b-versatile"
# full_script = get_transcript()

load_dotenv()


# speech_text = 'Give a brief about RoPE in Llama'
class llm_text:
    @staticmethod
    async def llm_response():
        try:
            full_script = await get_transcript()
            print(full_script)
            # if not full_script:
            #     return "No transcript available"

            client = Groq()

            stream = client.chat.completions.create(
            #
            # Required parameters
            #
            messages=[
            
                {"role": "system",
                "content": """You are a conversational assistant named Sahil.User will ask questions mixed with coding and textual content.Answer should be in detail and in simple language.,
                    Answer should be in detail and in simple language.""",
                },
                # Set a user message for the assistant to respond to.
                {
                    "role": "user",
                    "content": "Here is the user question {}".format(full_script),
                }
            ],
            # model=MODEL_NAME,
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_tokens=100,
            top_p=1,
            stop=None,
            stream=True,
        )

        # Print the completion returned by the LLM.
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
            return f"An error occurred: {e}"
if __name__ == "__main__":
    response = asyncio.run(llm_text.llm_response())
    print(f"LLM Response: {response}")

# Speech_text = 'Give a brief about attention mechanism in Llama'
# print(llm_text.llm_response(Speech_text))



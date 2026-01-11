from groq import Groq


class GroqClient:
    def __init__(self):
        try:
            self.client = Groq()
        except Exception as e:
            print(f"Connection to groq client failed: {e}")

    def get_chat_completion(self, history):
        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=history,
                temperature=0,
                max_completion_tokens=8192,
                top_p=1,
                reasoning_effort="medium",
                stream=False,
                stop=None,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Groq client call failed: {e}")


groq_client = GroqClient()

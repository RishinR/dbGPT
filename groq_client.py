from groq import Groq


class GroqClient:
    def __init__(self):
        self.client = Groq()

    def get_chat_completion(self, history):
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


groq_client = GroqClient()

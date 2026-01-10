from google import genai
from config import settings
from typing import List, Dict
from google.genai.types import Content, Part


class GeminiClient:
    def __init__(self):
        try:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        except Exception as e:
            print(f"Error in connecting to gemini: {e}")

    async def get_chat_completion(self, conversations: List[Dict]):
        try:
            history = []
            for msg in conversations:
                role = msg["role"]
                text = msg["content"]

                if role == "system":
                    role = "user"
                history.append(Content(role=role, parts=[Part(text=text)]))
            # create async chat session with history
            chat = self.client.aio.chats.create(
                model="gemini-2.5-flash", history=history
            )
            response = await chat.send_message("")
            return response.text
        except Exception as e:
            print(f"Failed to get gemini response: {e}")


gemini_client = GeminiClient()

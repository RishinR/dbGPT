from config import settings
from openai import AsyncAzureOpenAI


class OpenAIClient:
    def __init__(self):
        try:
            self.client = AsyncAzureOpenAI(
                azure_endpoint=settings.REVIN_INSIGHTS_AZURE_OPENAI_ENDPOINT,
                api_key=settings.REVIN_INSIGHTS_AZURE_OPENAI_APIKEY,
                api_version=settings.REVIN_INSIGHTS_AZURE_API_VERSION,
            )
        except Exception as e:
            print(f"Error in connecting to azure open ai: {e}")

    async def get_chat_completion(self, history):
        response = await self.client.chat.completions.create(
            model=settings.REVIN_INSIGHTS_AZURE_API_MODEL,
            messages=history,
            temperature=0,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )
        return response.choices[0].message.content


openai_client = OpenAIClient()

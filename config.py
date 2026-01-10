import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.POSTGRES_BD_URI = os.getenv("POSTGRES_DB_URI")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


settings = Settings()

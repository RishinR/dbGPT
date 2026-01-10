import os
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.POSTGRES_DB_URI = os.getenv("POSTGRES_DB_URI", "")

        parsed = urlparse(self.POSTGRES_DB_URI)
        query = parse_qs(parsed.query)
        options = query.get("options", [""])[0]

        schema = None
        if "search_path=" in options:
            schema = options.split("search_path=")[1]

        self.DB_SCHEMA = schema
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


settings = Settings()

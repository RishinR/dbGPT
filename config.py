import os
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        # PostgreSQL settings
        self.POSTGRES_DB_URI = os.getenv("POSTGRES_DB_URI", "")
        
        parsed = urlparse(self.POSTGRES_DB_URI)
        query = parse_qs(parsed.query)
        options = query.get("options", [""])[0]

        schema = "public"
        if "search_path=" in options:
            schema = options.split("search_path=")[1]

        self.DB_SCHEMA = schema
        
        # MongoDB settings
        self.MONGODB_URI = os.getenv("MONGODB_URI", "")
        self.MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "")
        
        # Database type selection
        self.DB_TYPE = os.getenv("DB_TYPE", "postgres").lower()  # 'postgres' or 'mongodb'
        
        # API Keys
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")


settings = Settings()
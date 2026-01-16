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

        schema = "public"
        if "search_path=" in options:
            schema = options.split("search_path=")[1]

        self.DB_SCHEMA = schema
        self.REVIN_INSIGHTS_AZURE_OPENAI_ENDPOINT = os.getenv(
            "REVIN_INSIGHTS_AZURE_OPENAI_ENDPOINT"
        )
        self.REVIN_INSIGHTS_AZURE_OPENAI_APIKEY = os.getenv(
            "REVIN_INSIGHTS_AZURE_OPENAI_APIKEY"
        )
        self.REVIN_INSIGHTS_AZURE_API_VERSION = os.getenv(
            "REVIN_INSIGHTS_AZURE_API_VERSION"
        )
        self.REVIN_INSIGHTS_AZURE_API_MODEL = os.getenv(
            "REVIN_INSIGHTS_AZURE_API_MODEL"
        )


settings = Settings()

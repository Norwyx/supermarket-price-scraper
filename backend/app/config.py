from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Path to .env file
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=str(ENV_FILE), env_ignore_empty=True)

settings = Settings()

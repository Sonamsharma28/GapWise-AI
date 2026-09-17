import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./gapwise.db")
    secret_key: str = os.getenv("SECRET_KEY", "gapwise-dev-super-secret-key-2026")
    access_token_expire_minutes: int = 1440
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173")

    @property
    def sync_database_url(self) -> str:
        url = self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

settings = Settings()

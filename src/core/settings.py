from typing import List
from pathlib import Path
from functools import cached_property, lru_cache

from pydantic import Field
from google.oauth2 import service_account
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.utils.load_creds import load_json_path

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # App Settings
    # ------------------------------------------------------------------
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=False)

    # ------------------------------------------------------------------
    # Tavily Settings
    # ------------------------------------------------------------------
    TAVILY_API_KEY: str = Field(...)

    # ------------------------------------------------------------------
    # Gemini Settings
    # ------------------------------------------------------------------
    GEMINI_API_KEY: str = Field(...)
    LOCATION: str = Field(default="global")

    GEMINI_MODEL_PRO: str = Field(default="gemini-2.5-pro")
    GEMINI_MODEL_FLASH: str = Field(default="gemini-2.5-flash")
    GEMINI_MODEL_LITE: str = Field(default="gemini-2.5-flash-lite")

    # ------------------------------------------------------------------
    # Google Cloud Settings
    # ------------------------------------------------------------------
    SERVICE_ACCOUNT_FILE_PATH: Path = load_json_path("model_credentials")
    SERVICE_ACCOUNT_SCOPE: List[str] = ["https://www.googleapis.com/auth/cloud-platform"]

    # ------------------------------------------------------------------
    # Paths
    # ------------------------------------------------------------------
    LOGS_DIR: Path = BASE_DIR / "LOGS"
    PROMPTS_DIR: Path = BASE_DIR / "src" / "prompts"

    # ------------------------------------------------------------------
    # Directory Management
    # ------------------------------------------------------------------
    def create_directories(self) -> None:
        """
        Create all required application directories.
        """
        directories = [
            self.LOGS_DIR,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Google Credentials
    # ------------------------------------------------------------------
    @cached_property
    def credentials(self):
        """
        Lazily load Google Cloud credentials.
        """
        return service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE_PATH,
            scopes=self.SERVICE_ACCOUNT_SCOPE,
        )


@lru_cache
def get_settings() -> Settings:
    """
    Create and cache application settings.
    """
    settings = Settings()
    settings.create_directories()
    return settings


settings = get_settings()
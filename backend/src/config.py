"""Application configuration via pydantic-settings."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root is three levels up from this file:
# backend/src/config.py -> backend/src -> backend -> openalpha (project root)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Central configuration loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM provider selection
    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-4-20250514"

    # API keys
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    # Ollama (local)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"

    # Display
    verbose: bool = False

    # Data directories (relative to project root)
    investors_dir: Path = _PROJECT_ROOT / "investors"
    skills_dir: Path = _PROJECT_ROOT / "skills"
    prompts_dir: Path = _PROJECT_ROOT / "prompts"


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (parsed once per process)."""
    return Settings()

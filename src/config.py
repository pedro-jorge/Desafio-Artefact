from pathlib import Path
from functools import lru_cache, cached_property
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    GROQ_API_KEY: SecretStr
    LLM_MODEL: str
    LLM_TEMPERATURE: float

    ROOT: Path = ROOT_DIR
    DOC_DIR: Path = ROOT_DIR / "data"
    PDF_PATH: Path = DOC_DIR / "políticas_da_loja.pdf"
    PROMPT_TEMPLATE: Path = ROOT_DIR / "src" / "prompt.txt"

    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", env_file_encoding="utf-8")
    
    @cached_property
    def PROMPT(self) -> str:
        if not self.PROMPT_TEMPLATE.exists():
            raise FileNotFoundError(f"Prompt template file not found: {self.PROMPT_TEMPLATE}")
        return self.PROMPT_TEMPLATE.read_text(encoding="utf-8").strip()

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
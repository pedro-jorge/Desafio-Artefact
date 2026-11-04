from pathlib import Path
from functools import lru_cache, cached_property
from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    LLM_MODEL: str = "qwen3:8b"
    LLM_TEMPERATURE: float = 0.0
    LLM_BASE_URL: str = "http://ollama:11434"
    NUM_CTX_TOKENS: int = 8192
    
    ROOT: Path = ROOT_DIR
    DOC_DIR: Path = ROOT_DIR / "data"
    PDF_PATH: Path = DOC_DIR / "políticas_da_loja.pdf"
    DB_PATH: Path = DOC_DIR / "database.db"
    PROMPT_TEMPLATE: Path = ROOT_DIR / "src" / "prompt.txt"
    
    @cached_property
    def PROMPT(self) -> str:
        if not self.PROMPT_TEMPLATE.exists():
            raise FileNotFoundError(f"Prompt template file not found: {self.PROMPT_TEMPLATE}")
        return self.PROMPT_TEMPLATE.read_text(encoding="utf-8").strip()

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    DB_PATH: str = "data/processed/wholesale.db"
    MODEL_VERSION: str = "gemini-2.0-flash-exp"
    LOG_FILE: str = "experiments/logs.csv"
    MAX_REQUESTS_PER_MINUTE: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

def validate_paths():
    db_path = Path(settings.DB_PATH)
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {settings.DB_PATH}")
    
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

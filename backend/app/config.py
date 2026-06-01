from pydantic import BaseSettings, AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "Driver Drowsiness Backend"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./backend.db"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:4200"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

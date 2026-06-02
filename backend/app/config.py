from pydantic import BaseSettings, AnyHttpUrl
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Driver Drowsiness Backend"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./backend.db"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:4200"]

    # Notification settings
    WEBHOOK_URLS: List[AnyHttpUrl] = []
    ALERT_EMAIL_TO: List[str] = []
    SMTP_SERVER: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMS_PROVIDER: str | None = None
    SMS_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

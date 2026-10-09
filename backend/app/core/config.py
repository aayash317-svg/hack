import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Campus Safety & Harassment Reporting System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "synthetic-dev-secret-key-change-in-production-campus-safety-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database: Default to SQLite for seamless local running/testing, or MySQL if specified
    # Example MySQL: mysql+pymysql://root:password@localhost:3306/campus_safety_db
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./campus_safety.db")

    # Storage
    EVIDENCE_STORAGE_DIR: str = os.getenv("EVIDENCE_STORAGE_DIR", "./storage/evidence")
    MAX_UPLOAD_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 MB
    ALLOWED_MEDIA_TYPES: list[str] = [
        "image/png",
        "image/jpeg",
        "image/jpg",
        "application/pdf",
    ]

    # Institution Settings Placeholders
    INSTITUTION_NAME: str = "Apex Institute of Technology"
    EMERGENCY_HELPLINE: str = "+91 00000 00000"
    SECURITY_GATE_CONTACT: str = "Campus Security Gate 1 & Student Welfare Block"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Storage backend settings
    GCS_BUCKET: str = "None"  # Assumes GCS is storage backend
    GCS_PROJECT: str = "None"  # Assumes GCS is storage backend
    STORAGE_BACKEND: Literal["local", "gcs"] = "local"

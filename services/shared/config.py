from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    lab_allowed_origins: str = "http://localhost:4321"
    lab_vault_path: str = "./data/vault"
    lab_max_upload_bytes: int = 10_485_760
    lab_job_timeout_seconds: int = 300
    lab_job_max_attempts: int = 3
    model_config = SettingsConfigDict(env_file=".env.lab", extra="ignore")
    @property
    def origins(self) -> list[str]:
        return [value.strip() for value in self.lab_allowed_origins.split(",") if value.strip()]

@lru_cache
def settings() -> Settings:
    return Settings()

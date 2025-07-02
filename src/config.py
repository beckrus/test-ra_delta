from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: str
    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int

    ALLOW_ORIGINS: List[str] = ["http://127.0.0.1:8000", "http://localhost:8000"]

    @property
    def DB_URL(self) -> str:
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @field_validator("MODE")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        allowed = {"TEST", "DEV", "PROD"}
        if v not in allowed:
            raise ValueError(f"MODE must be one of {allowed}")
        return v

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

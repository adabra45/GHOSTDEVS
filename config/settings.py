from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    # Limits
    max_iterations: int = 15
    max_cost_usd: float = 0.0          # free

    # Sandbox
    sandbox_type: Literal["local", "docker", "e2b"] = "local"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
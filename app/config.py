from pydantic import BaseSettings


class Settings(BaseSettings):
    ollama_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()

from pydantic import BaseSettings

class Settings(BaseSettings):
    ollama_api_key: str
    cashu_api_key: str
    # Other settings

    class Config:
        env_file = ".env"

settings = Settings()

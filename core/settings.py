from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DB_USER: str = Field(env="DB_USER")
    DB_NAME: str = Field(env="DB_NAME")
    DB_HOST: str = Field(env="DB_HOST")
    DB_PORT: str = Field(env="DB_PORT")
    DB_PASSWORD: str = Field(env="DB_PASSWORD")
    API_ID: int = Field(env="API_ID")
    API_HASH: str = Field(env="API_HASH")
    BOT_TOKEN: str = Field(env="BOT_TOKEN")
    BOT_NAME: str = Field(env="BOT_NAME")

    class Config:
        env_file = ".env"


settings = Settings()

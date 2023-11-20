from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    UVICORN_PORT: int
    UVICORN_HOST: str
    BACKEND_PORT: int
    APP_TITLE: str
    MONGO_INITDB_DATABASE: str
    MONGODB_URL: str
    MONGO_PORTS: int
    KAFKA_TOPIC_NAME: str
    BOOTSTRAP_SERVER: str

    model_config = SettingsConfigDict(env_file=".env")


app_settings = Settings()

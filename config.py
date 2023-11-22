from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    UVICORN_PORT: int
    UVICORN_HOST: str
    BACKEND_PORT: int
    TITLE: str

    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env")


class KafkaSettings(BaseSettings):
    TOPIC_NAME: str
    BOOTSTRAP_SERVER: str

    model_config = SettingsConfigDict(env_prefix="KAFKA_", env_file=".env")


class MongoDBSettings(BaseSettings):
    MONGO_INITDB_DATABASE: str
    MONGO_URL: str
    MONGO_PORTS: int

    model_config = SettingsConfigDict(env_prefix="MONGODB_", env_file=".env")


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    kafka: KafkaSettings = KafkaSettings()
    mongo: MongoDBSettings = MongoDBSettings()


settings = Settings()

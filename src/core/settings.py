from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    # Banco de dados único
    DATABASE_URL: str

    # Variáveis do Docker Compose
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str

settings = Settings()
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    # Bronze - Dados Brutos
    BRONZE_DATABASE_URL: str

    # Silver - Dados Processados
    SILVER_DATABASE_URL: str

    # Logs - Dados de Log
    LOGS_DATABASE_URL: str

settings = Settings()
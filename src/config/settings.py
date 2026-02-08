from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Postgres
    POSTGRESSQL_URL: str = "postgresql://localhost:27017"
    POSTGRESSQL_DATABASE: str = "cadastro_unificado"

    # API Pessoas (Time 02)
    PESSOA_API_URL: str = "http://localhost:8001"

    class Config:
        env_file = ".env"


settings = Settings()
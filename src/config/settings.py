from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Postgres
    POSTGRESSQL_URL: str = "jdbc:postgresql://127.0.0.1:5432"
    POSTGRESSQL_DATABASE: str = "postgres"
    POSTGRESSQL_USER: str = "postgres"
    POSTGRESSQL_PASSWORD: str = "189Sud36@"

    # API Pessoas (Time 02)
    PESSOA_API_URL: str = "http://localhost:8001"

    class Config:
        env_file = ".env"


settings = Settings()
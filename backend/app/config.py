from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://astroai:astroai@localhost:5432/astroai"

    jwt_secret_key: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    astrology_provider: str = "mock"
    prokerala_client_id: str = ""
    prokerala_client_secret: str = ""

    geocoding_provider: str = "mock"
    geocoding_api_key: str = ""

    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-5"
    llm_api_key: str = ""


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://astroai:astroai@localhost:5432/astroai"

    jwt_secret_key: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    # Encrypts user-supplied LLM API keys at rest (app.services.encryption). Any
    # string works -- it's hashed into a valid Fernet key -- but MUST be changed
    # and kept stable in production (rotating it makes existing stored keys undecryptable).
    encryption_key: str = "dev-encryption-key-change-me"

    astrology_provider: str = "mock"
    prokerala_client_id: str = ""
    prokerala_client_secret: str = ""
    # Self-hosted AstroEngine instance (LAN-only, no API key) -- see app.astrology.providers.astroengine_provider
    astroengine_base_url: str = "http://192.168.68.114:8000"

    geocoding_provider: str = "mock"
    geocoding_api_key: str = ""

    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-5"
    llm_api_key: str = ""


settings = Settings()

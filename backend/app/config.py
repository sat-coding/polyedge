from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")
    database_path: str = "data/polyedge.db"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.4-2026-03-05"
    openai_fast_model: str = "gpt-5.4-mini"
    paper_trading: bool = True
    bankroll: float = 1000.0
    kelly_multiplier: float = 0.25
    ev_threshold: float = 0.005

settings = Settings()

from typing import Literal

from pydantic import BaseModel

LLMProviderName = Literal["anthropic", "openai", "google", "deepseek"]


class LLMSettingsUpdate(BaseModel):
    provider: LLMProviderName
    api_key: str
    model: str | None = None


class LLMSettingsResponse(BaseModel):
    provider: str | None
    model: str | None
    has_api_key: bool

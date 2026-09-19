"""
LLM client, configurable via env vars (LLM_PROVIDER / LLM_MODEL) and only
ever called from the backend -- never from the React frontend.
"""

import httpx

from app.config import settings

_ANTHROPIC_MESSAGES_URL = "https://api.anthropic.com/v1/messages"


class LLMClient:
    def complete(self, system_prompt: str, user_message: str) -> str:
        raise NotImplementedError


class AnthropicLLMClient(LLMClient):
    def complete(self, system_prompt: str, user_message: str) -> str:
        response = httpx.post(
            _ANTHROPIC_MESSAGES_URL,
            headers={
                "x-api-key": settings.llm_api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": settings.llm_model,
                "max_tokens": 1024,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_message}],
            },
            timeout=30.0,
        )
        response.raise_for_status()
        payload = response.json()
        return "".join(block.get("text", "") for block in payload.get("content", []))


class EchoLLMClient(LLMClient):
    """Used when no LLM_API_KEY is configured, so the chat endpoint is testable end-to-end."""

    def complete(self, system_prompt: str, user_message: str) -> str:
        return (
            "[No LLM_API_KEY configured -- this is a placeholder response.] "
            f"You asked: '{user_message}'. Once an LLM key is set, this will be answered "
            "using your real chart data and retrieved astrology knowledge."
        )


def get_llm_client() -> LLMClient:
    if settings.llm_provider == "anthropic" and settings.llm_api_key:
        return AnthropicLLMClient()
    return EchoLLMClient()

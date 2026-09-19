"""
LLM client, configurable per-user ("bring your own key" in Settings) with a
server-wide env-var fallback (LLM_PROVIDER / LLM_MODEL / LLM_API_KEY), and
only ever called from the backend -- never from the React frontend.

Supported providers: anthropic, openai, google, deepseek. OpenAI and
DeepSeek both speak the same OpenAI-compatible chat-completions shape, so
they share one implementation parameterized by base URL -- adding another
OpenAI-compatible provider later is one line, not a new class.
"""

import httpx

from app.config import settings
from app.models.user import User
from app.services.encryption import decrypt_secret

_ANTHROPIC_MESSAGES_URL = "https://api.anthropic.com/v1/messages"
_OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
_DEEPSEEK_CHAT_URL = "https://api.deepseek.com/chat/completions"
_GOOGLE_GENERATE_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

_DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-5",
    "openai": "gpt-4o-mini",
    "google": "gemini-2.0-flash",
    "deepseek": "deepseek-chat",
}


class LLMClient:
    def complete(self, system_prompt: str, user_message: str) -> str:
        raise NotImplementedError


class AnthropicLLMClient(LLMClient):
    def __init__(self, api_key: str, model: str) -> None:
        self._api_key = api_key
        self._model = model

    def complete(self, system_prompt: str, user_message: str) -> str:
        response = httpx.post(
            _ANTHROPIC_MESSAGES_URL,
            headers={
                "x-api-key": self._api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": self._model,
                "max_tokens": 1024,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_message}],
            },
            timeout=30.0,
        )
        response.raise_for_status()
        payload = response.json()
        return "".join(block.get("text", "") for block in payload.get("content", []))


class _OpenAICompatibleLLMClient(LLMClient):
    """Shared by OpenAI and DeepSeek -- both speak the same chat-completions shape."""

    def __init__(self, base_url: str, api_key: str, model: str) -> None:
        self._base_url = base_url
        self._api_key = api_key
        self._model = model

    def complete(self, system_prompt: str, user_message: str) -> str:
        response = httpx.post(
            self._base_url,
            headers={"Authorization": f"Bearer {self._api_key}", "content-type": "application/json"},
            json={
                "model": self._model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            },
            timeout=30.0,
        )
        response.raise_for_status()
        payload = response.json()
        return payload["choices"][0]["message"]["content"]


class GoogleLLMClient(LLMClient):
    def __init__(self, api_key: str, model: str) -> None:
        self._api_key = api_key
        self._model = model

    def complete(self, system_prompt: str, user_message: str) -> str:
        url = _GOOGLE_GENERATE_URL_TEMPLATE.format(model=self._model)
        response = httpx.post(
            url,
            params={"key": self._api_key},
            json={
                "system_instruction": {"parts": [{"text": system_prompt}]},
                "contents": [{"role": "user", "parts": [{"text": user_message}]}],
            },
            timeout=30.0,
        )
        response.raise_for_status()
        payload = response.json()
        parts = payload["candidates"][0]["content"]["parts"]
        return "".join(part.get("text", "") for part in parts)


class EchoLLMClient(LLMClient):
    """Used when no LLM key is configured (server-wide or per-user), so the chat
    endpoint is testable end-to-end without any external account."""

    def complete(self, system_prompt: str, user_message: str) -> str:
        return (
            "[No LLM key configured -- this is a placeholder response.] "
            f"You asked: '{user_message}'. Once an LLM key is set (in Settings, or by the "
            "server operator), this will be answered using your real chart data and "
            "retrieved astrology knowledge."
        )


def _build_client(provider: str, api_key: str, model: str | None) -> LLMClient:
    model = model or _DEFAULT_MODELS.get(provider, "")
    if provider == "anthropic":
        return AnthropicLLMClient(api_key, model)
    if provider == "openai":
        return _OpenAICompatibleLLMClient(_OPENAI_CHAT_URL, api_key, model)
    if provider == "deepseek":
        return _OpenAICompatibleLLMClient(_DEEPSEEK_CHAT_URL, api_key, model)
    if provider == "google":
        return GoogleLLMClient(api_key, model)
    return EchoLLMClient()


def get_llm_client(user: User | None = None) -> LLMClient:
    """Prefers the given user's own key (Settings page); falls back to the
    server-wide env-var configuration; falls back to the echo placeholder."""
    if user is not None and user.llm_provider and user.llm_api_key_encrypted:
        api_key = decrypt_secret(user.llm_api_key_encrypted)
        return _build_client(user.llm_provider, api_key, user.llm_model)

    if settings.llm_provider and settings.llm_api_key:
        return _build_client(settings.llm_provider, settings.llm_api_key, settings.llm_model)

    return EchoLLMClient()

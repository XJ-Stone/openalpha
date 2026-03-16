"""LLM provider abstraction. Thin wrappers around official SDKs."""

from __future__ import annotations

import json as _json
import logging
from abc import ABC, abstractmethod
from typing import Any, Generator, TypeVar

import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class LLMProvider(ABC):
    """Base class for all LLM providers."""

    @abstractmethod
    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        stream: bool = True,
        tools: list[dict] | None = None,
    ) -> str | Generator[str, None, None]:
        """Send messages to the LLM.

        When *stream* is True, yield string chunks.
        When *stream* is False, return the full response string.
        """
        ...

    @abstractmethod
    def chat_structured(
        self,
        messages: list[dict[str, str]],
        response_model: type[T],
    ) -> T:
        """Send messages and parse the response into a Pydantic model."""
        ...


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider using the official SDK."""

    def __init__(self, api_key: str, model: str) -> None:
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is required for the Anthropic provider.")
        import anthropic

        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        stream: bool = True,
        tools: list[dict] | None = None,
    ) -> str | Generator[str, None, None]:
        """Call the Anthropic Messages API."""
        # Separate system message from the rest
        system: str | None = None
        user_messages: list[dict[str, str]] = []
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                user_messages.append(msg)

        kwargs: dict[str, Any] = {
            "model": self._model,
            "max_tokens": 4096,
            "messages": user_messages,
        }
        if system:
            kwargs["system"] = system

        if stream:
            return self._stream(kwargs)

        response = self._client.messages.create(**kwargs)
        return response.content[0].text

    def chat_structured(
        self,
        messages: list[dict[str, str]],
        response_model: type[T],
    ) -> T:
        """Use Anthropic tool_use to enforce structured output."""
        system: str | None = None
        user_messages: list[dict[str, str]] = []
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                user_messages.append(msg)

        # Build a single tool from the Pydantic schema
        schema = response_model.model_json_schema()
        tool_def = {
            "name": "structured_output",
            "description": f"Return the result as a {response_model.__name__}",
            "input_schema": schema,
        }

        kwargs: dict[str, Any] = {
            "model": self._model,
            "max_tokens": 4096,
            "messages": user_messages,
            "tools": [tool_def],
            "tool_choice": {"type": "tool", "name": "structured_output"},
        }
        if system:
            kwargs["system"] = system

        response = self._client.messages.create(**kwargs)

        # Extract tool_use input from response
        for block in response.content:
            if block.type == "tool_use":
                return response_model.model_validate(block.input)

        raise RuntimeError("Anthropic returned no tool_use block for structured output")

    def _stream(self, kwargs: dict[str, Any]) -> Generator[str, None, None]:
        with self._client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                yield text


class OpenAIProvider(LLMProvider):
    """OpenAI provider using the official SDK."""

    def __init__(self, api_key: str, model: str) -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for the OpenAI provider.")
        import openai

        self._client = openai.OpenAI(api_key=api_key)
        self._model = model

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        stream: bool = True,
        tools: list[dict] | None = None,
    ) -> str | Generator[str, None, None]:
        """Call the OpenAI Chat Completions API."""
        if stream:
            return self._stream(messages)

        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,  # type: ignore[arg-type]
        )
        return response.choices[0].message.content or ""

    def chat_structured(
        self,
        messages: list[dict[str, str]],
        response_model: type[T],
    ) -> T:
        """Use OpenAI structured output (beta.chat.completions.parse)."""
        completion = self._client.beta.chat.completions.parse(
            model=self._model,
            messages=messages,  # type: ignore[arg-type]
            response_format=response_model,
        )
        result = completion.choices[0].message.parsed
        if result is None:
            raise RuntimeError("OpenAI returned no parsed output for structured output")
        return result

    def _stream(self, messages: list[dict[str, str]]) -> Generator[str, None, None]:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,  # type: ignore[arg-type]
            stream=True,
        )
        for chunk in response:
            delta = chunk.choices[0].delta  # type: ignore[union-attr]
            if delta.content:
                yield delta.content


class OllamaProvider(LLMProvider):
    """Ollama provider via its OpenAI-compatible HTTP endpoint."""

    def __init__(self, base_url: str, model: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        stream: bool = True,
        tools: list[dict] | None = None,
    ) -> str | Generator[str, None, None]:
        """Call Ollama's /v1/chat/completions endpoint."""
        url = f"{self._base_url}/v1/chat/completions"
        payload: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "stream": stream,
        }

        if stream:
            return self._stream(url, payload)

        with httpx.Client(timeout=120) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    def chat_structured(
        self,
        messages: list[dict[str, str]],
        response_model: type[T],
    ) -> T:
        """Ollama structured output via JSON mode + prompt-based schema."""
        schema = response_model.model_json_schema()
        # Append schema instruction to the last user message
        augmented = list(messages)
        last = augmented[-1]
        augmented[-1] = {
            **last,
            "content": (
                f"{last['content']}\n\n"
                f"Respond with ONLY valid JSON matching this schema:\n"
                f"```json\n{_json.dumps(schema, indent=2)}\n```"
            ),
        }

        url = f"{self._base_url}/v1/chat/completions"
        payload: dict[str, Any] = {
            "model": self._model,
            "messages": augmented,
            "stream": False,
            "format": "json",
        }

        with httpx.Client(timeout=120) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            raw_text = data["choices"][0]["message"]["content"]

        return response_model.model_validate_json(raw_text)

    def _stream(self, url: str, payload: dict[str, Any]) -> Generator[str, None, None]:
        with httpx.Client(timeout=120) as client:
            with client.stream("POST", url, json=payload) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line or not line.startswith("data: "):
                        continue
                    data_str = line[len("data: "):]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        chunk = _json.loads(data_str)
                        content = chunk["choices"][0]["delta"].get("content", "")
                        if content:
                            yield content
                    except (KeyError, _json.JSONDecodeError):
                        continue


def get_provider(settings: Any) -> LLMProvider:
    """Factory: return the appropriate LLMProvider based on settings.llm_provider."""
    provider = settings.llm_provider.lower()

    if provider == "anthropic":
        return AnthropicProvider(
            api_key=settings.anthropic_api_key,
            model=settings.llm_model,
        )
    elif provider == "openai":
        return OpenAIProvider(
            api_key=settings.openai_api_key,
            model=settings.llm_model,
        )
    elif provider == "ollama":
        return OllamaProvider(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
        )
    else:
        raise ValueError(
            f"Unknown LLM provider: {settings.llm_provider!r}. "
            "Supported: anthropic, openai, ollama."
        )

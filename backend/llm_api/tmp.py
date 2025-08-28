from typing import Callable, Any, Dict
from litellm import completion


def callable_client(
    provider: str, host: str, model: str
) -> Callable[[str, Dict[str, str]], str]:
    """
    Create an LLM client callable.

    Args:
        provider: Name of the LLM API provider (e.g., "openai", "anthropic", "ollama").
        host: Base URL of the API host, including port (e.g., "http://localhost:8000").
        model: Model identifier to use (e.g., "gpt-3.5-turbo").

    Returns:
        A callable that accepts a string input and returns the model's string output.
    """

    provider = provider.lower()

    def client_fn(prompt: str, args: dict[str, str]) -> str:
        text = prompt.format(**args)
        resp: Any = completion(
            model=f"{provider}/{model}",
            messages=[{"role": "user", "content": text}],
            api_base=host,
            stream=False,  # ensure dict-like response
        )
        return resp["choices"][0]["message"]["content"]

    return client_fn

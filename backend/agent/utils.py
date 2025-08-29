from typing import Callable, Any, Dict
from litellm import completion
import json


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


def parse_json_response(response: str) -> dict:
    """Given the raw response from an LLM expected to be in JSON format, returns the response parsed down to a dictionary"""

    cleaned_response = response.strip()
    # remove markdown code blocks if present
    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response[7:-3].strip()
    elif cleaned_response.startswith("```"):
        cleaned_response = cleaned_response[3:-3].strip()

    return json.loads(cleaned_response)


def read_prompt_template(name: str) -> str:
    with open(f"./agent/prompts/{name}.txt", "r") as f:
        feature_request_prompt = f.read()
        return feature_request_prompt

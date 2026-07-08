"""
ollama_client.py
----------------
A tiny wrapper around the local Ollama HTTP API.

Ollama runs on http://localhost:11434 by default.
We only need one endpoint: POST /api/generate

Docs: https://github.com/ollama/ollama/blob/main/docs/api.md
"""

import requests


# Default local Ollama endpoint. Change if you run Ollama on a different host/port.
OLLAMA_URL = "http://localhost:11434/api/generate"

# Default model. Change this in ONE place to switch models everywhere.
# Good beginner-friendly options: "gemma2:2b" (small/fast) or "qwen2.5:7b" (smarter).
DEFAULT_MODEL = "qwen2.5:7b"


class OllamaError(Exception):
    """Raised when we cannot talk to Ollama (server down, model missing, etc.)."""
    pass


def generate(prompt: str, model: str = DEFAULT_MODEL, temperature: float = 0.7) -> str:
    """
    Send a prompt to the local Ollama server and return the model's text reply.

    Parameters
    ----------
    prompt : str
        The full prompt (system + user instructions combined).
    model : str
        The Ollama model tag, e.g. "qwen2.5:7b" or "gemma2:2b".
    temperature : float
        Higher = more creative, lower = more focused. 0.7 is a good default.

    Returns
    -------
    str
        The model's generated text.

    Raises
    ------
    OllamaError
        If Ollama is not running, the model is missing, or the request fails.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,          # We want the full answer in one response.
        "options": {
            "temperature": temperature,
        },
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    except requests.exceptions.ConnectionError:
        raise OllamaError(
            "Could not connect to Ollama at http://localhost:11434.\n"
            "Make sure Ollama is installed and running:\n"
            "  1. Download from https://ollama.com/download\n"
            "  2. Start it (the Ollama app should be running in the background)\n"
            "  3. Pull the model:  ollama pull qwen2.5:7b"
        )
    except requests.exceptions.Timeout:
        raise OllamaError("Ollama took too long to respond. Try a smaller model like gemma2:2b.")

    if response.status_code != 200:
        raise OllamaError(
            f"Ollama returned an error (HTTP {response.status_code}): {response.text}"
        )

    data = response.json()
    # The response JSON looks like: {"model": "...", "response": "...", "done": true, ...}
    return data.get("response", "").strip()


def check_ollama_available(model: str = DEFAULT_MODEL) -> tuple[bool, str]:
    """
    Quick health check we can call before running the boardroom.
    Returns (is_ok, message).
    """
    try:
        # /api/tags lists installed models. If this works, Ollama is up.
        tags = requests.get("http://localhost:11434/api/tags", timeout=5)
        if tags.status_code != 200:
            return False, f"Ollama responded with HTTP {tags.status_code}."

        installed = [m["name"] for m in tags.json().get("models", [])]
        if model not in installed:
            return False, (
                f"Ollama is running, but the model '{model}' is not installed.\n"
                f"Run this in your terminal:  ollama pull {model}"
            )
        return True, f"Ollama is running and '{model}' is available."
    except requests.exceptions.ConnectionError:
        return False, (
            "Could not reach Ollama at http://localhost:11434.\n"
            "Start the Ollama app, then reload this page."
        )
    except Exception as e:
        return False, f"Unexpected error while checking Ollama: {e}"

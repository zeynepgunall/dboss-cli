import os
import re

import requests

OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = os.environ.get("DBOSS_MODEL", "qwen2.5-coder:3b")


def strip_code_fences(text: str) -> str:
    # Remove opening fence line: ```plaintext, ```bash, ``` etc.
    text = re.sub(r"^```[^\n]*\n", "", text)
    # Remove closing fence line
    text = re.sub(r"\n```\s*$", "", text)
    return text.strip()


class OllamaError(Exception):
    pass


def generate(prompt: str, model: str = DEFAULT_MODEL) -> str:
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    try:
        resp = requests.post(url, json=payload, timeout=120)
    except requests.exceptions.ConnectionError:
        raise OllamaError(
            "Ollama'ya bağlanılamadı. `ollama serve` çalışıyor mu? (localhost:11434)"
        )
    if resp.status_code == 404:
        raise OllamaError(
            f"Model bulunamadı: {model!r}. `ollama pull {model}` çalıştır."
        )
    if not resp.ok:
        raise OllamaError(f"Ollama HTTP {resp.status_code}: {resp.text[:200]}")
    return resp.json()["response"]

# Groq client (OpenAI-compatible)
import os
import re
import json
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3-70b")

def logger(msg: str):
    print(msg, flush=True)

def _extract_json_array(text: str):
    m = re.search(r"\[\s*{[\s\S]*}\s*\]", text)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    try:
        return json.loads(text)
    except Exception:
        return None

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def call_groq(system_prompt: str, user_prompt: str, temperature: float = 0.2, timeout: int = 60) -> str:
    assert GROQ_API_KEY, "Missing GROQ_API_KEY"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
    }
    r = requests.post(url, headers=headers, json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

def chat_json_array(system_prompt: str, user_prompt: str) -> list:
    raw = call_groq(system_prompt, user_prompt)
    arr = _extract_json_array(raw)
    if not isinstance(arr, list):
        # stricter retry
        strict_user = user_prompt + "\nReturn ONLY a JSON array with objects. No commentary, no markdown."
        raw = call_groq(system_prompt, strict_user)
        arr = _extract_json_array(raw)
    if not isinstance(arr, list):
        raise ValueError(f"Groq did not return a JSON array.\nGot: {raw[:500]}")
    return arr

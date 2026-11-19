"""Cached LLM call. Groq by default, Gemini optional. Same prompt means a cache hit and no API call."""
import hashlib
import os

from diskcache import Cache

_cache = Cache(os.environ.get("LLM_CACHE_DIR", ".cache/llm"))
GROQ_MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")


def complete(prompt: str, provider: str | None = None, max_tokens: int = 512) -> str:
    provider = provider or os.environ.get("DEFAULT_LLM_PROVIDER", "groq")
    key = hashlib.sha256(f"{provider}|{prompt}".encode()).hexdigest()
    if key in _cache:
        return _cache[key]
    if provider == "groq":
        from groq import Groq
        # In the cloud env the proxy injects the real key; any placeholder works here.
        client = Groq(api_key=os.environ.get("GROQ_API_KEY") or "proxy-injected")
        r = client.chat.completions.create(
            model=GROQ_MODEL, temperature=0, max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}])
        out = r.choices[0].message.content.strip()
    elif provider == "gemini":
        from google import genai
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or "proxy-injected")
        out = client.models.generate_content(model=GEMINI_MODEL, contents=prompt).text.strip()
    else:
        raise ValueError(provider)
    _cache[key] = out
    return out

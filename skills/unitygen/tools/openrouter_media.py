import base64
import os
from typing import Any

import requests

CHAT_COMPLETIONS_URL = "https://openrouter.ai/api/v1/chat/completions"


def require_api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")
    return key


def default_image_model() -> str:
    return os.environ.get("OPENROUTER_IMAGE_MODEL", "google/gemini-3.1-flash-image-preview")


def default_vision_model() -> str:
    return os.environ.get("OPENROUTER_VISION_MODEL", "google/gemini-2.0-flash-001")


def _headers() -> dict[str, str]:
    h = {
        "Authorization": f"Bearer {require_api_key()}",
        "Content-Type": "application/json",
    }
    site = os.environ.get("OPENROUTER_SITE_URL")
    if site:
        h["HTTP-Referer"] = site
    title = os.environ.get("OPENROUTER_APP_NAME")
    if title:
        h["X-Title"] = title
    return h


def chat_completions(payload: dict[str, Any]) -> dict[str, Any]:
    r = requests.post(CHAT_COMPLETIONS_URL, headers=_headers(), json=payload, timeout=600)
    try:
        data = r.json()
    except Exception:
        r.raise_for_status()
        raise RuntimeError(f"OpenRouter non-JSON response: {r.text[:500]}")
    if r.status_code >= 400:
        err = data.get("error") if isinstance(data, dict) else None
        msg = err.get("message", str(err)) if isinstance(err, dict) else r.text[:500]
        raise RuntimeError(f"OpenRouter HTTP {r.status_code}: {msg}")
    return data


def png_bytes_to_data_url(png: bytes) -> str:
    b64 = base64.standard_b64encode(png).decode("ascii")
    return f"data:image/png;base64,{b64}"


def extract_first_generated_png(data: dict[str, Any]) -> bytes:
    choices = data.get("choices")
    if not choices:
        raise ValueError("OpenRouter response has no choices")
    msg = choices[0].get("message") or {}
    images = msg.get("images") or []
    for im in images:
        if not isinstance(im, dict):
            continue
        iu = im.get("image_url") or im.get("imageUrl")
        url = None
        if isinstance(iu, dict):
            url = iu.get("url")
        elif isinstance(iu, str):
            url = iu
        if not url or "base64," not in url:
            continue
        raw = url.split("base64,", 1)[1]
        return base64.standard_b64decode(raw)
    raise ValueError("No generated image in assistant message (check model supports image output and modalities)")


def extract_assistant_text(data: dict[str, Any]) -> str | None:
    choices = data.get("choices")
    if not choices:
        return None
    msg = choices[0].get("message") or {}
    c = msg.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        parts = []
        for p in c:
            if isinstance(p, dict) and p.get("type") == "text":
                parts.append(p.get("text") or "")
        return "\n".join(parts) if parts else None
    return None

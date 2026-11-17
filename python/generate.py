"""Gemini 4 Carbon API example for PoYo (Python 3.9+, standard library only).

Usage:
    python python/generate.py                                 # Chat Completions (OpenAI format)
    python python/generate.py payloads/gemini-native.json     # Gemini Native generateContent
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PAYLOAD = ROOT / "payloads" / "chat-completions.json"
MODEL = "gemini-4-carbon"


def load_env() -> None:
    for env_path in (Path.cwd() / ".env", ROOT / ".env"):
        if not env_path.exists():
            continue
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


load_env()
API_KEY = os.environ.get("POYO_API_KEY", "")
BASE_URL = os.environ.get("POYO_BASE_URL", "https://api.poyo.ai").rstrip("/")
if not API_KEY or API_KEY == "YOUR_POYO_API_KEY_HERE":
    sys.exit("Set POYO_API_KEY in your environment or repo-root .env file.")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "poyo-gemini-4-carbon-api-example/1.0",
}


def post_json(path: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            status, text = response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        status, text = error.code, error.read().decode("utf-8", "replace")
    try:
        body = json.loads(text) if text else {}
    except ValueError:
        body = {"raw": text}
    if status >= 400 or (isinstance(body, dict) and body.get("error")):
        raise RuntimeError(f"PoYo request failed: {json.dumps({'http_status': status, 'body': body}, indent=2)}")
    return body


payload_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PAYLOAD
payload = json.loads(payload_path.read_text(encoding="utf-8"))

if "contents" in payload:
    result = post_json(f"/v1beta/models/{MODEL}:generateContent", payload)
    candidates = result.get("candidates") or [{}]
    parts = (candidates[0].get("content") or {}).get("parts") or []
    # Thinking models can return parts without text; keep only text parts.
    print("".join(p["text"] for p in parts if isinstance(p.get("text"), str) and not p.get("thought")))
    print(json.dumps({"usageMetadata": result.get("usageMetadata")}, indent=2))
else:
    payload.setdefault("model", MODEL)
    result = post_json("/v1/chat/completions", payload)
    choices = result.get("choices") or [{}]
    print((choices[0].get("message") or {}).get("content") or "")
    print(json.dumps({"usage": result.get("usage")}, indent=2))

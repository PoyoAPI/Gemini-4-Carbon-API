# Gemini 4 Carbon API: cURL quickstart

```bash
export POYO_API_KEY="your-api-key"
export POYO_BASE_URL="https://api.poyo.ai"
```

## Chat Completions (OpenAI format)

```bash
curl -X POST "$POYO_BASE_URL/v1/chat/completions" \
  -H "Authorization: Bearer $POYO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "gemini-4-carbon",
  "messages": [
    {
      "role": "system",
      "content": "You are a senior security engineer. Be precise and cite line numbers."
    },
    {
      "role": "user",
      "content": "Review this Python handler for vulnerabilities and propose a patched version:\n\nimport sqlite3\n\ndef get_user(conn, username):\n    cur = conn.cursor()\n    cur.execute(\"SELECT * FROM users WHERE name = '\''\" + username + \"'\''\")\n    return cur.fetchone()"
    }
  ],
  "max_tokens": 2048
}'
```

## Streaming with Chat Completions

Add `"stream": true` to receive server-sent events:

```bash
curl -X POST "$POYO_BASE_URL/v1/chat/completions" \
  -H "Authorization: Bearer $POYO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "gemini-4-carbon",
  "messages": [
    {
      "role": "user",
      "content": "Explain the difference between a mutex and a semaphore in three sentences."
    }
  ],
  "stream": true
}'
```

## Gemini Native generateContent

The model ID goes in the URL path, not the body. The response is Google's `GenerateContentResponse` without a `code` / `data` wrapper.

```bash
curl -X POST "$POYO_BASE_URL/v1beta/models/gemini-4-carbon:generateContent" \
  -H "Authorization: Bearer $POYO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "Plan a step-by-step migration of a 200-file JavaScript codebase to TypeScript. List the phases, the risks in each phase, and how to verify each phase before moving on."
        }
      ]
    }
  ],
  "generationConfig": {
    "maxOutputTokens": 4096,
    "temperature": 0.7
  }
}'
```

## Gemini Native streaming

`streamGenerateContent` returns `text/event-stream`: each `data:` line is a partial `GenerateContentResponse`, and the stream ends with `data: [DONE]`.

```bash
curl -N -X POST "$POYO_BASE_URL/v1beta/models/gemini-4-carbon:streamGenerateContent" \
  -H "Authorization: Bearer $POYO_API_KEY" \
  -H "Content-Type: application/json" \
  -d @payloads/gemini-native.json
```

Keep the API key on your server. Add timeouts, bounded retries, and usage logging before production.

See the [full README](../README.md) and [production notes](../docs/production-notes.md).

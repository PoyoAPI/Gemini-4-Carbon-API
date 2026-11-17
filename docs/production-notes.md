# Gemini 4 Carbon API production notes

## Confirmed contract

- Chat Completions: `POST /v1/chat/completions` with `"model": "gemini-4-carbon"`
- Gemini Native: `POST /v1beta/models/gemini-4-carbon:generateContent` or `:streamGenerateContent`
- Authentication: `Authorization: Bearer <POYO_API_KEY>`
- Responses use each format's native shape, without the `code` / `data` wrapper used by generation tasks

## Input limits

| Field | Requirement | Constraint |
| --- | --- | --- |
| model (Chat Completions) | required | gemini-4-carbon. |
| messages | required | Role/content messages: system, user, assistant. |
| max_tokens | optional | Integer ≥ 1. Gemini 4 Carbon returns up to 64K output tokens. |
| temperature / top_p | optional | 0–2 / 0–1. |
| stream | optional | true returns server-sent events. |
| contents (Gemini Native) | required | Role (user or model) plus parts with text or inlineData. |
| generationConfig | optional | temperature (0–2), topP (0–1), topK (≥ 1), maxOutputTokens (≥ 1), stopSequences. |
| safetySettings | optional | Category and threshold pairs. |

Context window: 1M tokens. Input: text, image, audio, video, and PDF; output: text.

Gemini Native errors use the Google error shape: `{"error": {"code": 400, "message": "...", "status": "INVALID_ARGUMENT"}}`. An unknown model id returns 404.

## Operational checklist

- Keep API keys in a server-side secret manager.
- Validate user input before calling the API.
- Apply request timeouts and retry only rate limits or transient 5xx responses.
- Bound output tokens and log usage for cost control.
- Redact sensitive prompt and response content from logs.
- Recheck the live model page before hard-coding prices.

## Failure handling

Treat non-2xx HTTP responses and bodies with an `error` object as errors. Preserve the HTTP status and a redacted response body for debugging. Retry only 429 and transient 5xx responses.

Schema: [PoYo API documentation](https://docs.poyo.ai/api-manual/chat-series/google?utm_source=github&utm_medium=readme&utm_campaign=gemini-4-carbon-api)

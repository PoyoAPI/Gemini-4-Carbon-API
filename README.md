# Gemini 4 Carbon API: cURL, Python, and Node.js Examples

[![Gemini 4 Carbon on PoYo](https://img.shields.io/badge/Try%20on%20PoYo-gemini--4--carbon-84cc16)](https://poyo.ai/models/gemini-4-carbon?utm_source=github&utm_medium=readme&utm_campaign=gemini-4-carbon-api) [![API docs](https://img.shields.io/badge/API-docs-22d3ee)](https://docs.poyo.ai/api-manual/chat-series/gemini-native-format?utm_source=github&utm_medium=readme&utm_campaign=gemini-4-carbon-api) [![Check](https://github.com/PoyoAPI/Gemini-4-Carbon-API/actions/workflows/check.yml/badge.svg)](https://github.com/PoyoAPI/Gemini-4-Carbon-API/actions/workflows/check.yml)

Runnable examples for Google **Gemini 4 Carbon** through PoYo, in both the OpenAI-compatible Chat Completions format and the Gemini Native `generateContent` format: long-horizon agentic coding, knowledge work over dense documents, and security review with a 1M-token context window.

**Answer:** To use the Gemini 4 Carbon API, send a server-side request to `POST https://api.poyo.ai/v1/chat/completions` with `"model": "gemini-4-carbon"`, or to `POST https://api.poyo.ai/v1beta/models/gemini-4-carbon:generateContent`, with a PoYo API key. The examples in this repository run with Python 3.9+, Node.js 22+, or cURL.

Last verified against the live PoYo schema and pricing on **November 17, 2026**.

## Gemini 4 Carbon at a glance

- **Model ID:** `gemini-4-carbon`
- **Formats:** Chat Completions (`/v1/chat/completions`) and Gemini Native (`/v1beta/models/gemini-4-carbon:generateContent` and `:streamGenerateContent`)
- **Context:** 1M tokens; up to 64K output tokens per response
- **Input:** text, image, audio, video, and PDF; output is text
- **Availability:** announced by Google on October 28, 2026; on the Gemini API paid tier since November 10, 2026
- **Price on PoYo:** $1.60 input, $8.00 output, and $0.08 cache read per 1M tokens, 20% below Google's $2.00 / $10.00

## Quickstart

1. Create a key in the [PoYo dashboard](https://poyo.ai/dashboard/api-key?utm_source=github&utm_medium=readme&utm_campaign=gemini-4-carbon-api).
2. Copy `.env.example` to `.env` and replace the placeholder.
3. Run one of the examples. Each prints the model's text and the token usage.

```dotenv
POYO_API_KEY=YOUR_POYO_API_KEY_HERE
POYO_BASE_URL=https://api.poyo.ai
```

### Python

```bash
python python/generate.py                              # Chat Completions
python python/generate.py payloads/gemini-native.json  # Gemini Native
```

[`python/generate.py`](python/generate.py) uses only the Python standard library.

### Node.js

```bash
node node/index.mjs
node node/index.mjs payloads/gemini-native.json
```

### cURL

```bash
curl -X POST "https://api.poyo.ai/v1/chat/completions" \
  -H "Authorization: Bearer $POYO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini-4-carbon", "messages": [{"role": "user", "content": "Explain the difference between a mutex and a semaphore in three sentences."}]}'
```

Streaming and Gemini Native requests are in [curl/generate.md](curl/generate.md).

### OpenAI SDK

Point the OpenAI SDK at `https://api.poyo.ai/v1`, use your PoYo API key, and set `model` to `gemini-4-carbon`.

## Example requests

| File | Format | Task |
| --- | --- | --- |
| [`chat-completions.json`](payloads/chat-completions.json) | Chat Completions | Security review of a SQL-injection-prone handler, `max_tokens: 2048` |
| [`gemini-native.json`](payloads/gemini-native.json) | Gemini Native | JavaScript-to-TypeScript migration plan, `maxOutputTokens: 4096` |

## Request fields

### Chat Completions

| Field | Requirement | Meaning |
| --- | --- | --- |
| model | required | `gemini-4-carbon`. |
| messages | required | `system`, `user`, and `assistant` messages with `content`. |
| max_tokens | optional | Maximum generated tokens. |
| temperature | optional | 0–2. |
| top_p | optional | 0–1. Use either `top_p` or `temperature`. |
| stream | optional | `true` returns server-sent events. |

### Gemini Native

| Field | Requirement | Meaning |
| --- | --- | --- |
| contents | required | Turns with `role` (`user` or `model`) and `parts` (`text` or `inlineData`). |
| generationConfig | optional | `temperature`, `topP`, `topK`, `maxOutputTokens`, `stopSequences`. |
| safetySettings | optional | Category and threshold pairs. |

In Gemini Native, the model ID goes in the URL path. The response is Google's `GenerateContentResponse`: text is in `candidates[].content.parts[].text` and token counts in `usageMetadata`. Thinking parts can carry `thought: true` or a `thoughtSignature` without `text`; skip them when you join the text.

## Pricing

1 credit = $0.005.

| Usage | PoYo | Google list price |
| --- | --- | --- |
| Input | 320 credits ($1.60) per 1M tokens | $2.00 per 1M tokens |
| Output | 1,600 credits ($8.00) per 1M tokens | $10.00 per 1M tokens |
| Cache read | 16 credits ($0.08) per 1M tokens | $0.10 per 1M tokens |

Example: a request with 10,000 input tokens and 2,000 output tokens costs 10,000 × $1.60 / 1M + 2,000 × $8.00 / 1M = $0.032 (6.4 credits). Google counts thinking tokens as output. Confirm current prices on the [model page](https://poyo.ai/models/gemini-4-carbon?utm_source=github&utm_medium=readme&utm_campaign=gemini-4-carbon-api).

## When to choose Carbon over Argon

Gemini 4 Carbon and Gemini 4 Argon have the same token price. Google positions Argon as the efficient model with faster responses and lower token spend per turn. Carbon spends more tokens to reason and verify, and scores higher on Google's model card, for example 65.2% vs 57.1% on Terminal-Bench 4.0 (AA) and 96.2% vs 84.2% on GraphWalks 256K–1M. Pick Carbon for the hardest coding, research, and security tasks.

## Production guidance

Set an application timeout long enough for deep reasoning, retry only 429 and transient 5xx responses, cap `max_tokens` or `maxOutputTokens`, and record token usage. Do not put `POYO_API_KEY` in browser or mobile client code. LLM responses come back in each format's native shape, so check the HTTP status and the `error` object rather than a `code` field.

## FAQ

**How much does the Gemini 4 Carbon API cost?** On PoYo, $1.60 per 1M input tokens, $8.00 per 1M output tokens, and $0.08 per 1M cache-read tokens, 20% below Google's price.

**What are the context window and max output?** A 1M-token context window and up to 64K output tokens per response.

**Can I use the OpenAI SDK?** Yes. Set the base URL to `https://api.poyo.ai/v1` and `model` to `gemini-4-carbon`.

**Does it support streaming?** Yes: `"stream": true` in Chat Completions, or `:streamGenerateContent` in Gemini Native.

**Is there a free tier?** Google lists no free tier for Gemini 4 Carbon. On PoYo you pay as you go with credits and can try the model in the Playground first.

## Repository map

- [`payloads/`](payloads) — Chat Completions and Gemini Native request bodies
- [`python/generate.py`](python/generate.py) — standard-library Python example
- [`node/index.mjs`](node/index.mjs) — dependency-free Node.js example
- [`curl/generate.md`](curl/generate.md) — copy-paste cURL requests, including streaming
- [`docs/production-notes.md`](docs/production-notes.md) — limits and rollout checklist

## Related repositories

- [Gemini-3.5-Flash-API](https://github.com/PoyoAPI/Gemini-3.5-Flash-API) — Gemini 3.5 Flash examples
- [Claude-Opus-5-API](https://github.com/PoyoAPI/Claude-Opus-5-API) — Claude Opus 5 through the Anthropic Messages format
- [awesome-poyo-api](https://github.com/PoyoAPI/awesome-poyo-api) — every PoYo model repository in one list
- [poyo-devtools](https://github.com/PoyoAPI/poyo-devtools) — PoYo CLI, MCP bridge, and Agent Skill

## Links

- [Gemini 4 Carbon API on PoYo](https://poyo.ai/models/gemini-4-carbon?utm_source=github&utm_medium=readme&utm_campaign=gemini-4-carbon-api)
- [Gemini Native API reference](https://docs.poyo.ai/api-manual/chat-series/gemini-native-format?utm_source=github&utm_medium=readme&utm_campaign=gemini-4-carbon-api)
- [Google models on PoYo](https://docs.poyo.ai/api-manual/chat-series/google?utm_source=github&utm_medium=readme&utm_campaign=gemini-4-carbon-api)
- [Chat Completions API reference](https://docs.poyo.ai/api-manual/chat-series/chat-completions?utm_source=github&utm_medium=readme&utm_campaign=gemini-4-carbon-api)
- [PoYo model catalog](https://poyo.ai/models?utm_source=github&utm_medium=readme&utm_campaign=gemini-4-carbon-api)

## License

MIT

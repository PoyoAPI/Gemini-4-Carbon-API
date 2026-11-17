import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

for (const envPath of [resolve(process.cwd(), ".env"), resolve(process.cwd(), "../.env")]) {
  if (!existsSync(envPath)) continue;
  for (const line of readFileSync(envPath, "utf8").split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const index = trimmed.indexOf("=");
    if (index < 0) continue;
    const key = trimmed.slice(0, index).trim();
    const value = trimmed.slice(index + 1).trim();
    if (!process.env[key]) process.env[key] = value;
  }
}

const apiKey = process.env.POYO_API_KEY;
const baseUrl = process.env.POYO_BASE_URL || "https://api.poyo.ai";
if (!apiKey || apiKey === "YOUR_POYO_API_KEY_HERE") {
  console.error("Set POYO_API_KEY in your environment or repo-root .env file.");
  process.exit(1);
}

const MODEL = "gemini-4-carbon";

async function requestJson(path, payload) {
  const response = await fetch(`${baseUrl}${path}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const text = await response.text();
  let body = {};
  if (text) {
    try { body = JSON.parse(text); } catch { body = { raw: text }; }
  }
  if (!response.ok || body?.error) {
    throw new Error(`PoYo request failed: ${JSON.stringify({ http_status: response.status, body }, null, 2)}`);
  }
  return body;
}

// Pass a payload file, e.g. `node node/index.mjs payloads/gemini-native.json`.
// Payloads with "contents" use Gemini Native; payloads with "messages" use Chat Completions.
const repoRoot = fileURLToPath(new URL("..", import.meta.url));
const payloadPath = process.argv[2]
  ? resolve(process.cwd(), process.argv[2])
  : resolve(repoRoot, "payloads/chat-completions.json");
const payload = JSON.parse(readFileSync(payloadPath, "utf8"));

if (payload.contents) {
  const result = await requestJson(`/v1beta/models/${MODEL}:generateContent`, payload);
  // Thinking models can return parts without text; keep only text parts.
  const parts = result.candidates?.[0]?.content?.parts ?? [];
  console.log(parts.filter((part) => typeof part.text === "string" && !part.thought).map((part) => part.text).join(""));
  console.log(JSON.stringify({ usageMetadata: result.usageMetadata }, null, 2));
} else {
  const result = await requestJson("/v1/chat/completions", { ...payload, model: payload.model || MODEL });
  console.log(result.choices?.[0]?.message?.content ?? "");
  console.log(JSON.stringify({ usage: result.usage }, null, 2));
}

# DevAssist — engineering-focused CLI LLM client

A Python command-line client demonstrating conversation state, streaming, provider usage accounting, stop reasons, retry policy, context limits, strict JSON-schema extraction, and a validated tool-calling loop.

## 1. Setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and add an API key from the provider dashboard. Never commit `.env`; `.gitignore` excludes it. The key is read only from the environment. Do not paste it into source code, screenshots, README, or GitHub. If it was ever committed, revoke it and create a new key; deleting the file in a later commit does not erase Git history.

## 2. Run

```powershell
python assistant.py
```

Commands: `/stateless`, `/tool`, `/invoice [path]`, `/quit`. Normal text starts a multi-turn conversation. The interactive client sends its own local history on each request.

## 3. Requirements map

1. **Multi-turn and stateless proof:** `CLI.history` stores system/user/assistant messages. `/stateless` makes two independent requests; the second does not resend the first message.
2. **System role:** `SYSTEM_PROMPT` defines DevAssist.
3. **Streaming/timing:** streamed chunks are printed immediately; first visible text chunk and total wall-clock durations are measured with `time.perf_counter()`. Record your own run; timings depend on network/model and are not hard-coded.
4. **Token accounting:** usage comes from provider response `usage.prompt_tokens` and `usage.completion_tokens`; cost is estimated from configurable published rates in `.env`. No local tokenizer approximation is used for billing counts.
5. **Stop reasons:** `stop`, `length`, `content_filter`, `tool_calls`, unknown reasons, and refusal metadata are handled explicitly.
6. **Retries:** HTTP 429 and 5xx only, up to five attempts, exponential delay plus random jitter. Other 4xx errors are raised without retry. SDK automatic retries are disabled to avoid hidden duplicate attempts.
7. **Context:** provider token-count endpoint counts the candidate history; oldest user/assistant turn pairs are dropped and reported until within `CONTEXT_TOKEN_BUDGET`.
8. **Structured output:** `/invoice` uses strict JSON Schema mode. Regex output is printed beside model extraction.
9. **Tool loop:** `/tool` offers a calculator; Pydantic validates arguments, tool name is allowlisted, division-by-zero is blocked, and the loop is capped.
10. **Secrets:** `.env` + `.gitignore`; no key in source.

## 4. Invoice OCR fixture — important

The original DocuScan OCR output was not available among the files accessible for this build. `data/invoice_ocr.txt` is therefore a **synthetic, clearly labelled sample**, not your original invoice. Replace its contents with the exact OCR text you saved during the OCR project, then run `/invoice`. Do not submit the sample comparison as evidence from your original OCR task. Regex baseline is deliberately simple and may need adapting to your original field patterns.

## 5. Pricing and model configuration

Defaults in `.env.example` are example standard rates for `gpt-4o-mini` (USD per 1M input/output tokens). Pricing changes; verify the current provider pricing page before reporting costs. Change `OPENAI_MODEL`, `INPUT_USD_PER_MILLION`, and `OUTPUT_USD_PER_MILLION` together. The CLI reports token counts returned by the provider; the cost calculation is an estimate and excludes any non-token charges.

Official references:
- API pricing: https://platform.openai.com/pricing
- Chat Completions: https://platform.openai.com/docs/api-reference/chat
- Structured Outputs: https://platform.openai.com/docs/guides/structured-outputs
- Function calling: https://platform.openai.com/docs/guides/function-calling

## 6. Evidence to capture for submission

Run the app with your own API key and capture terminal output for:
- a multi-turn name recall (first tell it your name, then ask it to recall it);
- `/stateless` (two calls, second request without history);
- one streamed answer showing TTFT and total time;
- token/cost line after a turn;
- `/invoice` with your original OCR text and regex/model comparison;
- `/tool` showing model request, local validated execution, and final answer;
- context trimming: temporarily set budget very low (e.g. 300) and continue chatting;
- max-token handling: temporarily set `MAX_OUTPUT_TOKENS=20` and request a long answer;
- refusal handling: test an explicitly disallowed request and retain provider refusal result if returned.

Do not invent TTFT, token counts, costs, refusal, truncation or API outputs. Save actual terminal captures in `evidence/`.

## 7. Local tests

```powershell
pytest -q
```

These tests cover calculator validation and regex extraction locally; API-backed behaviour requires a valid key and network connection.

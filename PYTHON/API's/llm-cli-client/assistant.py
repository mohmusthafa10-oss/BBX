"""Engineering-focused CLI chat client using OpenAI Chat Completions."""
from __future__ import annotations
import json, os, random, sys, time
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from openai import OpenAI, APIStatusError, RateLimitError
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
INPUT_RATE = float(os.getenv("INPUT_USD_PER_MILLION", "0.15"))
OUTPUT_RATE = float(os.getenv("OUTPUT_USD_PER_MILLION", "0.60"))
MAX_OUTPUT = int(os.getenv("MAX_OUTPUT_TOKENS", "500"))
CONTEXT_BUDGET = int(os.getenv("CONTEXT_TOKEN_BUDGET", "6000"))
SYSTEM_PROMPT = "You are DevAssist, a concise, friendly programming tutor. Explain concepts clearly and ask clarifying questions when needed. Never claim to have executed code you have not run."

class InvoiceFields(BaseModel):
    invoice_number: str | None = None
    invoice_date: str | None = None
    vendor: str | None = None
    total: float | None = None
    currency: str | None = None

class CalculatorArgs(BaseModel):
    operation: str = Field(pattern="^(add|subtract|multiply|divide)$")
    a: float = Field(ge=-1_000_000, le=1_000_000)
    b: float = Field(ge=-1_000_000, le=1_000_000)

class CLI:
    def __init__(self, client: OpenAI):
        self.client = client
        self.history: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.total_cost = 0.0

    def retry(self, fn):
        for attempt in range(5):
            try:
                return fn()
            except RateLimitError:
                if attempt == 4: raise
            except APIStatusError as exc:
                if exc.status_code < 500 or exc.status_code > 599: raise
                if attempt == 4: raise
            delay = min(16, 0.75 * (2 ** attempt)) + random.uniform(0, 0.5)
            print(f"\n[retry] transient API error; waiting {delay:.2f}s ({attempt+1}/5)", file=sys.stderr)
            time.sleep(delay)

    def report_usage(self, usage: Any):
        if usage is None:
            print("[usage] Provider did not return token usage for this response.")
            return
        inp, out = usage.prompt_tokens, usage.completion_tokens
        cost = (inp * INPUT_RATE + out * OUTPUT_RATE) / 1_000_000
        self.total_cost += cost
        print(f"\n[tokens] input={inp:,} output={out:,} | turn=${cost:.8f} | running=${self.total_cost:.8f}")

    def manage_context(self):
        # Use the provider's token-count endpoint, not a local tokenizer estimate.
        while len(self.history) > 3:
            counted = self.retry(lambda: self.client.responses.input_tokens.count(
                model=MODEL, input=self.history))
            if counted.input_tokens <= CONTEXT_BUDGET:
                return
            removed = self.history[1:3]
            del self.history[1:3]
            print(f"[context] budget exceeded ({counted.input_tokens:,}>{CONTEXT_BUDGET:,}); dropped oldest {len(removed)//2} user/assistant turn(s).")

    def chat(self, user_text: str):
        self.history.append({"role": "user", "content": user_text})
        self.manage_context()
        start = time.perf_counter(); first = None; pieces=[]; usage=None; finish=None; refusal=False
        def request():
            return self.client.chat.completions.create(
                model=MODEL, messages=self.history, max_tokens=MAX_OUTPUT,
                stream=True, stream_options={"include_usage": True})
        stream = self.retry(request)
        for chunk in stream:
            if chunk.usage is not None: usage = chunk.usage
            if not chunk.choices: continue
            choice = chunk.choices[0]
            if choice.delta.content:
                if first is None:
                    first = time.perf_counter(); print(f"[timing] time-to-first-token={(first-start):.3f}s\nAssistant: ", end="", flush=True)
                print(choice.delta.content, end="", flush=True); pieces.append(choice.delta.content)
            if choice.finish_reason is not None: finish = choice.finish_reason
            if getattr(choice.delta, "refusal", None): refusal = True
        elapsed = time.perf_counter()-start
        answer = "".join(pieces)
        print()
        if refusal:
            print("[stop] refusal: provider marked this response as a refusal.")
        elif finish == "length":
            print("[stop] max_tokens reached: output may be truncated. Increase MAX_OUTPUT_TOKENS or ask to continue.")
        elif finish == "stop": print("[stop] normal completion.")
        elif finish == "content_filter": print("[stop] content_filter: provider stopped output due to its safety filter.")
        elif finish == "tool_calls": print("[stop] tool_calls: model requested a tool; handled by tool demo.")
        else: print(f"[stop] unexpected/unknown finish reason: {finish!r}")
        print(f"[timing] total={(elapsed):.3f}s; time-to-first-token={(first-start):.3f}s" if first else f"[timing] total={elapsed:.3f}s; no text token received")
        self.report_usage(usage)
        if answer and finish in ("stop", "length"): self.history.append({"role":"assistant", "content":answer})

    def structured_invoice(self, path: Path):
        raw = path.read_text(encoding="utf-8")
        schema = {"type":"object", "properties": {
            "invoice_number":{"type":["string","null"]}, "invoice_date":{"type":["string","null"]},
            "vendor":{"type":["string","null"]}, "total":{"type":["number","null"]},
            "currency":{"type":["string","null"]}}, "required":["invoice_number","invoice_date","vendor","total","currency"], "additionalProperties":False}
        response = self.retry(lambda: self.client.chat.completions.create(
            model=MODEL, messages=[{"role":"system","content":"Extract invoice fields. Return null for missing values; do not infer."},{"role":"user","content":raw}],
            response_format={"type":"json_schema","json_schema":{"name":"invoice_fields","strict":True,"schema":schema}}, max_tokens=300))
        msg=response.choices[0].message
        if msg.refusal: print("[structured] Refusal:",msg.refusal)
        elif response.choices[0].finish_reason == "length": print("[structured] Truncated; increase MAX_OUTPUT_TOKENS.")
        else:
            extracted=InvoiceFields.model_validate_json(msg.content)
            regex=regex_invoice(raw)
            print("\n[structured model fields]\n"+extracted.model_dump_json(indent=2))
            print("[regex fields]\n"+json.dumps(regex,indent=2))
            print("[comparison] Review differences manually; regex is intentionally simple.")
        self.report_usage(response.usage)

    def calculator_demo(self):
        tools=[{"type":"function","function":{"name":"calculator","description":"Perform one basic arithmetic operation.","parameters":CalculatorArgs.model_json_schema(),"strict":True}}]
        messages=[{"role":"system","content":"Use the calculator tool for arithmetic requests. Do not calculate mentally."},{"role":"user","content":"Use the calculator to calculate (184.5 divided by 3) plus 27."}]
        for _ in range(4):
            response=self.retry(lambda:self.client.chat.completions.create(model=MODEL,messages=messages,tools=tools,tool_choice="auto",max_tokens=300))
            self.report_usage(response.usage)
            choice=response.choices[0]; messages.append(choice.message)
            if choice.finish_reason == "length": print("[tool] Model response truncated."); return
            if choice.message.refusal: print("[tool] Refusal:",choice.message.refusal); return
            if choice.finish_reason == "stop": print("[tool result]",choice.message.content); return
            if choice.finish_reason != "tool_calls": print("[tool] Unhandled stop reason:",choice.finish_reason); return
            for call in choice.message.tool_calls:
                if call.function.name != "calculator": raise ValueError("Unknown tool requested")
                args=CalculatorArgs.model_validate_json(call.function.arguments)
                result=calculate(args)
                print(f"[tool execution] calculator({args.operation}, {args.a}, {args.b}) = {result}")
                messages.append({"role":"tool","tool_call_id":call.id,"content":str(result)})
        print("[tool] Safety limit reached: too many tool turns.")

def calculate(x: CalculatorArgs) -> float:
    if x.operation == "add": return x.a+x.b
    if x.operation == "subtract": return x.a-x.b
    if x.operation == "multiply": return x.a*x.b
    if x.b == 0: raise ValueError("Division by zero is not allowed")
    return x.a/x.b

def regex_invoice(text: str) -> dict:
    import re
    def find(pattern):
        m=re.search(pattern,text,re.I|re.M); return m.group(1).strip() if m else None
    total=find(r"(?:grand\s+)?total\s*[:\-]?\s*(?:AED|USD|INR|₹|\$)?\s*([\d,]+\.\d{2})")
    return {"invoice_number":find(r"invoice\s*(?:no|number|#)\s*[:#-]?\s*([A-Z0-9/-]+)"),
            "invoice_date":find(r"date\s*[:\-]?\s*(\d{1,4}[/-]\d{1,2}[/-]\d{1,4})"),
            "vendor":find(r"(?m)^([A-Z][A-Za-z &.,'-]{2,})$"),
            "total":float(total.replace(",","")) if total else None,
            "currency":find(r"\b(AED|USD|INR)\b|([₹$])")}

def stateless_demo(client: OpenAI):
    print("\n=== STATELESS PROOF ===")
    first=client.chat.completions.create(model=MODEL,messages=[{"role":"user","content":"My name is Midhun. Reply only: remembered."}],max_tokens=20)
    print("Turn 1:",first.choices[0].message.content)
    second=client.chat.completions.create(model=MODEL,messages=[{"role":"user","content":"What is my name?"}],max_tokens=40)
    print("Turn 2 WITHOUT prior messages:",second.choices[0].message.content)
    print("Compare: the second request contains no name/history. Model recall is not guaranteed; this run demonstrates lack of application-managed memory.")
    for r in (first,second):
        u=r.usage
        if u: print(f"[tokens] input={u.prompt_tokens} output={u.completion_tokens}")

def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Missing OPENAI_API_KEY. Copy .env.example to .env and add your API key.")
    client=OpenAI(api_key=os.environ["OPENAI_API_KEY"],timeout=60,max_retries=0)
    app=CLI(client)
    print(f"DevAssist CLI | model={MODEL} | context budget={CONTEXT_BUDGET:,} provider tokens")
    print("Commands: /stateless, /invoice [path], /tool, /quit")
    while True:
        try: line=input("\nYou: ").strip()
        except (EOFError,KeyboardInterrupt): print("\nBye."); break
        if not line: continue
        if line=="/quit": break
        if line=="/stateless": stateless_demo(client); continue
        if line=="/tool": app.calculator_demo(); continue
        if line.startswith("/invoice"):
            parts=line.split(maxsplit=1); path=Path(parts[1]) if len(parts)>1 else ROOT/"data"/"invoice_ocr.txt"
            app.structured_invoice(path); continue
        try: app.chat(line)
        except Exception as exc: print(f"\n[error] {type(exc).__name__}: {exc}")

if __name__=="__main__": main()

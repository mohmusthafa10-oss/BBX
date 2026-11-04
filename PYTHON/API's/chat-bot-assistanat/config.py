import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent

load_dotenv(ROOT / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

MAX_OUTPUT_TOKENS = int(
    os.getenv("MAX_OUTPUT_TOKENS", 500)
)

CONTEXT_TOKEN_BUDGET = int(
    os.getenv("CONTEXT_TOKEN_BUDGET", 6000)
)

INPUT_RATE = float(
    os.getenv("INPUT_USD_PER_MILLION", 0)
)

OUTPUT_RATE = float(
    os.getenv("OUTPUT_USD_PER_MILLION", 0)
)

SYSTEM_PROMPT = """
You are DevAssist, a concise and friendly programming tutor.

Explain programming concepts clearly.
Use simple examples.
Ask clarifying questions when needed.
Never claim to have executed code you have not run.
"""
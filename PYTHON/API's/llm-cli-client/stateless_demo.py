"""Standalone repeatable stateless API demonstration."""
from assistant import stateless_demo, OpenAI
import os
if not os.getenv("OPENAI_API_KEY"):
    raise SystemExit("Set OPENAI_API_KEY in .env first")
stateless_demo(OpenAI(api_key=os.environ["OPENAI_API_KEY"], max_retries=0))

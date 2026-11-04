import time

from google.genai import types

from config import (
    MODEL,
    SYSTEM_PROMPT,
    MAX_OUTPUT_TOKENS,
    CONTEXT_TOKEN_BUDGET
)

from services.gemini_client import retry_call


class ChatService:

    def __init__(self, client, usage_tracker):

        self.client = client
        self.usage_tracker = usage_tracker

        self.history = []

        self.chat_config = types.GenerateContentConfig(

            system_instruction=SYSTEM_PROMPT,

            max_output_tokens=MAX_OUTPUT_TOKENS
        )

    # -------------------------
    # Context Management
    # -------------------------

    def manage_context(self):

        while len(self.history) > 2:

            counted = retry_call(
                lambda: self.client.models.count_tokens(
                    model=MODEL,
                    contents=self.history
                )
            )

            token_count = counted.total_tokens or 0

            if token_count <= CONTEXT_TOKEN_BUDGET:
                return

            del self.history[:2]

            print(
                f"\n[context] Removed oldest conversation turn."
                f" Tokens: {token_count}"
            )

    # -------------------------
    # Stop Reason
    # -------------------------

    def check_finish_reason(self, response):

        try:

            reason = (
                response.candidates[0].finish_reason.name
            )

        except (AttributeError, IndexError, TypeError):

            reason = "UNKNOWN"

        if reason == "STOP":

            print("\n[stop] Normal completion.")

        elif reason == "MAX_TOKENS":

            print("\n[stop] Maximum output tokens reached.")

        elif reason in (
            "SAFETY",
            "BLOCKLIST",
            "PROHIBITED_CONTENT"
        ):

            print("\n[stop] Safety-related stop.")

        elif reason == "RECITATION":

            print("\n[stop] Recitation-related stop.")

        else:

            print(f"\n[stop] {reason}")

    # -------------------------
    # Chat
    # -------------------------

    def chat(self, user_text):

        self.history.append(
            types.Content(
                role="user",
                parts=[
                    types.Part(text=user_text)
                ]
            )
        )

        self.manage_context()

        start = time.perf_counter()

        first_token = None
        answer_parts = []
        usage = None
        last_chunk = None

        stream = retry_call(
            lambda: self.client.models.generate_content_stream(

                model=MODEL,

                contents=self.history,

                config=self.chat_config
            )
        )

        for chunk in stream:

            last_chunk = chunk

            if chunk.usage_metadata is not None:

                usage = chunk.usage_metadata

            text = chunk.text or ""

            if text:

                if first_token is None:

                    first_token = time.perf_counter()

                    print(
                        f"\n[TTFT] "
                        f"{first_token - start:.3f}s"
                    )

                    print("\nAssistant: ", end="", flush=True)

                print(text, end="", flush=True)

                answer_parts.append(text)

        elapsed = time.perf_counter() - start

        answer = "".join(answer_parts)

        print()

        self.check_finish_reason(last_chunk)

        print(
            f"[timing] Total: {elapsed:.3f}s"
        )

        if first_token is not None:

            print(
                f"[timing] TTFT: "
                f"{first_token - start:.3f}s"
            )

        else:

            print("[timing] No text received.")

        self.usage_tracker.report(usage)

        if answer:

            self.history.append(
                types.Content(
                    role="model",
                    parts=[
                        types.Part(text=answer)
                    ]
                )
            )
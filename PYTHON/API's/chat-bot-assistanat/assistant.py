from pathlib import Path

from config import (
    GEMINI_API_KEY,
    MODEL,
    ROOT,
    CONTEXT_TOKEN_BUDGET
)

from services.gemini_client import create_client

from services.chat_service import ChatService

from services.usage_service import UsageTracker

from services.invoice_service import extract_invoice

from services.tool_service import calculator_demo

from stateless_demo import stateless_demo


def main():

    if not GEMINI_API_KEY:

        raise SystemExit(
            "Missing GEMINI_API_KEY. Check your .env file."
        )

    client = create_client(GEMINI_API_KEY)

    usage_tracker = UsageTracker()

    chat = ChatService(
        client,
        usage_tracker
    )

    print(
        f"\nDevAssist Gemini CLI"
        f"\nModel: {MODEL}"
        f"\nContext budget: {CONTEXT_TOKEN_BUDGET}"
    )

    print(
        "\nCommands:"
        "\n/stateless"
        "\n/invoice [path]"
        "\n/tool"
        "\n/quit"
    )

    while True:

        try:

            line = input("\nYou: ").strip()

        except (EOFError, KeyboardInterrupt):

            print("\nGoodbye!")

            break

        if not line:

            continue

        if line == "/quit":

            break

        try:

            if line == "/stateless":

                stateless_demo(client)

            elif line == "/tool":

                calculator_demo(
                    client,
                    usage_tracker
                )

            elif line.startswith("/invoice"):

                parts = line.split(maxsplit=1)

                path = (
                    Path(parts[1])
                    if len(parts) > 1
                    else ROOT / "data" / "invoice_ocr.txt"
                )

                extract_invoice(
                    client,
                    path,
                    usage_tracker
                )

            else:

                chat.chat(line)

        except Exception as exc:

            print(
                f"\n[error] {type(exc).__name__}: {exc}"
            )


if __name__ == "__main__":

    main()
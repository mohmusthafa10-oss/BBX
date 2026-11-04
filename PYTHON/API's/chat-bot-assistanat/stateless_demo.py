from config import GEMINI_API_KEY, MODEL

from services.gemini_client import create_client, retry_call


def stateless_demo(client):

    print("\n=== STATELESS DEMONSTRATION ===")

    first = retry_call(
        lambda: client.models.generate_content(

            model=MODEL,

            contents=(
                "My name is Midhun. "
                "Reply only: remembered."
            )
        )
    )

    print("\nTurn 1:", first.text)

    second = retry_call(
        lambda: client.models.generate_content(

            model=MODEL,

            contents="What is my name?"
        )
    )

    print("\nTurn 2 without previous history:", second.text)

    print(
        "\nThe second request does not contain "
        "the first request's conversation."
    )


if __name__ == "__main__":

    if not GEMINI_API_KEY:

        raise SystemExit("Missing GEMINI_API_KEY")

    client = create_client(GEMINI_API_KEY)

    stateless_demo(client)
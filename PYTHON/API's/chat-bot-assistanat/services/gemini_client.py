import random
import time

from google import genai
from google.genai import errors


def create_client(api_key):

    return genai.Client(
        api_key=api_key
    )


def retry_call(function, attempts=5):

    for attempt in range(attempts):

        try:
            return function()

        except errors.APIError as exc:

            status = getattr(exc, "code", None)

            if status is None:
                status = getattr(
                    exc,
                    "status_code",
                    None
                )

            retryable = (
                status == 429
                or (
                    isinstance(status, int)
                    and 500 <= status <= 599
                )
            )

            if not retryable or attempt == attempts - 1:
                raise

            delay = (
                min(16, 0.75 * (2 ** attempt))
                + random.uniform(0, 0.5)
            )

            print(
                f"\n[retry] Waiting {delay:.2f}s "
                f"({attempt + 1}/{attempts})"
            )

            time.sleep(delay)
            
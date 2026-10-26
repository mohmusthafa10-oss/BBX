
import os
import time
import random
import logging
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import requests
from dotenv import load_dotenv


# -------------------------
# 1. Configuration
# -------------------------

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError(
        "API_KEY is missing. Add it to your .env file."
    )


# -------------------------
# 2. Logging
# -------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


class APIClient:
    def __init__(self, api_key, timeout=10, max_attempts=5):
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        self.timeout = timeout
        self.max_attempts = max_attempts

        # Reuse one session across requests.
        self.session = requests.Session()

        # Configure shared headers once.
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _get_retry_after(self, response):
        """Return Retry-After in seconds, or None if invalid/missing."""
        value = response.headers.get("Retry-After")

        if not value:
            return None

        # Retry-After can be a number of seconds.
        try:
            return max(0.0, float(value))
        except ValueError:
            pass

        # It can also be an HTTP date.
        try:
            retry_time = parsedate_to_datetime(value)

            if retry_time.tzinfo is None:
                retry_time = retry_time.replace(tzinfo=timezone.utc)

            seconds = (
                retry_time - datetime.now(timezone.utc)
            ).total_seconds()

            return max(0.0, seconds)

        except (TypeError, ValueError, OverflowError):
            return None

    def get(self, url, params=None):
        """GET with retries for HTTP 429 and 5xx only."""

        for attempt in range(1, self.max_attempts + 1):
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout,
            )

            status = response.status_code

            # Retry only rate limits and server errors.
            if status == 429 or 500 <= status <= 599:

                # The final failed attempt must not sleep or retry.
                if attempt == self.max_attempts:
                    response.raise_for_status()

                retry_after = self._get_retry_after(response)

                if retry_after is not None:
                    # The server's Retry-After takes precedence.
                    wait_time = retry_after
                    logging.info(
                        "HTTP %s | attempt %s/%s | "
                        "Retry-After: waiting %.2f seconds",
                        status, attempt, self.max_attempts, wait_time,
                    )
                else:
                    # Retry 1: cap 1s; retry 2: cap 2s; then 4, 8...
                    backoff_cap = min(2 ** (attempt - 1), 60)

                    # Full jitter: choose a random wait from 0 to the cap.
                    wait_time = random.uniform(0, backoff_cap)

                    logging.info(
                        "HTTP %s | attempt %s/%s | "
                        "backoff cap %.2fs | actual wait %.2fs",
                        status, attempt, self.max_attempts,
                        backoff_cap, wait_time,
                    )

                time.sleep(wait_time)
                continue

            # Do not retry other 4xx errors. Retrying the same request
            # usually cannot fix a bad URL, missing resource, or bad input.
            response.raise_for_status()
            return response

        # Defensive fallback; normally the loop returns or raises.
        raise RuntimeError("GET attempts exhausted")

    def paginate(
        self,
        url,
        params=None,
        page_param="page",
        page_size_param="limit",
        page_size=10,
        items_key=None,
    ):
        """Yield records from successive pages until no data remains."""

        page = 1

        while True:
            page_params = dict(params or {})
            page_params[page_param] = page

            if page_size_param:
                page_params[page_size_param] = page_size

            response = self.get(url, params=page_params)
            data = response.json()

            if isinstance(data, list):
                records = data
            elif isinstance(data, dict) and items_key:
                records = data.get(items_key, [])
            else:
                raise ValueError(
                    "Expected a JSON list or a dictionary with items_key."
                )

            if not records:
                # An empty page tells us there is no more data.
                return

            yield from records
            page += 1

    def close(self):
        """Close the session when finished."""
        self.session.close()


if __name__ == "__main__":
    client = APIClient(API_KEY)

    try:
        # JSONPlaceholder supports _page and _limit.
        records = client.paginate(
            "https://jsonplaceholder.typicode.com/posts",
            params={},
            page_param="_page",
            page_size_param="_limit",
            page_size=10,
        )

        first_five = []

        for record in records:
            print(record["id"], record["title"])
            first_five.append(record)

            if len(first_five) == 5:
                break

    finally:
        client.close()


import logging

from api_client import APIClient, API_KEY

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

client = APIClient(API_KEY)

try:
    for status in (429, 500):
        url = f"https://httpbin.org/status/{status}"

        print(f"\nTesting HTTP {status}")

        try:
            client.get(url)
        except Exception as exc:
            print(f"Finished: {type(exc).__name__}: {exc}")

finally:
    client.close()

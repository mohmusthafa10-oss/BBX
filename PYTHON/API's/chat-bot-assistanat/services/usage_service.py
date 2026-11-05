from config import INPUT_RATE, OUTPUT_RATE


class UsageTracker:

    def __init__(self):

        self.total_cost = 0.0

    def report(self, usage):

        if usage is None:

            print("[usage] No token information returned.")
            return

        input_tokens = (
            usage.prompt_token_count or 0
        )

        output_tokens = (
            usage.candidates_token_count or 0
        )

        cost = (
            input_tokens * INPUT_RATE
            + output_tokens * OUTPUT_RATE
        ) / 1_000_000

        self.total_cost += cost

        print(
            f"\n[tokens] Input: {input_tokens:,}"
            f" | Output: {output_tokens:,}"
        )

        print(
            f"[cost] Turn: ${cost:.8f}"
            f" | Total: ${self.total_cost:.8f}"
        )




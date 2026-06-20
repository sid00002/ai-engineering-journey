import time
import random
import logging

from ollama import chat

from exceptions import LLMServiceException


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class LLMClient:

    MODEL_CONTEXT_LIMITS = {
        "qwen2.5:3b": 32768,
        "llama3.2": 8192
    }

    def __init__(
        self,
        model_name,
        timeout=30,
        max_retries=3
    ):
        self.model_name = model_name
        self.timeout = timeout
        self.max_retries = max_retries

    def would_exceed_context_limit(
        self,
        token_count
    ):
        limit = self.MODEL_CONTEXT_LIMITS.get(
            self.model_name,
            8192
        )

        return token_count > limit

    def generate(
        self,
        prompt
    ):
        start = time.time()

        for attempt in range(
            self.max_retries
        ):

            try:

                response = chat(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                latency = (
                    time.time() - start
                )

                logging.info(
                    f"Model={self.model_name} "
                    f"Latency={latency:.2f}s"
                )

                return response["message"]["content"]

            except Exception as e:

                if attempt == self.max_retries - 1:
                    raise LLMServiceException(
                        str(e)
                    )

                delay = (
                    2 ** attempt
                    + random.uniform(0, 1)
                )

                logging.warning(
                    f"Retry {attempt + 1}"
                    f" after {delay:.2f}s"
                )

                time.sleep(delay)
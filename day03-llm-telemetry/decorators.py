import time
import functools
import tiktoken

from llm_metrics import LLMMetrics

encoding = tiktoken.get_encoding("cl100k_base")

def track_llm_metrics(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        prompt = kwargs.get("prompt")

        if prompt is None:
            prompt = args[1]

        input_tokens = len(
            encoding.encode(prompt)
        )

        start = time.perf_counter()

        response = func(*args, **kwargs)
        latency = time.perf_counter() - start

        output_tokens = len(
            encoding.encode(response)
        )

        LLMMetrics.add_metrics(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency=latency
        )
        print("\n------ LLM Call ------")
        print(f"Input Tokens : {input_tokens}")
        print(f"Output Tokens: {output_tokens}")
        print(f"Latency      : {latency:.2f} sec")
        print("----------------------\n")

        return response
    return wrapper

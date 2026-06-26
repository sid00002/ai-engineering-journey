

class LLMMetrics:
    total_calls = 0
    total_input_tokens = 0
    total_output_tokens = 0
    total_tokens = 0
    total_latency = 0

    @classmethod
    def add_metrics(
        cls,
        input_tokens,
        output_tokens,
        latency
    ):
        cls.total_calls += 1
        cls.total_input_tokens += input_tokens
        cls.total_output_tokens += output_tokens
        cls.total_tokens += input_tokens + output_tokens
        cls.total_latency += latency

    @classmethod
    def get_summary(cls):
        avg_latency = (
            cls.total_latency / cls.total_calls
            if cls.total_calls > 0
            else 0
        )

        print("\n========== LLM Session Summary ==========")
        print(f"Total Calls      : {cls.total_calls}")
        print(f"Input Tokens     : {cls.total_input_tokens}")
        print(f"Output Tokens    : {cls.total_output_tokens}")
        print(f"Total Tokens     : {cls.total_tokens}")
        print(f"Average Latency  : {avg_latency:.2f} sec")
        print("Estimated Cost   : $0 (Ollama)")
        print("=========================================\n")
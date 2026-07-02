from llm_client import LLMClient

client = LLMClient()

result = client.detect_tool_call(
    "What is the weather in Mumbai?"
)

print(result)
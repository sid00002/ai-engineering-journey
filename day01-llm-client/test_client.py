from llm_client import LLMClient

client = LLMClient(
    model_name="qwen2.5:3b"
)

response = client.generate(
    "Explain RAG in one paragraph."
)

print(response)
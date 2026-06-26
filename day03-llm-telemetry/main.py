from llm_client import LLMClient
from llm_metrics import LLMMetrics

client = LLMClient("qwen2.5:3b")

prompts = [
    "Explain RAG.",
    "Explain embeddings.",
    "Explain vector databases.",
    "What is LangGraph?",
    "What is MCP?"
]

for prompt in prompts:

    print(client.generate(prompt))

LLMMetrics.get_summary()
from ollama import chat

response = chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain hallucination in LLMs."
        }
    ]
)

print(response["message"]["content"])
from context_window_manager import (
    ContextWindowManager
)

manager = ContextWindowManager(
    model_name="gpt-4",
    max_token_budget=100
)

system_prompt = """
You are a helpful AI assistant.
"""

messages = [
    {
        "role": "user",
        "content": "My name is Siddhesh."
    },
    {
        "role": "assistant",
        "content": "Nice to meet you."
    },
    {
        "role": "user",
        "content": (
            "I am a backend engineer "
            "working with Java and Spring Boot."
        )
    },
    {
        "role": "assistant",
        "content": (
            "That's a strong foundation."
        )
    },
    {
        "role": "user",
        "content": (
            "I want to transition "
            "into AI Engineering."
        )
    },
    {
        "role": "assistant",
        "content": (
            "Great choice."
        )
    },
    {
        "role": "user",
        "content": (
            "Can you explain RAG systems?"
        )
    }
]

fitted = manager.fit_messages(
    system_prompt,
    messages
)

print("\nMessages Kept:\n")

for message in fitted:
    print(
        f"{message['role']}: "
        f"{message['content']}"
    )
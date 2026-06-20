from ollama import chat

messages = []

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append({
        "role": "user",
        "content" : user_input
    })

    response = chat(
        model = "qwen2.5:3b",
        messages = messages
    )

    assistant_reply = response["message"]["content"]
    print(f"\nBot: {assistant_reply}\n")

    messages.append({
        "role": "assistant",
        "content": assistant_reply
    })
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key = os.getenv("GEMINI_API_KEY")
)

messages = []

print("Chatbot Started")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    messages.append(
        {
            "role": "user",
            "parts" : [{"text": user_input}]
        }
    )

    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = messages
    )

    bot_reply = response.text
    print(f"Bot: {bot_reply}\n")

    messages.append(
        {
            "role": "model",
            "parts": [{"text": bot_reply}]
        }
    )
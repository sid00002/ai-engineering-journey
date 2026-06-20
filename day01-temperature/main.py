from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

PROMPT = "Explain RAG in one paragraph."


def run_experiment(temperature, runs=3):
    print("=" * 50)
    print(f"TEMPERATURE = {temperature}")
    print("=" * 50)

    for i in range(runs):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=PROMPT,
            config=types.GenerateContentConfig(
                temperature=temperature
            )
        )

        print(f"\nResponse {i + 1}")
        print(response.text)


run_experiment(1.0)
print("\n\n")
run_experiment(0)
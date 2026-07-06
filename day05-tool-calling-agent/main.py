"""
main.py

Entry point for the AI Tool Calling Agent.

Run:
    python main.py
"""

from agent import Agent


def print_banner():
    print("=" * 60)
    print("🤖 AI Tool Calling Agent")
    print("=" * 60)
    print("Available tools:")
    print("• Weather")
    print("• Currency Conversion")
    print()
    print("Example:")
    print("What is the weather in Mumbai and what is 500 USD in INR?")
    print()
    print("Type 'exit' to quit.")
    print("=" * 60)


def main():

    agent = Agent()

    print_banner()

    while True:

        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("\nGoodbye!")
            break

        try:

            response = agent.run(user_input)

            print("\nAssistant:")
            print("-" * 60)
            print(response)
            print("-" * 60)

        except Exception as e:

            print("\nError:")
            print(e)


if __name__ == "__main__":
    main()
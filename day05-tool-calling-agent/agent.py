"""
agent.py

Simple AI Agent capable of:

1. Detecting tool calls
2. Executing tools
3. Sending tool results back to the LLM
4. Returning the final answer
"""

import re

from tool_registry import ToolRegistry
from llm_client import LLMClient


class Agent:

    def __init__(self):

        self.registry = ToolRegistry()
        self.llm = LLMClient()

    def _extract_tools(self, user_message):
        """
        Simple rule-based parser.

        Since Ollama/Qwen may not always return reliable
        JSON tool calls, we detect the required tools
        ourselves.

        Returns:

        [
            {
                "tool": "...",
                "arguments": {...}
            }
        ]
        """

        tool_calls = []

        message = user_message.lower()

        weather_match = re.search(
            r"weather.*?in\s+([a-zA-Z ]+)",
            message
        )

        if weather_match:

            city = weather_match.group(1).strip()

            # remove trailing "and"
            city = city.replace("and", "").strip()

            tool_calls.append(
                {
                    "tool": "get_weather",
                    "arguments": {
                        "city": city
                    }
                }
            )

        currency_match = re.search(
            r"(\d+)\s+([A-Za-z]{3})\s+(?:to|in)\s+([A-Za-z]{3})",
            user_message
        )

        if currency_match:

            amount = float(currency_match.group(1))

            from_currency = currency_match.group(2)

            to_currency = currency_match.group(3)

            tool_calls.append(
                {
                    "tool": "convert_currency",
                    "arguments": {
                        "amount": amount,
                        "from_currency": from_currency,
                        "to_currency": to_currency
                    }
                }
            )

        return tool_calls

    def run(self, user_message):

        print("=" * 60)
        print("User")
        print("=" * 60)
        print(user_message)
        print()

        tool_calls = self._extract_tools(
            user_message
        )

        tool_results = []

        for call in tool_calls:

            tool = call["tool"]

            arguments = call["arguments"]

            print(f"Executing Tool: {tool}")

            result = self.registry.execute(
                tool,
                **arguments
            )

            tool_results.append(
                {
                    "tool": tool,
                    "result": result
                }
            )

            print(result)
            print()

        if not tool_results:

            print("No tools required.\n")

            messages = [
                {
                    "role": "user",
                    "content": user_message
                }
            ]

            return self.llm.generate(messages)

        print("=" * 60)
        print("Generating Final Response...")
        print("=" * 60)

        return self.llm.generate_final_answer(
            user_message,
            tool_results
        )
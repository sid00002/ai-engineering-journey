from database import setup_database
from tools import (
    get_order_status,
    get_product_info,
    create_support_ticket,
)
from tool_registry import ToolRegistry
from logger import ToolCallLogger
from intent_resolver import IntentResolver
from response_formatter import ResponseFormatter
from agent import CustomerSupportAgent


def main():
    setup_database()

    registry = ToolRegistry()

    registry.register_tool("get_order_status", get_order_status)
    registry.register_tool("get_product_info", get_product_info)
    registry.register_tool("create_support_ticket", create_support_ticket)

    logger = ToolCallLogger()

    resolver = IntentResolver()

    formatter = ResponseFormatter()

    agent = CustomerSupportAgent(
        registry=registry,
        logger=logger,
        intent_resolver=resolver,
        response_formatter=formatter
    )

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = agent.process_request(user_input)

        print("\nAssistant:")
        print(response)


if __name__ == "__main__":
    main()
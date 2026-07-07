from intent_resolver import IntentResolver
from response_formatter import ResponseFormatter


class CustomerSupportAgent:
    MAX_TOOL_CALLS = 5

    def __init__(
        self,
        registry,
        logger,
        intent_resolver: IntentResolver,
        response_formatter: ResponseFormatter
    ):
        self.registry = registry
        self.logger = logger
        self.intent_resolver = intent_resolver
        self.response_formatter = response_formatter

    def process_request(self, user_input: str) -> str:
        tool_calls = 0

        try:
            intent = self.intent_resolver.resolve(user_input)

            if intent is None:
                return "Sorry, I couldn't understand your request."

            if tool_calls >= self.MAX_TOOL_CALLS:
                return "Maximum tool call limit exceeded."

            response = self.logger.execute_with_logging(
                registry=self.registry,
                tool_name=intent.tool_name,
                **intent.arguments
            )

            tool_calls += 1

            return self.response_formatter.format(response)

        except Exception as e:
            return f"Unexpected error: {str(e)}"
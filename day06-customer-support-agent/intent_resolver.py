import re
from typing import Optional

from intent import Intent


class IntentResolver:
    """
    Resolves a user's natural language request into a tool invocation.

    Current implementation:
        - Rule based (Regex + Keyword Matching)

    Future implementation:
        - LLM Function Calling
        - Gemini Tool Calling
        - OpenAI Tool Calling
    """

    EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    def resolve(self, user_input: str) -> Optional[Intent]:
        text = user_input.lower()

        if "order" in text:

            match = re.search(r"ORD\d+", user_input)

            if not match:
                return None

            return Intent(
                tool_name="get_order_status",
                arguments={
                    "order_id": match.group()
                }
            )

        if "product" in text:

            match = re.search(r"P\d+", user_input)

            if not match:
                return None

            return Intent(
                tool_name="get_product_info",
                arguments={
                    "product_id": match.group()
                }
            )

        support_keywords = [
            "ticket",
            "support",
            "issue",
            "problem",
            "complaint",
            "help"
        ]

        if any(keyword in text for keyword in support_keywords):

            email_match = re.search(self.EMAIL_REGEX, user_input)

            if not email_match:
                return None

            email = email_match.group()

            priority = "medium"

            if "high" in text:
                priority = "high"

            elif "low" in text:
                priority = "low"

            return Intent(
                tool_name="create_support_ticket",
                arguments={
                    "customer_email": email,
                    "issue_description": user_input,
                    "priority": priority
                }
            )

        return None
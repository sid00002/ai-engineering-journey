from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ModelPricing:
    """
    Pricing per 1 million tokens.
    """

    input_cost_per_million: float
    output_cost_per_million: float


class CostEstimator:
    """
    Estimates LLM request cost based on token usage.
    """

    DEFAULT_PRICING = {
        "gpt-4.1-mini": ModelPricing(
            input_cost_per_million=0.40,
            output_cost_per_million=1.60,
        ),
        "gpt-4.1": ModelPricing(
            input_cost_per_million=2.00,
            output_cost_per_million=8.00,
        ),
        "gemini-2.5-flash": ModelPricing(
            input_cost_per_million=0.30,
            output_cost_per_million=2.50,
        ),
    }

    @classmethod
    def estimate(
        cls,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:

        pricing = cls.DEFAULT_PRICING.get(model)

        if pricing is None:
            return 0.0

        input_cost = (
            input_tokens / 1_000_000
        ) * pricing.input_cost_per_million

        output_cost = (
            output_tokens / 1_000_000
        ) * pricing.output_cost_per_million

        return round(input_cost + output_cost, 8)
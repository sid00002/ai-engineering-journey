from __future__ import annotations

from typing import List

from cost_estimator import CostEstimator
from executor import ToolExecutor
from models import (
    AgentResult,
    ToolCall,
    ToolExecutionResult,
)


class Agent:
    """
    Generic Tool Calling Agent.

    Coordinates the LLM and ToolExecutor.
    """

    MAX_TOOL_CALLS_PER_ITERATION = 5

    def __init__(
        self,
        llm_client,
        executor: ToolExecutor,
        registry,
        max_iterations: int = 5,
    ):

        self.llm = llm_client

        self.executor = executor

        self.registry = registry

        self.max_iterations = max_iterations

    async def run(
        self,
        user_message: str,
    ) -> AgentResult:

        messages = [
            {
                "role": "user",
                "content": user_message,
            }
        ]

        tool_calls: List[ToolCall] = []

        tool_results: List[ToolExecutionResult] = []

        total_cost = 0.0

        iteration = 0

        while iteration < self.max_iterations:

            iteration += 1

            llm_response = await self.llm.generate(
                messages=messages,
                tools=self.registry.export_schemas(),
            )

            total_cost += CostEstimator.estimate(
                model=llm_response.model,
                input_tokens=llm_response.input_tokens,
                output_tokens=llm_response.output_tokens,
            )

            if llm_response.finished:

                return AgentResult(
                    final_message=llm_response.message,
                    tool_calls=tool_calls,
                    tool_results=tool_results,
                    iterations=iteration,
                    total_cost=total_cost,
                )

            current_tool_calls = llm_response.tool_calls[
                : self.MAX_TOOL_CALLS_PER_ITERATION
            ]

            tool_calls.extend(current_tool_calls)

            results = await self.executor.execute_many(
                current_tool_calls
            )

            tool_results.extend(results)

            for call, result in zip(
                current_tool_calls,
                results,
            ):

                messages.append(
                    {
                        "role": "tool",
                        "tool_name": call.tool_name,
                        "content": str(result.result)
                        if result.success
                        else str(result.error),
                    }
                )

        return AgentResult(
            final_message="Maximum iteration limit reached.",
            tool_calls=tool_calls,
            tool_results=tool_results,
            iterations=iteration,
            total_cost=total_cost,
        )
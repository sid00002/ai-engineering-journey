from __future__ import annotations

import asyncio
import time
from typing import List

from logger import ExecutionLogger
from models import (
    ToolCall,
    ToolError,
    ToolExecutionResult,
)
from registry import ToolRegistry
from validator import ToolValidator


class ToolExecutor:
    """
    Executes registered tools.

    Responsibilities:
        - Lookup tools
        - Validate arguments
        - Execute sync/async tools
        - Apply timeout
        - Log execution
        - Return structured results
    """

    def __init__(
        self,
        registry: ToolRegistry,
        logger: ExecutionLogger,
        timeout_seconds: float = 5.0,
    ):
        self.registry = registry
        self.logger = logger
        self.timeout_seconds = timeout_seconds

    async def execute(
        self,
        tool_call: ToolCall,
    ) -> ToolExecutionResult:

        start = time.perf_counter()

        try:
            metadata = self.registry.get(tool_call.tool_name)

        except Exception as e:

            result = ToolExecutionResult(
                success=False,
                tool_name=tool_call.tool_name,
                error=ToolError(
                    code="TOOL_NOT_FOUND",
                    message=str(e),
                ),
            )

            self.logger.log(tool_call, result)

            return result

        validation_error = ToolValidator.validate(
            metadata,
            tool_call.arguments,
        )

        if validation_error:

            result = ToolExecutionResult(
                success=False,
                tool_name=tool_call.tool_name,
                error=validation_error,
            )

            self.logger.log(tool_call, result)

            return result


        try:

            if metadata.is_async:

                coroutine = metadata.function(
                    **tool_call.arguments
                )

                tool_result = await asyncio.wait_for(
                    coroutine,
                    timeout=self.timeout_seconds,
                )

            else:

                tool_result = await asyncio.wait_for(
                    asyncio.to_thread(
                        metadata.function,
                        **tool_call.arguments,
                    ),
                    timeout=self.timeout_seconds,
                )

            execution_time = (
                time.perf_counter() - start
            ) * 1000

            result = ToolExecutionResult(
                success=True,
                tool_name=tool_call.tool_name,
                result=tool_result,
                execution_time_ms=execution_time,
            )

            self.logger.log(tool_call, result)

            return result

        except asyncio.TimeoutError:

            execution_time = (
                time.perf_counter() - start
            ) * 1000

            result = ToolExecutionResult(
                success=False,
                tool_name=tool_call.tool_name,
                error=ToolError(
                    code="TIMEOUT",
                    message=f"Tool execution exceeded {self.timeout_seconds} seconds.",
                ),
                execution_time_ms=execution_time,
            )

            self.logger.log(tool_call, result)

            return result

        except Exception as e:

            execution_time = (
                time.perf_counter() - start
            ) * 1000

            result = ToolExecutionResult(
                success=False,
                tool_name=tool_call.tool_name,
                error=ToolError(
                    code="EXECUTION_ERROR",
                    message=str(e),
                ),
                execution_time_ms=execution_time,
            )

            self.logger.log(tool_call, result)

            return result

    async def execute_many(
        self,
        tool_calls: List[ToolCall],
    ) -> List[ToolExecutionResult]:
        """
        Execute multiple tool calls concurrently.
        """

        tasks = [
            self.execute(tool_call)
            for tool_call in tool_calls
        ]

        return await asyncio.gather(*tasks)
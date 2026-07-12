from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(slots=True)
class ToolMetaData:
    """
    Represents a registered tool.

    Attributes:
        name: Name exposed to the LLM.
        description: Human-readable description.
        function: Python callable.
        schema: JSON Schema for validation.
        is_async: Whether the tool is asynchronous.
    
    """
    name:str
    description:str
    function:Callable[..., Any]
    schema:dict[str, Any]
    is_async:bool


@dataclass(slots=True)
class ToolCall:
    """
    Represents a tool invocation requested by the LLM.
    """
    tool_name:str
    arguments:dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ToolError:
    """
    Structured error returned by the framework.
    """
    code: str
    message:str


@dataclass(slots=True)
class ToolExecutionResult:
    """
    Result of executing one tool.
    """
    success: bool
    tool_name: str
    result: Any | None = None
    error: ToolError | None = None
    execution_time_ms: float = 0.0

@dataclass(slots=True)
class AgentResult:
    """
    Final result returned by the agent.
    """
    final_message:str
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_results: list[ToolExecutionResult] = field(default_factory=list)
    iterations: int=0
    total_cost: float = 0.0
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ToolError:
    code: str
    message: str


@dataclass
class ToolResponse:
    success: bool
    data: Optional[Any] = None
    error: Optional[ToolError] = None




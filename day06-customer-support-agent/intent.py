from dataclasses import dataclass, field
from typing import Any


@dataclass
class Intent:
    """
    Represents the intent extracted from a user's request.

    Attributes:
        tool_name: Name of the tool to invoke.
        arguments: Keyword arguments to pass to the tool.
    """

    tool_name: str
    arguments: dict[str, Any] = field(default_factory=dict)
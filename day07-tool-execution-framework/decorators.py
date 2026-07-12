from __future__ import annotations
from dataclasses import dataclass
from functools import wraps
from typing import Callable, Optional


@dataclass(slots=True)
class ToolDefination:
    """
    Lightweight metadata attached to a tool function.

    This is NOT the same as ToolMetadata.
    ToolMetadata is created later by ToolRegistry after
    schema generation and async detection.
    """
    name: str
    description: str


def tool(name: Optional[str] = None):
    """
    Decorator that marks a function as an AI tool.

    Example:

        @tool()
        def add(a: int, b: int):
            \"\"\"Adds two numbers.\"\"\"

        @tool(name="weather")
        def get_weather(city: str):
            \"\"\"Returns weather.\"\"\"
    """
    def decorator(func: Callable):
        tool_name  = name or func.__name__

        description = (
            func.__doc__.strip()
            if func.__doc__ 
            else ""
        )

        definition = ToolDefination(
            name=tool_name,
            description=description
        )
        setattr(func, "_tool_definition", definition)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator
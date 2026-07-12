from __future__ import annotations
import inspect
from typing import Any, Callable
from decorators import ToolDefination
from models import ToolMetaData
from schema_generator import SchemaGenerator


class ToolRegistry:
    """
    Stores all registered tools.

    Responsible for:
    - Registering tools
    - Generating schemas
    - Retrieving tool metadata
    """
    def __init__(self):
        self._tools: dict[str, ToolMetaData] = {}
    
    def register(self, func: Callable) -> None:
        """
        Register a tool function.
        """
        defination: ToolDefination | None = getattr(
            func,
            "__tool_defination__",
            None
        )

        if defination is None:
            raise ValueError(
                f"Function '{func.__name__}' is not decorated with @tool."
            )
        
        if defination.name in self._tools:
            raise ValueError(
                f"Tool '{defination.name}' is already registered."
            )
        
        schema = SchemaGenerator.generate_schema(func)

        metadata = ToolMetaData(
            name = defination.name,
            description= defination.description,
            function= func,
            schema= schema,
            is_async= inspect.iscoroutinefunction(func)
        )

        self._tools[defination.name] = metadata

    
    def get(self, tool_name:str) -> ToolMetaData:
        """
        Retrieve metadata for a tool.
        """
        if tool_name not in self._tools:
            raise ValueError(f"Tool '{tool_name}' is not registered.")
        
        return self._tools[tool_name]
    
    def exists(self, tool_name: str)-> bool:
        """
        Check whether a tool exists.
        """
        return tool_name in self._tools
    
    def list_tools(self) -> list[ToolMetaData]:
        """
        List all registered tools.
        """
        return list(self._tools.values())
    
    def export_schemas(self) -> list[dict]:
        """
        Export tool definitions for an LLM.
        """
        exported = []
        for tool in self._tools.values():
            exported.append({
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.schema
            })
        return exported
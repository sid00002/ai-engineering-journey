from typing import Callable
from models import ToolResponse, ToolError


class ToolRegistry:
    def __init__(self):
        self._tools = {}

    
    def register_tool(self, name: str, func: Callable):
        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered.")
        self._tools[name] = func

    
    def has_tool(self, name: str) -> bool:
        return name in self._tools
    
    def get_tool(self, name: str):
        if not self.has_tool(name):
            raise ValueError(f"Tool '{name}' is not registered.")
        
        return self._tools[name]
    
    def execute(
            self, 
            tool_name:str,
            **kwargs
    ) -> ToolResponse:
        if not self.has_tool(tool_name):
            return ToolResponse(
                success=False,
                error=ToolError(
                    code="TOOL_NOT_FOUND",
                    message=f"Tool '{tool_name}' is not registered."
                )
            )
        
        tool = self.get_tool(tool_name)
        try:
            return tool(**kwargs)
        except TypeError as e:
            return ToolResponse(
                success= False,
                error= ToolError(
                    code = "INVALID_ARGUMENTS",
                    message=str(e)
                )
            )
        except Exception as e:
            return ToolResponse(
                success=False,
                error=ToolError(
                    code="TOOL_EXECUTION_ERROR",
                    message=str(e)
                )
            )
        
    def list_tools(self):
        return list(self._tools.keys())
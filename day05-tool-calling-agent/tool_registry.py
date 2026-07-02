"""
tool_registry.py

Maintains a registry of all tools available to the AI agent.

The agent never imports tools directly.
Instead, it asks the registry to execute them.
"""

from tools import get_weather
from tools import convert_currency


class ToolRegistry:
    
    def __init__(self):
        self.tools = {
            "get_weather": get_weather,
            "convert_currency": convert_currency
        }   

    def get_available_tools(self):
        """
        Returns all available tool names.
        """
        return list(self.tools.keys())
    
    def has_tool(self, tool_name:str)-> bool:
        """
        Checks whether a tool exists.
        """

        return tool_name in self.tools
    
    def execute(self, tool_name:str, **kwargs):
        """
        Execute a tool by name.

        Example:
        
        registry.execute(
            "get_weather",
            city="Mumbai"
        )
        """

        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found in registry.")
        
        tool = self.tools[tool_name]
        return tool(**kwargs)
    
    def describe_tools(self):
        """
        Returns metadata about every tool.
        This metadata can later be passed to an LLM
        for native function calling.
        """

        return [
            {
                "name": "get_weather",
                "description": "Get current weather information for a city.",
                "parameters": {
                    "city": "string"
                }
            },
            {
                "name": "convert_currency",
                "description": "Convert money between currencies.",
                "parameters": {
                    "amount": "float",
                    "from_currency": "string",
                    "to_currency": "string"
                }
            }
        ]
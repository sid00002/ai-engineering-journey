"""
llm_client.py

Wrapper around Ollama.
"""

import json
from ollama import chat

class LLMClient:
    def __init__(self, model="qwen2.5:3b"):
        self.model = model
    
    def generate(self, messages):
        response = chat(
            model = self.model,
            messages = messages
        )

        return response["message"]["content"]
    
    def detect_tool_call(self, user_message):
        """
        Ask the model whether a tool should be used.

        Returns JSON only.
        """
        prompt = f"""
You are an AI agent.

Available tools:

1. get_weather(city)

2. convert_currency(amount, from_currency, to_currency)

If a tool is needed return ONLY valid JSON.

Examples:

{{
    "tool": "get_weather",
    "arguments": {{
        "city": "Mumbai"
    }}
}}

OR

{{
    "tool": "convert_currency",
    "arguments": {{
        "amount": 500,
        "from_currency": "USD",
        "to_currency": "INR"
    }}
}}

If no tool is required return

{{
    "tool": null
}}

User:

{user_message}

"""
        
        response = chat(
            model = self.model,
            messages = [
                {
                    "role":"user",
                    "content": prompt
                }
            ]
        )

        content = response["message"]["content"]
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"tool": None}
        

    
    def generate_final_answer(
        self,
        user_message,
        tool_results
    ):

        prompt = f"""
User Question

{user_message}

Tool Results

{json.dumps(tool_results, indent=2)}

Answer the user naturally using the tool results.
"""

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]
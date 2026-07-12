from __future__ import annotations
from typing import Any
from models import ToolError, ToolMetaData

class ToolValidator:
    """
    Validates tool call arguments against the generated JSON schema.
    """
    JSON_TYPE_MAPPING = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "array": list,
        "object": dict,
    }

    @classmethod
    def validate(
        cls,
        metadata: ToolMetaData,
        arguments: dict[str, Any]
    ) -> ToolError | None:
        
        schema = metadata.schema
        properties = schema.get("properties", {})
        required = schema.get("required", [])

        for field in required:
            if field not in arguments:
                return ToolError(
                    code="MISSING_REQUIRED_ARGUMENT",
                    message=f"Missing required argument: '{field}'"
                )
            
        for field in arguments:
            if field not in properties:
                return ToolError(
                    code="UNKNOWN_ARGUMENT",
                    message=f"Unexpected argument: '{field}'"
                )
            
        for field, value in arguments.items():
            expected_json_type = properties[field]["type"]
            expected_python_type = cls.JSON_TYPE_MAPPING.get(expected_json_type)

            if not isinstance(value, expected_python_type):
                return ToolError(
                    code="INVALID_ARGUMENT_TYPE",
                    message=(
                        f"Argument '{field}' "
                        f"must be of type "
                        f"{expected_json_type}."
                    )
                )
        return None
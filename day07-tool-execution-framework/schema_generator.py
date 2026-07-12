from __future__ import annotations
import inspect
from typing import Any, get_origin, get_args


class SchemaGenerator:
    """
    Generates JSON Schema definitions from Python function signatures.
    """
    PYTHON_TO_JSON_TYPES = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
    }

    @classmethod
    def generate_schema(cls, func) -> dict[str, Any]:
        """
        Generate a JSON schema from a Python function.
        """
        signature = inspect.signature(func)
        properties = {}
        required = []
        for parameter in signature.parameters.values():
            parameter_schema = cls._parameter_schema(parameter)
            properties[parameter.name] = parameter_schema
            
            if parameter.default is inspect.Parameter.empty:
                required.append(parameter.name)

        return {
            "type": "object",
            "properties": properties,
            "required": required    
        }


@classmethod
def _parameter_schema(cls, parameter: inspect.Parameter) -> dict[str, Any]:
    annotations = parameter.annotation
    json_type = cls._map_python_type(annotations)
    schema = {
        "type": json_type
    }

    if parameter.default is not inspect.Parameter.empty:
        schema["default"] = parameter.default
    
    return schema


@classmethod
def _map_python_type(cls, annotation)-> str:
    origin = get_origin(annotation)

    if origin is list:
        return "array"
    
    if origin is dict:
        return "object"
    
    if origin is None:
        return cls.PYTHON_TO_JSON_TYPES.get(annotation, "string")
    
    return "string"
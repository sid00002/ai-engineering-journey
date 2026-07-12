from __future__ import annotations
import json
import logging
from pathlib import Path
from datetime import datetime

from models import ToolCall, ToolExecutionResult


class ExecuteLogger:
    """
    Logs every tool execution.

    Each log entry contains:
    - Timestamp
    - Tool name
    - Arguments
    - Success/Failure
    - Execution time
    - Result/Error
    """

    def __init__(
            self,
            log_directory: str = "logs",
            log_file:str = "tool_execution.log"
    ):
        Path(log_directory).mkdir(
            parents=True, exist_ok=True
        )

        self.logger = logging.getLogger("ToolExecutor")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.FileHandler(
                Path(log_directory) / log_file
            )

            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        
    
    def log(
            self,
            tool_call: ToolCall,
            result: ToolExecutionResult
    ) -> None:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),

            "tool": tool_call.tool_name,

            "arguments": tool_call.arguments,

            "success": result.success,

            "execution_time_ms": round(
                result.execution_time_ms,
                2
            ),

            "result": result.result,

            "error": (
                None
                if result.error is None
                else {
                    "code": result.error.code,
                    "message": result.error.message,
                }
            )
        }

        self.logger.info(
            json.dumps(
                log_entry,
                indent=2,
                default=str
            )
        )
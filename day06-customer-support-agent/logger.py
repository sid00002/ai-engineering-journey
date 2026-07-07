import json
import logging
import os
from datetime import datetime
from time import perf_counter
from models import ToolResponse, ToolError


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "tool_calls.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(message)s"
)

class ToolCallLogger:
    def log(
            self, 
            tool_name:str,
            arguments:dict,
            response:ToolResponse,
            latency_ms:float
    ):
        log_entry ={
            "timestamp": datetime.utcnow().isoformat(),
            "tool": tool_name,
            "arguments": arguments,
            "success": response.success,
            "latency_ms": latency_ms    
        }

        if response.success:
            log_entry["result"] = response.data
        else:
            log_entry["error"] = {
                "code": response.error.code,
                "message": response.error.message
            }
        
        logging.info(json.dumps(log_entry))
    

    def execute_with_logging(
            self, 
            registry,
            tool_name,
            **kwargs
    ):
        start = perf_counter()
        response = registry.execute(tool_name, **kwargs)
        end = perf_counter()
        latency_ms = (end - start) * 1000
        self.log(tool_name, kwargs, response, latency_ms)
        return response

"""
Tool definitions and strict schema validation for the xv6 AI agent.
Enforces Layer 1 security: strict allowlist, path confinement, parameter checking.
"""

from typing import Dict, Any, Callable
import os

TOOLS_SCHEMA = {
    "list_files": {
        "description": "Lists files in the current xv6 guest directory",
        "parameters": {},
        "required": []
    },
    "read_file": {
        "description": "Reads contents of a file in xv6 guest",
        "parameters": {
            "path": {"type": "string", "description": "Absolute or relative path to file"}
        },
        "required": ["path"]
    },
    "write_file": {
        "description": "Writes text to a file in xv6 guest",
        "parameters": {
            "path": {"type": "string", "description": "Path to file"},
            "content": {"type": "string", "description": "Text content to write"}
        },
        "required": ["path", "content"]
    },
    "summarize": {
        "description": "Summarizes the given text",
        "parameters": {
            "text": {"type": "string", "description": "Text to summarize"}
        },
        "required": ["text"]
    },
    "speculative_run": {
        "description": "Runs a command speculatively inside xv6 using xbegin/xcommit/xabort",
        "parameters": {
            "command": {"type": "string", "description": "Shell command to run speculatively"},
            "commit": {"type": "boolean", "description": "True to commit, False to abort"}
        },
        "required": ["command", "commit"]
    }
}

ALLOWED_TOOLS = set(TOOLS_SCHEMA.keys())

def validate_action(action: Dict[str, Any]) -> None:
    """
    Validates a structured action dictionary proposed by an agent or planner.
    Raises ValueError on validation failure.
    """
    if not isinstance(action, dict):
        raise ValueError("Action must be a dictionary")
    
    tool_name = action.get("tool")
    if not tool_name or tool_name not in ALLOWED_TOOLS:
        raise ValueError(f"Unknown or unauthorized tool: '{tool_name}'")
    
    args = action.get("args", {})
    if not isinstance(args, dict):
        raise ValueError("Tool arguments must be a dictionary")
        
    schema = TOOLS_SCHEMA[tool_name]
    for req in schema["required"]:
        if req not in args:
            raise ValueError(f"Missing required parameter '{req}' for tool '{tool_name}'")
            
    # Check path traversal or dangerous characters in file paths
    if "path" in args:
        path = args["path"]
        if not isinstance(path, str) or not path.strip():
            raise ValueError("Invalid path format")
        if ";" in path or "|" in path or "&" in path or "`" in path:
            raise ValueError("Path contains illegal shell metacharacters")

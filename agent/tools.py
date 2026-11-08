"""Strict allow-list and argument validation for the host-side xv6 agent."""
import re
from typing import Any, Dict

TOOLS_SCHEMA = {
 "list_files":{"required":[],"parameters":{}},
 "read_file":{"required":["path"],"parameters":{"path":"string"}},
 "summarize":{"required":["text"],"parameters":{"text":"string"}},
 "write_file":{"required":["path","content"],"parameters":{"path":"string","content":"string"}},
 "speculative_run":{"required":["command","commit"],"parameters":{"command":"string","commit":"boolean"}},
}
ALLOWED_TOOLS=set(TOOLS_SCHEMA)
_SAFE_PATH=re.compile(r"^/?[A-Za-z0-9_.-]{1,14}$")

def validate_action(action: Dict[str,Any])->None:
 if not isinstance(action,dict): raise ValueError("Action must be an object")
 if set(action)-{"tool","args"}: raise ValueError("Unexpected action fields")
 tool=action.get("tool")
 if tool not in ALLOWED_TOOLS: raise ValueError(f"Unknown or unauthorized tool: {tool!r}")
 args=action.get("args",{})
 if not isinstance(args,dict): raise ValueError("Tool arguments must be an object")
 schema=TOOLS_SCHEMA[tool]
 if set(args)!=set(schema["required"]): raise ValueError(f"Expected exactly these arguments: {schema['required']}")
 for key,kind in schema["parameters"].items():
  value=args[key]
  if kind=="string" and not isinstance(value,str): raise ValueError(f"{key} must be a string")
  if kind=="boolean" and type(value) is not bool: raise ValueError(f"{key} must be a boolean")
 if "path" in args and not _SAFE_PATH.fullmatch(args["path"]):
  raise ValueError("Path must be a single safe xv6 filename (no directories or shell syntax)")
 if tool=="speculative_run" and not re.fullmatch(r"rm [A-Za-z0-9_.-]{1,14}",args["command"]):
  raise ValueError("Only a single safe rm filename command is accepted")

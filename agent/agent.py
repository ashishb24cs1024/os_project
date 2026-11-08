"""Deterministic, fail-closed agent for the current xv6 milestone.
Mutating tools remain disabled until kernel speculation and a guest harness exist.
"""
from typing import Any, Dict
from bridge import QEMUBridge
from tools import validate_action

class ToolExecutor:
 def __init__(self,bridge:QEMUBridge): self.bridge=bridge
 def execute(self,action:Dict[str,Any])->str:
  validate_action(action); tool=action["tool"]; args=action.get("args",{})
  if tool=="list_files": return self.bridge.send_command("ls")
  if tool=="read_file": return self.bridge.send_command("cat "+args["path"].lstrip("/"))
  if tool=="summarize":
   lines=[line.strip() for line in args["text"].splitlines() if line.strip()]
   return f"Summary: {len(lines)} non-empty lines. "+(lines[0] if lines else "No content.")
  if tool in {"write_file","speculative_run"}:
   raise NotImplementedError(f"{tool} disabled: implement and verify kernel speculation and a safe guest harness first")
  raise ValueError(f"Unhandled tool: {tool}")

class Agent:
 def __init__(self,executor:ToolExecutor): self.executor=executor
 def plan_deterministic(self,request:str)->Dict[str,Any]:
  req=request.strip(); low=req.lower()
  if low in {"list","list files","show files"}: return {"tool":"list_files","args":{}}
  if low.startswith("read "): return {"tool":"read_file","args":{"path":req[5:].strip()}}
  if low.startswith("summarize "): return {"tool":"summarize","args":{"text":req[10:].strip()}}
  raise ValueError("Use list files, read filename, or summarize text")
 def run(self,request:str)->str:
  action=self.plan_deterministic(request); print("[Agent] Proposed action:",action)
  result=self.executor.execute(action); print("[Agent] Observation:",result); return result

if __name__=="__main__":
 bridge=QEMUBridge()
 try:
  bridge.start(); agent=Agent(ToolExecutor(bridge))
  agent.run("list files"); agent.run("read README")
 finally: bridge.close()

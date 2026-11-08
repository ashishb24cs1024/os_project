"""
Deterministic AI Agent & Tool Dispatcher.
Executes structured actions validated against TOOLS_SCHEMA,
and communicates observations back from the xv6 QEMU bridge.
"""

from typing import Dict, Any
from tools import validate_action, TOOLS_SCHEMA
from bridge import QEMUBridge

class ToolExecutor:
    def __init__(self, bridge: QEMUBridge):
        self.bridge = bridge

    def execute(self, action: Dict[str, Any]) -> str:
        validate_action(action)
        tool = action["tool"]
        args = action.get("args", {})

        if tool == "list_files":
            return self.bridge.send_command("ls")
        elif tool == "read_file":
            path = args["path"]
            return self.bridge.send_command(f"cat {path}")
        elif tool == "write_file":
            path = args["path"]
            content = args["content"]
            return self.bridge.send_command(f"echo \"{content}\" > {path}")
        elif tool == "summarize":
            text = args["text"]
            lines = text.strip().splitlines()
            return f"Summary: Contains {len(lines)} lines. Snippet: '{lines[0] if lines else ''}'"
        elif tool == "speculative_run":
            cmd = args["command"]
            commit = args["commit"]
            # In xv6 with Problem 5 support:
            # We wrap the command in a speculative harness runner
            action_type = "commit" if commit else "abort"
            return self.bridge.send_command(f"spectest {action_type} \"{cmd}\"")
        else:
            raise ValueError(f"Unhandled tool: {tool}")

class Agent:
    def __init__(self, executor: ToolExecutor):
        self.executor = executor

    def plan_deterministic(self, request: str) -> Dict[str, Any]:
        """
        Milestone C: Deterministic rule-based planner.
        Translates human user intent into structured JSON tool calls.
        """
        req = request.lower().strip()
        if req.startswith("list") or "files" in req:
            return {"tool": "list_files", "args": {}}
        elif req.startswith("read ") or "cat " in req:
            path = request.split()[-1]
            return {"tool": "read_file", "args": {"path": path}}
        elif req.startswith("summarize"):
            text = request[len("summarize"):].strip()
            return {"tool": "summarize", "args": {"text": text}}
        else:
            # Default fallthrough
            return {"tool": "list_files", "args": {}}

    def run(self, request: str) -> str:
        """Runs the planner, validates the action, and executes via bridge."""
        action = self.plan_deterministic(request)
        print(f"[Agent] Proposed Action: {action}")
        observation = self.executor.execute(action)
        print(f"[Agent] Observation: {observation}")
        return observation

if __name__ == "__main__":
    bridge = QEMUBridge(mock=True)
    bridge.start()
    executor = ToolExecutor(bridge)
    agent = Agent(executor)

    print("\n--- Testing list_files ---")
    agent.run("list files")

    print("\n--- Testing read report.txt ---")
    agent.run("read report.txt")

    bridge.close()

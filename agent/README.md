# AI Agent & QEMU Bridge

This directory contains the host-side Python AI agent, tool dispatcher, and serial console bridge connecting to the xv6 guest running inside QEMU.

## Architecture

1. `tools.py`: Defines the strict tool schemas and input validation logic (Layer 1 security).
2. `bridge.py`: Handles serial communication with xv6 running under QEMU (or mock environment for automated testing).
3. `agent.py`: Implements the deterministic planner (Milestone C) translating goals into structured tool calls.
4. `test_injection.py`: End-to-end prompt injection test harness demonstrating how kernel externalization barriers prevent unauthorized state corruption.

## Running the Agent

To test the deterministic agent and tool dispatcher:
```bash
python3 agent.py
```

To run the prompt injection experiment:
```bash
python3 test_injection.py
```

# ThanOS: xv6 Operating Systems Project

**Course:** CSL3030 Operating Systems Lab, IIT Jodhpur  
**Team Number:** 37  
**Team Name:** ThanOS  
**Assigned Project:** **Problem 5 — Externalization Barriers for Speculative Processes (Hard)**

---

## Team Members

| Name | Roll Number | Primary Focus |
|---|---|---|
| **Dasari Ashish Rathnam** | **B24CS1024** | Kernel Speculation & Buffer-Cache Shadow Layer (`kernel/bio.c`, `kernel/param.h`) |
| **Jangili Mahalaxmi** | **B24CS1033** | Speculative Process Lifecycle & Syscalls (`proc.c`, `sysproc.c`, `fork` inheritance) |
| **Talari Shreehitha** | **B24CS1075** | Externalization Barriers & I/O Buffering (`console.c`, `pipe.c`) |
| **Lagudu Pooja Rani** | **B24ES1017** | Atomic Commit/Abort, Log Journaling (`log.c`, `fs.c`) & AI Agent Integration |

---

## Project Structure

```
os_project/
├── docs/                       # Course handouts and detailed architecture specs
│   ├── OS Project .xlsx        # Team allocations & project mapping from department
│   ├── xv6_projects.pdf        # Complete lab project specification document
│   ├── Agentic_system_doc.pdf  # AI Agent + xv6 integration guide
│   ├── PROBLEM_SPEC.md         # Deep-dive analysis and design for Problem 5
│   ├── AGENT_SPEC.md           # AI Agent & QEMU bridge specification
│   └── TEAM_AND_ROADMAP.md     # 20-day timeline & individual task assignments
│
├── xv6-riscv/                  # Cloned modern RISC-V xv6 operating system tree
│   ├── kernel/                 # Kernel source (bio.c, proc.c, console.c, pipe.c, etc.)
│   ├── user/                   # User programs (sh.c, spectest.c, etc.)
│   └── Makefile                # xv6 build and QEMU invocation rules
│
├── agent/                      # Host-side Python AI Agent & QEMU Bridge
│   ├── agent.py                # Deterministic planner & tool loop
│   ├── bridge.py               # Serial console connection to QEMU guest
│   ├── tools.py                # Tool schemas and strict input validation
│   ├── test_injection.py       # Prompt-injection harness proving kernel enforcement
│   └── README.md               # Guide to running the agent
│
├── tests/                      # Verification scripts and benchmark utilities
│   ├── benchmark_cliff.py      # Write cost measurement (1KB to 64KB) showing shadow cliff
│   └── xv6_user_tests/         # xv6 user programs for testing speculation isolation
│
└── README.md                   # This project index
```

---

## Prerequisites & Installation (Arch Linux)

To compile and emulate xv6 for RISC-V on Arch Linux, install the GNU cross-compiler toolchain and QEMU emulator:

```bash
sudo pacman -S --needed riscv64-elf-gcc riscv64-elf-binutils riscv64-elf-gdb qemu-system-riscv
```

---

## Quickstart

### 1. Building and Running xv6
```bash
cd xv6-riscv
make qemu
```
*(To exit QEMU: press `Ctrl-A` then `X`)*

### 2. Running AI Agent & Prompt Injection Tests
```bash
cd agent
python3 test_injection.py
```

### 3. Running Benchmark Cliff Simulation
```bash
cd tests
python3 benchmark_cliff.py
```

---

## Deliverables Checklist
1. **Archive:** `ThanOS_5.zip` containing strictly added/modified files.
2. **Report:** 2-page handwritten summary with problem analysis and mathematical formulations.
3. **Evidence:** Raw QEMU logs, GDB debugging transcript, and 1 KB–64 KB write cost graph.
4. **Design Journal:** Git commits every 2 days documenting attempts, failures, and resolutions.

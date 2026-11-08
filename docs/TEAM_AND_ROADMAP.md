# Team ThanOS — Project Roadmap & Work Breakdown

**Course:** CSL3030 Operating Systems Lab, IIT Jodhpur  
**Team Number:** 37  
**Team Name:** ThanOS  
**Assigned Project:** Problem 5 — Externalization Barriers for Speculative Processes  

---

## 1. Team Members & Roles

| Name | Roll Number | Primary Assigned Responsibilities |
|---|---|---|
| **Dasari Ashish Rathnam** | **B24CS1024** | **Kernel Speculation Subsystem & Bio Shadow Layer** (`kernel/bio.c`, `kernel/param.h`, `bread`/`bwrite` redirect, shadow buffer table, shadow slot allocation & failure handling) |
| **Jangili Mahalaxmi** | **B24CS1033** | **Process Lifecycle & Syscall Interface** (`proc.c`, `proc.h`, `syscall.c`, `syscall.h`, `sysproc.c`, `fork` propagation of `p->spec`, `xbegin`, `xcommit`, `xabort`) |
| **Talari Shreehitha** | **B24CS1075** | **Externalization Barriers & I/O Buffering** (`console.c` console buffering until commit, `pipe.c` external reader detection & write isolation) |
| **Lagudu Pooja Rani** | **B24ES1017** | **Filesystem Integration, Atomic Commit/Abort & Agent/Tests** (`log.c`, log transaction commit in `xcommit`, `fs.c` create/unlink tests, Python Host Agent bridge & prompt injection harness) |

---

## 2. 20-Day Project Timeline (Milestones)

### Days 1 to 3: Codebase Study & System Call Baseline
- [x] Clone and inspect the modern `xv6-riscv` tree (`sleep_prepare`, `printk`, `copyin`, `LOGBLOCKS`).
- [ ] Implement the baseline worked example syscall `hello(a,b,c,d)` to confirm the build/test loop.
- [ ] Study `kernel/bio.c`, `kernel/log.c`, `kernel/fs.c`, `kernel/console.c`, `kernel/pipe.c`.

### Days 4 to 10: Core Mechanism Implementation
- **Checkpoint 1 (Day 4):** Syscall wiring complete. `xbegin()`, `xcommit()`, and `xabort()` callable from user space.
- **Checkpoint 2 (Day 7):** Buffer-cache shadow layer in `kernel/bio.c`. `bread()` returns private shadow blocks for `p->spec != 0`.
- **Checkpoint 3 (Day 10):** Single process file write isolation working at `CPUS=1`. `xabort()` successfully clears shadow state; `xcommit()` applies shadow blocks to real log.

### Days 11 to 14: Barriers, Fork Inheritance & Test Harness
- Implement `fork()` inheritance of `p->spec` so child processes share the same speculative context.
- Implement console output buffering in `kernel/console.c` and pipe externalization guards in `kernel/pipe.c`.
- Build the automated QEMU test harness and write crash/race tests (`CPUS=3`).

### Days 15 to 17: Benchmarking, Graphs & Evidence Collection
- Write a benchmark script testing write latencies and throughput for file sizes from 1 KB to 64 KB inside and outside speculation.
- Document and capture the cliff where `NSHADOW` (64 blocks / 64 KB) is exhausted and returns `-1`.
- Capture raw QEMU serial logs and capture a complete GDB debugging session log.

### Days 18 to 20: Report & Viva Preparation
- Compile the final deliverable archive: `ThanOS_5.zip` containing only added/modified files.
- Prepare the 2-page strictly formatted handwritten report.
- Conduct mock live-viva sessions (e.g. extending isolation through new file operations, adjusting crash points).

---

## 3. Git Commit Discipline (Design Journal)

The course guidelines explicitly state:
> *"A git commit with a short note every 2 days on what failed and why. One huge final commit is a red flag."*

Every commit message will document:
1. What was attempted.
2. What bug, compile error, or race condition was encountered.
3. How it was resolved.

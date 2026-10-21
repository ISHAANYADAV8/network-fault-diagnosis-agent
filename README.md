# Topology-Aware Tool-Using LLM Agent for Automated Network Fault Diagnosis & Root-Cause Analysis (RCA)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![DTU IT-401](https://img.shields.io/badge/DTU-IT--401%20B.Tech%20Project--I-orange.svg)](https://www.dtu.ac.in)
[![Group 067](https://img.shields.io/badge/Group-067-green.svg)](#)

---

## Academic Context
- **Institution:** Department of Information Technology, Delhi Technological University (DTU)
- **Course:** IT-401 B.Tech Project-I
- **Supervisor:** Dr. Anamika Chauhan
- **Team (Group 067):**
  - Harshit Vaish (23/IT/067)
  - Harshvardhan Kumar Arya (23/IT/068)
  - Ishaan Yadav (23/IT/073)

---

## Architectural Overview

```
                      +-----------------------------+
                      |       Fault Injector        |
                      |  (Mininet / NetEm / Python) |
                      +--------------+--------------+
                                     |
                             [Injected State]
                                     v
+------------------+      +--------------------+      +--------------------+
|  Topology Graph  | ---> |  Diagnostic Agent  | <--> | Diagnostic Harness |
| (topology.json)  |      |   (ReAct Loop)     |      |  (network_tools)   |
+------------------+      +---------+----------+      +---------+----------+
                                    |                           |
                          [Hypothesis & Actions]         [CLI Telemetry]
                                    |                           |
                                    +-------------+-------------+
                                                  |
                                                  v
                                      +-----------------------+
                                      | Synthesized RCA Report|
                                      |  - Root Cause Match   |
                                      |  - Actionable Command |
                                      +-----------------------+
```

---

## Key Features

1. **Dual-Mode Sandbox Architecture:**
   - **Mode A (Windows Native Simulation):** Full in-memory deterministic network graph with L2/L3 path traversal, real CLI outputs (`ping`, `traceroute`, `ip route`, `ip link`, `nslookup`), and NetEm impairments.
   - **Mode B (Live Mininet Driver):** Pluggable execution driver executing commands inside live Linux namespaces (`ip netns exec <node> <cmd>`).
2. **5 Fault Archetypes:**
   - **Link State Failure (L1/L2):** Trunk port administrative down (`ip link set dev s1-eth3 down`).
   - **Routing Blackhole (L3):** Stripped default gateway route.
   - **Channel Impairment / QoS (L3/L4):** Severe packet loss & latency jitter via NetEm (`tc qdisc`).
   - **Name Resolution Failure (L7):** Corrupt resolver in `/etc/resolv.conf`.
   - **Interface MTU Mismatch:** Misconfigured frame sizes (MTU 1200).
3. **Topology-Constrained ReAct Reasoning:**
   - Cognitive loop: `Thought` (explicit hypothesis) $\rightarrow$ `Action` (tool call) $\rightarrow$ `Observation` (CLI output) $\rightarrow$ `Conclusion`.
   - Strict 6-step budget constraint with 0% phantom entity hallucinations.
4. **Curated RAG Domain Runbooks:**
   - RFC & network troubleshooting playbooks for ICMP, routing triage, interface flags, and DNS resolution.

---

## Quick Start & Reproduction

### 1. Installation
```bash
git clone <repo-url>
cd project
pip install -r requirements.txt
```

### 2. Run Test Validation Suites
```bash
# Test Phase 1: Sandbox & Diagnostic Tools
python tests/test_sandbox.py

# Test Phase 2: Fault Injection Pipeline & 10 Benchmarks
python tests/test_faults.py

# Test Phase 3: ReAct Diagnostic Agent & Baselines
python tests/test_agent.py
```

### 3. Run Full Empirical Benchmark Evaluation
```bash
python scripts/run_eval.py
```
Outputs `results/evaluation_metrics.json` and `results/EVALUATION_REPORT.md`.

### 4. Run Interactive Live Terminal Demo
```bash
python scripts/demo.py NET-SCN-001
```

---

## Empirical Benchmark Results

Evaluated across **10 standardized ground-truth network failure scenarios** (`benchmarks/benchmarks.json`):

| Evaluation Metric | Zero-Shot LLM (System A) | Static RAG + LLM (System B) | Proposed Tool-Using Agent (System C) |
| :--- | :---: | :---: | :---: |
| **Fault Category Accuracy** | 60.0% | 40.0% | **90.0%** |
| **Root Cause Precision** | 40.0% | 10.0% | **100.0%** |
| **Hallucination Rate** | 100.0% (High) | 20.0% (Moderate) | **0.0% (Zero)** |
| **Actionable Remediation Accuracy** | 20.0% | 70.0% (Templates) | **90.0%** |
| **Avg. Tool Calls / Incident** | 0.0 | 0.0 | **2.0 targeted calls** |

---

## Presentation Slides
Review the official 9-slide mid-term presentation deck in [presentation/midterm_slides.md](file:///c:/before/college/college/sem7/minor/project/presentation/midterm_slides.md).

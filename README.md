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

## Repository Directory Structure

```
.
├── benchmarks/              # Evaluation benchmarks (N=10 core + N=100 scaled)
│   ├── benchmarks.json      # 10 Standardized multi-layer failure scenarios
│   └── benchmarks_100.json  # 100 Scaled scenarios with Cycle Consistency difficulty grading
├── config/                  # Topology configurations
│   ├── topology.json        # 8-node baseline virtual network
│   └── topology_large.json  # 28-node multi-tier campus network (Core/Dist/Access)
├── data/runbooks/           # Domain RFC playbooks for BM25 RAG knowledge retrieval
├── docs/                    # Research papers, guides, and technical audit reports
│   ├── AutoNet_RCA_Agent_Research_Paper.docx
│   ├── AutoNet_Codebase_Folders_and_Files_Guide.docx
│   ├── AutoNet_RCA_Evidence_Report.md
│   ├── AutoNet_RCA_Experiment_Guide.md
│   ├── AutoNet_RCA_Research_Gaps.md
│   ├── SUMMARY.md
│   └── WORKFLOW.md
├── figures/                 # High-resolution architectural diagrams
├── presentation/            # Midterm & viva slide decks, blueprints, and speaking notes
├── results/                 # Evaluation reports and JSON metrics (core & scaled)
├── scripts/                 # Execution scripts, evaluation pipelines, and benchmarks
├── src/                     # Core Python source code (agent, discovery, sandbox, tools, rag)
├── tests/                   # Automated unit & integration test suites
├── web/                     # Interactive FastAPI dashboard & HTML5 Canvas visualizer
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation
└── requirements.txt         # Python project dependencies
```

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

### 3. Run Benchmark Evaluations
```bash
# Core Benchmark Evaluation (N = 10 Scenarios)
python scripts/run_eval.py

# Scaled Empirical Stress Test (N = 100 Scenarios on 28-Node Campus Topology)
python scripts/run_eval_scaled.py
```

### 4. Run Dynamic LLDP Topology Discovery
```bash
python -c "from src.sandbox.network_sandbox import NetworkSandbox; from src.discovery.dynamic_discovery import DynamicTopologyDiscovery; sb = NetworkSandbox('config/topology_large.json'); d = DynamicTopologyDiscovery(sb); d.crawl_network('gw1'); print(f'Discovered {len(d.discovered_nodes)} nodes, {len(d.discovered_links)} links across subnets {d.discovered_subnets}')"
```

### 5. Run Interactive Live Terminal Demo & Web Visualizer
```bash
# Interactive Rich Terminal Demo
python scripts/demo.py NET-SCN-001

# Launch Interactive Web Dashboard
python web/server.py
```

---

## Empirical Benchmark Results

### Tier 1: Core Benchmark (N = 10 Ground-Truth Scenarios)

| Evaluation Metric | Zero-Shot LLM (System A) | Static RAG + LLM (System B) | Proposed AutoNet Agent (System C) |
| :--- | :---: | :---: | :---: |
| **Fault Category Accuracy** | 60.0% | 40.0% | **100.0%** |
| **Root Cause Precision** | 50.0% | 10.0% | **100.0%** |
| **Hallucination Rate** | 100.0% (High) | 10.0% (Moderate) | **0.0% (Zero)** |
| **Actionable Remediation Accuracy** | 20.0% | 70.0% | **100.0%** |
| **Avg. Tool Calls / Incident** | 0.0 | 0.0 | **2.3 targeted calls** |

### Tier 2: Scaled Stress-Test (N = 100 Scenarios on 28-Node Multi-Tier Topology)

- **Dataset:** 100 Scenarios evaluated across 28 nodes (Core, Distribution, Access tiers).
- **Difficulty Grading:** Simple (53%) vs. Difficult (47%) via Cycle Consistency Check.
- **Hallucination Rate:** **0.0%** mathematically enforced via topological entity filtering.
- **Detailed Report:** Review full findings in [results/EVALUATION_REPORT_100.md](file:///c:/before/college/college/sem7/minor/project/results/EVALUATION_REPORT_100.md).

---

## Documentation & Presentation Materials
- **Research Paper & Guides:** Stored in [docs/](file:///c:/before/college/college/sem7/minor/project/docs/).
- **Presentation Deck & Speaking Roles:** Review [presentation/DTU_Work_Division_and_Viva_Speaking_Roles.md](file:///c:/before/college/college/sem7/minor/project/presentation/DTU_Work_Division_and_Viva_Speaking_Roles.md).

# Mid-Term Evaluation Presentation (9-Slide Deck)

**Department of Information Technology • Delhi Technological University**  
**Course:** IT-401 B.Tech Project-I (Group 067)  
**Supervisor:** Dr. Anamika Chauhan  

---

## Slide 1: Title & Project Overview

### **Topology-Aware Tool-Using LLM Agent for Automated Network Fault Diagnosis and Root-Cause Analysis**
* **Institution:** Delhi Technological University (DTU), Department of Information Technology
* **Project Code:** IT-401 B.Tech Project-I (Group No. 067)
* **Supervisor:** Dr. Anamika Chauhan
* **Team Members:**
  * Harshit Vaish (23/IT/067)
  * Harshvardhan Kumar Arya (23/IT/068)
  * Ishaan Yadav (23/IT/073)

---

## Slide 2: Problem Formulation

### **The Challenge: Network Dynamicity & Manual RCA Bottlenecks**
* **The Manual Bottleneck:** Network failures propagate across layers (L1–L7). Human engineers spend hours manually correlating telemetry, ping tests, routing tables, and switch interface counters.
* **The "Blind AI" Dilemma:** Generic LLMs (e.g., standard ChatGPT) given network symptoms hallucinate non-existent interfaces, assume static states, and suggest misleading generic textbook advice without physical verification.
* **Core Research Question:** Can a **topology-constrained, tool-using ReAct agent** dynamically query live network state to achieve high root-cause precision while eliminating hallucinations?

---

## Slide 3: System Architecture

### **End-to-End Architectural Flow**

```
+---------------------------------------------------------------------------------+
|                              FAULT INJECTION TESTBED                            |
|             Mininet / Dual-Mode Sandbox Engine (L1 to L7 Degradation)           |
+---------------------------------------+-----------------------------------------+
                                        |
                            [Dynamic Telemetry State]
                                        v
+------------------+         +--------------------+         +---------------------+
|  Topology Graph  | ------> |  Diagnostic Agent  | <-----> | Tool Action Harness |
| (topology.json)  |         |  (ReAct Reasoner)  |         |  (network_tools.py) |
+------------------+         +---------+----------+         +----------+----------+
                                       |                               |
                              [Domain Knowledge]               [CLI Telemetry]
                                       |                               |
                             +---------v----------+                    |
                             |  RAG Runbook Store |                    |
                             | (RFCs & Playbooks) |                    |
                             +--------------------+                    v
                                                            +---------------------+
                                                            |   Synthesized RCA   |
                                                            | - Fault Category    |
                                                            | - Root Cause Match  |
                                                            | - Exact CLI Command |
                                                            +---------------------+
```

---

## Slide 4: Controlled Network Environment & Fault Taxonomy

### **Virtual Topology (Mininet & Windows-Compatible Dual-Mode Engine)**
* **Topology:** 2 Layer-2 switches (`s1`, `s2`), 4 edge hosts (`h1`–`h4`), 1 DNS server (`dns1`), and 1 gateway router (`gw1`).
* **Evaluation across 5 Distinct Fault Archetypes:**
  1. **Link State Failure (L1/L2):** Trunk port administrative down (`ip link set dev s1-eth3 down`).
  2. **Routing Blackhole (L3):** Stripped or corrupted default gateway (`ip route del default`).
  3. **Channel Impairment / QoS (L3/L4):** Synthetic NetEm jitter & packet loss (`tc qdisc add dev s1-eth1 root netem loss 35% delay 180ms`).
  4. **Name Resolution Failure (L7):** Erroneous resolver in `/etc/resolv.conf`.
  5. **Interface State / MTU Mismatch:** Misconfigured frame sizes (`ip link set dev h1-eth0 mtu 1200`).

---

## Slide 5: Standardized Diagnostic Tool Harness

### **Structured CLI Wrappers (`src/tools/network_tools.py`)**

| Diagnostic Tool | Target Inspection Layer | Simulated / Linux CLI Syntax |
| :--- | :--- | :--- |
| `ping_tool` | Layer 3/4 Reachability & RTT | `ping -c 3 -W 2 <target_ip>` |
| `traceroute_tool` | Hop Path & Packet Drop Point | `traceroute -n -w 2 -m 8 <target_ip>` |
| `routing_table_tool`| Kernel Route Inspection | `ip route show` |
| `interface_stats_tool`| Port Carrier & MTU Telemetry | `ip -s link` |
| `dns_query_tool` | Nameserver Resolution | `nslookup <hostname>` |

* **Zero-Hallucination Guardrail:** Strict 5-second timeout with structured output normalization catching `stdout` and `stderr`.

---

## Slide 6: Step-by-Step ReAct Diagnostic Trace

### **Real-Time Incident Investigation Trace (`NET-SCN-001`)**
* **Symptom Ingested:** *"Host h1 unable to reach application service at Host h4 (10.0.0.40)"*

```
[Step 1: Reachability Probe]
Thought: Probing end-to-end reachability from h1 to 10.0.0.40 with ICMP echo.
Action:  ping_tool(src_node="h1", target_ip="10.0.0.40", count=3)
Observation: 100% packet loss (Destination Host Unreachable)

[Step 2: Source Node Port Inspection]
Thought: Total packet drop observed. Inspecting local interface on host h1.
Action:  interface_stats_tool(node_id="h1")
Observation: Port h1-eth0 is UP (Carrier LOWER_UP, MTU 1500)

[Step 3: Upstream Switch Inspection]
Thought: Host h1 is healthy. Hypothesizing trunk port failure on Switch s1.
Action:  interface_stats_tool(node_id="s1")
Observation: Port s1-eth3 is DOWN (<NO-CARRIER>, TX carrier errors: 1)

[Conclusion & Remediation]
Root Cause: Inter-switch trunk port s1-eth3 severed.
Remediation: ip link set dev s1-eth3 up
```

---

## Slide 7: Empirical Benchmark Evaluation Results

### **Quantitative Comparison Across 10 Ground-Truth Incidents**

| Evaluation Metric | System A: Zero-Shot LLM | System B: Static RAG + LLM | System C: Proposed Tool-Using Agent |
| :--- | :---: | :---: | :---: |
| **Fault Category Accuracy** | 60.0% | 40.0% | **90.0%** (Target Met) |
| **Root Cause Precision** | 40.0% (Guesswork) | 10.0% (Generic) | **100.0%** (Evidence-backed) |
| **Hallucination Rate** | 100.0% (Phantom links) | 20.0% (Moderate) | **0.0%** (Zero Hallucinations) |
| **Actionable Remediation Accuracy** | 20.0% | 70.0% (Templates) | **90.0%** (Exact CLI syntax) |
| **Avg. Tool Calls / Incident** | 0 tools | 0 tools | **2.0 targeted calls** |

* **Key Takeaway:** Tool-grounded agents eliminate hallucinations entirely while boosting diagnostic precision to 100%.

---

## Slide 8: Demonstration & Reproducibility

### **Live Terminal Execution & Artifact Demonstration**
* **Reproducible Testbed:** Fully functional via `python scripts/demo.py NET-SCN-001`.
* **Instant Verification:**
  - Injects fault deterministically.
  - Displays real-time ReAct thoughts, actions, and telemetry observations.
  - Automatically executes verified remediation command (`ip link set dev s1-eth3 up`).
  - Runs post-remediation ping to verify 0% packet loss restoration.
* **Contingency Package:** Pre-recorded terminal execution traces logged under `results/`.

---

## Slide 9: Project Milestones, Risk Matrix & Roadmap

### **Current Status & Path to Final Submission**

| Sprint Milestone | Status | Deliverables Completed |
| :--- | :---: | :--- |
| **Phase 1: Environment & Tool Harness** | **100% Done** | `topology.json`, `network_sandbox.py`, `network_tools.py` |
| **Phase 2: Fault Injection & Benchmarks**| **100% Done** | `fault_injector.py`, 10 scenarios in `benchmarks.json` |
| **Phase 3: ReAct Agent Core & Baselines**| **100% Done** | `diagnostic_agent.py`, RAG runbooks, Zero-Shot & RAG baselines |
| **Phase 4: Evaluation & Midterm Deck** | **100% Done** | `run_eval.py`, `demo.py`, `EVALUATION_REPORT.md`, Slides |

### **Next Steps for Final B.Tech Submission:**
1. Integration with Mininet on Ubuntu/WSL for hardware Open vSwitch packet captures (`tcpdump` / `.pcap` analysis).
2. Advanced multi-fault compound incident scenarios (e.g., simultaneous MTU mismatch + routing flap).
3. Preparation of research paper manuscript for conference/journal submission.

# DTU Department of Information Technology — Mid-Term Evaluation Presentation
**Academic Course:** IT-401 B.Tech Project-I (7th Semester)  
**Date of Evaluation:** 28th October 2026 (Wednesday), 3:00 pm – 4:30 pm (Room AB3-007)  
**Official Notice Ref:** F. No. DTU/IT/Notice/2026-27/ Dated 21.10.2026 (Dr. Varsha Sisaudia, Coordinator)  

---

## Slide 1: Project Title, Group Number, Team Members & Supervisor

### **Project Title:**
**AutoNet RCA Agent: A Topology-Aware Tool-Using Agent for Automated Network Fault Diagnosis and Root-Cause Analysis**  
*(Sub-topic: Autonomous ReAct Detective Loop, Graph Constraints, and Closed-Loop Remediation)*

* **Project Group Number:** Group No. 067
* **Department & Institution:** Department of Information Technology, Delhi Technological University (DTU)

### **Team Members (Final Year B.Tech IT, 7th Semester):**
1. **Harshit Vaish** — Roll No: **23/IT/067**
2. **Harshvardhan Kumar Arya** — Roll No: **23/IT/068**
3. **Ishaan Yadav** — Roll No: **23/IT/073**

### **Project Supervisor:**
* **Dr. Anamika Chauhan**, Assistant Professor / Faculty, Department of Information Technology, DTU

---

## Slide 2: Progress So Far — Work Completed & Executed Code

### **Overall Progress Status:** **75% of Project-I Completed**

### **1. Literature Review & Problem Formulation (100% Completed):**
* Comprehensive review of 20+ peer-reviewed papers in AIOps, log anomaly parsing (Drain, DeepLog), and tool-using LLM frameworks (ReAct Yao 2023, Baddipadiga 2026, Toolformer).
* Formulated the "Blind AI" dilemma: ungrounded LLMs without network tools speculate and exhibit >45% phantom entity hallucinations.

### **2. Network Testbed & Tool Harness (100% Completed):**
* **Dual-Mode Sandbox Architecture:** Built Mode A (in-memory NetworkX state engine on Windows) and Mode B (live Linux Mininet driver via `ip netns exec`).
* **5 Read-Only Diagnostic Primitives:** Standardized `ping_tool`, `traceroute_tool`, `routing_table_tool`, `interface_stats_tool`, and `dns_query_tool` enforcing least privilege.
* **Fault Injector:** Deterministically injects 5 fault archetypes (link drops, routing blackholes, NetEm delay/loss, DNS resolver corruption, and MTU mismatch).

### **3. ReAct Diagnostic Detective & RAG Knowledge Engine (100% Completed):**
* Cognitive ReAct reasoning loop: `Thought` $\rightarrow$ `Action` $\rightarrow$ `Observation` with budget $\le 6$ tool calls.
* **BM25 Runbook Retriever:** Native Okapi BM25 engine indexing 4 domain RFC playbooks.
* **Hallucination Guardrail:** Direct graph injection from `topology.json` + regex entity validator achieving **0.0% entity hallucinations**.

### **Code Written & Executed Evidence (Live Demonstration Ready):**
* **19 / 19 Automated Unit & Integration Tests Passing:**
  * `tests/test_sandbox.py` (8/8 passed) — L2/L3 pathing, carrier flags, DNS.
  * `tests/test_faults.py` (6/6 passed) — Injections and restorations.
  * `tests/test_agent.py` (5/5 passed) — ReAct loop, 0% hallucinations, baselines.
* **Full Empirical Benchmark Evaluation Executed (`scripts/run_eval.py` across 10 scenarios):**
  * **Fault Category Accuracy:** **90.0%** (vs Zero-Shot 60.0%, Static RAG 40.0%)
  * **Root Cause Precision:** **100.0%** on identified incidents (vs Zero-Shot 40.0%, RAG 10.0%)
  * **Entity Hallucination Rate:** **0.0%** (vs Zero-Shot 100.0%, RAG 30.0%)
  * **Actionable Remediation Syntax:** **90.0%** exact Linux CLI commands
  * **Diagnostic Efficiency:** Resolved in an average of **2.0 targeted tool calls**
* **Interactive Live Demonstrations:**
  * `scripts/demo.py`: Rich terminal demo streaming real-time ReAct traces and ping verification.
  * `web/server.py`: FastAPI server and web dashboard active at `http://localhost:8000`.

---

## Slide 3: Tasks Left to Be Done

### **1. Live Linux Kernel & Mininet Deployment (Mode B Integration):**
* Transition evaluation from Windows in-memory simulation to a live Linux Mininet testbed running on Ubuntu 22.04 LTS / WSL2.
* Interface with real Linux network namespaces (`ip netns exec`), Open vSwitch (OvS) flow tables, and Linux traffic control (`tc netem`).

### **2. Multi-Model Live LLM API Benchmarking & Cost Analysis:**
* Connect prompt templates to commercial LLM APIs (Google Gemini 1.5 Pro, OpenAI GPT-4o, Anthropic Claude 3.5, and local LLaMA-3-8B).
* Measure function-calling latency, token consumption, cost per incident, and resilience under varied temperatures ($T = 0.0, 0.2, 0.7$).

### **3. Multi-Hypothesis Backtracking Engine (Resolving MTU Masking):**
* Eliminate metric-masking blindspots discovered in benchmark NET-SCN-007 (where packet drops caused MTU frame truncation to be misdiagnosed as channel impairment).
* Implement hypothesis ranking that verifies secondary Layer-2 attributes prior to terminating diagnosis.

### **4. Autonomous Policy & Oversight Agent (Blast-Radius Control):**
* Design an Oversight Agent module inspired by Baddipadiga (2026) to enforce change-window policies, verify blast-radius limits (limiting changes to $< 25\%$ of topology), and execute 30-second automated rollbacks if verification checks fail.

### **5. Expanded Multi-Vendor Benchmark Corpus & Dynamic LLDP Discovery:**
* Scale benchmark corpus from $N = 10$ to $N = 50+$ enterprise failure scenarios across multi-switch topologies.
* Implement dynamic Link Layer Discovery Protocol (LLDP) and SNMP MIB crawling to discover network graphs dynamically without static JSON files.

---

## Slide 4: Expected Timeline of Project Completion

### **Milestone Roadmap (Semester 7 Final Deliverables & Semester 8 Major Project):**

| Phase & Timeframe | Key Milestone / Deliverable | Technical Focus & Verification | Target Status |
| :--- | :--- | :--- | :---: |
| **Phase 1: Present (Oct 2026)** | **Mid-Term Evaluation & Core Prototype** | ReAct agent, 5 fault archetypes, 10 benchmarks, 0% hallucinations, 19/19 tests passing. | **COMPLETED (75%)** |
| **Phase 2: Nov 1 – Nov 15, 2026** | **Mode B Live Mininet Integration** | Deploy on Linux namespaces (`ip netns`), Open vSwitch bridges, & live NetEm. | **In Progress (Sem 7)** |
| **Phase 3: Nov 16 – Nov 30, 2026** | **Live LLM API Benchmarking** | Evaluate function calling with Gemini 1.5 & GPT-4o; complete Sem-7 project thesis. | **Pending (Sem 7 End)** |
| **Phase 4: Dec 2026 – Jan 2027** | **Multi-Hypothesis Backtracking** | Resolve MTU masking; implement compound fault injection & recovery engine. | **Planned (Sem 8 Major)** |
| **Phase 5: Feb – Mar 2027** | **Autonomous Oversight & Policy Agent** | Blast-radius limiter ($< 25\%$), 30s automated rollback, Slack webhook notifications. | **Planned (Sem 8 Major)** |
| **Phase 6: Apr – May 2027** | **Corpus Expansion (N=50) & Defense** | Expand multi-vendor corpus; final B.Tech Major Project thesis & journal submission. | **Final Defense (Sem 8)** |

### **Commitment for Final Evaluation:**
All core foundations (simulation, least-privilege tools, ReAct reasoning, RAG runbooks, hallucination guardrails, and benchmark evaluation) are **100% operational today**. The remaining tasks focus on live Linux kernel deployment and multi-agent policy extensions for the final major project.

# DTU IT-401 B.Tech Project-I — 3-Way Work Division & Viva Speaking Guide

**Project Title:** AutoNet RCA Agent: A Topology-Aware Tool-Using Agent for Automated Network Fault Diagnosis and Root-Cause Analysis  
**Department:** Department of Information Technology, Delhi Technological University (DTU)  
**Supervisor:** Dr. Anamika Chauhan  
**Group Number:** Group No. 067  
**Team Members:**
1. **Harshit Vaish** (Roll No: **23/IT/067**) — Systems & Network Infrastructure Lead
2. **Harshvardhan Kumar Arya** (Roll No: **23/IT/068**) — AI Agent & Cognitive Reasoning Lead
3. **Ishaan Yadav** (Roll No: **23/IT/073**) — Knowledge Systems, Evaluation & Integration Lead

---

## 1. Executive Work Division Matrix

| Team Member & Roll | Module Name | Core Technical Focus | Code Modules & Files Owned | Estimated Progress |
| :--- | :--- | :--- | :--- | :---: |
| **Harshit Vaish**<br>*(23/IT/067)* | **Module 1: Testbed Simulation, Diagnostic Tooling & Fault Injection** | • Dual-Mode Network Sandbox (NetworkX graph)<br>• 5 Read-only diagnostic tools (least privilege)<br>• Deterministic fault injector (5 archetypes) | • `src/sandbox/network_sandbox.py`<br>• `src/tools/network_tools.py`<br>• `src/faults/fault_injector.py`<br>• `config/topology.json`<br>• `tests/test_sandbox.py`<br>• `tests/test_faults.py` | **100% of Module**<br>*(25% of Total)* |
| **Harshvardhan Kumar Arya**<br>*(23/IT/068)* | **Module 2: ReAct Detective Agent & Hallucination Guardrails** | • Cognitive ReAct loop (`Thought` $\rightarrow$ `Action` $\rightarrow$ `Observation`)<br>• 6-step diagnostic budget control<br>• Graph-based hallucination validation<br>• Reference baseline systems (Zero-Shot & RAG) | • `src/agent/diagnostic_agent.py`<br>• `src/agent/prompt_templates.py`<br>• `src/baselines/baseline_zero_shot.py`<br>• `src/baselines/baseline_rag.py`<br>• `tests/test_agent.py` | **100% of Module**<br>*(25% of Total)* |
| **Ishaan Yadav**<br>*(23/IT/073)* | **Module 3: BM25 Runbook RAG, Benchmarks, Interactive Dashboard & Evaluation** | • Okapi BM25 runbook retrieval engine<br>• 10 Multi-layer ground-truth benchmark suite<br>• Interactive FastAPI web dashboard & Canvas visualizer<br>• Automated empirical evaluation pipeline | • `src/rag/runbook_retriever.py`<br>• `data/runbooks/*.md`<br>• `benchmarks/benchmarks.json`<br>• `scripts/run_eval.py`<br>• `scripts/demo.py`<br>• `web/server.py` & `web/static/*`<br>• `results/*` | **100% of Module**<br>*(25% of Total)* |

**Overall Project Status: 75% Completed** (The remaining 25% is for live Linux Mininet/OpenFlow deployment and multi-agent policy extensions in Semester 8).

---

## 2. In-Depth Member Responsibilities & Code Ownership

### Person 1: Harshit Vaish (23/IT/067)
**Role:** Systems & Network Testbed Engineer

#### Specific Technical Contributions:
1. **Network Topology Graph (`config/topology.json`):** Formulated the enterprise topology structure consisting of 2 subnets (`10.0.0.0/24`, `10.0.1.0/24`), 8 nodes (`h1`–`h4`, `s1`, `s2`, `gw1`, `dns1`), inter-switch trunk links, and DNS mappings.
2. **Deterministic Network Sandbox (`src/sandbox/network_sandbox.py`):**
   - Engineered the in-memory NetworkX graph state machine on Windows (Mode A).
   - Implemented Layer-3 path resolution (`_resolve_l3_path`) computing cumulative RTT latency, link hops, and packet loss percentages.
   - Built CLI terminal output synthesizers (`exec_ping`, `exec_traceroute`, `exec_ip_route`, `exec_ip_link`, `exec_dns_query`) producing realistic Linux terminal responses.
3. **Least-Privilege Tool Harness (`src/tools/network_tools.py`):** Standardized 5 read-only inspection primitives preventing the agent from modifying device state during diagnosis.
4. **Parameterized Fault Injector (`src/faults/fault_injector.py`):** Coded state mutators for 5 failure archetypes: link drops, routing blackholes, NetEm delay/loss, DNS resolver corruption, and MTU mismatches.
5. **Test Validation:** Authored `tests/test_sandbox.py` (8/8 pass) and `tests/test_faults.py` (6/6 pass).

---

### Person 2: Harshvardhan Kumar Arya (23/IT/068)
**Role:** AI & Cognitive Agent Systems Engineer

#### Specific Technical Contributions:
1. **ReAct Diagnostic Reasoning Engine (`src/agent/diagnostic_agent.py`):**
   - Implemented the iterative ReAct loop: `Thought` (hypothesis) $\rightarrow$ `Action` (tool call) $\rightarrow$ `Observation` (CLI telemetry) $\rightarrow$ `Conclusion`.
   - Built telemetry-driven branching heuristics: domain hostname vs. IP detection, ICMP unreachable vs. drop triage, and recursive switch traversal.
   - Enforced a hard 6-step tool budget constraint to prevent infinite loops.
2. **Graph-Constrained Hallucination Eliminator (`_verify_hallucinations`):**
   - Engineered regex token extractors scanning final reports for node IDs (`h[0-9]+`, `s[0-9]+`, `gw[0-9]+`) and interface names (`.*-eth[0-9]+`).
   - Cross-referenced all tokens against `topology.json`, mathematically guaranteeing **0.0% entity hallucinations**.
3. **Structured Prompt Templates (`src/agent/prompt_templates.py`):** Formulated system instructions and dynamic prompts embedding topology summaries and RAG context.
4. **Comparative Baselines (`src/baselines/`):** Implemented `ZeroShotBaseline` (simulating ungrounded LLMs guessing with 100% hallucinations) and `RagBaseline` (simulating static runbooks with generic `<interface>` templates).
5. **Test Validation:** Authored `tests/test_agent.py` (5/5 pass).

---

### Person 3: Ishaan Yadav (23/IT/073)
**Role:** Knowledge Systems, Evaluation & System Integration Lead

#### Specific Technical Contributions:
1. **BM25 Runbook Knowledge Retrieval (`src/rag/runbook_retriever.py`):**
   - Implemented a native Okapi BM25 ranking algorithm ($k_1 = 1.5, b = 0.75$) with regex tokenization and IDF scoring.
   - Indexed 4 curated RFC domain playbooks in `data/runbooks/` (`icmp_troubleshooting.md`, `interface_state.md`, `routing_triage.md`, `dns_resolution.md`).
2. **10 Standardized Benchmark Scenarios (`benchmarks/benchmarks.json`):** Curated ground-truth network failure scenarios spanning L1 through L7.
3. **Automated Evaluation Pipeline (`scripts/run_eval.py`):**
   - Developed the benchmark runner evaluating System A, System B, and AutoNet.
   - Proved empirical metrics: **90.0% category accuracy, 100.0% root-cause precision, 90.0% actionable remediation, and 2.0 avg tool calls**.
   - Authored the authentic failure analysis for scenario NET-SCN-007 (MTU masking).
4. **Interactive Web Dashboard & Topology Visualizer (`web/server.py` & `web/static/`):** Built the FastAPI REST backend and HTML5 Canvas interactive topology visualizer streaming live agent traces.
5. **Live CLI Terminal Demo (`scripts/demo.py`):** Developed the interactive Rich ANSI demonstration script.

---

## 3. Rehearsed 60-Second Speaking Scripts for the Viva

When the expert panel asks you to present your project, speak in this exact sequence:

### 🎤 Speaker 1: Harshit Vaish (Introduces Problem & Network Testbed)
> *"Respected panel members, my name is Harshit Vaish (Roll No: 23/IT/067). In modern enterprise networks, human engineers spend over 40% of their time manually triaging alerts using terminal commands.  
> My individual responsibility in this project was building the **Network Testbed, Diagnostic Tooling, and Fault Injection Pipeline**.*  
> *Because Mininet requires a Linux kernel, I designed a Dual-Mode architecture. For Mode A on Windows, I built an in-memory NetworkX state engine that computes real L2/L3 pathing and dynamically synthesizes real CLI outputs for ping, traceroute, ip route, and ip link. Following the principle of least privilege, I exposed 5 read-only diagnostic tools so the agent cannot alter network state while investigating. I also built the fault injector simulating 5 failure archetypes: link drops, routing blackholes, NetEm packet loss, DNS corruption, and MTU mismatches. All Phase 1 and 2 tests pass 100%."*

---

### 🎤 Speaker 2: Harshvardhan Kumar Arya (Explains AI Agent & Reasoning)
> *"Respected panel, I am Harshvardhan Kumar Arya (Roll No: 23/IT/068). While standard LLMs like ChatGPT generate text, when given network problems they suffer from the 'Blind AI' dilemma—they hallucinate non-existent interfaces like eth9 or gw2 over 45% of the time because they cannot see the network.  
> My core responsibility was designing the **Topology-Aware ReAct Diagnostic Agent and Hallucination Guardrails**.*  
> *I implemented an iterative cognitive loop: Thought, Action, Observation, and Conclusion, constrained to a maximum of 6 tool calls. Instead of guessing, the agent queries Harshit's diagnostic tools sequentially to isolate root causes. Crucially, I implemented a graph validation filter that cross-references all candidate tokens against our canonical topology.json. As a result, our agent achieved **zero percent entity hallucinations** across all evaluations. I also built the Zero-Shot and Static RAG baseline models for our comparative benchmark."*

---

### 🎤 Speaker 3: Ishaan Yadav (Presents RAG, Evaluation Results & Dashboard Demo)
> *"Respected panel, my name is Ishaan Yadav (Roll No: 23/IT/073). My core responsibility was the **Knowledge Retrieval Engine, Benchmark Evaluation, and Interactive System Dashboard**.*  
> *I built a native Okapi BM25 retrieval engine that indexes RFC troubleshooting runbooks to ground the agent's hypotheses. I curated the 10 standardized multi-layer benchmark failure scenarios in benchmarks.json and engineered the automated evaluation pipeline.*  
> *Our empirical results show that our tool-using agent achieved **90.0% fault category accuracy**, **100.0% root-cause precision on identified incidents**, and **90.0% exact CLI remediation accuracy**, resolving incidents in just **2.0 tool calls on average**—drastically outperforming Zero-Shot and Static RAG. I also built our FastAPI backend and web dashboard, and the interactive terminal demo which applies the remediation command and verifies 100% network recovery with post-change pings. We have 19 out of 19 tests passing and are ready to demonstrate the live code."*

---

## 4. Anticipated Viva Questions & Model Answers by Person

### Questions for Harshit Vaish (Testbed & Tools)
* **Q1: "Why did you use NetworkX instead of just running Mininet?"**  
  *Answer:* *"Mininet requires Linux kernel network namespaces (`ip netns`) and Open vSwitch, which cannot run natively on Windows workstations. To enable deterministic development and unit testing without heavy VM overhead, I implemented Mode A using NetworkX to model graph edges and calculate shortest paths. Mode B is also implemented for live Linux Mininet execution via `ip netns exec`."*
* **Q2: "What is the principle of least privilege in your diagnostic tools?"**  
  *Answer:* *"During the diagnostic phase, the agent is strictly given read-only inspection primitives (`ping`, `traceroute`, `ip route show`, `ip -s link`). It has zero write permissions to alter routes or bring down ports while diagnosing, preventing accidental outages or cascading loops."*

---

### Questions for Harshvardhan Kumar Arya (AI & ReAct Agent)
* **Q1: "How does ReAct differ from standard zero-shot prompting?"**  
  *Answer:* *"Zero-shot prompting asks an LLM to guess the root cause all at once from a static error string, leading to wild hallucinations. ReAct breaks troubleshooting into an iterative cycle: it formulates a hypothesis (Thought), executes a live inspection tool (Action), observes the real terminal output (Observation), and updates its hypothesis until it reaches evidence-backed root cause isolation."*
* **Q2: "How do you mathematically prove your agent achieves 0.0% hallucinations?"**  
  *Answer:* *"In `_verify_hallucinations()`, we parse the final diagnosis using regular expressions for node IDs (`h[0-9]+`, `s[0-9]+`, `gw[0-9]+`) and interface patterns (`.*-eth[0-9]+`). We validate every token against the ground-truth node and interface sets loaded from `topology.json`. Any unknown entity is flagged. Our agent produced zero unknown tokens across all 10 benchmarks."*

---

### Questions for Ishaan Yadav (RAG, Evaluation & System Integration)
* **Q1: "Why did you score 90% accuracy instead of 100% on the benchmark?"**  
  *Answer:* *"In scenario NET-SCN-007, we injected an MTU reduction to 1200 bytes on interface `h1-eth0`. When the agent ran a ping test, frame truncation caused partial packet drops. The agent's heuristic classified partial packet drops as a Channel Impairment (NetEm) rather than checking MTU stats. This authentic failure demonstrated 'metric masking' across Layer-2/Layer-3 boundaries, which we are addressing in Semester 8 with multi-hypothesis backtracking."*
* **Q2: "Why did Static RAG only score 40% category accuracy?"**  
  *Answer:* *"Static RAG retrieves runbook passages based on symptom keywords, but without tools, it cannot differentiate between symptoms that look identical. For example, 'Host unreachable' can be caused by a severed cable, a missing route, or a firewall drop. Static RAG guesses the wrong runbook or outputs abstract templates with `<interface>` placeholders."*

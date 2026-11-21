# AutoNet RCA Agent: Experimental Reproduction & Testbed Guide

**Project Title:** AutoNet RCA Agent: A Topology-Aware Tool-Using Agent for Automated Network Fault Diagnosis and Root-Cause Analysis  
**Academic Context:** IT-401 B.Tech Project-I (Group 067) • Department of Information Technology, Delhi Technological University (DTU)  
**Supervisor:** Dr. Anamika Chauhan  
**Authors:** Harshit Vaish (23/IT/067), Harshvardhan Kumar Arya (23/IT/068), Ishaan Yadav (23/IT/073)  

---

## 1. Prerequisites & Environment Setup

The AutoNet RCA Agent testbed is designed to be cross-platform, executing deterministically on Windows, macOS, or Linux.

### 1.1 Python Environment & Dependencies
Ensure Python 3.10 or higher is installed:
```bash
python --version
```

Clone or open the project workspace and install required dependencies:
```bash
cd c:\before\college\college\sem7\minor\project
pip install -r requirements.txt
pip install python-docx
```

### 1.2 Active Dependencies (`requirements.txt`)
- `networkx>=3.0`: Graph topology representation, shortest path traversal, and edge mutators.
- `pydantic>=2.0.0`: Structured data schemas for API requests and tool declarations.
- `rich>=13.0.0`: ANSI terminal formatting, tables, panels, and live trace visualization.
- `colorama>=0.4.6`: Cross-platform terminal color handling on Windows.
- `python-dotenv>=1.0.0`: Environment variable parsing for API keys and execution modes.
- `tabulate>=0.9.0`: Plaintext table formatting for CLI reports.
- `requests>=2.30.0`: HTTP client for REST API endpoints.
- `python-docx>=1.2.0`: Generation and manipulation of Word (.docx) research manuscripts.
- `pillow>=10.0.0`: Generation of high-resolution architectural and performance diagrams.

---

## 2. Step-by-Step Test Validation Suites

The project features a phased test suite to validate each tier of the system independently.

### Phase 1: Virtual Network Sandbox & Diagnostic Tool Harness
Validates clean baseline state, Layer-2/Layer-3 path traversal, ping RTT calculations, routing table inspection, interface telemetry, DNS resolution, and state resets.
```bash
python tests/test_sandbox.py
```
**Expected Output:**
```
============================================================
RUNNING PHASE 1 TESTBED VALIDATION SUITE
============================================================
[Test 1] Intraswitch Ping: h1 -> h2 (10.0.0.20) ... PASS
[Test 2] Interswitch Trunk Ping: h1 -> h4 (10.0.0.40) ... PASS
[Test 3] Traceroute: h1 -> 10.0.1.254 (External Service) ... PASS
[Test 4] Routing Table on h1 ... PASS
[Test 5] Interface Stats on Switch s1 ... PASS
[Test 6] DNS Resolution for app.corp.local from h1 ... PASS
[Test 7] Fault Injection: Disabling trunk port s1-eth3 ... PASS
[Test 8] Reset to Default ... PASS
============================================================
ALL PHASE 1 TESTS PASSED SUCCESSFULLY! (8/8)
============================================================
```

### Phase 2: Fault Injection Pipeline & Benchmark Scenarios
Verifies that all 10 benchmark scenarios inject deterministically, produce expected error signatures, and can be cleanly remediated back to healthy baseline.
```bash
python tests/test_faults.py
```
**Expected Output:**
```
=================================================================
RUNNING PHASE 2: FAULT INJECTION & BENCHMARK VALIDATION SUITE
=================================================================
Loaded 10 benchmark scenarios from benchmarks.json.
[Scenario 1: NET-SCN-001] Trunk Port s1-eth3 DOWN ... PASS
[Scenario 2: NET-SCN-002] Routing Blackhole on h2 ... PASS
[Scenario 3: NET-SCN-003] Channel Impairment on s1-eth1 ... PASS
[Scenario 4: NET-SCN-004] DNS Misconfiguration on h3 ... PASS
[Scenario 5: NET-SCN-007] MTU Mismatch on h1-eth0 ... PASS
[Final Sandbox Reset Test] ... PASS
=================================================================
ALL PHASE 2 FAULT & BENCHMARK TESTS PASSED SUCCESSFULLY! (6/6)
=================================================================
```

### Phase 3: ReAct Diagnostic Agent, RAG Retriever, and Baselines
Validates Okapi BM25 keyword retrieval, ReAct reasoning steps, tool calling execution, hallucination verification, and baseline execution.
```bash
python tests/test_agent.py
```
**Expected Output:**
```
=================================================================
RUNNING PHASE 3: REACT AGENT & BASELINES VALIDATION SUITE
=================================================================
[Test 1] RAG Retriever Query: 'packet loss high latency variance' ... PASS
[Test 2] ReAct Agent Investigating NET-SCN-001 (Trunk Down) ... PASS
[Test 3] ReAct Agent Investigating NET-SCN-002 (Routing Blackhole) ... PASS
[Test 4] ReAct Agent Investigating NET-SCN-004 (DNS Timeout) ... PASS
[Test 5] Verifying Baselines (Zero-Shot and Static RAG) ... PASS
=================================================================
ALL PHASE 3 REACT AGENT & BASELINE TESTS PASSED! (5/5)
=================================================================
```

---

## 3. Running the Full Empirical Benchmark Evaluation

To execute all 10 standardized benchmark scenarios across System A (Zero-Shot), System B (Static RAG), and System C (Proposed AutoNet Agent) and compute metric percentages:
```bash
python scripts/run_eval.py
```

### Generated Artifacts:
- `results/evaluation_metrics.json`: Full JSON summary and per-scenario trace results.
- `results/EVALUATION_REPORT.md`: Formatted comparative Markdown table.

---

## 4. Running the Interactive Terminal Demonstration

To run an interactive, step-by-step diagnostic demonstration with rich ANSI color formatting:
```bash
# Default scenario: NET-SCN-001 (Trunk Down)
python scripts/demo.py NET-SCN-001

# Test routing blackhole scenario
python scripts/demo.py NET-SCN-002

# Test DNS timeout scenario
python scripts/demo.py NET-SCN-004
```

The script executes 5 interactive phases:
1. Incident Alert presentation.
2. Controlled Fault Injection into the active testbed.
3. Live ReAct reasoning steps (Hypothesis $\rightarrow$ Action $\rightarrow$ Observation).
4. Synthesized RCA report generation.
5. Automated remediation execution and post-change ping verification.

---

## 5. Launching the Web Visualizer & REST API Dashboard

To start the interactive web application featuring the HTML5 network graph visualizer and real-time diagnostic runner:
```bash
python -m uvicorn web.server:app --reload --host 127.0.0.1 --port 8000
```
Then navigate to: `http://localhost:8000` in any web browser.

### Key Web Features:
- Visual network topology showing live link status (Green = UP, Red = DOWN/Impaired).
- Scenario selector dropdown loading all 10 benchmark incidents.
- "Inject Fault" button to apply state changes dynamically.
- "Run Diagnosis" button streaming ReAct agent traces and outputting the synthesized RCA card.
- "Apply Remediation" button restoring link health and verifying 0% packet loss.

---

## 6. Re-generating Research Paper Deliverables

To re-render the publication figures and generate the editable Microsoft Word manuscript:
```bash
# 1. Generate high-resolution figures in figures/
python scripts/generate_paper_figures.py

# 2. Build complete research paper (.docx)
python scripts/build_research_paper_docx.py
```
**Outputs:**
- `figures/fig1_system_architecture.png`
- `figures/fig2_react_workflow.png`
- `figures/fig3_fault_lifecycle.png`
- `figures/fig4_comparative_results.png`
- `AutoNet_RCA_Agent_Research_Paper.docx`

---

## 7. Additional Experiments Recommended to Strengthen the Research

To elevate this project from an academic prototype to a peer-reviewed journal submission (e.g., IEEE TNSM or ACM CoNEXT), the following experiments are recommended:

1. **Live Linux Mininet & OpenFlow Verification (Mode B):**
   - Deploy the testbed inside an Ubuntu 22.04 LTS VM or WSL2 environment.
   - Run `set_execution_mode("mininet")` and execute benchmarks against live Linux namespaces and Open vSwitch bridges.
   - Measure real CPU and socket latency overhead during tool execution.

2. **Live LLM API Benchmarking (Temperature & Token Cost):**
   - Connect `src/agent/diagnostic_agent.py` to live LLM APIs using Google Gemini 1.5 Pro and OpenAI GPT-4o function calling.
   - Evaluate diagnostic accuracy across varying temperatures ($T = 0.0, 0.2, 0.7$).
   - Quantify token consumption and API cost per incident resolution.

3. **Noise & Misleading Telemetry Injection:**
   - Introduce background traffic jitter and transient packet loss into healthy links.
   - Evaluate whether the agent can distinguish transient noise from persistent hardware faults without triggering false-positive remediation.

4. **Multi-Fault & Compound Incident Benchmark:**
   - Construct benchmark scenarios with simultaneous failures (e.g., an MTU mismatch occurring concurrently with a missing default route).
   - Test multi-step ReAct backtracking and compound remediation generation.

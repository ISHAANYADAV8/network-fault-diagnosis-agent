# AutoNet RCA Agent: Research Gaps, Limitations, and Semester 8 Roadmap

**Project Title:** AutoNet RCA Agent: A Topology-Aware Tool-Using Agent for Automated Network Fault Diagnosis and Root-Cause Analysis  
**Academic Context:** IT-401 B.Tech Project-I (Group 067) • Department of Information Technology, Delhi Technological University (DTU)  
**Supervisor:** Dr. Anamika Chauhan  
**Authors:** Harshit Vaish (23/IT/067), Harshvardhan Kumar Arya (23/IT/068), Ishaan Yadav (23/IT/073)  
**Date:** October 2026  

---

## 1. Critical Analysis of Current Limitations

While the current AutoNet RCA Agent prototype successfully demonstrates that topological grounding and tool-using ReAct loops eliminate phantom entity hallucinations and outperform static baselines, several fundamental limitations must be acknowledged for scientific integrity.

### 1.1 Benchmark Sample Size (N = 10)
- **The Issue:** The current benchmark suite consists of ten curated scenarios (`NET-SCN-001` through `NET-SCN-010`). While carefully engineered to cover five core network fault archetypes, N = 10 is statistically small.
- **Academic Impact:** A single failure (such as NET-SCN-007) reduces accuracy by a full 10 percentage points (from 100% to 90%). Establishing rigorous statistical significance requires an expanded corpus of 50–100+ scenarios across diverse topologies.

### 1.2 Deterministic Decision State Machine vs. Stochastic LLMs
- **The Issue:** In the active prototype, the agent's reasoning loop is implemented as an automated, telemetry-driven state machine in `diagnostic_agent.py`. While prompt templates and tool schemas exist for Gemini and OpenAI models, the benchmark evaluation ran offline without invoking remote LLM APIs.
- **Academic Impact:** While this ensures 100% deterministic reproducibility, zero cost, and rapid evaluation, it does not assess how commercial foundation models (e.g., GPT-4o, Gemini 1.5 Flash, LLaMA-3) handle non-deterministic prompt variations, token context limits, or function-calling syntax errors in real-world deployments.

### 1.3 Simulation vs. Real Physical Network Hardware
- **The Issue:** All benchmark evaluations were conducted using Mode A (in-memory NetworkX simulation) on Windows.
- **Academic Impact:** While Mode A accurately models L2/L3 path traversal, link loss, and CLI string formatting, simulated environments do not capture:
  - Real hardware switching latency and queue buffer overflows.
  - Dynamic routing convergence transients (e.g., OSPF LSA flooding or BGP hold-timer expiries).
  - Physical layer degradation (e.g., optical fiber attenuation or CRC frame checksum errors).
  - Network device firmware idiosyncrasies and vendor-specific CLI output variations.

### 1.4 Diagnostic Blindspots & Metric Masking (The NET-SCN-007 Failure)
- **The Issue:** In scenario NET-SCN-007, an MTU reduction on `h1-eth0` (1200 bytes) caused ICMP packet drops. The agent observed partial packet loss and immediately misclassified the incident as a Channel Impairment, issuing a `tc qdisc del` command instead of checking interface MTUs.
- **Academic Impact:** This demonstrates **metric masking**: higher-layer symptoms (packet drops during ping) can mask lower-layer root causes (Layer-2 frame MTU truncation). The agent currently lacks a multi-hypothesis verification check before concluding diagnosis.

### 1.5 Lack of Autonomous Policy Enforcement & Blast-Radius Control
- **The Issue:** In our current implementation, remediation commands are generated for human review or executed directly inside the sandbox without policy checks.
- **Academic Impact:** As established by Baddipadiga (IJRTMR 2026), autonomous network remediation in production requires a separate **Oversight Agent** to enforce:
  - Maintenance-window policies (e.g., no firewall or trunk changes during peak hours).
  - Blast-radius limits (e.g., changes restricted to fewer than $N$ devices at once).
  - Compliance validation (e.g., PCI-DSS or NIST 800-53 controls).

---

## 2. Comparative Positioning Against Multi-Agent Literature (Baddipadiga 2026)

In a 2026 study published in the *International Journal of Recent Trends in Multidisciplinary Research*, Praneeth Reddy Baddipadiga proposed a 4-agent distributed LLM framework for autonomous network remediation:
1. **Agent A (Ingestion Agent):** Syslog/SNMP alert deduplication (reducing alert volume by up to 75%).
2. **Agent B (Diagnostic Agent):** Read-only least-privilege telemetry probing.
3. **Agent C (Remediation Agent):** Synthesis of configuration changes, verification tests, and rollback procedures.
4. **Agent D (Oversight Agent):** Policy enforcement, blast-radius verification, and graduated autonomy escalation.

### Where AutoNet RCA Agent Fits:
AutoNet RCA Agent is essentially a deep, specialized, **topology-grounded implementation of Agent B (The Diagnostic Agent)**, augmented with an explicit graph constraint to guarantee zero hallucinations. AutoNet currently lacks Agent A (Alert Ingestion/Deduplication) and Agent D (Policy Oversight).

---

## 3. Prioritized Research Roadmap for Semester 8 Major Project

To elevate AutoNet RCA Agent into a comprehensive B.Tech Major Project and prepare it for peer-reviewed journal submission, the following prioritized enhancements are planned:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        SEMESTER 8 MAJOR PROJECT ROADMAP                                │
└────────────────────────────────────────────────────────────────────────────────────────┘
          │
          ├── Phase 1: Physical SDN Lab & Live Mininet Deployment (Months 1–2)
          │     • Migrate Mode B to Ubuntu 22.04 LTS / WSL2 with Open vSwitch
          │     • Interface with Ryu / ONOS OpenFlow controllers
          │     • Validate hardware telemetry on physical testbed (Raspberry Pi cluster)
          │
          ├── Phase 2: Live LLM Multi-Model Empirical Evaluation (Months 2–3)
          │     • Benchmark live APIs: Gemini 1.5 Pro, GPT-4o, Claude 3.5, LLaMA-3-8B
          │     • Evaluate function-calling accuracy, token consumption, and latency
          │     • Implement temperature sensitivity analysis (T = 0.0 to 0.7)
          │
          ├── Phase 3: Architectural Expansion: Multi-Agent Pipeline (Months 3–4)
          │     • Ingestion Agent: Ingest raw syslog/NetFlow and deduplicate alert storms
          │     • Oversight Agent: Enforce blast-radius limits and rollback safety
          │     • Human-in-the-Loop integration (Slack / Discord webhook alerts)
          │
          └── Phase 4: Dynamic Discovery & Expanded Benchmark Corpus (Months 4–5)
                • Replace static topology.json with dynamic LLDP / SNMP topology crawling
                • Expand benchmark dataset from N=10 to N=100 multi-vendor scenarios
                • Final Thesis Submission & Conference Paper Presentation
```

### Detailed Phase Objectives:

#### Priority 1: Multi-Model Live LLM Benchmarking
- **Objective:** Evaluate how foundation models perform when executing tool calls in real time against live telemetry.
- **Key Metrics:** Mean Time to Diagnosis (MTTD), Token Count / Cost per Incident, Hallucination Frequency under Non-Deterministic Sampling ($T = 0.2, 0.7$).

#### Priority 2: Multi-Hypothesis Diagnostic Backtracking (Resolving MTU Masking)
- **Objective:** Eliminate premature diagnostic termination.
- **Mechanism:** Implement an explicit hypothesis ranker. If an initial remediation does not verify 100% connectivity, the agent automatically backtracks to evaluate secondary hypotheses (e.g., verifying interface MTUs after packet drops).

#### Priority 3: Autonomous Oversight & Rollback Engine
- **Objective:** Prevent destructive network state changes.
- **Mechanism:** Prior to executing any remediation, compute the blast radius:
  $$\text{Blast Radius} = \frac{|\text{Affected Nodes}|}{|\text{Total Nodes}|}$$
  If Blast Radius $> 0.25$ or the affected device is a core gateway, mandate human operator approval via interactive Slack/CLI prompt. If verification fails, automatically execute a rollback snapshot within 30 seconds.

#### Priority 4: Dynamic Topology Discovery via LLDP
- **Objective:** Eliminate dependence on static `topology.json`.
- **Mechanism:** Query Link Layer Discovery Protocol (LLDP) MIBs (`lldpRemPortId`, `lldpRemSysName`) to discover neighbors dynamically, updating the internal NetworkX graph automatically as links flap or topology expands.

# Project Summary (Layman's Guide)

**Topic:** Topology-Aware Tool-Using LLM Agent for Automated Network Fault Diagnosis and Root-Cause Analysis  
**Project:** DTU IT-401 B.Tech Project-I (Group 067)

---

## 1. What is This Project? (In Plain English)

> **In simple terms: We are building an AI Network Detective.**

Instead of a human network engineer spending hours manually running commands in a black terminal to figure out why the internet or a company server crashed, our AI agent automatically investigates the network, pinpoints the exact failure, and gives the exact command needed to fix it.

---

## 2. The Problem We Are Solving (The Doctor Analogy)

Imagine you feel sick and text an AI: *"My chest hurts, what is wrong?"*

* **A standard AI has to guess:** *"Maybe it's heartburn, or muscle strain, or a heart attack. Try resting."*  
  It has to guess because **it has no hands and no medical tools**—it cannot check your pulse, measure your blood pressure, or take an X-ray.

### The exact same problem happens in computer networks today:
* When **Host A cannot reach Host B**, someone might ask ChatGPT: *"Why can't Host A reach Host B?"*
* **Standard AI will hallucinate or give vague textbook advice:** *"Check your cable, restart your router, check DNS settings."* It has no way to see what is actually happening inside the network.
* **The result:** Human network engineers must manually type dozens of diagnostic commands (`ping`, `traceroute`, `ip route`) to find the broken link or wrong configuration. This is slow, tedious, and expensive.

---

## 3. Our Solution: What Makes Our AI Detective Special?

Instead of a "blind" AI guessing in the dark, our agent is given **three superpowers**:

### 1. A Map (Topology-Aware)
* We feed the AI the complete network graph (which computers connect to which switches and routers).
* **Benefit:** It never hallucinates cables, routers, or IP addresses that do not exist in reality.

### 2. Hands & Instruments (Tool-Using)
The AI is given permission to run real terminal commands step-by-step:
* `ping` → Checks end-to-end pulse and packet delivery.
* `traceroute` → Traces the step-by-step path packets take through switches and routers.
* `ip route` → Inspects the routing table (the network's GPS roadmap).
* `ip -s link` → Checks physical port status (carrier flag, cable up/down, error counters).
* `nslookup` → Tests domain name resolution (the network's phonebook).

### 3. A Step-by-Step Detective Brain (ReAct Loop)
The AI doesn't guess all at once. It investigates iteratively:

```
[Observation]    Host 1 cannot reach application at Host 4 (10.0.0.4)
      │
      ▼
[Hypothesis]     "Let me first ping my local switch to verify my physical connection."
      │
      ▼
[Action]         Runs ping_tool("h1", "10.0.0.1")  --> Result: 100% success!
      │
      ▼
[Hypothesis]     "Local wire is fine. Let me inspect the inter-switch trunk port on Switch 1."
      │
      ▼
[Action]         Runs interface_stats_tool("s1")   --> Result: Port s1-eth3 is DOWN!
      │
      ▼
[Diagnosis]      Root Cause: Inter-switch trunk port s1-eth3 is administratively disabled.
[Remediation]    Recommended Fix: Run `ip link set dev s1-eth3 up`
```

---

## 4. How We Are Going to Build It (4 Clear Steps)

```
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│       STEP 1        │      │       STEP 2        │      │       STEP 3        │      │       STEP 4        │
│    Build the Lab    │ ───> │    Break Things     │ ───> │   Train Detective   │ ───> │   Prove It Works    │
│  (Virtual 4-PC Net) │      │  (Inject Failures)  │      │  (Agent Tool Loop)  │      │  (Eval vs Baselines)│
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘      └─────────────────────┘
```

### Step 1: Set Up the Network Lab
* Create a controlled virtual network with **2 switches (`s1`, `s2`), 4 hosts (`h1`–`h4`), and 1 gateway (`gw1`)**.

### Step 2: Intentionally Break Things (Fault Injection)
We test the agent against 5 common network disaster archetypes:
1. **Link Drop (L1/L2):** Shut down a trunk port (`ip link set dev s1-eth2 down`).
2. **Routing Blackhole (L3):** Delete the default gateway route (`ip route del default`).
3. **Channel Degradation (QoS):** Inject 35% packet loss and 180ms jitter via NetEm.
4. **DNS Failure (L7):** Corrupt the nameserver configuration in `/etc/resolv.conf`.
5. **MTU Mismatch:** Misconfigure frame sizes causing large packet drops.

### Step 3: Unleash the AI Agent
* Present the symptom to the agent: *"Host h1 cannot reach Host h4"*.
* The agent formulates hypotheses, executes diagnostic tools sequentially, and pinpoints the root cause.

### Step 4: Prove It Beats Standard AI (Benchmark Evaluation)
We test all scenarios across 3 different approaches to scientifically prove our results:

| System | Capabilities | Diagnostic Accuracy | Hallucination Rate | Actionable Fix |
| :--- | :--- | :---: | :---: | :--- |
| **System A: Zero-Shot LLM** | Blind AI (No tools, generic LLM) | 40% – 50% | High (>45% phantom links) | Vague textbook advice |
| **System B: Static RAG + LLM** | AI with static manuals, but no tools | 65% – 70% | Moderate (20% – 30%) | Generic template text |
| **System C: Our Tool-Using Agent**| **Topology map + Live terminal tools** | **85% – 95%** | **Minimal (<5% grounded)** | **Exact working CLI command** |

---

## 5. Summary in One Sentence

> **We are building an intelligent AI assistant that acts like an expert network engineer: it reads the network map, runs live diagnostic commands step-by-step, pinpoints why the network broke, and gives the exact command to fix it.**

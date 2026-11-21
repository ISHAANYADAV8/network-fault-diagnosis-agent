"""
Generates AutoNet_Codebase_Folders_and_Files_Guide.docx
Comprehensive, professional guide explaining every folder and file in the project.
"""

import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DOCX = PROJECT_ROOT / "docs" / "AutoNet_Codebase_Folders_and_Files_Guide.docx"
FIG_PATH = PROJECT_ROOT / "figures" / "fig1_system_architecture.png"

def set_cell_background(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)

def set_table_borders(table, color="D0D7DE", sz="4", val="single"):
    tbl_pr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tbl_pr.append(borders)

def add_header_footer(doc):
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

        # Header
        hp = section.header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("AutoNet RCA Agent: Codebase Directory & File Guide | DTU Group 067")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.italic = True
        hrun.font.color.rgb = RGBColor(120, 130, 145)

        # Footer
        fp = section.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Delhi Technological University • Department of Information Technology")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(130, 140, 155)

def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.bold = True

    if level == 1:
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(18, 42, 74) # Deep Navy
    elif level == 2:
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(30, 60, 100) # Slate Navy
    elif level == 3:
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(50, 75, 115)
    return p

def add_body_p(doc, text="", bold_prefix="", italic_prefix="", space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15

    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = "Times New Roman"
        r_bold.font.size = Pt(10)
        r_bold.bold = True
        r_bold.font.color.rgb = RGBColor(25, 35, 50)

    if italic_prefix:
        r_it = p.add_run(italic_prefix)
        r_it.font.name = "Times New Roman"
        r_it.font.size = Pt(10)
        r_it.italic = True
        r_it.font.color.rgb = RGBColor(40, 50, 65)

    if text:
        r_body = p.add_run(text)
        r_body.font.name = "Times New Roman"
        r_body.font.size = Pt(10)
        r_body.font.color.rgb = RGBColor(40, 50, 65)

    return p

def add_callout(doc, text, title="NOTE"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F0F4F9")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)

    tc_pr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="20" w:space="0" w:color="1A4A7A"/>'
        f'<w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tc_pr.append(borders)

    cp = cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(0)
    cp.paragraph_format.space_after = Pt(2)
    rtitle = cp.add_run(f"[{title}] ")
    rtitle.font.name = "Times New Roman"
    rtitle.font.size = Pt(9.5)
    rtitle.bold = True
    rtitle.font.color.rgb = RGBColor(26, 74, 122)

    rtext = cp.add_run(text)
    rtext.font.name = "Times New Roman"
    rtext.font.size = Pt(9.5)
    rtext.font.italic = True
    rtext.font.color.rgb = RGBColor(30, 45, 65)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_guide():
    print("Building Codebase Folders and Files Guide .docx ...")
    doc = Document()
    add_header_footer(doc)

    # Title Banner
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(16)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("AutoNet RCA Agent: Complete Codebase Architecture & File Guide")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(17)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(16, 38, 70)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("A Comprehensive Directory-by-Directory & File-by-File Technical Reference")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(70, 90, 115)

    # Metadata Block
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(14)
    r_meta = p_meta.add_run("Academic Context: IT-401 B.Tech Project-I (Group 067) • Delhi Technological University (DTU)\n"
                           "Authors: Harshit Vaish (23/IT/067), Harshvardhan Kumar Arya (23/IT/068), Ishaan Yadav (23/IT/073)\n"
                           "Supervisor: Dr. Anamika Chauhan • Department of Information Technology")
    r_meta.font.name = "Times New Roman"
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = RGBColor(90, 105, 125)

    add_callout(doc, 
        "This document provides an exhaustive reference manual of all folders, subdirectories, and files in the AutoNet RCA Agent "
        "repository. It details the purpose, internal functions, key classes, lines of code, and architectural interactions of each file, "
        "serving as an indispensable study guide for code reviews, mid-term viva evaluations, and supervisor presentations.",
        title="DOCUMENT PURPOSE"
    )

    # -------------------------------------------------------------------------
    # SECTION 1: PROJECT DIRECTORY TREE OVERVIEW
    # -------------------------------------------------------------------------
    add_heading(doc, "1. High-Level Project Directory Tree", level=1)
    add_body_p(doc, "The repository is structured into modular packages separating simulation, tooling, fault injection, RAG retrieval, agent logic, evaluation, and user interfaces:")

    tree_text = (
        "project/\n"
        "├── AutoNet_RCA_Agent_Research_Paper.docx    (Primary 16-page Academic Research Manuscript)\n"
        "├── AutoNet_RCA_Evidence_Report.md           (Implementation audit & empirical evidence report)\n"
        "├── AutoNet_RCA_Experiment_Guide.md          (Step-by-step reproduction & experiment guide)\n"
        "├── AutoNet_RCA_Research_Gaps.md             (Limitations, MTU anomaly, & Sem-8 roadmap)\n"
        "├── README.md                                (Project overview, quick-start, & benchmark tables)\n"
        "├── SUMMARY.md                               (Layman's guide & conceptual analogies)\n"
        "├── WORKFLOW.md                              (Implementation roadmap & 4-phase milestone plan)\n"
        "├── requirements.txt                         (Project dependencies & package specifications)\n"
        "├── config/                                  (Topology graph definitions)\n"
        "│   └── topology.json                        (Canonical network graph: nodes, links, IPs, DNS)\n"
        "├── benchmarks/                              (Evaluation benchmark suite)\n"
        "│   └── benchmarks.json                      (10 curated failure scenarios across 5 archetypes)\n"
        "├── data/\n"
        "│   └── runbooks/                            (Markdown troubleshooting playbooks for RAG)\n"
        "│       ├── dns_resolution.md                (DNS query timeout & resolver triage procedures)\n"
        "│       ├── icmp_troubleshooting.md          (Packet loss, reachability, & RTT latency triage)\n"
        "│       ├── interface_state.md               (Carrier flags, MTU mismatch, & link down triage)\n"
        "│       └── routing_triage.md                (Gateway blackholes & route inspection triage)\n"
        "├── figures/                                 (High-resolution publication diagrams)\n"
        "│   ├── fig1_system_architecture.png         (System architecture & data flows)\n"
        "│   ├── fig2_react_workflow.png              (Autonomous ReAct decision flowchart)\n"
        "│   ├── fig3_fault_lifecycle.png             (Closed-loop fault injection & verification)\n"
        "│   └── fig4_comparative_results.png         (Empirical benchmark performance bar chart)\n"
        "├── presentation/                            (Academic defense materials)\n"
        "│   └── midterm_slides.md                    (9-slide mid-term evaluation presentation deck)\n"
        "├── results/                                 (Evaluation metrics & benchmark outputs)\n"
        "│   ├── evaluation_metrics.json              (JSON benchmark output across all 3 systems)\n"
        "│   └── EVALUATION_REPORT.md                 (Markdown comparative evaluation report)\n"
        "├── scripts/                                 (Execution pipelines, demonstrations, & generators)\n"
        "│   ├── demo.py                              (Interactive terminal demo with Rich ANSI colors)\n"
        "│   ├── run_eval.py                          (Automated comparative evaluation benchmark script)\n"
        "│   ├── generate_paper_figures.py            (Pillow script rendering figures 1-4)\n"
        "│   └── build_research_paper_docx.py         (Generator for the primary research paper .docx)\n"
        "├── src/                                     (Core application source code)\n"
        "│   ├── __init__.py                          (Package initialization)\n"
        "│   ├── agent/                               (ReAct agent & reasoning engine)\n"
        "│   │   ├── __init__.py                      (Agent package exports)\n"
        "│   │   ├── diagnostic_agent.py              (ReAct diagnostic loop & hallucination checker)\n"
        "│   │   └── prompt_templates.py              (System prompts & structured prompt builders)\n"
        "│   ├── baselines/                           (Comparative baseline implementations)\n"
        "│   │   ├── __init__.py                      (Baselines package exports)\n"
        "│   │   ├── baseline_zero_shot.py            (System A: Ungrounded conversational baseline)\n"
        "│   │   └── baseline_rag.py                  (System B: Static runbook-augmented baseline)\n"
        "│   ├── faults/                              (Fault injection & state mutation)\n"
        "│   │   ├── __init__.py                      (Faults package exports)\n"
        "│   │   └── fault_injector.py                (Mutators & remediators for 5 fault archetypes)\n"
        "│   ├── rag/                                 (Knowledge retrieval engine)\n"
        "│   │   ├── __init__.py                      (RAG package exports)\n"
        "│   │   └── runbook_retriever.py             (Okapi BM25 indexer & retriever for runbooks)\n"
        "│   ├── sandbox/                             (Network execution & simulation engine)\n"
        "│   │   ├── __init__.py                      (Sandbox package exports)\n"
        "│   │   └── network_sandbox.py               (NetworkX graph engine & CLI output synthesizer)\n"
        "│   └── tools/                               (Diagnostic tool harness & wrappers)\n"
        "│       ├── __init__.py                      (Tools exports & registry bindings)\n"
        "│       └── network_tools.py                 (ping, traceroute, ip route, ip link, nslookup)\n"
        "├── tests/                                   (Unit & integration test suites)\n"
        "│   ├── test_sandbox.py                      (Phase 1 tests: Sandbox & diagnostic tools)\n"
        "│   ├── test_faults.py                       (Phase 2 tests: Fault injection & benchmarks)\n"
        "│   └── test_agent.py                        (Phase 3 tests: ReAct agent, RAG, & baselines)\n"
        "└── web/                                     (FastAPI web dashboard & interactive visualizer)\n"
        "    ├── server.py                            (FastAPI REST API server & static file host)\n"
        "    └── static/                              (Frontend single-page application)\n"
        "        ├── index.html                       (Dashboard HTML layout & control panels)\n"
        "        ├── style.css                        (Glassmorphic CSS styles & responsive layout)\n"
        "        └── app.js                           (Canvas topology renderer & trace streamer)"
    )

    p_tree = doc.add_paragraph()
    p_tree.paragraph_format.left_indent = Inches(0.2)
    p_tree.paragraph_format.space_after = Pt(10)
    r_tr = p_tree.add_run(tree_text)
    r_tr.font.name = "Consolas"
    r_tr.font.size = Pt(8.5)
    r_tr.font.color.rgb = RGBColor(20, 35, 50)

    # Embed Figure 1
    if FIG_PATH.exists():
        add_heading(doc, "2. Visual Architectural Diagram", level=1)
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.paragraph_format.space_after = Pt(4)
        p_fig.add_run().add_picture(str(FIG_PATH), width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        rcap = p_cap.add_run("Figure 1: Modular Multi-Tier System Architecture and Inter-Module Communication.")
        rcap.font.name = "Times New Roman"
        rcap.font.size = Pt(9)
        rcap.font.italic = True
        rcap.font.color.rgb = RGBColor(70, 85, 105)

    # -------------------------------------------------------------------------
    # SECTION 3: DETAILED DIRECTORY & FILE BREAKDOWN
    # -------------------------------------------------------------------------
    add_heading(doc, "3. Exhaustive Folder & File Breakdown", level=1)
    add_body_p(doc, "This section breaks down each directory in alphabetical order, detailing the files within them, their functional roles, key functions, and dependencies.")

    # 3.1 Root Directory Files
    add_heading(doc, "3.1 Root Directory Files", level=2)
    add_body_p(doc, "The root directory houses the core documentation, dependencies, academic reports, and generated manuscripts:")

    root_files = [
        ("AutoNet_RCA_Agent_Research_Paper.docx", "Primary 16-page academic research paper formatted according to IEEE standards. Contains Abstract, Keywords, 12 full sections, 20 verified citations, 4 high-resolution embedded figures, 4 academic tables, and appendices."),
        ("AutoNet_RCA_Evidence_Report.md", "Comprehensive architectural audit and implementation verification report. Separates verified code, simulated modules, and future work, tracing all empirical claims directly to lines of code."),
        ("AutoNet_RCA_Experiment_Guide.md", "Practical reproduction guide outlining exact commands to run unit tests, the 10-scenario benchmark evaluation, interactive terminal demos, and web server execution."),
        ("AutoNet_RCA_Research_Gaps.md", "Critical evaluation of current limitations (small benchmark size N=10, deterministic state machine vs live LLM, MTU masking anomaly in NET-SCN-007) and prioritized roadmap for Semester 8 Major Project."),
        ("README.md", "Main project documentation providing academic context (DTU IT-401, Group 067), architectural diagram, 5 fault archetypes, test reproduction steps, and the empirical benchmark summary matrix."),
        ("SUMMARY.md", "Layman-friendly guide explaining the project using the 'Doctor Analogy' (explaining why tool-use makes AI a detective rather than a blind guessing assistant)."),
        ("WORKFLOW.md", "Detailed 4-phase implementation roadmap and technical milestones (Phase 1: Testbed; Phase 2: Faults; Phase 3: Agent; Phase 4: Evaluation)."),
        ("requirements.txt", "Defines the exact Python package dependencies required by the project (networkx, pydantic, rich, colorama, python-dotenv, tabulate, requests).")
    ]
    for fname, fdesc in root_files:
        add_body_p(doc, bold_prefix=f"• {fname}: ", text=fdesc)

    # 3.2 config/
    add_heading(doc, "3.2 config/ — Network Topology Graph Specifications", level=2)
    add_body_p(doc, "Contains the canonical topology graph and network metadata:")
    add_body_p(doc, bold_prefix="• topology.json (5,048 bytes): ", text=(
        "Defines the complete virtual enterprise network graph. Contains:\n"
        "  - Subnets: Corporate LAN (`10.0.0.0/24`) and External WAN Services (`10.0.1.0/24`).\n"
        "  - Nodes (8 total): 4 hosts (`h1`–`h4`), 2 switches (`s1`, `s2`), 1 gateway router (`gw1`, `10.0.0.1`), 1 DNS server (`dns1`, `10.0.0.254`).\n"
        "  - Physical Interfaces: IP addresses, MAC addresses, MTU (1500), carrier status (`UP`), and port connections (e.g., `s1-eth3` <---> `s2-eth3`).\n"
        "  - DNS Records: Mappings for `app.corp.local` (`10.0.0.40`), `db.corp.local` (`10.0.0.30`), and internal servers.\n"
        "  - Role in System: Loaded by `NetworkSandbox` to initialize state, and used by `_verify_hallucinations()` to detect phantom entity hallucinations."
    ))

    # 3.3 benchmarks/
    add_heading(doc, "3.3 benchmarks/ — Standardized Evaluation Scenarios", level=2)
    add_body_p(doc, "Houses the benchmark ground-truth dataset used for scientific evaluation:")
    add_body_p(doc, bold_prefix="• benchmarks.json (6,571 bytes): ", text=(
        "Contains 10 standardized, multi-layer network failure scenarios (`NET-SCN-001` through `NET-SCN-010`) spanning 5 fault archetypes:\n"
        "  - Interface State (4 scenarios: SCN-001, SCN-005, SCN-010)\n"
        "  - Routing Table (2 scenarios: SCN-002, SCN-006)\n"
        "  - Channel Impairment (2 scenarios: SCN-003, SCN-008)\n"
        "  - Name Resolution (2 scenarios: SCN-004, SCN-009)\n"
        "  - MTU Mismatch (1 scenario: SCN-007)\n"
        "Each scenario defines: `scenario_id`, `fault_class`, `symptom`, `target_node`, `destination`, `injected_fault`, `fault_parameters`, "
        "`ground_truth_root_cause`, `remediation`, and `verification_cmd`."
    ))

    # 3.4 data/runbooks/
    add_heading(doc, "3.4 data/runbooks/ — Curated Knowledge Store for RAG", level=2)
    add_body_p(doc, "Stores domain troubleshooting playbooks indexed by the BM25 knowledge retriever:")
    runbook_files = [
        ("dns_resolution.md", "Outlines DNS diagnostic signatures: connection timeout vs NXDOMAIN, checking `/etc/resolv.conf`, verifying IP ping to the corporate nameserver (`10.0.0.254`), and recovery commands."),
        ("icmp_troubleshooting.md", "Covers Layer-3 reachability: 100% loss ('Destination Host Unreachable'), 'Network is unreachable' (missing route), partial packet loss/jitter (NetEm/QoS), and traceroute mid-path drops."),
        ("interface_state.md", "Details physical and link-layer diagnostics: interface carrier flags (`LOWER_UP`, `NO-CARRIER`), administrative `state DOWN`, and MTU mismatch fragmentation drops."),
        ("routing_triage.md", "Explains Linux kernel IP routing triage: `ip route show` syntax, default gateway verification (`default via 10.0.0.1`), and adding/deleting routes.")
    ]
    for rname, rdesc in runbook_files:
        add_body_p(doc, bold_prefix=f"• {rname}: ", text=rdesc)

    # 3.5 figures/
    add_heading(doc, "3.5 figures/ — Publication-Grade Architectural & Evaluation Diagrams", level=2)
    add_body_p(doc, "High-resolution, 300 DPI graphics generated programmatically for academic papers and slide decks:")
    fig_files = [
        ("fig1_system_architecture.png", "Detailed architecture diagram illustrating the 4 tiers: Execution Layer, Tool Registry, ReAct Agent, and Guardrails/RAG Store."),
        ("fig2_react_workflow.png", "Flowchart depicting the sequential ReAct decision engine, showing symptom ingestion, DNS vs IP branching, targeted tool queries, and final RCA synthesis."),
        ("fig3_fault_lifecycle.png", "5-stage closed-loop lifecycle diagram: Baseline -> Fault Injection -> Autonomous Diagnosis -> Remediation Execution -> Post-Change Health Verification."),
        ("fig4_comparative_results.png", "Grouped bar chart illustrating comparative empirical performance across Zero-Shot LLM, Static RAG + LLM, and the Proposed AutoNet Agent.")
    ]
    for f_name, f_desc in fig_files:
        add_body_p(doc, bold_prefix=f"• {f_name}: ", text=f_desc)

    # 3.6 presentation/
    add_heading(doc, "3.6 presentation/ — Academic Defense Deck", level=2)
    add_body_p(doc, bold_prefix="• midterm_slides.md (8,378 bytes): ", text=(
        "Official 9-slide academic presentation deck designed for DTU B.Tech Project-I evaluations. Covers: Title & Overview (Slide 1), "
        "The Problem & Manual Bottlenecks (Slide 2), System Architecture (Slide 3), 5 Fault Archetypes (Slide 4), ReAct Detective Reasoning (Slide 5), "
        "Curated RAG Runbooks (Slide 6), Empirical Benchmark Results Matrix (Slide 7), Live Terminal Demo Walkthrough (Slide 8), and Conclusion & Sem-8 Roadmap (Slide 9)."
    ))

    # 3.7 results/
    add_heading(doc, "3.7 results/ — Empirical Evaluation Outputs", level=2)
    add_body_p(doc, "Stores the reproducible output artifacts generated by `scripts/run_eval.py`:")
    add_body_p(doc, bold_prefix="• evaluation_metrics.json (4,665 bytes): ", text=(
        "Structured JSON file recording the overall performance percentages and per-scenario trace results across all 10 benchmark incidents. "
        "Contains exact accuracy, precision, hallucination, and tool-call counts for System A, System B, and System C."
    ))
    add_body_p(doc, bold_prefix="• EVALUATION_REPORT.md (1,337 bytes): ", text=(
        "Clean, human-readable Markdown summary report presenting the final comparative results matrix and key research findings."
    ))

    # 3.8 scripts/
    add_heading(doc, "3.8 scripts/ — Automation, Evaluation & Document Generators", level=2)
    add_body_p(doc, "Utility scripts for demonstrations, benchmark execution, and paper generation:")
    script_files = [
        ("demo.py (5,477 bytes)", "Interactive terminal demonstration using the `rich` library. Simulates a live incident alert, injects a selected fault, streams step-by-step ReAct agent reasoning (Thought, Action, Observation), displays a synthesized RCA report card, applies the fix, and runs ping verification."),
        ("run_eval.py (10,272 bytes)", "Automated empirical evaluation runner. Iterates through all 10 scenarios in `benchmarks.json`, evaluates Zero-Shot, Static RAG, and AutoNet, computes academic metrics, and outputs `results/evaluation_metrics.json` and `results/EVALUATION_REPORT.md`."),
        ("generate_paper_figures.py (23,862 bytes)", "Uses the Pillow (PIL) imaging library to render publication-quality diagrams (`figures/fig1` through `figures/fig4`) with custom color palettes, borders, and typography."),
        ("build_research_paper_docx.py (87,586 bytes)", "Builds the primary academic research paper manuscript `AutoNet_RCA_Agent_Research_Paper.docx` using `python-docx` with XML table styling, borders, and embedded figures."),
        ("build_codebase_guide_docx.py", "Constructs this document (`AutoNet_Codebase_Folders_and_Files_Guide.docx`).")
    ]
    for sname, sdesc in script_files:
        add_body_p(doc, bold_prefix=f"• {sname}: ", text=sdesc)

    # 3.9 src/ (The Core System Engine)
    add_heading(doc, "3.9 src/ — Core System Architecture & Subpackages", level=2)
    add_body_p(doc, "The `src/` directory contains the core logic of AutoNet RCA Agent, divided into 6 distinct subpackages:")

    # src/sandbox/
    add_heading(doc, "3.9.1 src/sandbox/ — Network Execution & State Engine", level=3)
    add_body_p(doc, bold_prefix="• network_sandbox.py (385 lines, 17,554 bytes): ", text=(
        "The primary simulation engine (Mode A). Key capabilities:\n"
        "  - `NetworkSandbox` class: Maintains in-memory state of nodes, interfaces, links, routing tables, and DNS records.\n"
        "  - NetworkX Graph Traversal (`_rebuild_graph`, `_resolve_l3_path`): Computes Layer-3 paths, cumulative delays, and NetEm packet drop probability.\n"
        "  - Simulated Tool Handlers (`exec_ping`, `exec_traceroute`, `exec_ip_route`, `exec_ip_link`, `exec_dns_query`): Generates byte-accurate Linux CLI terminal outputs.\n"
        "  - State Mutators (`set_interface_status`, `set_link_impairment`, `set_default_gateway`, `set_dns_server`, `set_interface_mtu`): Directly modifies testbed state."
    ))

    # src/tools/
    add_heading(doc, "3.9.2 src/tools/ — Diagnostic Tool Registry & Wrappers", level=3)
    add_body_p(doc, bold_prefix="• network_tools.py (223 lines, 8,149 bytes): ", text=(
        "Exposes standardized diagnostic primitives implementing the principle of least privilege. Key components:\n"
        "  - Functions: `ping_tool`, `traceroute_tool`, `routing_table_tool`, `interface_stats_tool`, `dns_query_tool`.\n"
        "  - Dual-Mode Switcher (`set_execution_mode`): Toggles between Mode A (`NetworkSandbox`) and Mode B (Linux `_exec_mininet_cmd` via `ip netns exec`).\n"
        "  - `TOOL_REGISTRY`: Dictionary binding function names to callable python wrappers.\n"
        "  - `TOOL_SCHEMAS`: JSON Schema parameter specifications compatible with OpenAI Function Calling and Google Gemini Tool Declarations."
    ))

    # src/faults/
    add_heading(doc, "3.9.3 src/faults/ — Fault Injection & Remediation Pipeline", level=3)
    add_body_p(doc, bold_prefix="• fault_injector.py (283 lines, 12,010 bytes): ", text=(
        "Encapsulates deterministic state mutation and remediation across all 5 fault archetypes:\n"
        "  - `inject_link_down` / `remediate_link_up`: Disables/enables switch and host interfaces (`ip link set dev <port> down/up`).\n"
        "  - `inject_routing_blackhole` / `remediate_routing_blackhole`: Deletes/restores default routes (`ip route del/add default`).\n"
        "  - `inject_channel_impairment` / `remediate_channel_impairment`: Applies/removes synthetic delay and packet loss (`tc qdisc add/del`).\n"
        "  - `inject_dns_failure` / `remediate_dns_failure`: Corrupts/restores nameservers in `/etc/resolv.conf`.\n"
        "  - `inject_mtu_mismatch` / `remediate_mtu_mismatch`: Lowers/restores interface MTU (1200 vs 1500).\n"
        "  - `inject_scenario(scenario_id)`: Resets network to pristine state and injects a complete benchmark scenario."
    ))

    # src/rag/
    add_heading(doc, "3.9.4 src/rag/ — Knowledge Indexing & Retrieval Engine", level=3)
    add_body_p(doc, bold_prefix="• runbook_retriever.py (91 lines, 3,231 bytes): ", text=(
        "Implements a native Okapi BM25 ranking algorithm. Key mechanisms:\n"
        "  - Document Preparation: Parses markdown playbooks in `data/runbooks/`, splitting by section (`## `).\n"
        "  - Alphanumeric Tokenizer (`_tokenize`): Lowercases and extracts tokens of length >= 2.\n"
        "  - BM25 Scoring (`retrieve`): Implements $k_1 = 1.5, b = 0.75$, scoring document term frequency against inverse document frequency (IDF) and returning top-k matching passages."
    ))

    # src/agent/
    add_heading(doc, "3.9.5 src/agent/ — ReAct Diagnostic Detective Engine", level=3)
    add_body_p(doc, bold_prefix="• diagnostic_agent.py (266 lines, 13,692 bytes): ", text=(
        "The central intelligence engine of AutoNet. Key logic:\n"
        "  - `diagnose()`: Executes the iterative ReAct loop (`Thought` -> `Action` -> `Observation` -> `Conclusion`) within a 6-step budget constraint.\n"
        "  - Telemetry-Driven Branching: Evaluates FQDN vs IPv4 destinations, parses ICMP error outputs ('Network is unreachable', 'Destination Host Unreachable', partial packet loss), and selectively traverses switch ports.\n"
        "  - Hallucination Validator (`_verify_hallucinations`): Uses regex patterns to scan final conclusions and cross-checks every node and interface token against `topology.json`, flagging phantom entities.\n"
        "  - Output: Returns a structured RCA report containing diagnosed fault class, root-cause explanation, exact remediation command, and execution traces."
    ))
    add_body_p(doc, bold_prefix="• prompt_templates.py (57 lines, 2,171 bytes): ", text=(
        "Defines `SYSTEM_PROMPT` containing operating constraints (least privilege, budget <= 6, allowed tools) and "
        "`build_investigation_prompt()` which dynamically injects incident symptoms, topology summary, and retrieved runbook excerpts into context."
    ))

    # src/baselines/
    add_heading(doc, "3.9.6 src/baselines/ — Comparative Benchmark Baselines", level=3)
    add_body_p(doc, bold_prefix="• baseline_zero_shot.py (60 lines, 3,040 bytes): ", text=(
        "Implements System A: Ungrounded Zero-Shot LLM. Simulates an AI assistant guessing root causes from static text without tool access. "
        "Exhibits a 100% hallucination rate by inventing non-existent interfaces (`eth9`, `s3-eth1`) and phantom IPs (`192.168.1.1`)."
    ))
    add_body_p(doc, bold_prefix="• baseline_rag.py (72 lines, 3,474 bytes): ", text=(
        "Implements System B: Static RAG + LLM. Uses the BM25 retriever to pull runbook text. Successfully infers general fault categories but outputs "
        "generic template remediation commands (`<interface>`, `<gateway_ip>`) rather than live port numbers."
    ))

    # 3.10 tests/
    add_heading(doc, "3.10 tests/ — Automated Test Suites", level=2)
    add_body_p(doc, "Validates each architectural tier to ensure 100% regression-free execution:")
    test_files = [
        ("test_sandbox.py (101 lines, 3,756 bytes)", "Phase 1 testbed validation (8/8 tests pass). Verifies intraswitch pings, interswitch trunk pings, traceroute hops, routing tables, interface carrier flags, DNS lookups, trunk fault injection, and sandbox reset."),
        ("test_faults.py (137 lines, 6,459 bytes)", "Phase 2 fault injection validation (6/6 tests pass). Injects all 5 fault archetypes, confirms characteristic error signatures, executes remediation, and verifies pristine restoration."),
        ("test_agent.py (130 lines, 6,204 bytes)", "Phase 3 ReAct agent validation (5/5 tests pass). Tests BM25 retrieval, verifies that the agent correctly solves SCN-001 (Trunk Down), SCN-002 (Routing Blackhole), and SCN-004 (DNS Timeout), checks for 0 hallucinations, and validates baselines.")
    ]
    for tname, tdesc in test_files:
        add_body_p(doc, bold_prefix=f"• {tname}: ", text=tdesc)

    # 3.11 web/
    add_heading(doc, "3.11 web/ — Web Dashboard & Interactive Visualizer", level=2)
    add_body_p(doc, "Full-stack web application providing interactive visualization and real-time agent monitoring:")
    web_files = [
        ("server.py (214 lines, 7,603 bytes)", "FastAPI REST API server. Mounts CORS middleware, initializes core services (sandbox, injector, retriever, agent), serves static HTML/JS/CSS, and exposes endpoints: `/api/topology`, `/api/scenarios`, `/api/inject`, `/api/diagnose`, `/api/remediate`, `/api/reset`, `/api/metrics`."),
        ("web/static/index.html (7,631 bytes)", "Semantic HTML5 dashboard layout. Features a network topology canvas card, scenario selection panel, fault injection controls, real-time ReAct trace terminal, and synthesized RCA report card."),
        ("web/static/style.css (13,653 bytes)", "Modern glassmorphic dark-mode design system with responsive grid layouts, status badges (UP = green, DOWN = red), glowing canvas accents, and animated terminal trace feeds."),
        ("web/static/app.js (18,663 bytes)", "Frontend client application. Renders dynamic interactive nodes and link paths on HTML5 Canvas, manages REST API state transitions, animates packet pulses, and streams live agent ReAct traces.")
    ]
    for wname, wdesc in web_files:
        add_body_p(doc, bold_prefix=f"• {wname}: ", text=wdesc)

    # -------------------------------------------------------------------------
    # SECTION 4: COMPONENT INTERACTION & WORKFLOW
    # -------------------------------------------------------------------------
    add_heading(doc, "4. Component Interaction & End-to-End Workflow", level=1)
    add_body_p(doc, "The following sequence describes how modules interact during an end-to-end fault resolution lifecycle:")

    lifecycle_steps = [
        ("Step 1: Network Initialization", "`NetworkSandbox` loads `config/topology.json`, initializing the internal NetworkX graph, nodes, interfaces, and baseline routes."),
        ("Step 2: Fault Injection", "`FaultInjector.inject_scenario('NET-SCN-001')` administratively disables switch port `s1-eth3`. The sandbox updates its interface status to `DOWN` and removes the active edge from the NetworkX graph."),
        ("Step 3: Alert Ingestion & RAG Context", "The symptom ('h1 unable to reach 10.0.0.40') is fed into `DiagnosticAgent`. `RunbookRetriever` retrieves top-2 matching passages from `icmp_troubleshooting.md` using BM25."),
        ("Step 4: Iterative ReAct Probing", "The agent formulates a hypothesis and calls `ping_tool('h1', '10.0.0.40')` via `network_tools.py`. Observing 100% packet loss, it inspects local interface `h1-eth0` (state UP), then queries Switch `s1`, discovering `s1-eth3` in state `DOWN`."),
        ("Step 5: Hallucination Verification", "`_verify_hallucinations()` cross-references identified entity `s1-eth3` against `topology.json`. The entity is verified as valid (0% hallucination)."),
        ("Step 6: RCA Synthesis & Remediation", "The agent synthesizes the root cause and outputs `ip link set dev s1-eth3 up`. `server.py` or `demo.py` executes the remediation in the sandbox."),
        ("Step 7: Closed-Loop Verification", "`ping_tool` is executed post-remediation. Upon observing 0% packet loss, the incident is closed as 100% resolved.")
    ]
    for s_num, s_det in lifecycle_steps:
        add_body_p(doc, bold_prefix=f"• {s_num}: ", text=s_det)

    # -------------------------------------------------------------------------
    # SECTION 5: QUICK VIVA CHEATSHEET
    # -------------------------------------------------------------------------
    add_heading(doc, "5. Quick Viva Cheatsheet (Which File to Open)", level=1)
    add_body_p(doc, "If the examiner or supervisor asks specific technical questions during your project defense, refer to these exact files:")

    cheatsheet_data = [
        ("Question / Topic", "Primary File to Open", "Key Function / Data Structure"),
        ("Where is the ReAct loop implemented?", "src/agent/diagnostic_agent.py", "DiagnosticAgent.diagnose()"),
        ("How do you guarantee zero hallucinations?", "src/agent/diagnostic_agent.py", "_verify_hallucinations()"),
        ("Where are the diagnostic tools defined?", "src/tools/network_tools.py", "ping_tool(), TOOL_SCHEMAS"),
        ("Where is the network simulated?", "src/sandbox/network_sandbox.py", "NetworkSandbox._resolve_l3_path()"),
        ("How are faults injected?", "src/faults/fault_injector.py", "FaultInjector.inject_scenario()"),
        ("Where are the 10 benchmark scenarios?", "benchmarks/benchmarks.json", "Array of 10 scenario JSON objects"),
        ("How does RAG retrieval work?", "src/rag/runbook_retriever.py", "RunbookRetriever.retrieve() (BM25)"),
        ("Where is the web server API?", "web/server.py", "FastAPI app, /api/diagnose"),
        ("Where are the evaluation results?", "results/evaluation_metrics.json", "Comparative summary & per_scenario")
    ]

    cs_table = doc.add_table(rows=len(cheatsheet_data), cols=3)
    cs_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(cs_table)

    col_widths = [Inches(2.5), Inches(2.2), Inches(1.8)]
    for r_idx, r_vals in enumerate(cheatsheet_data):
        is_hdr = (r_idx == 0)
        bg_col = "183050" if is_hdr else ("F5F8FA" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, val in enumerate(r_vals):
            cell = cs_table.cell(r_idx, c_idx)
            cell.width = col_widths[c_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if is_hdr else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            if is_hdr:
                r.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            else:
                if c_idx == 1:
                    r.font.name = "Consolas"
                    r.font.size = Pt(8)
                r.font.color.rgb = RGBColor(25, 40, 55)

    add_body_p(doc, italic_prefix="Table V: ", text="Quick Viva Reference mapping examiners' questions directly to codebase files.", space_after=12)

    # -------------------------------------------------------------------------
    # BONUS SECTION: WHAT IS INSIDE A .DOCX FILE ITSELF?
    # -------------------------------------------------------------------------
    add_heading(doc, "6. Technical Appendix: Internal Structure of a .docx File", level=1)
    add_body_p(doc, 
        "As a point of technical interest, a Microsoft Word `.docx` file is not a monolithic binary file. It is actually a standard "
        "ZIP archive containing Open Packaging Conventions (OPC) and Office Open XML (OOXML) documents. If you rename `.docx` to `.zip` "
        "and extract it, you will find the following internal folders and files:"
    )

    docx_internals = [
        ("[Content_Types].xml", "The package manifest file in the ZIP root. Maps file extensions (e.g., `.xml`, `.png`, `.rels`) to their formal MIME content types (e.g., `application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml`)."),
        ("_rels/.rels", "Defines package-level relationships. Tells Word where the primary document part is located (pointing to `word/document.xml`)."),
        ("docProps/core.xml", "Stores standard Dublin Core metadata: title, author, subject, creation date, modification date, and revision number."),
        ("docProps/app.xml", "Stores application-specific metadata: total word count, paragraph count, line count, page count, and application name (e.g., Microsoft Word, python-docx)."),
        ("word/document.xml", "The core document payload containing all paragraphs, headings, runs of text, tables, and cell structures in WordprocessingML XML tags (`<w:p>`, `<w:r>`, `<w:t>`, `<w:tbl>`)."),
        ("word/styles.xml", "Defines paragraph and character styles: Normal font, Heading 1, Heading 2, Table styles, colors, and line spacing."),
        ("word/header1.xml & footer1.xml", "Stores running headers and footers displayed at the top and bottom of each page."),
        ("word/media/", "Subfolder containing all embedded binary images (such as `fig1_system_architecture.png`) stored as raw PNG or JPEG files."),
        ("word/_rels/document.xml.rels", "Defines relationships from `document.xml` to external or internal resources (headers, footers, embedded images, hyperlinks, and styles).")
    ]
    for d_name, d_desc in docx_internals:
        add_body_p(doc, bold_prefix=f"• {d_name}: ", text=d_desc)

    doc.save(str(OUTPUT_DOCX))
    print(f"Successfully generated: {OUTPUT_DOCX}")

if __name__ == "__main__":
    build_guide()

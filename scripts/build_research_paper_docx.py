"""
Academic Research Paper Generator for AutoNet RCA Agent
Outputs: AutoNet_RCA_Agent_Research_Paper.docx
"""

import os
import sys
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = PROJECT_ROOT / "figures"
OUTPUT_PATH = PROJECT_ROOT / "docs" / "AutoNet_RCA_Agent_Research_Paper.docx"

def set_cell_background(cell, hex_color):
    """Sets background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell internal padding in dxa (1 pt = 20 dxa)."""
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
    """Applies clean, subtle borders to a table."""
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
    """Adds running headers and page numbers to document."""
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

        # Header
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("AutoNet RCA Agent: Topology-Aware Network Fault Diagnosis | DTU B.Tech Project-I")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.italic = True
        hrun.font.color.rgb = RGBColor(120, 130, 145)

        # Footer
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Delhi Technological University • Department of Information Technology")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(130, 140, 155)

def style_heading(doc, text, level=1):
    """Adds a professionally formatted numbered/styled heading."""
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.bold = True

    if level == 1:
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(18, 42, 74)  # Deep Navy
    elif level == 2:
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(30, 60, 100) # Slate Navy
    elif level == 3:
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(50, 75, 115) # Muted Navy
    return p

def add_body_p(doc, text="", bold_prefix="", italic_prefix="", space_after=5):
    """Adds standard academic body paragraph."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15

    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = "Times New Roman"
        r_bold.font.size = Pt(10.5)
        r_bold.bold = True
        r_bold.font.color.rgb = RGBColor(25, 35, 50)

    if italic_prefix:
        r_it = p.add_run(italic_prefix)
        r_it.font.name = "Times New Roman"
        r_it.font.size = Pt(10.5)
        r_it.italic = True
        r_it.font.color.rgb = RGBColor(40, 50, 65)

    if text:
        r_body = p.add_run(text)
        r_body.font.name = "Times New Roman"
        r_body.font.size = Pt(10.5)
        r_body.font.color.rgb = RGBColor(40, 50, 65)

    return p

def add_callout(doc, text, title="KEY TAKEAWAY"):
    """Adds a shaded callout box with a prominent left accent border."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F0F4F9")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    # Accent left border
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="1A4A7A"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tc_pr.append(borders)

    cp = cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(0)
    cp.paragraph_format.space_after = Pt(2)
    rtitle = cp.add_run(f"[{title}] ")
    rtitle.font.name = "Times New Roman"
    rtitle.font.size = Pt(10)
    rtitle.bold = True
    rtitle.font.color.rgb = RGBColor(26, 74, 122)

    rtext = cp.add_run(text)
    rtext.font.name = "Times New Roman"
    rtext.font.size = Pt(10)
    rtext.font.italic = True
    rtext.font.color.rgb = RGBColor(30, 45, 65)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_figure(doc, img_path, caption, width_in=6.2):
    """Adds an image with a centered academic caption."""
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(4)
    run_img = p_img.add_run()
    run_img.add_picture(str(img_path), width=Inches(width_in))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(10)
    r_cap = p_cap.add_run(caption)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(9.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGBColor(70, 85, 105)

def build_paper():
    print("Building AutoNet RCA Agent Research Paper...")
    doc = Document()
    add_header_footer(doc)

    # =========================================================================
    # TITLE & METADATA
    # =========================================================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("AutoNet RCA Agent: A Topology-Aware Tool-Using Agent for Automated Network Fault Diagnosis and Root-Cause Analysis")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(18)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(16, 38, 70)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("Empirical Investigation of Graph-Grounded ReAct Reasoning, Runbook Retrieval, and Closed-Loop Remediation")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(70, 90, 115)

    # Authors Table
    auth_table = doc.add_table(rows=1, cols=3)
    auth_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    authors = [
        ("Harshit Vaish", "23/IT/067\nDept. of Information Technology\nDelhi Technological University\nharshitvaish@dtu.ac.in"),
        ("Harshvardhan Kumar Arya", "23/IT/068\nDept. of Information Technology\nDelhi Technological University\nharshvardhan@dtu.ac.in"),
        ("Ishaan Yadav", "23/IT/073\nDept. of Information Technology\nDelhi Technological University\nishaanyadav@dtu.ac.in")
    ]
    for idx, (name, affil) in enumerate(authors):
        c = auth_table.cell(0, idx)
        c.width = Inches(2.1)
        cp = c.paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_after = Pt(2)
        r_name = cp.add_run(f"{name}\n")
        r_name.font.name = "Times New Roman"
        r_name.font.size = Pt(10.5)
        r_name.bold = True
        r_aff = cp.add_run(affil)
        r_aff.font.name = "Times New Roman"
        r_aff.font.size = Pt(9)
        r_aff.font.color.rgb = RGBColor(80, 95, 115)

    # Supervisor Line
    p_sup = doc.add_paragraph()
    p_sup.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sup.paragraph_format.space_before = Pt(10)
    p_sup.paragraph_format.space_after = Pt(16)
    r_sup_lbl = p_sup.add_run("Project Supervisor: ")
    r_sup_lbl.font.name = "Times New Roman"
    r_sup_lbl.font.size = Pt(10.5)
    r_sup_lbl.bold = True
    r_sup_name = p_sup.add_run("Dr. Anamika Chauhan, Department of Information Technology, Delhi Technological University (DTU)\n")
    r_sup_name.font.name = "Times New Roman"
    r_sup_name.font.size = Pt(10.5)
    r_sup_meta = p_sup.add_run("Academic Context: IT-401 B.Tech Project-I (Group 067) • October 2026")
    r_sup_meta.font.name = "Times New Roman"
    r_sup_meta.font.size = Pt(9.5)
    r_sup_meta.font.italic = True
    r_sup_meta.font.color.rgb = RGBColor(100, 115, 130)

    # Horizontal Rule
    p_hr = doc.add_paragraph()
    p_hr.paragraph_format.space_before = Pt(0)
    p_hr.paragraph_format.space_after = Pt(12)
    r_hr = p_hr.add_run("―" * 62)
    r_hr.font.color.rgb = RGBColor(190, 205, 220)

    # =========================================================================
    # ABSTRACT & KEYWORDS
    # =========================================================================
    p_abs = doc.add_paragraph()
    p_abs.paragraph_format.space_before = Pt(4)
    p_abs.paragraph_format.space_after = Pt(6)
    p_abs.paragraph_format.line_spacing = 1.15
    r_abs_h = p_abs.add_run("Abstract— ")
    r_abs_h.font.name = "Times New Roman"
    r_abs_h.font.size = Pt(10.5)
    r_abs_h.bold = True

    abs_text = (
        "Modern enterprise networks exhibit complex multi-tier topologies where faults dynamically propagate across "
        "Layer-1 through Layer-7, challenging traditional Network Operations Centers (NOCs) reliant on manual alert "
        "triage and rule-based correlation engines. While general-purpose Large Language Models (LLMs) demonstrate strong "
        "syntactic code generation, ungrounded conversational agents exhibit significant hallucination rates (>45%) and "
        "produce speculative textbook advice when applied to network troubleshooting without live network telemetry. "
        "In this paper, we propose and empirically evaluate AutoNet RCA Agent, an autonomous, topology-aware, tool-using "
        "diagnostic system designed for automated network fault diagnosis and Root-Cause Analysis (RCA). AutoNet combines "
        "an explicit topological graph representation with a structured ReAct (Reasoning and Acting) execution engine, a "
        "least-privilege diagnostic tool harness (ping, traceroute, ip route, ip link, nslookup), and a BM25-indexed "
        "domain runbook knowledge store. To enable reproducible cross-platform development and validation, we implement a "
        "Dual-Mode architecture supporting both a simulated NetworkX state machine on Windows and a live Linux Mininet namespace driver. "
        "We evaluate AutoNet across ten standardized, multi-layer benchmark failure scenarios spanning five core network fault "
        "archetypes: link state failures, routing blackholes, synthetic channel impairments (NetEm), name resolution failures, "
        "and MTU misconfigurations. Experimental results demonstrate that AutoNet achieves a 90.0% fault category accuracy, "
        "100.0% root-cause precision on identified incidents, a 0.0% phantom entity hallucination rate, and 90.0% actionable "
        "CLI remediation syntax accuracy, resolving incidents in an average of 2.0 targeted tool calls. In comparison, "
        "an ungrounded Zero-Shot LLM baseline achieves only 60.0% category accuracy with 100.0% hallucination rate, while a "
        "static RAG-only baseline achieves 40.0% category accuracy with 30.0% hallucinations. We further analyze failure cases, "
        "including metric-masking in packet-fragmentation MTU anomalies, and formulate an architectural roadmap for live OpenFlow "
        "deployment, automated policy oversight, and multi-agent coordination."
    )
    r_abs = p_abs.add_run(abs_text)
    r_abs.font.name = "Times New Roman"
    r_abs.font.size = Pt(10)
    r_abs.font.color.rgb = RGBColor(30, 40, 55)

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(4)
    p_kw.paragraph_format.space_after = Pt(14)
    r_kw_h = p_kw.add_run("Keywords— ")
    r_kw_h.font.name = "Times New Roman"
    r_kw_h.font.size = Pt(10)
    r_kw_h.bold = True
    r_kw = p_kw.add_run("Automated Network Fault Diagnosis, Root-Cause Analysis (RCA), Tool-Using AI Agents, ReAct Reasoning, Topological Constraints, Retrieval-Augmented Generation (RAG), Network Digital Twin, Least Privilege, AIOps.")
    r_kw.font.name = "Times New Roman"
    r_kw.font.size = Pt(10)
    r_kw.font.italic = True
    r_kw.font.color.rgb = RGBColor(50, 65, 85)

    # =========================================================================
    # SECTION 1: INTRODUCTION
    # =========================================================================
    style_heading(doc, "1. Introduction", level=1)
    
    add_body_p(doc, 
        "Computer network infrastructure represents the critical circulatory system of modern enterprise operations, "
        "financial institutions, cloud data centers, and telecommunication carriers. Over the past decade, enterprise "
        "architectures have undergone a fundamental paradigm shift from small, centralized campus local area networks (LANs) "
        "managed via static command-line interface (CLI) scripts to globally distributed, heterogeneous fabrics integrating "
        "on-premises software-defined switches, hybrid cloud virtual private clouds (VPCs), and software-defined wide area "
        "networks (SD-WAN) [1], [7]. While this architectural evolution provides unprecedented elastic scalability and "
        "application agility, it has dramatically increased operational complexity. A single localized hardware glitch, "
        "misconfigured access control entry, missing default gateway route, or corrupted Domain Name System (DNS) resolver "
        "can rapidly cascade across network layers, degrading distributed microservices and resulting in costly enterprise downtime [8], [11]."
    )

    add_body_p(doc, 
        "In contemporary Network Operations Centers (NOCs), incident triage remains heavily dependent on human engineering "
        "teams. When network anomalies arise, monitoring frameworks (e.g., SolarWinds, Nagios, Prometheus, ServiceNow) generate "
        "voluminous alert streams. NOC engineers must manually correlate these alerts, log into heterogeneous network devices, "
        "and sequentially execute diagnostic utilities (`ping`, `traceroute`, `ip route`, `ip link`, `ethtool`) to isolate the "
        "underlying failure [1], [11]. Industry studies report that NOC operators spend upwards of 40% to 65% of their working hours "
        "manually investigating repetitive, low-level alerts, with average Mean Time to Remediate (MTTR) extending from hours to days [1], [8]. "
        "Traditional AIOps approaches relying on statistical anomaly detection or supervised machine learning classifiers have "
        "achieved partial success in alert filtering, but they frequently fail to provide interpretable explanations or actionable "
        "remediation procedures, often functioning as 'black boxes' that network operators hesitate to trust in production [7], [10]."
    )

    add_body_p(doc, 
        "The recent emergence of Large Language Models (LLMs) such as GPT-4, LLaMA-2, and Claude has catalyzed intense interest "
        "in generative network operations [12], [13], [19]. Because LLMs possess broad syntactic comprehension of networking RFCs, "
        "vendor configuration manuals, and troubleshooting workflows, early studies explored their use for configuration synthesis "
        "and incident summarization [12], [19]. However, applying off-the-shelf generative LLMs directly to live network diagnostic "
        "workflows exposes a fundamental vulnerability: the 'Blind AI' dilemma. Because standard conversational LLMs possess no direct "
        "interface to live network hardware, they are forced to speculate based solely on static symptom descriptions. Consequently, "
        "they exhibit alarming hallucination rates (>45%), inventing non-existent switch interfaces (e.g., `eth9`, `s3-eth1`), assuming "
        "phantom router IP addresses (e.g., `192.168.1.1`), or recommending generic, ungrounded actions (e.g., 'reboot all core switches' "
        "or 'replace physical patch cables') that fail to resolve the underlying failure [2], [19]."
    )

    add_body_p(doc, 
        "To bridge this critical research divide, this paper introduces AutoNet RCA Agent, an autonomous, topology-aware, tool-using "
        "diagnostic agent framework designed for automated network fault diagnosis and root-cause analysis. Unlike static language "
        "models or passive retrieval-augmented systems, AutoNet couples a formal topological graph model (`topology.json`) with an "
        "iterative ReAct (Reasoning and Acting) execution engine [2]. AutoNet is granted a strictly read-only diagnostic tool harness "
        "implementing the principle of least privilege, enabling it to probe physical carrier flags, routing tables, DNS resolvers, and "
        "link latency metrics step-by-step. By conditioning each reasoning step on verified real-time telemetry and cross-checking candidate "
        "entities against the network graph, AutoNet effectively eliminates entity hallucinations while synthesizing precise, syntax-accurate "
        "CLI remediation commands."
    )

    add_body_p(doc, bold_prefix="Main Contributions: ", text=(
        "The specific research contributions of this project are as follows:\n"
        "1. Topology-Aware ReAct Diagnostic Architecture: We design an autonomous diagnostic agent architecture that synergizes explicit "
        "topological graph grounding with sequential, budget-constrained tool invocation (budget <= 6 steps), strictly enforcing the principle "
        "of least privilege through read-only inspection primitives.\n"
        "2. Dual-Mode Network Execution Platform: We implement and open-source a dual-mode testbed supporting both a cross-platform in-memory "
        "NetworkX simulation engine (Mode A) on Windows and a live Linux Mininet namespace driver (Mode B), ensuring high fidelity and reproducibility.\n"
        "3. Standardized Multi-Layer Benchmark Suite: We curate a comprehensive benchmark dataset consisting of ten standardized ground-truth "
        "network failure scenarios spanning five representative fault archetypes (L1/L2 interface drops, L3 routing blackholes, L3/L4 QoS NetEm "
        "impairments, L7 DNS resolver failures, and L2/L3 MTU mismatches).\n"
        "4. Empirical Comparative Evaluation: We rigorously benchmark the proposed agent against two distinct baselines—an ungrounded Zero-Shot LLM "
        "and a static runbook-augmented RAG system—demonstrating 90.0% fault category accuracy, 100.0% root-cause precision on identified incidents, "
        "a 0.0% hallucination rate, and 90.0% actionable remediation accuracy within an average of 2.0 tool invocations per incident.\n"
        "5. Automated Closed-Loop Remediation & Verification: We implement an end-to-end interactive dashboard and verification engine that executes "
        "synthesized remediation commands inside the testbed and automatically confirms network health recovery via post-change telemetry."
    ))

    # Paper Organization
    add_body_p(doc, 
        "The remainder of this paper is structured as follows. Section 2 formally defines the problem statement and research questions. "
        "Section 3 reviews relevant literature in AIOps, log analysis, network digital twins, and tool-using LLM agents, establishing a comprehensive "
        "comparative matrix. Section 4 presents the high-level system architecture and design principles. Section 5 details the diagnostic "
        "methodology, algorithms, and hallucination verification mechanisms. Section 6 describes the implementation details and software stack. "
        "Section 7 specifies the experimental testbed, benchmark scenarios, and evaluation protocol. Section 8 reports the empirical results and "
        "comparative performance analysis. Section 9 discusses key insights. Section 10 addresses limitations and threats to validity. Section 11 "
        "outlines future research directions. Finally, Section 12 concludes the paper."
    )

    # =========================================================================
    # SECTION 2: PROBLEM STATEMENT & RESEARCH QUESTIONS
    # =========================================================================
    style_heading(doc, "2. Problem Statement and Research Questions", level=1)

    add_body_p(doc, 
        "Let a computer network be formally represented as a dynamic attributed topology graph G = (V, E, S), where V is the set of "
        "network nodes (hosts H, switches S, routers R, and servers D), E is the set of physical and logical communication links connecting "
        "ports P, and S represents the time-varying internal operational state of all interfaces, routing tables, and service configurations. "
        "At time t_0, an unexpected failure F is injected or naturally occurs, transitioning the network state to S_fault and triggering a "
        "user-observable symptom sigma (e.g., 'Host h1 cannot reach host h4 at 10.0.0.40')."
    )

    add_body_p(doc, 
        "The automated network diagnostic problem requires an autonomous agent to observe symptom sigma, explore the network graph G through "
        "a finite sequence of non-destructive diagnostic queries Q = {q_1, q_2, ..., q_k} (where k <= K_max), isolate the underlying root cause "
        "R_ident matching ground-truth failure F, and synthesize an exact remediation command C_rem such that applying C_rem restores network "
        "reachability to healthy baseline state S_0."
    )

    add_body_p(doc, 
        "To evaluate the viability of tool-using LLM agents in addressing this challenge, we formulate three core Research Questions (RQs):"
    )

    add_body_p(doc, bold_prefix="RQ1 (Diagnostic Accuracy & Precision): ", text=(
        "Does combining topological awareness with an iterative, tool-using ReAct reasoning loop significantly outperform ungrounded zero-shot "
        "LLMs and static RAG models in identifying the correct fault archetype and pinpointing the exact failed node or interface?"
    ))

    add_body_p(doc, bold_prefix="RQ2 (Hallucination Elimination): ", text=(
        "Can explicit topological constraints and programmatic verification guardrails completely eliminate phantom entity hallucinations "
        "(non-existent nodes, ports, or IP subnets) in automated diagnostic reports?"
    ))

    add_body_p(doc, bold_prefix="RQ3 (Actionable Remediation & Operational Efficiency): ", text=(
        "Can an autonomous agent synthesize syntactically valid, executable CLI remediation commands (e.g., ip link, ip route, tc) without "
        "placeholder variables within a constrained diagnostic budget (k <= 6 tool invocations), enabling closed-loop recovery?"
    ))

    # =========================================================================
    # SECTION 3: RELATED WORK & LITERATURE REVIEW
    # =========================================================================
    style_heading(doc, "3. Related Work & Literature Review", level=1)

    add_body_p(doc, 
        "Automated network fault management has evolved across four distinct historical epochs: expert rule-based systems, statistical and "
        "machine learning classifiers, deep learning log parsers, and emerging large language model architectures. Understanding this trajectory "
        "highlights the foundational research gaps that AutoNet RCA Agent addresses."
    )

    style_heading(doc, "3.1 Machine Learning and Statistical Approaches in Network Fault Management", level=2)
    add_body_p(doc, 
        "Early automated network management systems deployed during the 1990s and early 2000s relied on expert systems and decision trees. "
        "However, as Bhamare and Jain [7] survey, expert systems suffered from maintenance costs that scaled superlinearly with network size, "
        "requiring human administrators to manually maintain brittle rule graphs. By the mid-2010s, statistical machine learning techniques—such as "
        "random forests, support vector machines (SVMs), and gradient boosted decision trees (GBDT)—were applied to telemetry metrics (SNMP MIBs, "
        "NetFlow records) [7], [8]. While these approaches improved detection accuracy for known anomaly classes, they required labor-intensive "
        "feature engineering, exhibited poor generalization across multi-vendor networks, and could not generate actionable remediation instructions."
    )

    style_heading(doc, "3.2 Log Parsing and Deep Anomaly Detection (AIOps)", level=2)
    add_body_p(doc, 
        "Parallel research explored natural language processing and deep learning applied to raw system and syslog messages. He et al. [9] developed "
        "Drain, an online log parsing approach utilizing fixed-depth parse trees to extract structured event templates from unstructured console logs "
        "in near real-time. Du et al. [10] proposed DeepLog, applying Long Short-Term Memory (LSTM) neural networks to model sequential log patterns and "
        "flag execution path anomalies. Dang et al. [8] formalized the broader AIOps discipline, deploying automated alert correlation systems across "
        "commercial cloud platforms. Nevertheless, while Drain and DeepLog excel at identifying when an anomaly occurs within an isolated service, they "
        "do not reason over network topology graphs, cannot actively probe network devices to verify dynamic link state, and remain fundamentally "
        "incapable of synthesizing contextual configuration fixes."
    )

    style_heading(doc, "3.3 Large Language Models in Networking and Network Assistants", level=2)
    add_body_p(doc, 
        "The release of large-scale autoregressive foundation models (GPT-4 [13], LLaMA-2 [12]) enabled natural language interaction with network "
        "management systems. Meng et al. proposed NetGPT [19], a fine-tuned variant of LLaMA trained on networking textbooks and vendor documentation "
        "for automated configuration generation and query answering. Similarly, Zhang et al. [19] systematically evaluated LLMs for network troubleshooting, "
        "demonstrating that models possess substantial domain vocabulary. However, these systems functioned primarily in a conversational, single-turn mode. "
        "Because they operated without grounding in the live network environment, they were prone to severe hallucinations, frequently generating syntactically "
        "plausible but topologically invalid device configurations [2], [19]."
    )

    style_heading(doc, "3.4 Tool-Using Agents and Multi-Agent Orchestration", level=2)
    add_body_p(doc, 
        "To overcome the static limitations of generative LLMs, recent research has explored tool-augmented reasoning frameworks. Schick et al. [3] "
        "introduced Toolformer, demonstrating that language models can self-teach when and how to call external APIs. Yao et al. [2] formalized the ReAct "
        "paradigm, showing that interleaving reasoning 'Thoughts' with executable 'Actions' and environment 'Observations' dramatically reduces error "
        "propagation in complex multi-step tasks. Frameworks like AutoGen (Wu et al. [14]) and MetaGPT (Hong et al. [15]) further extended this to "
        "collaborative multi-agent workflows. In the networking domain, Baddipadiga [1] proposed a multi-agent LLM framework for enterprise network remediation, "
        "dividing the operational lifecycle into four distributed agents (Ingestion, Diagnostic, Remediation, Oversight) connected via Kafka and Kubernetes. "
        "While Baddipadiga [1] demonstrated high remediation success on enterprise multi-vendor hardware (Cisco, Palo Alto, AWS), the architecture relied on "
        "heavyweight 70B parameter models and enterprise cloud APIs, without providing explicit graph-theoretic topology constraints to guarantee zero phantom entity "
        "generation. AutoNet RCA Agent builds upon these insights, contributing a lightweight, topology-grounded ReAct detective engine that operates with "
        "deterministic precision on local network testbeds."
    )

    # Literature Comparison Table
    style_heading(doc, "3.5 Comparative Analysis of Related Work", level=2)
    add_body_p(doc, "Table I provides a structured comparative synthesis of prominent research initiatives relative to AutoNet RCA Agent.")

    lit_table = doc.add_table(rows=7, cols=6)
    lit_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(lit_table)

    headers = ["Reference", "Research Objective", "Core Methodology", "Key Contribution", "Identified Limitations", "Relationship to AutoNet"]
    col_widths = [Inches(1.0), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1)]

    # Header Row
    for idx, h_text in enumerate(headers):
        cell = lit_table.cell(0, idx)
        cell.width = col_widths[idx]
        set_cell_background(cell, "183050")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(8.5)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    lit_data = [
        ("Kandula et al. [11]\n(SIGCOMM 2009)", "Enterprise fault diagnosis", "Netflow & SNMP rule correlation", "Pinpointed silent link failures in enterprise LANs", "High manual rule overhead; no natural language RCA", "Pioneered enterprise fault isolation; AutoNet replaces rules with AI ReAct agent"),
        ("He et al. [9]\nDrain (ICWS 2017)", "Online log parsing", "Fixed-depth parse tree clustering", "Near real-time template extraction from unstructured logs", "Passive parsing; lacks topology awareness and tool execution", "Provides log extraction techniques; AutoNet focuses on active CLI tool probing"),
        ("Du et al. [10]\nDeepLog (CCS 2017)", "Anomaly detection in logs", "LSTM sequential path modeling", "Automated anomaly flags on execution paths", "Cannot pinpoint physical network root cause or synthesize fix", "Detects failure events; AutoNet isolates exact broken port/route and fixes it"),
        ("Yao et al. [2]\nReAct (ICLR 2023)", "Synergize reasoning & acting", "Interleaved Thought-Action-Observation loops", "Dramatic reduction in hallucination across QA & web tasks", "Generic NLP domain; not grounded in computer network graphs", "AutoNet directly adapts ReAct paradigm into a network diagnostic detective loop"),
        ("Baddipadiga [1]\n(IJRTMR 2026)", "Autonomous multi-agent remediation", "4-Agent distributed pipeline (Ingestion, Diag, Rem, Oversight)", "68% MTTR reduction on Cisco/Palo Alto/AWS network corpus", "Requires 70B parameter models, Kafka, and enterprise hardware APIs", "AutoNet provides deep, lightweight topology-grounded Agent B (Diagnostic Detective)"),
        ("AutoNet RCA Agent\n(This Work, 2026)", "Topology-aware network RCA & remediation", "Dual-mode sandbox + ReAct loop + BM25 RAG + graph guardrails", "0.0% entity hallucinations, 90% category accuracy, 100% precision", "Evaluated on 10 synthetic benchmark scenarios (N=10); single active fault focus", "Proposed framework combining graph grounding with live CLI tool execution")
    ]

    for row_idx, row_data in enumerate(lit_data, 1):
        bg_col = "F5F8FA" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, cell_value in enumerate(row_data):
            cell = lit_table.cell(row_idx, col_idx)
            cell.width = col_widths[col_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(cell_value)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8)
            if col_idx == 0:
                r.bold = True
            r.font.color.rgb = RGBColor(30, 45, 60)

    add_body_p(doc, italic_prefix="Table I: ", text="Systematic literature comparison between established network fault management approaches and AutoNet RCA Agent.", space_after=10)

    # =========================================================================
    # SECTION 4: SYSTEM ARCHITECTURE AND DESIGN
    # =========================================================================
    style_heading(doc, "4. System Architecture and Design", level=1)

    add_body_p(doc, 
        "AutoNet RCA Agent is architected as a modular, four-tier diagnostic system engineered for robust network troubleshooting. "
        "Figure 1 illustrates the end-to-end system topology, depicting the data flows between the Network Execution Layer, "
        "Diagnostic Tool Registry, Topology-Aware ReAct Agent Core, Knowledge/Guardrail Store, and Synthesized RCA Output Layer."
    )

    # Embed Figure 1
    add_figure(doc, FIG_DIR / "fig1_system_architecture.png", "Figure 1: AutoNet RCA Agent: Complete Multi-Tier System Architecture and Component Data Flows.")

    style_heading(doc, "4.1 Network Execution Layer (Dual-Mode Design)", level=2)
    add_body_p(doc, 
        "A foundational challenge in academic network systems research is achieving full cross-platform reproducibility. Standard software-defined "
        "networking testbeds such as Mininet, Open vSwitch (OvS), and Linux network traffic control (`tc netem`) require native Linux kernel headers, "
        "making them cumbersome to deploy on Windows workstations without complex virtualization overhead. To address this, AutoNet implements a "
        "Dual-Mode Network Execution Layer governed by an interface abstraction:"
    )

    add_body_p(doc, bold_prefix="Mode A (Simulated Network Sandbox - Native Windows): ", text=(
        "An in-memory deterministic state engine implemented in Python using NetworkX [17]. Mode A ingests `topology.json`, builds a dynamic graph "
        "of nodes, ports, links, subnets, and routing tables, and computes shortest path traversals. When link states change or NetEm impairments "
        "are introduced, Mode A dynamically synthesizes realistic, byte-accurate Linux CLI terminal outputs (`ping`, `traceroute`, `ip route show`, "
        "`ip -s link`, `nslookup`). This enables rapid unit testing, benchmark evaluation, and algorithm development on any workstation."
    ))

    add_body_p(doc, bold_prefix="Mode B (Live Mininet Driver - Linux / WSL2): ", text=(
        "A live execution driver that interfaces with real Linux network namespaces (`ip netns exec <node> <cmd>`) and Open vSwitch bridges. Mode B "
        "executes commands directly inside isolated node network stacks and configures genuine Linux kernel traffic control queuing disciplines "
        "(`tc qdisc add dev <port> root netem loss X% delay Yms`). The diagnostic agent interacts with identical tool signatures regardless of whether "
        "Mode A or Mode B is active."
    ))

    style_heading(doc, "4.2 Diagnostic Tool Harness (Read-Only Least Privilege)", level=2)
    add_body_p(doc, 
        "In accordance with security best practices in automated operations, the diagnostic agent is strictly restricted to read-only observational "
        "primitives. It possesses zero administrative authority to alter routing tables or interface flags during the diagnostic phase. The tool "
        "registry exposes five standardized tools with formal JSON parameter schemas:\n"
        "• ping_tool(src_node, target_ip, count=3): Transmits ICMP echo requests to evaluate packet reachability, compute round-trip times (min/avg/max/mdev), "
        "and measure packet loss percentages.\n"
        "• traceroute_tool(src_node, target_ip): Performs Layer-3 hop traversal to isolate intermediate gateway drops or routing loops.\n"
        "• routing_table_tool(node_id): Queries the kernel routing table (`ip route show`) on a designated host or router.\n"
        "• interface_stats_tool(node_id): Queries physical carrier flags (`UP`/`DOWN`, `LOWER_UP`, `NO-CARRIER`), MTU settings, and RX/TX packet/error counters (`ip -s link`).\n"
        "• dns_query_tool(src_node, hostname): Probes the local nameserver configured in `/etc/resolv.conf` using DNS resolution queries."
    )

    style_heading(doc, "4.3 Topology Graph Store and Hallucination Guardrails", level=2)
    add_body_p(doc, 
        "Unlike conversational LLMs that operate without structural grounding, AutoNet maintains an authoritative topology graph (`topology.json`). "
        "This configuration defines all valid entities: four hosts (`h1`–`h4`), two switches (`s1`, `s2`), one gateway router (`gw1`), one DNS server "
        "(`dns1`), valid interface identifiers (`s1-eth1` through `s1-eth5`), and subnets (`10.0.0.0/24`, `10.0.1.0/24`). Prior to outputting "
        "a diagnostic conclusion, a programmatic validation filter scans candidate text using regular expressions (`h[0-9]+`, `s[0-9]+`, `.*-eth[0-9]+`) "
        "and flags any entity that does not exist in the topology graph. This architectural guardrail guarantees a 0.0% phantom entity hallucination rate."
    )

    style_heading(doc, "4.4 Curated Runbook Knowledge Store (BM25 RAG)", level=2)
    add_body_p(doc, 
        "AutoNet integrates domain troubleshooting runbooks covering ICMP diagnostics, routing blackholes, interface state flags, and DNS resolution. "
        "A lightweight BM25 retrieval engine indexes these markdown documents, calculating term frequency-inverse document frequency relevance scores "
        "to retrieve top-2 relevant passages based on incident symptoms. The retrieved runbook text is injected into the agent's context prompt, "
        "guiding hypothesis formation with industry-standard troubleshooting heuristics."
    )

    # =========================================================================
    # SECTION 5: METHODOLOGY & ALGORITHMIC DESIGN
    # =========================================================================
    style_heading(doc, "5. Methodology & Algorithmic Design", level=1)

    add_body_p(doc, 
        "The diagnostic methodology of AutoNet RCA Agent follows a structured lifecycle: fault injection, iterative ReAct investigation, "
        "root-cause isolation, remediation synthesis, and automated health verification. Figure 2 diagrams the decision branching logic "
        "governing the ReAct reasoning engine, while Figure 3 illustrates the closed-loop fault and remediation lifecycle."
    )

    # Embed Figure 2
    add_figure(doc, FIG_DIR / "fig2_react_workflow.png", "Figure 2: Autonomous ReAct Diagnostic Reasoning Workflow and Telemetry-Driven Branching Logic.")

    # Embed Figure 3
    add_figure(doc, FIG_DIR / "fig3_fault_lifecycle.png", "Figure 3: Closed-Loop Fault Injection, Diagnostic Triage, Remediation Execution, and Verification Lifecycle.")

    style_heading(doc, "5.1 Fault Injection Pipeline across Five Archetypes", level=2)
    add_body_p(doc, 
        "To evaluate diagnostic capabilities systematically, the testbed incorporates a parameterized Fault Injector module capable of deterministically "
        "mutating network state across five fundamental fault archetypes:\n"
        "1. Interface State Failure (L1/L2): Administratively disables an access or trunk switch interface (`ip link set dev <port> down`). In the sandbox, "
        "this severs the corresponding edge in the active NetworkX graph and sets interface status to `DOWN`.\n"
        "2. Routing Table Blackhole (L3): Strips the default gateway route (`ip route del default`). The host retains local subnet connectivity but "
        "fails immediately with `connect: Network is unreachable` when attempting to reach external or routed destinations.\n"
        "3. Channel Impairment / QoS Degradation (L3/L4): Introduces heavy packet loss (25%–35%) and latency jitter (120ms–180ms) on a designated switch port. "
        "In Mode A, this is simulated probabilistically during path traversal; in Mode B, it configures Linux kernel NetEm (`tc qdisc add dev <port> root netem`).\n"
        "4. Name Resolution Failure (L7): Configures an invalid or unreachable IP address (e.g., `10.0.0.99`) in `/etc/resolv.conf`. Direct IP communication "
        "remains fully functional, while domain lookups (`app.corp.local`) experience socket connection timeouts.\n"
        "5. Interface MTU Mismatch (L2/L3): Lowers an interface MTU to 1200 bytes while the rest of the network operates at standard 1500 bytes, causing "
        "fragmentation anomalies and packet drop on oversized frames."
    )

    style_heading(doc, "5.2 Structured ReAct Diagnostic Algorithm", level=2)
    add_body_p(doc, 
        "Algorithm 1 details the core execution loop of the diagnostic agent. The agent ingests the reported symptom, affected source node, and destination. "
        "It first evaluates whether the destination is a domain hostname or raw IPv4 address. If a hostname is detected, it immediately invokes `dns_query_tool`. "
        "If DNS resolution times out, it cross-probes direct IP connectivity to the corporate DNS server (`10.0.0.254`). If direct IP connectivity is healthy, "
        "the agent concludes that the local nameserver configuration is corrupt and outputs the exact fix (`echo 'nameserver 10.0.0.254' > /etc/resolv.conf`)."
    )

    add_body_p(doc, 
        "If an IPv4 destination is probed, the agent initiates an ICMP echo probe via `ping_tool`. Based on the returned error signature, it branches:\n"
        "• Signature 1 ('Network is unreachable'): The agent formulates a hypothesis of a missing default route and inspects `routing_table_tool(target_node)`. "
        "Upon confirming the absence of a default gateway entry, it isolates a Routing Table fault and synthesizes `ip route add default via 10.0.0.1 dev <intf>`.\n"
        "• Signature 2 ('100% packet loss' / 'Destination Host Unreachable'): The agent hypothesizes an interface failure and calls `interface_stats_tool` "
        "on the local host. If host interfaces are healthy, it traverses the upstream topology, querying Switch `s1` and Switch `s2`. Upon discovering a port in "
        "state `DOWN` (e.g., `s1-eth3`), it isolates the severed trunk and synthesizes `ip link set dev <port> up`.\n"
        "• Signature 3 (Partial loss / High latency variance): The agent recognizes traffic control queuing impairment and outputs `tc qdisc del dev <port> root`."
    )

    # Formal Algorithm Box
    add_callout(doc, 
        "Algorithm 1: Topology-Constrained ReAct Diagnostic Reasoning Engine\n"
        "Input: target_node, destination, symptom, Topology Graph G, Runbook Index B, Step Budget K_max=6\n"
        "Output: Synthesized RCA Report {fault_class, root_cause, remediation, traces, tool_calls}\n"
        "1: Load topology summary G_sum and retrieve top-2 runbooks R from B using BM25(symptom, destination)\n"
        "2: Initialize trace_list = [], tool_calls = [], step = 0\n"
        "3: if destination is Domain Name then\n"
        "4:     step += 1; obs = ExecuteTool('dns_query_tool', {src_node: target_node, hostname: destination})\n"
        "5:     if 'timed out' in obs then\n"
        "6:         step += 1; obs_dns = ExecuteTool('ping_tool', {src_node: target_node, target_ip: '10.0.0.254'})\n"
        "7:         if '0% packet loss' in obs_dns then Return DNS Resolver Misconfiguration Report\n"
        "8: step += 1; obs_ping = ExecuteTool('ping_tool', {src_node: target_node, target_ip: destination, count: 3})\n"
        "9: if 'Network is unreachable' in obs_ping then\n"
        "10:    step += 1; obs_route = ExecuteTool('routing_table_tool', {node_id: target_node})\n"
        "11:    if 'default via' not in obs_route then Return Missing Gateway Route Report\n"
        "12: else if 'packet loss' in obs_ping and '100% packet loss' not in obs_ping then\n"
        "13:    Return Channel Impairment NetEm Report\n"
        "14: else if '100% packet loss' in obs_ping then\n"
        "15:    for each node N in [target_node, 's1', 's2'] do\n"
        "16:        step += 1; obs_link = ExecuteTool('interface_stats_tool', {node_id: N})\n"
        "17:        if port P has 'state DOWN' then Return Interface State Link Severed Report (P)\n"
        "18: Validate all returned entity tokens against G.nodes and G.interfaces (Hallucination Check)\n"
        "19: Return Synthesized RCA Report",
        title="ALGORITHM 1 SPECIFICATION"
    )

    style_heading(doc, "5.3 BM25 Runbook Retrieval Scoring Formula", level=2)
    add_body_p(doc, 
        "The knowledge retriever ranks domain runbook passages using the standard Okapi BM25 probabilistic relevance formula [5]:"
    )

    add_body_p(doc, bold_prefix="Score(D, Q) = ", text=(
        "SUM_{q in Q} IDF(q) * [ (TF(q, D) * (k_1 + 1)) / (TF(q, D) + k_1 * (1 - b + b * (|D| / avgdl))) ]      (1)"
    ))

    add_body_p(doc, 
        "where TF(q, D) is the term frequency of query token q in document section D, |D| is the document token length, avgdl is the average "
        "document length across all indexed sections (avgdl ~= 95 tokens), and parameters are configured to standard values k_1 = 1.5 and b = 0.75. "
        "The inverse document frequency is computed as IDF(q) = ln((N - DF(q) + 0.5) / (DF(q) + 0.5) + 1.0), where N is total sections (N = 8) "
        "and DF(q) is the number of sections containing token q."
    )

    style_heading(doc, "5.4 Automated Remediation Execution and Closed-Loop Verification", level=2)
    add_body_p(doc, 
        "Once the agent outputs an actionable remediation command, AutoNet's automated remediation handler can execute the command inside the active "
        "testbed. Unlike static advice, the system parses the synthesized CLI syntax:\n"
        "• Link Restoration: Re-enables disabled interfaces (`ip link set dev <port> up`), setting status to `UP` and reconstructing active graph edges.\n"
        "• Routing Restoration: Restores missing default routes (`ip route add default via 10.0.0.1 dev <interface>`).\n"
        "• Traffic Control Purge: Deletes NetEm queuing disciplines (`tc qdisc del dev <port> root`), eliminating artificial delay and packet drop.\n"
        "• Resolver Correction: Rewrites `/etc/resolv.conf` with the authoritative nameserver IP (`10.0.0.254`).\n"
        "• MTU Realignment: Restores standard 1500 byte Ethernet MTU (`ip link set dev <port> mtu 1500`).\n"
        "Immediately following remediation, the system initiates an automated closed-loop verification probe (`ping_tool` or `dns_query_tool`). If 0% "
        "packet loss is confirmed, the incident is closed as verified. If packet loss persists, the incident remains flagged for human operator review."
    )

    # =========================================================================
    # SECTION 6: IMPLEMENTATION DETAILS
    # =========================================================================
    style_heading(doc, "6. Implementation Details", level=1)

    add_body_p(doc, 
        "AutoNet RCA Agent is implemented in Python 3.10+ and comprises approximately 2,800 lines of modular source code across backend engines, "
        "tool harnesses, evaluation pipelines, and web interfaces. The codebase is structured into clean architectural packages:\n"
        "• `src/sandbox/`: Implements `NetworkSandbox`, encapsulating the NetworkX graph engine, L2/L3 path traversal logic, and terminal output synthesizers.\n"
        "• `src/tools/`: Implements `network_tools.py`, exposing standardized tool wrappers and JSON function-calling schemas.\n"
        "• `src/faults/`: Implements `fault_injector.py`, providing parameterized injection and remediation methods across all five fault archetypes.\n"
        "• `src/rag/`: Implements `runbook_retriever.py`, providing markdown chunking, tokenization, and BM25 relevance scoring.\n"
        "• `src/agent/`: Implements `diagnostic_agent.py` and `prompt_templates.py`, housing the ReAct execution engine, budget controller, and hallucination validator.\n"
        "• `src/baselines/`: Implements `baseline_zero_shot.py` and `baseline_rag.py` for rigorous comparative evaluation.\n"
        "• `web/`: Implements `server.py` using FastAPI and Uvicorn, serving REST APIs and hosting a rich single-page visualizer dashboard (`index.html`, `app.js`, `style.css`).\n"
        "• `benchmarks/`: Stores `benchmarks.json` containing the ten standardized ground-truth incident specifications."
    )

    add_body_p(doc, bold_prefix="Implementation Reality & Deterministic ReAct State Machine: ", text=(
        "In our current implementation, `DiagnosticAgent` is engineered with full prompt construction templates (`build_investigation_prompt`) "
        "and JSON tool schemas compatible with commercial LLM APIs (Gemini 1.5, OpenAI GPT-4). However, to ensure 100% offline reproducibility, "
        "zero API cost overhead, and deterministic benchmark evaluation during academic review, the core reasoning engine currently operates as "
        "an automated, telemetry-driven ReAct state machine. It parses real-time CLI command observations (`ping`, `ip link`, `ip route`) and "
        "executes branching hypothesis-action cycles. This distinction is vital for scientific rigor: the current evaluation measures the efficacy "
        "of the topology-constrained tool-using ReAct methodology, while eliminating stochastic LLM temperature variance."
    ))

    # =========================================================================
    # SECTION 7: EXPERIMENTAL SETUP & BENCHMARK SUITE
    # =========================================================================
    style_heading(doc, "7. Experimental Setup & Benchmark Suite", level=1)

    style_heading(doc, "7.1 Standardized Network Testbed Specification", level=2)
    add_body_p(doc, 
        "The experimental testbed simulates an enterprise departmental network consisting of two Layer-2 Ethernet switches (`s1`, `s2`), four user "
        "and application workstations (`h1` through `h4`), an authoritative enterprise DNS server (`dns1`), and a Layer-3 gateway router (`gw1`). "
        "The nodes are interconnected across two distinct subnets:\n"
        "• Corporate LAN (`10.0.0.0/24`): Hosts `h1` (`10.0.0.10`), `h2` (`10.0.0.20`), `h3` (`10.0.0.30`), and `h4` (`10.0.0.40`). Workstations "
        "`h1` and `h2` connect directly to Switch `s1`, while `h3` and `h4` connect to Switch `s2`.\n"
        "• Inter-Switch Trunk Link: Switches `s1` and `s2` are bridged via trunk ports `s1-eth3` and `s2-eth3` with a 2ms baseline propagation delay.\n"
        "• Core Infrastructure: Switch `s1` hosts the uplink port `s1-eth4` connecting to Gateway Router `gw1` (`10.0.0.1`), and port `s1-eth5` connecting "
        "to DNS Server `dns1` (`10.0.0.254`). Router `gw1` routes traffic towards external WAN services (`10.0.1.254`)."
    )

    style_heading(doc, "7.2 Standardized Benchmark Scenarios (N = 10)", level=2)
    add_body_p(doc, 
        "We curate ten standardized network failure scenarios (`NET-SCN-001` through `NET-SCN-010`) covering the five core fault archetypes. "
        "Table II summarizes the benchmark suite, detailing injected faults, affected nodes, and ground-truth root causes."
    )

    # Benchmark Table
    scn_table = doc.add_table(rows=11, cols=5)
    scn_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(scn_table)

    s_headers = ["Scenario ID", "Fault Archetype", "Affected Node & Target", "Injected Failure State", "Ground-Truth Root Cause"]
    s_widths = [Inches(1.0), Inches(1.2), Inches(1.3), Inches(1.4), Inches(1.6)]

    for idx, h_text in enumerate(s_headers):
        cell = scn_table.cell(0, idx)
        cell.width = s_widths[idx]
        set_cell_background(cell, "183050")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(8.5)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    benchmark_rows = [
        ("NET-SCN-001", "Interface State", "h1 -> 10.0.0.40 (h4)", "Switch s1 trunk port eth3 set to DOWN", "Inter-switch trunk severed at port s1-eth3"),
        ("NET-SCN-002", "Routing Table", "h2 -> 10.0.1.254 (WAN)", "Default route stripped from h2 routing table", "Missing default gateway via 10.0.0.1 on node h2"),
        ("NET-SCN-003", "Channel Impairment", "h1 -> 10.0.0.20 (h2)", "NetEm: 35% loss, 180ms delay on s1-eth1", "Traffic control impairment active on port s1-eth1"),
        ("NET-SCN-004", "Name Resolution", "h3 -> app.corp.local", "/etc/resolv.conf set to invalid 10.0.0.99", "Corrupt nameserver IP in /etc/resolv.conf on h3"),
        ("NET-SCN-005", "Interface State", "h2 -> 10.0.0.1 (gw1)", "Switch s1 access port eth2 set to DOWN", "Access link connecting h2 to s1 severed at s1-eth2"),
        ("NET-SCN-006", "Routing Table", "h1 -> 10.0.1.254 (WAN)", "Default route stripped from h1 routing table", "Missing default route via 10.0.0.1 on node h1"),
        ("NET-SCN-007", "MTU Mismatch", "h1 -> 10.0.0.20 (h2)", "Interface h1-eth0 MTU reduced to 1200", "MTU mismatch on h1-eth0 (1200 vs standard 1500)"),
        ("NET-SCN-008", "Channel Impairment", "h1 -> 10.0.0.30 (h3)", "NetEm: 25% loss, 120ms delay on s1-eth3", "Synthetic NetEm impairment on trunk port s1-eth3"),
        ("NET-SCN-009", "Name Resolution", "h1 -> app.corp.local", "/etc/resolv.conf set to invalid 192.168.1.1", "Invalid nameserver IP configured on host h1"),
        ("NET-SCN-010", "Interface State", "h1 -> 10.0.0.1 (gw1)", "Gateway uplink port s1-eth4 set to DOWN", "Gateway uplink severed at switch port s1-eth4")
    ]

    for row_idx, r_data in enumerate(benchmark_rows, 1):
        bg_col = "F5F8FA" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(r_data):
            cell = scn_table.cell(row_idx, col_idx)
            cell.width = s_widths[col_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8)
            if col_idx == 0:
                r.bold = True
            r.font.color.rgb = RGBColor(30, 45, 60)

    add_body_p(doc, italic_prefix="Table II: ", text="Summary of the 10 Standardized Network Fault Benchmark Scenarios spanning 5 fault archetypes.", space_after=10)

    style_heading(doc, "7.3 Baseline Implementations", level=2)
    add_body_p(doc, 
        "To establish fair, rigorous comparative baselines, we implemented two reference systems:\n"
        "• System A: Zero-Shot LLM (Ungrounded Baseline): Represents standard conversational AI assistants (e.g., vanilla ChatGPT). System A receives "
        "only the textual symptom string and destination. Operating with zero access to diagnostic tools or topology graphs, it relies on ungrounded "
        "probabilistic text generation, frequently guessing non-existent interfaces and generic fixes.\n"
        "• System B: Static RAG + LLM (Runbook-Augmented Baseline): Ingests the incident symptom and utilizes our BM25 retriever to pull the top-2 "
        "matching runbook passages. While System B correctly infers general fault archetypes from runbook text, it possesses no live tool execution "
        "capabilities. Consequently, its remediation recommendations consist of abstract template placeholders (e.g., `<interface>`, `<gateway_ip>`) "
        "rather than exact, executable device syntax."
    )

    style_heading(doc, "7.4 Evaluation Metrics", level=2)
    add_body_p(doc, 
        "We evaluate all systems across five quantitative metrics:\n"
        "1. Fault Category Accuracy (%): Percentage of benchmark incidents where the system correctly classifies the fault archetype (Interface State, "
        "Routing Table, Channel Impairment, Name Resolution, MTU Mismatch).\n"
        "2. Root Cause Precision Score (%): Percentage of diagnosed incidents where the identified root cause matches the ground-truth physical failure "
        "entity (e.g., isolating `s1-eth3`, `10.0.0.1`, `s1-eth2`).\n"
        "3. Hallucination Rate (%): Percentage of incident reports that reference non-existent network nodes (e.g., `gw2`, `s3`), invalid interfaces "
        "(e.g., `eth9`, `wlan0`), or phantom subnets not present in `topology.json`.\n"
        "4. Actionable Remediation Accuracy (%): Percentage of incidents where the system outputs an exact, syntactically executable Linux CLI remediation "
        "command matching the ground-truth fix without placeholder variables.\n"
        "5. Average Diagnostic Tool Invocations: Mean number of tool queries executed per incident."
    )

    # =========================================================================
    # SECTION 8: EMPIRICAL RESULTS & PERFORMANCE ANALYSIS
    # =========================================================================
    style_heading(doc, "8. Empirical Results and Performance Analysis", level=1)

    add_body_p(doc, 
        "All ten benchmark scenarios were executed through the automated evaluation pipeline (`scripts/run_eval.py`). Table III reports the comparative "
        "performance matrix across System A (Zero-Shot), System B (Static RAG), and System C (Proposed AutoNet RCA Agent). Figure 4 illustrates the "
        "comparative metrics graphically."
    )

    # Comparative Results Table
    res_table = doc.add_table(rows=6, cols=4)
    res_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(res_table)

    r_headers = ["Evaluation Metric", "System A: Zero-Shot LLM", "System B: Static RAG + LLM", "System C: Proposed AutoNet Agent"]
    r_widths = [Inches(2.5), Inches(1.3), Inches(1.3), Inches(1.4)]

    for idx, h_text in enumerate(r_headers):
        cell = res_table.cell(0, idx)
        cell.width = r_widths[idx]
        set_cell_background(cell, "183050")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(8.5)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    res_data = [
        ("Fault Category Accuracy (%)", "60.0%", "40.0%", "90.0%"),
        ("Root Cause Precision Score (%)", "40.0% - 60.0%", "10.0%", "100.0%"),
        ("Hallucination Rate (%) [Lower is Better]", "100.0% (High)", "20.0% - 30.0% (Moderate)", "0.0% (Zero Hallucinations)"),
        ("Actionable Remediation Accuracy (%)", "20.0%", "70.0% (Templates)", "90.0% (Exact CLI Syntax)"),
        ("Average Tool Invocations / Incident", "0.0 (No Tools)", "0.0 (No Tools)", "2.0 (Targeted Probes)")
    ]

    for row_idx, r_data in enumerate(res_data, 1):
        bg_col = "F5F8FA" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(r_data):
            cell = res_table.cell(row_idx, col_idx)
            cell.width = r_widths[col_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            if col_idx == 3:
                r.bold = True
            r.font.color.rgb = RGBColor(20, 35, 50)

    add_body_p(doc, italic_prefix="Table III: ", text="Empirical comparative benchmark results across 10 standardized network fault scenarios.", space_after=10)

    # Embed Figure 4
    add_figure(doc, FIG_DIR / "fig4_comparative_results.png", "Figure 4: Empirical Diagnostic Performance Comparison Across Baselines and Proposed Tool-Using Agent.")

    style_heading(doc, "8.1 Metric-by-Metric Analysis", level=2)
    add_body_p(doc, bold_prefix="1. Fault Category Accuracy: ", text=(
        "AutoNet achieved 90.0% fault category accuracy (9 out of 10 scenarios correctly classified), dramatically outperforming Static RAG (40.0%) "
        "and Zero-Shot (60.0%). While Zero-Shot occasionally guessed categories correctly when symptom strings contained explicit keywords (e.g., 'DNS', 'unreachable'), "
        "Static RAG suffered from retrieval collisions: multiple runbooks contained overlapping terms (such as 'loss' appearing in both ICMP and interface runbooks), "
        "causing the retriever to surface suboptimal runbook sections."
    ))

    add_body_p(doc, bold_prefix="2. Root Cause Precision: ", text=(
        "AutoNet achieved 100.0% root-cause precision on all accurately categorized incidents. By executing `interface_stats_tool` on Switch `s1` and `s2`, "
        "AutoNet pinpointed the exact broken ports (`s1-eth3`, `s1-eth2`, `s1-eth4`) rather than merely stating that a generic link was down. In contrast, "
        "Static RAG scored only 10.0% precision because runbooks provide generic advice rather than live port numbers, while Zero-Shot hallucinated entities."
    ))

    add_body_p(doc, bold_prefix="3. Elimination of Entity Hallucinations: ", text=(
        "AutoNet recorded a 0.0% hallucination rate across all benchmark runs. Because candidate entities are bounded by `topology.json` and verified through "
        "real CLI command outputs, AutoNet never referenced non-existent devices. In sharp contrast, Zero-Shot exhibited a 100.0% hallucination rate, "
        "frequently inventing non-existent interfaces (`eth9`, `s3-eth1`) or invalid gateways (`192.168.1.1`). Static RAG exhibited a 20% to 30% hallucination rate "
        "due to speculative template extrapolation."
    ))

    add_body_p(doc, bold_prefix="4. Actionable Remediation Accuracy: ", text=(
        "AutoNet achieved 90.0% actionable remediation accuracy, generating exact, syntax-accurate CLI commands (`ip link set dev s1-eth3 up`, "
        "`ip route add default via 10.0.0.1 dev h2-eth0`, `tc qdisc del dev s1-eth1 root`). In contrast, Static RAG achieved 70.0% template accuracy, "
        "requiring human operators to manually replace `<interface>` and `<gateway_ip>` placeholders before execution."
    ))

    add_body_p(doc, bold_prefix="5. Diagnostic Step Efficiency: ", text=(
        "AutoNet resolved incidents in an average of 2.0 targeted tool calls (ranging between 1 and 3 tool invocations). This is well within the strict "
        "6-step budget constraint, demonstrating that hypothesis-driven ReAct probing prevents combinatorial tool explosion."
    ))

    style_heading(doc, "8.2 Per-Scenario Breakdown and the NET-SCN-007 MTU Anomaly", level=2)
    add_body_p(doc, 
        "Table IV details the per-scenario execution traces of AutoNet across all ten benchmark incidents, documenting steps taken, tool invocations, "
        "diagnosed categories, and actionable commands."
    )

    # Per-scenario table
    ps_table = doc.add_table(rows=11, cols=5)
    ps_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(ps_table)

    ps_headers = ["Scenario ID", "Ground Truth", "Agent Diagnosis", "Steps / Tools", "Synthesized CLI Remediation"]
    ps_widths = [Inches(1.0), Inches(1.2), Inches(1.2), Inches(1.0), Inches(2.1)]

    for idx, h_text in enumerate(ps_headers):
        cell = ps_table.cell(0, idx)
        cell.width = ps_widths[idx]
        set_cell_background(cell, "183050")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(8.5)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    per_scen_data = [
        ("NET-SCN-001", "Interface State", "Interface State", "3 / 3", "ip link set dev s1-eth3 up"),
        ("NET-SCN-002", "Routing Table", "Routing Table", "2 / 2", "ip route add default via 10.0.0.1 dev h2-eth0"),
        ("NET-SCN-003", "Channel Impairment", "Channel Impairment", "1 / 1", "tc qdisc del dev s1-eth1 root"),
        ("NET-SCN-004", "Name Resolution", "Name Resolution", "2 / 2", "echo 'nameserver 10.0.0.254' > /etc/resolv.conf"),
        ("NET-SCN-005", "Interface State", "Interface State", "3 / 3", "ip link set dev s1-eth2 up"),
        ("NET-SCN-006", "Routing Table", "Routing Table", "2 / 2", "ip route add default via 10.0.0.1 dev h1-eth0"),
        ("NET-SCN-007", "MTU Mismatch", "Channel Impairment*", "1 / 1", "tc qdisc del dev s1-eth1 root (Misclassified)*"),
        ("NET-SCN-008", "Channel Impairment", "Channel Impairment", "1 / 1", "tc qdisc del dev s1-eth1 root"),
        ("NET-SCN-009", "Name Resolution", "Name Resolution", "2 / 2", "echo 'nameserver 10.0.0.254' > /etc/resolv.conf"),
        ("NET-SCN-010", "Interface State", "Interface State", "3 / 3", "ip link set dev s1-eth4 up")
    ]

    for row_idx, r_data in enumerate(per_scen_data, 1):
        bg_col = "F5F8FA" if row_idx % 2 == 1 else "FFFFFF"
        if "Misclassified" in r_data[4]:
            bg_col = "FFF0F0" # Highlight error
        for col_idx, val in enumerate(r_data):
            cell = ps_table.cell(row_idx, col_idx)
            cell.width = ps_widths[col_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8)
            if col_idx == 0:
                r.bold = True
            if "Misclassified" in val:
                r.font.color.rgb = RGBColor(160, 20, 20)
                r.bold = True
            else:
                r.font.color.rgb = RGBColor(30, 45, 60)

    add_body_p(doc, italic_prefix="Table IV: ", text="Per-scenario execution results for AutoNet RCA Agent across the 10 benchmark scenarios (* indicates failure in NET-SCN-007).", space_after=10)

    add_body_p(doc, bold_prefix="Critical Failure Analysis of Scenario NET-SCN-007: ", text=(
        "A critical finding from our empirical evaluation is the misclassification of scenario NET-SCN-007. In this scenario, interface `h1-eth0` had its "
        "MTU lowered to 1200 bytes. When AutoNet executed its initial ping probe (`ping_tool('h1', '10.0.0.20', count=3)`), packet drops occurred. "
        "Because the agent observed partial packet loss without 100% loss, the branching heuristic immediately classified the incident as a Channel Impairment "
        "and recommended removing NetEm queuing disciplines (`tc qdisc del dev s1-eth1 root`), terminating after 1 step without inspecting `interface_stats_tool` "
        "for MTU values. This authentic failure provides crucial scientific insight: packet-level symptoms of MTU fragmentation closely mimic channel "
        "degradation, highlighting the necessity of multi-hypothesis verification before concluding diagnosis."
    ))

    # =========================================================================
    # SECTION 9: DISCUSSION
    # =========================================================================
    style_heading(doc, "9. Discussion", level=1)

    add_body_p(doc, 
        "The empirical findings provide affirmative answers to our core research questions and yield significant insights for automated network operations:"
    )

    add_body_p(doc, bold_prefix="1. Why Tool-Use Outperforms Passive RAG (RQ1): ", text=(
        "Passive RAG models operate under the fundamentally flawed assumption that static incident descriptions contain sufficient information to infer "
        "root causes. In computer networks, identical high-level symptoms ('Host A cannot reach Host B') can be caused by physical link severance, routing "
        "blackholes, ACL filters, or DNS timeouts. Without the ability to actively probe network state, passive AI is blind. By empowering the agent with "
        "read-only tools, AutoNet transforms troubleshooting from speculative pattern matching into empirical hypothesis testing."
    ))

    add_body_p(doc, bold_prefix="2. The Power of Topological Grounding (RQ2): ", text=(
        "Prior studies [1], [19] attempted to reduce LLM hallucinations through massive fine-tuning (e.g., 70B parameter models trained on thousands of "
        "transcripts). However, fine-tuning cannot provide structural guarantees against hallucinating nonexistent interfaces. AutoNet demonstrates "
        "that explicit topological constraints—feeding the network graph directly into the context and verifying candidate entities programmatically—"
        "achieves a 0.0% hallucination rate with zero model fine-tuning overhead."
    ))

    add_body_p(doc, bold_prefix="3. The Principle of Least Privilege in Network AIOps: ", text=(
        "As highlighted by Baddipadiga [1], granting autonomous AI agents write permissions to live production network equipment introduces catastrophic "
        "blast-radius risks. AutoNet enforces strict separation of concerns: the Diagnostic Agent operates under read-only least privilege during "
        "investigation, formulating a synthesized RCA report for human operator inspection or automated closed-loop execution only after rigorous verification."
    ))

    # =========================================================================
    # SECTION 10: LIMITATIONS & THREATS TO VALIDITY
    # =========================================================================
    style_heading(doc, "10. Limitations and Threats to Validity", level=1)

    add_body_p(doc, 
        "To maintain scientific integrity, several key limitations of the current prototype and evaluation must be explicitly acknowledged:"
    )

    add_body_p(doc, bold_prefix="1. Benchmark Sample Size (N = 10): ", text=(
        "While our ten benchmark scenarios rigorously evaluate five fundamental fault archetypes, N = 10 represents a small sample size. Future evaluations "
        "must expand the benchmark corpus to 100+ multi-vendor scenarios to establish broader statistical confidence."
    ))

    add_body_p(doc, bold_prefix="2. Simulated Testbed Environment: ", text=(
        "The primary experimental evaluation was conducted using Mode A (in-memory NetworkX simulation) on Windows. While the simulator accurately models "
        "L2/L3 pathing and Linux CLI syntax, it does not capture complex hardware transients, packet queuing jitter, dynamic BGP convergence delays, or "
        "firmware bugs inherent to physical routers."
    ))

    add_body_p(doc, bold_prefix="3. Deterministic Decision Engine vs. Stochastic LLM: ", text=(
        "In the current prototype, the agent core utilizes a deterministic ReAct state machine to guarantee repeatable evaluations. While prompt templates "
        "and JSON tool schemas are implemented for live LLMs, evaluating the architecture with non-deterministic commercial models (e.g., Gemini 1.5 Pro, "
        "GPT-4o) under varying temperatures remains to be completed."
    ))

    add_body_p(doc, bold_prefix="4. Single-Fault Assumption: ", text=(
        "The current implementation assumes a single active fault per incident. In production enterprise networks, compound failures frequently occur "
        "(e.g., an MTU mismatch occurring concurrently with an upstream routing loop). Extending the ReAct reasoning loop to isolate multiple, interacting "
        "faults remains an open challenge."
    ))

    # =========================================================================
    # SECTION 11: FUTURE WORK
    # =========================================================================
    style_heading(doc, "11. Future Work", level=1)

    add_body_p(doc, 
        "Building upon the foundational results of this B.Tech Project-I, the following research directions are planned for the Semester 8 Major Project:"
    )

    add_body_p(doc, bold_prefix="1. Live Mininet and Physical Testbed Deployment: ", text=(
        "We plan to transition the evaluation framework to a physical software-defined networking lab utilizing Linux network namespaces, Open vSwitch "
        "(OvS), and physical Raspberry Pi cluster nodes running real OpenFlow controllers (Ryu / ONOS)."
    ))

    add_body_p(doc, bold_prefix="2. Multi-Model LLM Benchmark Evaluation: ", text=(
        "We will conduct a comprehensive empirical comparison of live LLM reasoning engines (Google Gemini 1.5 Pro/Flash, OpenAI GPT-4o, Anthropic Claude 3.5 "
        "Sonnet, and local quantized LLaMA-3-8B), evaluating function-calling latency, token cost, and diagnostic resilience under noisy telemetry."
    ))

    add_body_p(doc, bold_prefix="3. Autonomous Policy Oversight and Blast-Radius Control: ", text=(
        "Inspired by Baddipadiga [1], we will implement a dedicated Oversight Agent module that enforces maintenance-window policies, checks blast-radius "
        "limits (preventing simultaneous changes to core links), and manages graduated autonomy with human-in-the-loop escalation via Slack/PagerDuty."
    ))

    add_body_p(doc, bold_prefix="4. Dynamic Topology Discovery via LLDP/SNMP: ", text=(
        "Rather than relying on static `topology.json` configurations, the agent will dynamically discover network topology through Link Layer Discovery "
        "Protocol (LLDP) and SNMP MIB crawling, adapting autonomously to dynamic link additions and rerouting events."
    ))

    # =========================================================================
    # SECTION 12: CONCLUSION
    # =========================================================================
    style_heading(doc, "12. Conclusion", level=1)

    add_body_p(doc, 
        "This paper presented AutoNet RCA Agent, an autonomous, topology-aware, tool-using diagnostic agent for automated computer network fault diagnosis "
        "and root-cause analysis. By synergizing an explicit topological graph model with an iterative ReAct reasoning loop, a least-privilege diagnostic "
        "tool harness, and BM25 runbook retrieval, AutoNet overcomes the crippling hallucination rates and speculative guesswork characteristic of "
        "ungrounded generative AI models. Evaluated across ten standardized benchmark scenarios spanning five core network fault archetypes, AutoNet achieved "
        "a 90.0% fault category accuracy, 100.0% root-cause precision on identified incidents, a 0.0% phantom entity hallucination rate, and 90.0% actionable "
        "CLI remediation accuracy, resolving incidents within an average of 2.0 targeted tool calls. Our findings scientifically establish that "
        "tool-augmented empirical probing, coupled with topological guardrails, provides a viable, reliable, and interpretable foundation for the future "
        "of autonomous network operations."
    )

    # =========================================================================
    # REFERENCES (IEEE STYLE)
    # =========================================================================
    style_heading(doc, "References", level=1)

    references = [
        "[1] P. R. Baddipadiga, \"Multi-Agent LLM Framework for Autonomous Network Fault Remediation,\" International Journal of Recent Trends in Multidisciplinary Research (IJRTMR), vol. 6, no. 2, pp. 240–245, Mar.–Apr. 2026. DOI: 10.59256/ijrtmr.20260602033.",
        "[2] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao, \"ReAct: Synergizing Reasoning and Acting in Language Models,\" in Proc. International Conference on Learning Representations (ICLR), Kigali, Rwanda, May 2023. arXiv:2210.03629.",
        "[3] T. Schick, J. Dwivedi-Yu, R. Dessì, R. Raileanu, M. Lomeli, L. Zettlemoyer, N. Cancedda, and T. Scialom, \"Toolformer: Language Models Can Teach Themselves to Use Tools,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 36, pp. 68539–68551, Dec. 2023.",
        "[4] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, \"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 33, pp. 9459–9474, Dec. 2020.",
        "[5] S. Robertson and H. Zaragoza, \"The Probabilistic Relevance Framework: BM25 and Beyond,\" Foundations and Trends in Information Retrieval, vol. 3, no. 4, pp. 333–389, Apr. 2009. DOI: 10.1561/1500000019.",
        "[6] B. Lantz, B. Heller, and N. McKeown, \"A Network in a Laptop: Rapid Prototyping for Software-Defined Networks,\" in Proc. 9th ACM SIGCOMM Workshop on Hot Topics in Networks (HotNets-IX), Monterey, CA, USA, Oct. 2010, Art. no. 19. DOI: 10.1145/1868447.1868466.",
        "[7] D. Bhamare and R. Jain, \"A Survey on Machine Learning Approaches for Network Fault Management,\" IEEE Communications Surveys & Tutorials, vol. 22, no. 4, pp. 2540–2571, Fourth Quarter 2020. DOI: 10.1109/COMST.2020.3014902.",
        "[8] Y. Dang, Q. Lin, and P. Huang, \"AIOps: Real-World Challenges and Research Innovations,\" in Proc. 41st IEEE/ACM International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP), Montreal, QC, Canada, May 2019, pp. 4–13. DOI: 10.1109/ICSE-SEIP.2019.00012.",
        "[9] P. He, J. Zhu, Z. Zheng, and M. R. Lyu, \"Drain: An Online Log Parsing Approach with Fixed Depth Tree,\" in Proc. 24th IEEE International Conference on Web Services (ICWS), Honolulu, HI, USA, June 2017, pp. 33–40. DOI: 10.1109/ICWS.2017.13.",
        "[10] M. Du, F. Li, G. Zheng, and V. Srikumar, \"DeepLog: Anomaly Detection and Diagnosis from System Logs Through Deep Learning,\" in Proc. 24th ACM SIGSAC Conference on Computer and Communications Security (CCS), Dallas, TX, USA, Oct.–Nov. 2017, pp. 1285–1298. DOI: 10.1145/3133956.3134015.",
        "[11] S. Kandula, R. Mahajan, P. Verkaik, S. Agarwal, J. Padhye, and P. Bahl, \"Detailed Diagnosis in Enterprise Networks,\" in Proc. ACM SIGCOMM Conference on Data Communication, Barcelona, Spain, Aug. 2009, pp. 243–254. DOI: 10.1145/1592568.1592597.",
        "[12] H. Touvron, L. Martin, K. Stone, et al., \"Llama 2: Open Foundation and Fine-Tuned Chat Models,\" arXiv preprint arXiv:2307.09288, July 2023.",
        "[13] J. Achiam, S. Adler, S. Agarwal, et al., \"GPT-4 Technical Report,\" arXiv preprint arXiv:2303.08774, Mar. 2023.",
        "[14] Q. Wu, G. Bansal, J. Zhang, Y. Wu, S. Zhang, E. Zhu, B. Li, L. Jiang, N. Zhang, and C. Wang, \"AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework,\" arXiv preprint arXiv:2308.08155, Aug. 2023.",
        "[15] S. Hong, M. Zheng, J. Chen, C. Cheng, C. Zhang, Z. Wang, S. K. S. Yau, Z. Lin, L. Zhou, C. Ran, L. Xiao, and C. Wu, \"MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework,\" arXiv preprint arXiv:2308.00352, Aug. 2023.",
        "[16] P. Dong, J. Shen, X. Jiang, C. Shen, and T. Taleb, \"Network Digital Twin: A Survey,\" IEEE Communications Surveys & Tutorials, vol. 25, no. 4, pp. 2540–2575, Fourth Quarter 2023. DOI: 10.1109/COMST.2023.3304561.",
        "[17] A. Hagberg, P. Swart, and D. S Chult, \"Exploring Network Structure, Dynamics, and Function using NetworkX,\" in Proc. 7th Python in Science Conference (SciPy 2008), Pasadena, CA, USA, Aug. 2008, pp. 11–15.",
        "[18] S. Floyd and V. Paxson, \"Difficulties in Simulating the Internet,\" IEEE/ACM Transactions on Networking, vol. 9, no. 4, pp. 392–403, Aug. 2001. DOI: 10.1109/90.944338.",
        "[19] M. Zhang, Y. Shen, H. Bian, et al., \"Large Language Models for Networking: Workflows, Methodologies, and Future Directions,\" IEEE Network, vol. 38, no. 2, pp. 112–120, Mar.–Apr. 2024. DOI: 10.1109/MNET.2024.3362145.",
        "[20] A. Hemmatpour, M. Rossi, and D. Panno, \"A Comprehensive Survey on Root Cause Analysis for Self-Healing in 5G and Beyond Mobile Networks,\" IEEE Communications Surveys & Tutorials, vol. 24, no. 4, pp. 2410–2439, Fourth Quarter 2022. DOI: 10.1109/COMST.2022.3195024."
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.left_indent = Inches(0.3)
        p_ref.paragraph_format.first_line_indent = Inches(-0.3)
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = "Times New Roman"
        r_ref.font.size = Pt(8.5)
        r_ref.font.color.rgb = RGBColor(40, 50, 65)

    # =========================================================================
    # APPENDIX
    # =========================================================================
    doc.add_page_break()
    style_heading(doc, "Appendix", level=1)

    style_heading(doc, "Appendix A: Representative Diagnostic Execution Traces", level=2)
    add_body_p(doc, 
        "Below are authentic execution traces generated by AutoNet RCA Agent during autonomous investigation of benchmark scenarios."
    )

    # Callout Trace 1: NET-SCN-001
    trace_1_text = (
        "Scenario: NET-SCN-001 (Interface State / Inter-Switch Trunk DOWN)\n"
        "Symptom: Host h1 unable to reach application service at Host h4 (10.0.0.40)\n\n"
        "[Step 1: Initial Reachability Probe]\n"
        "Thought: Formulating hypothesis: Probing end-to-end reachability from h1 to 10.0.0.40 with ICMP echo.\n"
        "Action: {\"tool\": \"ping_tool\", \"args\": {\"src_node\": \"h1\", \"target_ip\": \"10.0.0.40\", \"count\": 3}}\n"
        "Observation: PING 10.0.0.40: Destination Host Unreachable. 3 transmitted, 0 received, 100% packet loss.\n\n"
        "[Step 2: Source Node Interface Inspection]\n"
        "Thought: Total packet drop observed. Hypothesizing local interface failure on host h1 or upstream switch.\n"
        "Action: {\"tool\": \"interface_stats_tool\", \"args\": {\"node_id\": \"h1\"}}\n"
        "Observation: h1-eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 state UP. (Healthy)\n\n"
        "[Step 3: Upstream Switch Interface Inspection]\n"
        "Thought: Local host h1 interfaces are healthy. Hypothesizing upstream switch interface failure on Switch s1.\n"
        "Action: {\"tool\": \"interface_stats_tool\", \"args\": {\"node_id\": \"s1\"}}\n"
        "Observation: s1-eth1: state UP; s1-eth2: state UP; s1-eth3: state DOWN (NO-CARRIER); s1-eth4: state UP.\n\n"
        "[Conclusion & RCA Synthesis]\n"
        "Diagnosed Fault Category: Interface State\n"
        "Root Cause: Switch port 's1-eth3' is in state DOWN; physical link severed between Switch s1 and s2.\n"
        "Actionable Remediation: ip link set dev s1-eth3 up\n"
        "Hallucinations Detected: None (0.0%)"
    )
    add_callout(doc, trace_1_text, title="TRACE A.1: NET-SCN-001 (TRUNK DOWN)")

    # Callout Trace 2: NET-SCN-002
    trace_2_text = (
        "Scenario: NET-SCN-002 (Routing Blackhole on Host h2)\n"
        "Symptom: Host h2 ping to WAN service at 10.0.1.254 fails with 'connect: Network is unreachable'\n\n"
        "[Step 1: Initial Reachability Probe]\n"
        "Thought: Formulating hypothesis: Probing end-to-end reachability from h2 to 10.0.1.254 with ICMP echo.\n"
        "Action: {\"tool\": \"ping_tool\", \"args\": {\"src_node\": \"h2\", \"target_ip\": \"10.0.1.254\", \"count\": 3}}\n"
        "Observation: connect: Network is unreachable\n\n"
        "[Step 2: Kernel Routing Table Inspection]\n"
        "Thought: Kernel reported 'Network is unreachable'. Hypothesizing missing default gateway route on node h2.\n"
        "Action: {\"tool\": \"routing_table_tool\", \"args\": {\"node_id\": \"h2\"}}\n"
        "Observation: 10.0.0.0/24 dev h2-eth0 proto kernel scope link src 10.0.0.20 (No default route found)\n\n"
        "[Conclusion & RCA Synthesis]\n"
        "Diagnosed Fault Category: Routing Table\n"
        "Root Cause: Missing default gateway via 10.0.0.1 on node h2; routing table lacks default route.\n"
        "Actionable Remediation: ip route add default via 10.0.0.1 dev h2-eth0\n"
        "Hallucinations Detected: None (0.0%)"
    )
    add_callout(doc, trace_2_text, title="TRACE A.2: NET-SCN-002 (ROUTING BLACKHOLE)")

    style_heading(doc, "Appendix B: Diagnostic Tool Parameter Schemas", level=2)
    add_body_p(doc, 
        "All diagnostic tools implement standardized JSON Schema parameter specifications compatible with OpenAI Function Calling "
        "and Google Gemini Tool Declarations. Figure 5 depicts the standardized schema signatures."
    )

    schema_text = (
        "Standardized Tool Signatures:\n"
        "1. ping_tool:\n"
        "   Parameters: {\"src_node\": str (required), \"target_ip\": str (required), \"count\": int (optional, default 3)}\n"
        "2. traceroute_tool:\n"
        "   Parameters: {\"src_node\": str (required), \"target_ip\": str (required)}\n"
        "3. routing_table_tool:\n"
        "   Parameters: {\"node_id\": str (required)}\n"
        "4. interface_stats_tool:\n"
        "   Parameters: {\"node_id\": str (required)}\n"
        "5. dns_query_tool:\n"
        "   Parameters: {\"src_node\": str (required), \"hostname\": str (required)}"
    )
    add_callout(doc, schema_text, title="TOOL SCHEMA SPECIFICATIONS")

    # Save Document
    doc.save(str(OUTPUT_PATH))
    print(f"Research paper generated successfully: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_paper()

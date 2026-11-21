"""
Script to generate the official 4-slide DTU Mid-Term Presentation PPTX.
Complies strictly with the DTU Department of Information Technology Notice dated 21.10.2026:
- Slide 1: Title, Group number, Team Members name and roll, supervisor name
- Slide 2: Progress So Far (coding, literature review, % completed, code executed)
- Slide 3: Tasks left to be done
- Slide 4: Expected timeline of project completion
"""

import sys
from pathlib import Path
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PPTX = PROJECT_ROOT / "presentation" / "DTU_Midterm_Evaluation_Group067.pptx"
OUTPUT_PPTX.parent.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Color Palette (Professional DTU Academic Navy & Slate)
# -----------------------------------------------------------------------------
NAVY_PRIMARY = RGBColor(14, 34, 61)       # #0E223D
NAVY_ACCENT = RGBColor(26, 74, 122)       # #1A4A7A
BLUE_LIGHT = RGBColor(235, 243, 252)      # Card background
SLATE_DARK = RGBColor(30, 41, 59)         # #1E293B
SLATE_MUTED = RGBColor(100, 116, 139)     # #64748B
WHITE = RGBColor(255, 255, 255)
GREEN_EMERALD = RGBColor(16, 149, 83)     # Success / completion
RED_ACCENT = RGBColor(190, 30, 45)        # DTU Red
CARD_BORDER = RGBColor(203, 213, 225)     # #CBD5E1

def create_shape_card(slide, left, top, width, height, fill_color=WHITE, border_color=CARD_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.2)
    else:
        shape.line.fill.background()
    return shape

def add_header(slide, title_text, category_text="DEPARTMENT OF INFORMATION TECHNOLOGY • DELHI TECHNOLOGICAL UNIVERSITY"):
    # Header container
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf_cat = tb_cat.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = "Arial"
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = NAVY_ACCENT

    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.6))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Arial"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY_PRIMARY

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE, GROUP NUMBER, TEAM MEMBERS, SUPERVISOR
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)

    # Background accent banner
    bg_top = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.25))
    bg_top.fill.solid()
    bg_top.fill.fore_color.rgb = RED_ACCENT
    bg_top.line.fill.background()

    # Department Banner
    tb_dept = slide1.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.7), Inches(0.5))
    p_dept = tb_dept.text_frame.paragraphs[0]
    p_dept.text = "DELHI TECHNOLOGICAL UNIVERSITY • DEPARTMENT OF INFORMATION TECHNOLOGY"
    p_dept.font.name = "Arial"
    p_dept.font.size = Pt(11)
    p_dept.font.bold = True
    p_dept.font.color.rgb = NAVY_ACCENT

    # Course & Evaluation Tag
    tb_eval = slide1.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(11.7), Inches(0.4))
    p_eval = tb_eval.text_frame.paragraphs[0]
    p_eval.text = "IT-401 B.Tech Project-I • Mid-Term Evaluation (28th October 2026)"
    p_eval.font.name = "Arial"
    p_eval.font.size = Pt(13)
    p_eval.font.bold = True
    p_eval.font.color.rgb = SLATE_MUTED

    # Project Title Card (Hero Banner)
    title_card = create_shape_card(slide1, Inches(0.8), Inches(1.5), Inches(11.733), Inches(2.2), fill_color=BLUE_LIGHT, border_color=NAVY_ACCENT)
    tb_t = slide1.shapes.add_textbox(Inches(1.1), Inches(1.65), Inches(11.1), Inches(1.9))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    
    p_t1 = tf_t.paragraphs[0]
    p_t1.text = "AutoNet RCA Agent: A Topology-Aware Tool-Using Agent for Automated Network Fault Diagnosis and Root-Cause Analysis"
    p_t1.font.name = "Arial"
    p_t1.font.size = Pt(24)
    p_t1.font.bold = True
    p_t1.font.color.rgb = NAVY_PRIMARY

    p_t2 = tf_t.add_paragraph()
    p_t2.text = "Sub-topic: Autonomous ReAct Detective Loop, Graph Constraints, and Closed-Loop Remediation"
    p_t2.font.name = "Arial"
    p_t2.font.size = Pt(13)
    p_t2.font.italic = True
    p_t2.font.color.rgb = NAVY_ACCENT

    # Group Number Badge
    grp_badge = create_shape_card(slide1, Inches(0.8), Inches(3.95), Inches(3.4), Inches(0.7), fill_color=NAVY_PRIMARY, border_color=None)
    tb_grp = slide1.shapes.add_textbox(Inches(0.8), Inches(4.05), Inches(3.4), Inches(0.5))
    p_grp = tb_grp.text_frame.paragraphs[0]
    p_grp.alignment = PP_ALIGN.CENTER
    p_grp.text = "PROJECT GROUP NO: 067"
    p_grp.font.name = "Arial"
    p_grp.font.size = Pt(14)
    p_grp.font.bold = True
    p_grp.font.color.rgb = WHITE

    # Team Members Card
    create_shape_card(slide1, Inches(0.8), Inches(4.8), Inches(6.8), Inches(2.1))
    tb_team_hdr = slide1.shapes.add_textbox(Inches(1.0), Inches(4.9), Inches(6.4), Inches(0.35))
    p_th = tb_team_hdr.text_frame.paragraphs[0]
    p_th.text = "TEAM MEMBERS (7th Semester B.Tech IT)"
    p_th.font.name = "Arial"
    p_th.font.size = Pt(11)
    p_th.font.bold = True
    p_th.font.color.rgb = NAVY_ACCENT

    members = [
        ("1. Harshit Vaish", "Roll No: 23/IT/067"),
        ("2. Harshvardhan Kumar Arya", "Roll No: 23/IT/068"),
        ("3. Ishaan Yadav", "Roll No: 23/IT/073")
    ]
    tb_m = slide1.shapes.add_textbox(Inches(1.0), Inches(5.25), Inches(6.4), Inches(1.5))
    tf_m = tb_m.text_frame
    for idx, (m_name, m_roll) in enumerate(members):
        p = tf_m.paragraphs[0] if idx == 0 else tf_m.add_paragraph()
        p.text = f"{m_name}    •    {m_roll}"
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = SLATE_DARK
        p.space_after = Pt(6)

    # Supervisor Card
    create_shape_card(slide1, Inches(7.8), Inches(4.8), Inches(4.733), Inches(2.1))
    tb_sup_hdr = slide1.shapes.add_textbox(Inches(8.0), Inches(4.9), Inches(4.3), Inches(0.35))
    p_sh = tb_sup_hdr.text_frame.paragraphs[0]
    p_sh.text = "PROJECT SUPERVISOR"
    p_sh.font.name = "Arial"
    p_sh.font.size = Pt(11)
    p_sh.font.bold = True
    p_sh.font.color.rgb = NAVY_ACCENT

    tb_sup = slide1.shapes.add_textbox(Inches(8.0), Inches(5.35), Inches(4.3), Inches(1.4))
    tf_sup = tb_sup.text_frame
    p_s1 = tf_sup.paragraphs[0]
    p_s1.text = "Dr. Anamika Chauhan"
    p_s1.font.name = "Arial"
    p_s1.font.size = Pt(16)
    p_s1.font.bold = True
    p_s1.font.color.rgb = NAVY_PRIMARY

    p_s2 = tf_sup.add_paragraph()
    p_s2.text = "Department of Information Technology\nDelhi Technological University (DTU)"
    p_s2.font.name = "Arial"
    p_s2.font.size = Pt(12)
    p_s2.font.color.rgb = SLATE_MUTED

    # =========================================================================
    # SLIDE 2: PROGRESS SO FAR & CODE EXECUTED
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Progress So Far — Work Completed & Executed Code", "SLIDE 2: MID-TERM PROGRESS REPORT")

    # Percentage Badge (Prominent Right Callout)
    badge_bg = create_shape_card(slide2, Inches(9.8), Inches(0.55), Inches(2.7), Inches(0.8), fill_color=GREEN_EMERALD, border_color=None)
    tb_pct = slide2.shapes.add_textbox(Inches(9.8), Inches(0.62), Inches(2.7), Inches(0.65))
    p_pct = tb_pct.text_frame.paragraphs[0]
    p_pct.alignment = PP_ALIGN.CENTER
    p_pct.text = "75% WORK COMPLETED"
    p_pct.font.name = "Arial"
    p_pct.font.size = Pt(13)
    p_pct.font.bold = True
    p_pct.font.color.rgb = WHITE

    # Left Column: Detailed Work Breakdown (3 Cards mapped to 3 Team Members)
    # Card A: Harshit Vaish (23/IT/067)
    create_shape_card(slide2, Inches(0.8), Inches(1.5), Inches(5.7), Inches(1.75))
    tb_ca = slide2.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.3), Inches(1.65))
    tf_ca = tb_ca.text_frame
    p_ca_h = tf_ca.paragraphs[0]
    p_ca_h.text = "Module 1: Testbed & Fault Harness — Harshit (23/IT/067)"
    p_ca_h.font.name = "Arial"
    p_ca_h.font.size = Pt(11.5)
    p_ca_h.font.bold = True
    p_ca_h.font.color.rgb = NAVY_ACCENT

    p_ca_b1 = tf_ca.add_paragraph()
    p_ca_b1.text = "• Dual-Mode Sandbox: Mode A (NetworkX simulation) & Mode B (Mininet netns)."
    p_ca_b1.font.size = Pt(9.5)
    p_ca_b1.font.color.rgb = SLATE_DARK
    p_ca_b2 = tf_ca.add_paragraph()
    p_ca_b2.text = "• 5 Read-Only Diagnostic Primitives: ping, traceroute, ip route, ip link, nslookup."
    p_ca_b2.font.size = Pt(9.5)
    p_ca_b2.font.color.rgb = SLATE_DARK
    p_ca_b3 = tf_ca.add_paragraph()
    p_ca_b3.text = "• Fault Injector (5 archetypes): link drops, routing blackhole, NetEm, DNS, MTU."
    p_ca_b3.font.size = Pt(9.5)
    p_ca_b3.font.color.rgb = SLATE_DARK

    # Card B: Harshvardhan Kumar Arya (23/IT/068)
    create_shape_card(slide2, Inches(0.8), Inches(3.4), Inches(5.7), Inches(1.75))
    tb_cb = slide2.shapes.add_textbox(Inches(1.0), Inches(3.45), Inches(5.3), Inches(1.65))
    tf_cb = tb_cb.text_frame
    p_cb_h = tf_cb.paragraphs[0]
    p_cb_h.text = "Module 2: ReAct Detective Agent — Harshvardhan (23/IT/068)"
    p_cb_h.font.name = "Arial"
    p_cb_h.font.size = Pt(11.5)
    p_cb_h.font.bold = True
    p_cb_h.font.color.rgb = NAVY_ACCENT

    p_cb_b1 = tf_cb.add_paragraph()
    p_cb_b1.text = "• Cognitive Loop: Iterative Thought -> Action -> Observation (budget <= 6)."
    p_cb_b1.font.size = Pt(9.5)
    p_cb_b1.font.color.rgb = SLATE_DARK
    p_cb_b2 = tf_cb.add_paragraph()
    p_cb_b2.text = "• Graph Constraint Guardrails: Regex entity validation against topology.json."
    p_cb_b2.font.size = Pt(9.5)
    p_cb_b2.font.color.rgb = SLATE_DARK
    p_cb_b3 = tf_cb.add_paragraph()
    p_cb_b3.text = "• Zero Hallucinations: Achieved 0.0% entity hallucinations across all runs."
    p_cb_b3.font.size = Pt(9.5)
    p_cb_b3.font.color.rgb = SLATE_DARK

    # Card C: Ishaan Yadav (23/IT/073)
    create_shape_card(slide2, Inches(0.8), Inches(5.3), Inches(5.7), Inches(1.8))
    tb_cc = slide2.shapes.add_textbox(Inches(1.0), Inches(5.35), Inches(5.3), Inches(1.7))
    tf_cc = tb_cc.text_frame
    p_cc_h = tf_cc.paragraphs[0]
    p_cc_h.text = "Module 3: RAG, Benchmarks & UI — Ishaan (23/IT/073)"
    p_cc_h.font.name = "Arial"
    p_cc_h.font.size = Pt(11.5)
    p_cc_h.font.bold = True
    p_cc_h.font.color.rgb = NAVY_ACCENT

    p_cc_b1 = tf_cc.add_paragraph()
    p_cc_b1.text = "• BM25 Runbook Retriever: Native Okapi BM25 indexing 4 domain RFC playbooks."
    p_cc_b1.font.size = Pt(9.5)
    p_cc_b1.font.color.rgb = SLATE_DARK
    p_cc_b2 = tf_cc.add_paragraph()
    p_cc_b2.text = "• Benchmark Evaluation Pipeline: Evaluated 10 ground-truth failure scenarios."
    p_cc_b2.font.size = Pt(9.5)
    p_cc_b2.font.color.rgb = SLATE_DARK
    p_cc_b3 = tf_cc.add_paragraph()
    p_cc_b3.text = "• Interactive Web Dashboard: FastAPI REST backend & HTML5 canvas visualizer."
    p_cc_b3.font.size = Pt(9.5)
    p_cc_b3.font.color.rgb = SLATE_DARK

    # Right Column: Code Written & Executed Evidence (Card D)
    create_shape_card(slide2, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.6), fill_color=BLUE_LIGHT, border_color=NAVY_ACCENT)
    tb_cd = slide2.shapes.add_textbox(Inches(7.0), Inches(1.6), Inches(5.3), Inches(5.3))
    tf_cd = tb_cd.text_frame
    tf_cd.word_wrap = True

    p_cd_h = tf_cd.paragraphs[0]
    p_cd_h.text = "CODE WRITTEN & EXECUTED EVIDENCE"
    p_cd_h.font.name = "Arial"
    p_cd_h.font.size = Pt(13)
    p_cd_h.font.bold = True
    p_cd_h.font.color.rgb = NAVY_PRIMARY

    evidence_items = [
        ("• 19 / 19 Automated Tests Passing:", "tests/test_sandbox.py (8/8), test_faults.py (6/6), test_agent.py (5/5)."),
        ("• Empirical Benchmark Executed (10 Scenarios):", "scripts/run_eval.py evaluated across 10 ground-truth failures."),
        ("• Proposed Agent Results vs Baselines:", "  - Category Accuracy: 90.0% (vs Zero-Shot 60%, RAG 40%)\n  - Root-Cause Precision: 100.0% (vs Zero-Shot 40%, RAG 10%)\n  - Entity Hallucination Rate: 0.0% (vs Zero-Shot 100%)\n  - Actionable CLI Remediation: 90.0% exact syntax\n  - Efficiency: 2.0 avg tool calls / incident (budget: 6)"),
        ("• Interactive Terminal Demo Executed:", "scripts/demo.py with live ANSI streaming of ReAct traces."),
        ("• FastAPI Backend & Web Dashboard Active:", "web/server.py running on http://localhost:8000 with live canvas.")
    ]

    for title, desc in evidence_items:
        p_t = tf_cd.add_paragraph()
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY_ACCENT
        p_t.space_before = Pt(4)

        p_d = tf_cd.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = SLATE_DARK

    # =========================================================================
    # SLIDE 3: TASKS LEFT TO BE DONE
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Tasks Left to Be Done — Technical Scope & Enhancements", "SLIDE 3: REMAINING WORK SCOPE")

    tasks = [
        ("1. Live Linux Kernel & Mininet Deployment (Mode B Integration)",
         "Transition the evaluation from Windows in-memory simulation (Mode A) to a live Linux Mininet testbed running on Ubuntu 22.04 LTS / WSL2. Execute real kernel namespace commands (`ip netns exec <node> <cmd>`) and configure native Open vSwitch (OvS) flow tables and Linux traffic control (`tc netem`)."),
        
        ("2. Multi-Model Live LLM API Benchmarking & Cost Analysis",
         "Connect the prompt templates to live external LLMs via function calling (Google Gemini 1.5 Pro/Flash, OpenAI GPT-4o, and local LLaMA-3-8B). Benchmark token latency, cost per incident, and diagnostic resilience under varied sampling temperatures (T = 0.0, 0.2, 0.7)."),
        
        ("3. Multi-Hypothesis Backtracking Engine (Resolving MTU Masking)",
         "Implement an iterative backtracking algorithm to resolve metric-masking blindspots. In benchmark NET-SCN-007, packet drops caused MTU truncation to be misclassified as channel degradation; multi-hypothesis ranking will verify secondary Layer-2 attributes prior to terminating diagnosis."),
        
        ("4. Autonomous Policy & Oversight Agent (Blast-Radius Control)",
         "Design an Oversight Agent module inspired by Baddipadiga (2026) to enforce change-window policies, compute blast-radius metrics (limiting changes to < 25% of topology), and trigger automated 30-second rollbacks if verification checks fail."),
        
        ("5. Expanded Multi-Vendor Benchmark Corpus & Dynamic LLDP Discovery",
         "Scale the benchmark dataset from N = 10 to N = 50+ diverse enterprise failure scenarios across multi-switch topologies. Implement dynamic Link Layer Discovery Protocol (LLDP) and SNMP crawling to discover network graphs dynamically rather than relying on static JSON files.")
    ]

    card_top = 1.45
    card_height = 1.05
    spacing = 1.15

    for idx, (t_title, t_desc) in enumerate(tasks):
        top_pos = card_top + idx * spacing
        card = create_shape_card(slide3, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(card_height), fill_color=WHITE, border_color=CARD_BORDER)
        
        # Left Accent Bar
        accent = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(top_pos), Inches(0.15), Inches(card_height))
        accent.fill.solid()
        accent.fill.fore_color.rgb = NAVY_ACCENT if idx % 2 == 0 else RED_ACCENT
        accent.line.fill.background()

        tb = slide3.shapes.add_textbox(Inches(1.15), Inches(top_pos + 0.08), Inches(11.2), Inches(card_height - 0.16))
        tf = tb.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        p_h.text = t_title
        p_h.font.name = "Arial"
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = NAVY_PRIMARY

        p_b = tf.add_paragraph()
        p_b.text = t_desc
        p_b.font.name = "Arial"
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = SLATE_DARK
        p_b.space_before = Pt(2)

    # =========================================================================
    # SLIDE 4: EXPECTED TIMELINE OF PROJECT COMPLETION
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Expected Timeline of Project Completion — Milestone Roadmap", "SLIDE 4: PROJECT EXECUTION TIMELINE")

    # Milestone Table
    table_shape = slide4.shapes.add_table(7, 4, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.3))
    table = table_shape.table

    table.columns[0].width = Inches(2.3)
    table.columns[1].width = Inches(3.4)
    table.columns[2].width = Inches(4.2)
    table.columns[3].width = Inches(1.833)

    t_headers = ["Phase & Timeframe", "Key Milestone / Deliverable", "Technical Focus & Verification", "Target Status"]
    for idx, h_text in enumerate(t_headers):
        cell = table.cell(0, idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE

    timeline_data = [
        ("Phase 1: Present (Oct 2026)", "Mid-Term Evaluation & Core Prototype", "ReAct agent, 5 fault archetypes, 10 benchmarks, 0% hallucinations, 19/19 tests.", "COMPLETED (75%)"),
        ("Phase 2: Nov 1 – Nov 15, 2026", "Mode B Live Mininet Integration", "Deploy on Linux namespaces (`ip netns`), Open vSwitch bridges, & live NetEm.", "In Progress (Sem 7)"),
        ("Phase 3: Nov 16 – Nov 30, 2026", "Live LLM API Benchmarking", "Evaluate function calling with Gemini 1.5 & GPT-4o; complete Sem-7 project thesis.", "Pending (Sem 7 End)"),
        ("Phase 4: Dec 2026 – Jan 2027", "Multi-Hypothesis Backtracking", "Resolve MTU masking; implement compound fault injection & recovery engine.", "Planned (Sem 8 Major)"),
        ("Phase 5: Feb – Mar 2027", "Autonomous Oversight & Policy Agent", "Blast-radius limiter (< 25%), 30s automated rollback, Slack webhook notifications.", "Planned (Sem 8 Major)"),
        ("Phase 6: Apr – May 2027", "Corpus Expansion (N=50) & Defense", "Expand multi-vendor corpus; final B.Tech Major Project thesis & journal submission.", "Final Defense (Sem 8)")
    ]

    for r_idx, (t_time, t_ms, t_foc, t_stat) in enumerate(timeline_data, 1):
        row_bg = BLUE_LIGHT if r_idx % 2 == 1 else WHITE
        vals = [t_time, t_ms, t_foc, t_stat]
        for c_idx, val in enumerate(vals):
            cell = table.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = NAVY_PRIMARY
            elif c_idx == 3:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
                p.font.color.rgb = GREEN_EMERALD if "COMPLETED" in val else (NAVY_ACCENT if "In Progress" in val else SLATE_MUTED)
            else:
                p.font.color.rgb = SLATE_DARK

    # Bottom Summary Box
    summary_card = create_shape_card(slide4, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.9), fill_color=BLUE_LIGHT, border_color=NAVY_ACCENT)
    tb_sum = slide4.shapes.add_textbox(Inches(1.0), Inches(6.12), Inches(11.3), Inches(0.75))
    tf_sum = tb_sum.text_frame
    tf_sum.word_wrap = True

    p_s_h = tf_sum.paragraphs[0]
    p_s_h.text = "SUMMARY & PROJECT COMMITMENT FOR FINAL EVALUATION"
    p_s_h.font.name = "Arial"
    p_s_h.font.size = Pt(11)
    p_s_h.font.bold = True
    p_s_h.font.color.rgb = NAVY_PRIMARY

    p_s_b = tf_sum.add_paragraph()
    p_s_b.text = "All core foundations (simulation, least-privilege tools, ReAct reasoning, RAG runbooks, hallucination guardrails, and benchmark evaluation) are 100% operational today. The remaining tasks focus on live Linux kernel deployment and multi-agent policy extensions for the final major project."
    p_s_b.font.name = "Arial"
    p_s_b.font.size = Pt(9.5)
    p_s_b.font.color.rgb = SLATE_DARK

    try:
        prs.save(str(OUTPUT_PPTX))
        print(f"PowerPoint successfully created: {OUTPUT_PPTX}")
    except PermissionError:
        fallback = PROJECT_ROOT / "presentation" / "DTU_Midterm_Evaluation_Group067_Updated.pptx"
        prs.save(str(fallback))
        print(f"Original file was open in PowerPoint. Saved updated presentation to: {fallback}")

if __name__ == "__main__":
    build_presentation()

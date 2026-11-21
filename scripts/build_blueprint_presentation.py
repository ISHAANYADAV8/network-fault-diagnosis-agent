"""
Generates the B.Tech Project-I Presentation based on the exact blueprint from
'presentation/B.Tech Project-I Progress Presentation.pdf' merged with our project data.
Output: presentation/BTech_Project_I_Blueprint_Presentation.pptx
"""

import sys
from pathlib import Path
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PPTX = PROJECT_ROOT / "presentation" / "BTech_Project_I_Blueprint_Presentation.pptx"
OUTPUT_PPTX.parent.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Blueprint Color Palette
# -----------------------------------------------------------------------------
# Slide 1 (Dark Theme)
S1_BG = RGBColor(18, 32, 58)          # #12203A (Deep Dark Navy)
S1_HDR = RGBColor(126, 151, 186)      # #7E97BA (Muted Blue)
S1_TITLE = RGBColor(255, 255, 255)    # #FFFFFF (White)
S1_TAG = RGBColor(56, 189, 248)       # #38BDF8 (Sky Blue)
S1_CARD_BG = RGBColor(28, 44, 76)     # #1C2C4C (Slightly lighter navy card)
S1_MUTED = RGBColor(148, 163, 184)    # #94A3B8 (Light slate)

# Slides 2, 3, 4 (Warm Off-White Blueprint Theme)
LIGHT_BG = RGBColor(245, 244, 239)    # #F5F4EF (Warm cream/off-white)
TEXT_DARK = RGBColor(18, 32, 58)      # #12203A (Deep Slate/Navy)
TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B (Slate gray)
CARD_BG = RGBColor(255, 255, 255)     # #FFFFFF (Crisp white card)
CARD_BORDER = RGBColor(226, 232, 240) # #E2E8F0 (Subtle border)
ACCENT_BLUE = RGBColor(37, 99, 235)   # #2563EB (Royal blue)
ACCENT_GREEN = RGBColor(16, 149, 83)  # #109553 (Emerald green)
CODE_CARD_BG = RGBColor(241, 245, 249)# #F1F5F9 (Code background)
CODE_TEXT = RGBColor(30, 41, 59)      # #1E293B

def set_slide_background(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_card(slide, left, top, width, height, fill_color=CARD_BG, border_color=CARD_BORDER, radius=None):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = fill_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def build_blueprint_deck():
    print("Building B.Tech Project-I Blueprint Presentation...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE, GROUP NUMBER, TEAM MEMBERS & SUPERVISOR (DARK THEME)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, S1_BG)

    # Header Department Tag
    tb_h = slide1.shapes.add_textbox(Inches(0.9), Inches(0.65), Inches(11.5), Inches(0.4))
    p_h = tb_h.text_frame.paragraphs[0]
    p_h.text = "Delhi Technological University  ·  Department of Information Technology"
    p_h.font.name = "Arial"
    p_h.font.size = Pt(12)
    p_h.font.bold = True
    p_h.font.color.rgb = S1_HDR

    # Main Project Title
    tb_title = slide1.shapes.add_textbox(Inches(0.9), Inches(1.15), Inches(11.5), Inches(1.8))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_t = tf_title.paragraphs[0]
    p_t.text = "Topology-Aware Tool-Using LLM Agent for\nAutomated Network Fault Diagnosis and Root-Cause Analysis"
    p_t.font.name = "Arial"
    p_t.font.size = Pt(28)
    p_t.font.bold = True
    p_t.font.color.rgb = S1_TITLE
    p_t.line_spacing = 1.15

    # Course & Group Tag
    tb_tag = slide1.shapes.add_textbox(Inches(0.9), Inches(3.1), Inches(11.5), Inches(0.4))
    p_tag = tb_tag.text_frame.paragraphs[0]
    p_tag.text = "IT-401 B.Tech Project-I  ·  Progress presentation  ·  Group 067"
    p_tag.font.name = "Arial"
    p_tag.font.size = Pt(13)
    p_tag.font.bold = True
    p_tag.font.color.rgb = S1_TAG

    # Divider Line
    line1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(3.65), Inches(11.5), Inches(0.02))
    line1.fill.solid()
    line1.fill.fore_color.rgb = RGBColor(40, 60, 95)
    line1.line.fill.background()

    # Left Container: Team Members
    add_card(slide1, Inches(0.9), Inches(3.95), Inches(6.8), Inches(2.9), fill_color=S1_CARD_BG, border_color=None)
    tb_m_hdr = slide1.shapes.add_textbox(Inches(1.15), Inches(4.1), Inches(6.3), Inches(0.35))
    pm_h = tb_m_hdr.text_frame.paragraphs[0]
    pm_h.text = "TEAM MEMBERS"
    pm_h.font.name = "Arial"
    pm_h.font.size = Pt(11)
    pm_h.font.bold = True
    pm_h.font.color.rgb = S1_HDR

    members = [
        ("Harshit Vaish", "23/IT/067"),
        ("Harshvardhan Kumar Arya", "23/IT/068"),
        ("Ishaan Yadav", "23/IT/073")
    ]
    tb_mb = slide1.shapes.add_textbox(Inches(1.15), Inches(4.5), Inches(6.3), Inches(2.1))
    tf_mb = tb_mb.text_frame
    for idx, (m_name, m_roll) in enumerate(members):
        p = tf_mb.paragraphs[0] if idx == 0 else tf_mb.add_paragraph()
        p.text = f"{m_name}    "
        r1 = p.runs[0]
        r1.font.name = "Arial"
        r1.font.size = Pt(14)
        r1.font.bold = True
        r1.font.color.rgb = S1_TITLE
        
        r2 = p.add_run()
        r2.text = m_roll
        r2.font.name = "Arial"
        r2.font.size = Pt(13)
        r2.font.color.rgb = S1_MUTED
        p.space_after = Pt(12)

    # Right Container: Project Supervisor
    add_card(slide1, Inches(8.0), Inches(3.95), Inches(4.4), Inches(2.9), fill_color=S1_CARD_BG, border_color=None)
    tb_s_hdr = slide1.shapes.add_textbox(Inches(8.25), Inches(4.1), Inches(3.9), Inches(0.35))
    ps_h = tb_s_hdr.text_frame.paragraphs[0]
    ps_h.text = "PROJECT SUPERVISOR"
    ps_h.font.name = "Arial"
    ps_h.font.size = Pt(11)
    ps_h.font.bold = True
    ps_h.font.color.rgb = S1_HDR

    tb_sb = slide1.shapes.add_textbox(Inches(8.25), Inches(4.5), Inches(3.9), Inches(2.0))
    tf_sb = tb_sb.text_frame
    p_sup_name = tf_sb.paragraphs[0]
    p_sup_name.text = "Dr. Anamika Chauhan"
    p_sup_name.font.name = "Arial"
    p_sup_name.font.size = Pt(17)
    p_sup_name.font.bold = True
    p_sup_name.font.color.rgb = S1_TITLE
    p_sup_name.space_after = Pt(6)

    p_sup_affil = tf_sb.add_paragraph()
    p_sup_affil.text = "Department of Information Technology\nDelhi Technological University"
    p_sup_affil.font.name = "Arial"
    p_sup_affil.font.size = Pt(12)
    p_sup_affil.font.color.rgb = S1_MUTED

    # =========================================================================
    # SLIDE 2: PROGRESS SO FAR (BLUEPRINT LAYOUT)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, LIGHT_BG)

    # Slide Title
    tb_s2_t = slide2.shapes.add_textbox(Inches(0.9), Inches(0.45), Inches(11.5), Inches(0.6))
    p_s2_t = tb_s2_t.text_frame.paragraphs[0]
    p_s2_t.text = "Progress so far"
    p_s2_t.font.name = "Arial"
    p_s2_t.font.size = Pt(24)
    p_s2_t.font.bold = True
    p_s2_t.font.color.rgb = TEXT_DARK

    # Left Column: Scope Badge & Progress Breakdown
    # Large Badge Card
    add_card(slide2, Inches(0.9), Inches(1.2), Inches(5.4), Inches(1.4), fill_color=CARD_BG)
    tb_scope = slide2.shapes.add_textbox(Inches(1.1), Inches(1.28), Inches(5.0), Inches(1.2))
    tf_scope = tb_scope.text_frame
    p_sc1 = tf_scope.paragraphs[0]
    p_sc1.text = "≈65%"
    p_sc1.font.name = "Arial"
    p_sc1.font.size = Pt(36)
    p_sc1.font.bold = True
    p_sc1.font.color.rgb = TEXT_DARK

    p_sc2 = tf_scope.add_paragraph()
    p_sc2.text = "of planned scope complete, estimated against the synopsis goals"
    p_sc2.font.name = "Arial"
    p_sc2.font.size = Pt(11)
    p_sc2.font.color.rgb = TEXT_MUTED

    # Progress Breakdown List Card
    add_card(slide2, Inches(0.9), Inches(2.75), Inches(5.4), Inches(4.2), fill_color=CARD_BG)
    tb_bdown = slide2.shapes.add_textbox(Inches(1.15), Inches(2.9), Inches(4.9), Inches(3.9))
    tf_bdown = tb_bdown.text_frame

    p_bd_h = tf_bdown.paragraphs[0]
    p_bd_h.text = "MILESTONE COMPLETION STATUS"
    p_bd_h.font.name = "Arial"
    p_bd_h.font.size = Pt(10.5)
    p_bd_h.font.bold = True
    p_bd_h.font.color.rgb = ACCENT_BLUE
    p_bd_h.space_after = Pt(8)

    progress_items = [
        ("Literature review", "70%", "Surveyed 20+ papers (ReAct, AIOps, Baddipadiga)"),
        ("Testbed and 10 fault scenarios", "85%", "[Harshit 23/IT/067] Dual-mode sandbox & 5 archetypes"),
        ("Baselines, RAG and ReAct agent", "75%", "[Harshvardhan 23/IT/068] ReAct loop & 0% hallucination"),
        ("Evaluation and analysis", "45%", "[Ishaan 23/IT/073] Benchmark runner & MTU analysis"),
        ("Paper, report and demo", "50%", "Full .docx paper, rich CLI demo & web dashboard")
    ]

    for item, pct, note in progress_items:
        p_row = tf_bdown.add_paragraph()
        p_row.text = f"{item}  —  "
        r_item = p_row.runs[0]
        r_item.font.name = "Arial"
        r_item.font.size = Pt(11)
        r_item.font.bold = True
        r_item.font.color.rgb = TEXT_DARK
        
        r_pct = p_row.add_run()
        r_pct.text = pct
        r_pct.font.name = "Arial"
        r_pct.font.size = Pt(11)
        r_pct.font.bold = True
        r_pct.font.color.rgb = ACCENT_GREEN

        p_note = tf_bdown.add_paragraph()
        p_note.text = f"  ↳ {note}"
        p_note.font.name = "Arial"
        p_note.font.size = Pt(9.5)
        p_note.font.color.rgb = TEXT_MUTED
        p_note.space_after = Pt(6)

    # Right Column: Code Written and Executed + Benchmark Table
    # Code Execution Box (Terminal Style)
    add_card(slide2, Inches(6.6), Inches(1.2), Inches(5.8), Inches(2.75), fill_color=CODE_CARD_BG, border_color=CARD_BORDER)
    tb_code = slide2.shapes.add_textbox(Inches(6.8), Inches(1.3), Inches(5.4), Inches(2.55))
    tf_code = tb_code.text_frame

    p_code_h = tf_code.paragraphs[0]
    p_code_h.text = "Code written and executed"
    p_code_h.font.name = "Arial"
    p_code_h.font.size = Pt(11.5)
    p_code_h.font.bold = True
    p_code_h.font.color.rgb = TEXT_DARK
    p_code_h.space_after = Pt(4)

    code_lines = [
        ("$ python tests/test_sandbox.py", "ALL PHASE 1 TESTS PASSED (8/8)"),
        ("$ python tests/test_faults.py", "ALL PHASE 2 TESTS PASSED (6/6)"),
        ("$ python tests/test_agent.py", "ALL PHASE 3 TESTS PASSED (5/5)"),
        ("$ python scripts/run_eval.py", "10 scenarios scored, results saved")
    ]
    for cmd, res in code_lines:
        p_c = tf_code.add_paragraph()
        p_c.text = cmd
        p_c.font.name = "Consolas"
        p_c.font.size = Pt(10)
        p_c.font.color.rgb = ACCENT_BLUE

        p_r = tf_code.add_paragraph()
        p_r.text = f"  ✓ {res}"
        p_r.font.name = "Consolas"
        p_r.font.size = Pt(9.5)
        p_r.font.color.rgb = ACCENT_GREEN
        p_r.space_after = Pt(2)

    # Benchmark Table Box
    add_card(slide2, Inches(6.6), Inches(4.1), Inches(5.8), Inches(2.85), fill_color=CARD_BG)
    tb_tbl_h = slide2.shapes.add_textbox(Inches(6.8), Inches(4.2), Inches(5.4), Inches(0.3))
    p_th = tb_tbl_h.text_frame.paragraphs[0]
    p_th.text = "EMPIRICAL BENCHMARK EVALUATION (N = 10 SCENARIOS)"
    p_th.font.name = "Arial"
    p_th.font.size = Pt(10)
    p_th.font.bold = True
    p_th.font.color.rgb = ACCENT_BLUE

    # Table
    t_shape = slide2.shapes.add_table(4, 4, Inches(6.8), Inches(4.55), Inches(5.4), Inches(1.8))
    table = t_shape.table
    table.columns[0].width = Inches(2.1)
    table.columns[1].width = Inches(1.1)
    table.columns[2].width = Inches(1.1)
    table.columns[3].width = Inches(1.1)

    t_hdrs = ["System", "Fault acc.", "Halluc.", "Fix acc."]
    for c_i, h in enumerate(t_hdrs):
        cell = table.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = TEXT_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        if c_i > 0:
            p.alignment = PP_ALIGN.CENTER

    t_rows = [
        ("Zero-shot LLM", "60%", "100%", "20%"),
        ("Static RAG + LLM", "40%", "30%", "70%"),
        ("AutoNet agent", "90%", "0%", "90%")
    ]
    for r_i, r_data in enumerate(t_rows, 1):
        bg_col = RGBColor(241, 245, 249) if r_i % 2 == 1 else RGBColor(255, 255, 255)
        for c_i, val in enumerate(r_data):
            cell = table.cell(r_i, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            if c_i == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_DARK
            else:
                p.alignment = PP_ALIGN.CENTER
                if r_i == 3:
                    p.font.bold = True
                    p.font.color.rgb = ACCENT_GREEN
                else:
                    p.font.color.rgb = TEXT_MUTED

    # Bottom summary tag
    tb_foot = slide2.shapes.add_textbox(Inches(6.8), Inches(6.45), Inches(5.4), Inches(0.4))
    p_ft = tb_foot.text_frame.paragraphs[0]
    p_ft.text = "About 2,000 lines of Python across src, web and scripts · 19 of 19 tests passing"
    p_ft.font.name = "Arial"
    p_ft.font.size = Pt(9.5)
    p_ft.font.italic = True
    p_ft.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 3: TASKS LEFT TO BE DONE (6-CARD BLUEPRINT GRID)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, LIGHT_BG)

    tb_s3_t = slide3.shapes.add_textbox(Inches(0.9), Inches(0.45), Inches(11.5), Inches(0.6))
    p_s3_t = tb_s3_t.text_frame.paragraphs[0]
    p_s3_t.text = "Tasks left to be done"
    p_s3_t.font.name = "Arial"
    p_s3_t.font.size = Pt(24)
    p_s3_t.font.bold = True
    p_s3_t.font.color.rgb = TEXT_DARK

    tasks_grid = [
        ("01 · AGENT", "Live LLM integration", "Replace the deterministic state machine with Gemini / GPT-4o function calling; test several temperatures."),
        ("02 · BASELINES", "Complete baselines", "Add the rule-based baseline from the synopsis; run LLM-only and LLM + RAG on live models."),
        ("03 · TESTBED", "Live Mininet testbed", "Run Mode B on Ubuntu / WSL2 with Open vSwitch; measure real tool latency and response time."),
        ("04 · ANALYSIS", "Ablation and error study", "Isolate topology, RAG and tool access; add backtracking to fix the MTU miss (NET-SCN-007)."),
        ("05 · BENCHMARK", "Larger benchmark", "Grow from 10 to 50+ scenarios, adding multi-fault cases and noisy telemetry."),
        ("06 · WRITE-UP", "Paper, report and demo", "Review 5–10 recent (2025–26) papers; finalise the research paper, project report and demo.")
    ]

    # 3 columns x 2 rows
    c_w = 3.65
    c_h = 2.45
    col_x = [0.9, 4.8, 8.7]
    row_y = [1.25, 4.1]

    for idx, (cat, title, desc) in enumerate(tasks_grid):
        r_idx = idx // 3
        c_idx = idx % 3
        x = col_x[c_idx]
        y = row_y[r_idx]

        add_card(slide3, Inches(x), Inches(y), Inches(c_w), Inches(c_h), fill_color=CARD_BG)

        tb_card = slide3.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.18), Inches(c_w - 0.4), Inches(c_h - 0.36))
        tf_c = tb_card.text_frame
        tf_c.word_wrap = True

        p_cat = tf_c.paragraphs[0]
        p_cat.text = cat
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE
        p_cat.space_after = Pt(4)

        p_title = tf_c.add_paragraph()
        p_title.text = title
        p_title.font.name = "Arial"
        p_title.font.size = Pt(13)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_DARK
        p_title.space_after = Pt(8)

        p_desc = tf_c.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = "Arial"
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = TEXT_MUTED
        p_desc.line_spacing = 1.15

    # =========================================================================
    # SLIDE 4: EXPECTED TIMELINE OF COMPLETION (5-STAGE BLUEPRINT FLOW)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, LIGHT_BG)

    tb_s4_t = slide4.shapes.add_textbox(Inches(0.9), Inches(0.45), Inches(11.5), Inches(0.6))
    p_s4_t = tb_s4_t.text_frame.paragraphs[0]
    p_s4_t.text = "Expected timeline of completion"
    p_s4_t.font.name = "Arial"
    p_s4_t.font.size = Pt(24)
    p_s4_t.font.bold = True
    p_s4_t.font.color.rgb = TEXT_DARK

    timeline_items = [
        ("Nov 2026", "Project-I close-out", "Project-I wrap-up", "Rule-based baseline, 5–10 recent papers, project report and demo."),
        ("Jan–Feb 2027", "Semester 8 · month 1–2", "Live Mininet testbed", "Mode B on Ubuntu / WSL2 with Open vSwitch; re-run all 10 scenarios."),
        ("Feb–Mar 2027", "Semester 8 · month 2–3", "Live LLM evaluation", "Gemini / GPT-4o function calling, temperature sweep, cost, latency."),
        ("Mar–Apr 2027", "Semester 8 · month 3–4", "Ablation and larger benchmark", "Ablation, MTU backtracking fix, 50+ scenarios incl. multi-fault."),
        ("Apr–May 2027", "Semester 8 · month 4–5", "Paper, final report, demo", "Final report, research paper for a peer-reviewed venue, demo.")
    ]

    t_y = 1.25
    t_h = 1.05
    t_gap = 0.15

    for idx, (t_date, t_stage, t_title, t_desc) in enumerate(timeline_items):
        y = t_y + idx * (t_h + t_gap)

        # Card container
        add_card(slide4, Inches(0.9), Inches(y), Inches(11.533), Inches(t_h), fill_color=CARD_BG)

        # Left Date Box
        tb_date = slide4.shapes.add_textbox(Inches(1.1), Inches(y + 0.15), Inches(2.3), Inches(0.75))
        tf_date = tb_date.text_frame
        p_d1 = tf_date.paragraphs[0]
        p_d1.text = t_date
        p_d1.font.name = "Arial"
        p_d1.font.size = Pt(13)
        p_d1.font.bold = True
        p_d1.font.color.rgb = ACCENT_BLUE

        p_d2 = tf_date.add_paragraph()
        p_d2.text = t_stage
        p_d2.font.name = "Arial"
        p_d2.font.size = Pt(9.5)
        p_d2.font.color.rgb = TEXT_MUTED

        # Vertical separator line
        sep = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.6), Inches(y + 0.15), Inches(0.02), Inches(t_h - 0.3))
        sep.fill.solid()
        sep.fill.fore_color.rgb = CARD_BORDER
        sep.line.fill.background()

        # Right Content Box
        tb_desc = slide4.shapes.add_textbox(Inches(3.8), Inches(y + 0.12), Inches(8.3), Inches(0.8))
        tf_desc = tb_desc.text_frame
        tf_desc.word_wrap = True

        p_t1 = tf_desc.paragraphs[0]
        p_t1.text = t_title
        p_t1.font.name = "Arial"
        p_t1.font.size = Pt(12)
        p_t1.font.bold = True
        p_t1.font.color.rgb = TEXT_DARK
        p_t1.space_after = Pt(2)

        p_t2 = tf_desc.add_paragraph()
        p_t2.text = t_desc
        p_t2.font.name = "Arial"
        p_t2.font.size = Pt(10)
        p_t2.font.color.rgb = TEXT_MUTED

    # Bottom commitment callout
    add_card(slide4, Inches(0.9), Inches(6.35), Inches(11.533), Inches(0.75), fill_color=CODE_CARD_BG, border_color=CARD_BORDER)
    tb_foot4 = slide4.shapes.add_textbox(Inches(1.1), Inches(6.42), Inches(11.1), Inches(0.6))
    p_f4 = tb_foot4.text_frame.paragraphs[0]
    p_f4.text = "Committed Milestones: Project-I close-out in November 2026, followed by live Linux kernel deployment and multi-agent expansion in Semester 8."
    p_f4.font.name = "Arial"
    p_f4.font.size = Pt(10)
    p_f4.font.italic = True
    p_f4.font.color.rgb = TEXT_DARK

    try:
        prs.save(str(OUTPUT_PPTX))
        print(f"Blueprint PowerPoint generated successfully: {OUTPUT_PPTX}")
    except PermissionError:
        fallback = OUTPUT_PPTX.with_name(OUTPUT_PPTX.stem + "_v2.pptx")
        prs.save(str(fallback))
        print(f"File locked by PowerPoint. Saved to fallback: {fallback}")

if __name__ == "__main__":
    build_blueprint_deck()

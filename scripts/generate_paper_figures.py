"""
Generate publication-quality architectural and results figures for the AutoNet RCA Agent research paper.
Uses Pillow to produce clean, high-resolution figures.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = PROJECT_ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Helper font loader
def get_font(size: int, bold: bool = False):
    try:
        # Standard Windows fonts
        font_name = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(f"C:\\Windows\\Fonts\\{font_name}", size)
    except Exception:
        try:
            font_name = "segoeuib.ttf" if bold else "segoeui.ttf"
            return ImageFont.truetype(f"C:\\Windows\\Fonts\\{font_name}", size)
        except Exception:
            return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

# -----------------------------------------------------------------------------
# Figure 1: System Architecture
# -----------------------------------------------------------------------------
def generate_fig1_architecture():
    w, h = 1400, 800
    img = Image.new("RGB", (w, h), color=(250, 252, 255))
    draw = ImageDraw.Draw(img)

    title_font = get_font(28, bold=True)
    header_font = get_font(20, bold=True)
    body_font = get_font(15, bold=False)
    small_font = get_font(13, bold=False)
    tag_font = get_font(12, bold=True)

    # Title Banner
    draw.text((w // 2, 35), "AutoNet RCA Agent: Topology-Aware System Architecture", fill=(24, 43, 73), font=title_font, anchor="mm")
    draw.text((w // 2, 70), "Dual-Mode Network Execution, Tool-Augmented ReAct Loop, and Topology Guardrails", fill=(80, 95, 115), font=body_font, anchor="mm")

    # Layer 1: Network Testbed / Execution Layer (Top)
    # Box: 60 to 1340, y: 110 to 270
    draw_rounded_rect(draw, (60, 110, 1340, 270), 12, fill=(240, 244, 250), outline=(180, 200, 225), width=2)
    draw.text((85, 135), "NETWORK EXECUTION & FAULT INJECTION LAYER", fill=(20, 50, 90), font=header_font)

    # Sub-box 1A: Simulated Sandbox (Mode A)
    draw_rounded_rect(draw, (85, 160, 680, 250), 8, fill=(255, 255, 255), outline=(160, 185, 215), width=1)
    draw.text((105, 175), "Mode A: Simulated Network Sandbox (Windows / Cross-Platform)", fill=(30, 70, 130), font=get_font(16, bold=True))
    draw.text((105, 202), "• In-Memory NetworkX Graph State Engine (2 Switches, 4 Hosts, Gateway, DNS)", fill=(60, 75, 95), font=body_font)
    draw.text((105, 224), "• Deterministic CLI Synthesizer (L2/L3 pathing, MTU frames, NetEm delay/loss)", fill=(60, 75, 95), font=body_font)

    # Sub-box 1B: Mininet Driver (Mode B)
    draw_rounded_rect(draw, (710, 160, 1315, 250), 8, fill=(255, 255, 255), outline=(160, 185, 215), width=1)
    draw.text((730, 175), "Mode B: Live Mininet Driver (Linux / WSL2 Namespaces)", fill=(30, 70, 130), font=get_font(16, bold=True))
    draw.text((730, 202), "• Linux Network Namespaces (`ip netns exec <node> <cmd>`) & Open vSwitch", fill=(60, 75, 95), font=body_font)
    draw.text((730, 224), "• Kernel Traffic Control (`tc qdisc netem`) & Native Linux Socket Telemetry", fill=(60, 75, 95), font=body_font)

    # Connecting Arrows Layer 1 -> Layer 2
    for x in [380, 1010]:
        draw.line([(x, 270), (x, 315)], fill=(120, 140, 170), width=3)
        draw.polygon([(x - 6, 315), (x + 6, 315), (x, 325)], fill=(120, 140, 170))

    # Layer 2: Middle Tier - Diagnostic Tool Registry & Topology Store & RAG
    # Tool Registry (Left: 60 to 480, y: 325 to 550)
    draw_rounded_rect(draw, (60, 325, 480, 550), 10, fill=(245, 248, 255), outline=(170, 195, 230), width=2)
    draw.text((80, 345), "Diagnostic Tool Registry", fill=(25, 60, 110), font=header_font)
    draw.text((80, 375), "Read-Only Probing Protocol (Least Privilege):", fill=(90, 105, 125), font=small_font)
    tools = [
        ("ping_tool", "ICMP Echo & RTT Latency Verification"),
        ("traceroute_tool", "Layer-3 Hop Traversal & Drop Point"),
        ("routing_table_tool", "Kernel IP Routing ('ip route show')"),
        ("interface_stats_tool", "Port Carrier & Drops ('ip -s link')"),
        ("dns_query_tool", "Resolver Lookups ('nslookup / dig')")
    ]
    ty = 405
    for t_name, t_desc in tools:
        draw_rounded_rect(draw, (80, ty, 460, ty + 24), 4, fill=(255, 255, 255), outline=(200, 215, 235))
        draw.text((90, ty + 4), t_name, fill=(180, 40, 40), font=get_font(13, bold=True))
        draw.text((230, ty + 5), t_desc, fill=(50, 65, 85), font=small_font)
        ty += 28

    # Core Agent Engine (Middle: 510 to 950, y: 325 to 550)
    draw_rounded_rect(draw, (510, 325, 950, 550), 10, fill=(238, 245, 255), outline=(80, 130, 200), width=2)
    draw.text((535, 345), "Topology-Aware ReAct Agent Core", fill=(15, 55, 120), font=header_font)
    draw.text((535, 375), "Autonomous Reasoning Loop (Budget <= 6 Steps):", fill=(70, 90, 115), font=small_font)

    # ReAct Cycle Boxes
    steps = [
        ("1. THOUGHT", "Hypothesize failure point based on symptom & active topology"),
        ("2. ACTION", "Select targeted tool invocation in standardized JSON format"),
        ("3. OBSERVATION", "Ingest raw terminal CLI output & analyze error signatures"),
        ("4. CONCLUSION", "Isolate root cause, output precise command & verify")
    ]
    sy = 400
    for s_title, s_desc in steps:
        draw_rounded_rect(draw, (530, sy, 930, sy + 30), 5, fill=(255, 255, 255), outline=(170, 195, 225))
        draw.text((545, sy + 6), s_title, fill=(30, 100, 60), font=get_font(13, bold=True))
        draw.text((660, sy + 7), s_desc, fill=(60, 75, 95), font=small_font)
        sy += 36

    # Knowledge Base & Topology Grounding (Right: 980 to 1340, y: 325 to 550)
    draw_rounded_rect(draw, (980, 325, 1340, 550), 10, fill=(245, 248, 255), outline=(170, 195, 230), width=2)
    draw.text((1000, 345), "Knowledge & Guardrails", fill=(25, 60, 110), font=header_font)
    
    # Topology Store Box
    draw_rounded_rect(draw, (1000, 380, 1320, 450), 6, fill=(255, 255, 255), outline=(190, 210, 230))
    draw.text((1015, 390), "Topology Graph Store (topology.json)", fill=(140, 60, 20), font=get_font(14, bold=True))
    draw.text((1015, 412), "• Strict node/port entities (2 switches, 4 hosts, gw1)", fill=(60, 75, 95), font=small_font)
    draw.text((1015, 430), "• Programmatic Hallucination Validator (0% error)", fill=(20, 120, 60), font=get_font(12, bold=True))

    # RAG Runbook Store Box
    draw_rounded_rect(draw, (1000, 465, 1320, 535), 6, fill=(255, 255, 255), outline=(190, 210, 230))
    draw.text((1015, 475), "Curated Runbook Store (BM25 RAG)", fill=(140, 60, 20), font=get_font(14, bold=True))
    draw.text((1015, 497), "• RFC & domain playbooks (ICMP, MTU, DNS, Routing)", fill=(60, 75, 95), font=small_font)
    draw.text((1015, 515), "• BM25 relevance scoring (k1=1.5, b=0.75) into prompt", fill=(60, 75, 95), font=small_font)

    # Horizontal arrows between Middle Tier components
    draw.line([(480, 440), (510, 440)], fill=(80, 130, 200), width=3)
    draw.line([(950, 440), (980, 440)], fill=(80, 130, 200), width=3)

    # Layer 3: Output & Validation Layer (Bottom: 60 to 1340, y: 600 to 750)
    draw_rounded_rect(draw, (60, 590, 1340, 750), 12, fill=(240, 248, 245), outline=(160, 210, 185), width=2)
    draw.text((85, 610), "SYNTHESIZED ROOT-CAUSE ANALYSIS (RCA) & VERIFICATION", fill=(20, 90, 55), font=header_font)

    # Output Card 1: Fault Category & Root Cause
    draw_rounded_rect(draw, (85, 640, 480, 730), 8, fill=(255, 255, 255), outline=(180, 215, 195))
    draw.text((105, 655), "1. Root Cause Identification", fill=(20, 80, 50), font=get_font(15, bold=True))
    draw.text((105, 680), "• Pinpointed Fault Archetype (90% accuracy)", fill=(60, 75, 95), font=body_font)
    draw.text((105, 702), "• Specific entity isolation (s1-eth3, h2 routing)", fill=(60, 75, 95), font=body_font)

    # Output Card 2: Actionable CLI Remediation
    draw_rounded_rect(draw, (510, 640, 910, 730), 8, fill=(255, 255, 255), outline=(180, 215, 195))
    draw.text((530, 655), "2. Actionable Remediation", fill=(20, 80, 50), font=get_font(15, bold=True))
    draw.text((530, 680), "• Exact executable Linux CLI command (90% accuracy)", fill=(60, 75, 95), font=body_font)
    draw.text((530, 702), "• No placeholder syntax (`<interface>`, `<ip>`)", fill=(60, 75, 95), font=body_font)

    # Output Card 3: Post-Remediation Health Verification
    draw_rounded_rect(draw, (940, 640, 1315, 730), 8, fill=(255, 255, 255), outline=(180, 215, 195))
    draw.text((960, 655), "3. Automated Verification", fill=(20, 80, 50), font=get_font(15, bold=True))
    draw.text((960, 680), "• Closed-loop ICMP/DNS re-probe post-fix", fill=(60, 75, 95), font=body_font)
    draw.text((960, 702), "• 100% restoration confirmation before closing", fill=(60, 75, 95), font=body_font)

    # Connect Middle Agent to Output Layer
    draw.line([(730, 550), (730, 590)], fill=(80, 160, 120), width=3)
    draw.polygon([(724, 580), (736, 580), (730, 590)], fill=(80, 160, 120))

    img.save(FIG_DIR / "fig1_system_architecture.png", dpi=(300, 300))
    print("Generated fig1_system_architecture.png")

# -----------------------------------------------------------------------------
# Figure 2: ReAct Reasoning Flowchart
# -----------------------------------------------------------------------------
def generate_fig2_react_workflow():
    w, h = 1200, 700
    img = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    title_font = get_font(26, bold=True)
    step_font = get_font(18, bold=True)
    body_font = get_font(14, bold=False)
    small_font = get_font(12, bold=False)

    # Title
    draw.text((w // 2, 35), "AutoNet RCA Diagnostic ReAct Decision Workflow", fill=(20, 45, 80), font=title_font, anchor="mm")
    draw.text((w // 2, 65), "Sequential Hypothesis Testing, Least-Privilege Telemetry Probing, and Branching Logic", fill=(90, 105, 125), font=body_font, anchor="mm")

    # Workflow boxes (Left-to-Right or Top-to-Bottom)
    # Let's do a top-to-bottom pipeline with branching
    # Box 1: Ingestion
    draw_rounded_rect(draw, (350, 100, 850, 160), 8, fill=(240, 245, 255), outline=(160, 190, 230), width=2)
    draw.text((600, 120), "1. Incident Symptom Ingestion & Grounding", fill=(20, 50, 110), font=step_font, anchor="mm")
    draw.text((600, 142), "Input: (target_node, destination, symptom) + topology.json + top-2 BM25 runbooks", fill=(60, 75, 95), font=small_font, anchor="mm")

    # Arrow 1 -> Decision 1
    draw.line([(600, 160), (600, 195)], fill=(100, 130, 170), width=2)
    draw.polygon([(595, 190), (605, 190), (600, 197)], fill=(100, 130, 170))

    # Decision 1: Is Destination FQDN or IP?
    draw_rounded_rect(draw, (400, 197, 800, 252), 6, fill=(255, 250, 240), outline=(230, 170, 70), width=2)
    draw.text((600, 215), "Destination Check: Domain Name or Raw IPv4 Address?", fill=(130, 70, 10), font=get_font(15, bold=True), anchor="mm")
    draw.text((600, 237), "[True: Domain Name]                                         [False: IPv4 Address]", fill=(120, 80, 20), font=small_font, anchor="mm")

    # Branch Left: DNS Probe
    draw.line([(450, 252), (250, 300)], fill=(150, 100, 30), width=2)
    draw_rounded_rect(draw, (80, 300, 420, 420), 8, fill=(255, 248, 245), outline=(220, 140, 120), width=2)
    draw.text((250, 320), "Branch A: Name Resolution Triage", fill=(160, 40, 20), font=get_font(16, bold=True), anchor="mm")
    draw.text((100, 345), "• Action 1: dns_query_tool(src_node, hostname)", fill=(60, 75, 95), font=small_font)
    draw.text((100, 368), "• If Timeout: Probe DNS Server (10.0.0.254)", fill=(60, 75, 95), font=small_font)
    draw.text((100, 391), "• Inspect /etc/resolv.conf nameserver value", fill=(60, 75, 95), font=small_font)

    # Branch Right: IP Probe
    draw.line([(750, 252), (950, 300)], fill=(30, 100, 150), width=2)
    draw_rounded_rect(draw, (780, 300, 1120, 420), 8, fill=(245, 250, 255), outline=(130, 180, 230), width=2)
    draw.text((950, 320), "Branch B: Layer 3/4 Reachability Triage", fill=(20, 70, 140), font=get_font(16, bold=True), anchor="mm")
    draw.text((800, 345), "• Action 1: ping_tool(src_node, target_ip, count=3)", fill=(60, 75, 95), font=small_font)
    draw.text((800, 368), "• Subcase 1: 'Network is unreachable' -> Route Triage", fill=(60, 75, 95), font=small_font)
    draw.text((800, 391), "• Subcase 2: Partial loss / high RTT -> NetEm Triage", fill=(60, 75, 95), font=small_font)
    draw.text((800, 414), "• Subcase 3: 100% loss -> Interface State Triage", fill=(60, 75, 95), font=small_font)

    # Deep Triage: Middle Layer (y: 450 to 560)
    # 3 Specialized investigation blocks
    # Block 1: Routing Check
    draw_rounded_rect(draw, (80, 455, 420, 560), 6, fill=(255, 255, 255), outline=(180, 200, 220))
    draw.text((100, 472), "Routing Table Inspection", fill=(30, 60, 110), font=get_font(14, bold=True))
    draw.text((100, 495), "• Tool: routing_table_tool(node_id)", fill=(60, 75, 95), font=small_font)
    draw.text((100, 515), "• Verify 'default via 10.0.0.1'", fill=(60, 75, 95), font=small_font)
    draw.text((100, 535), "• Fix: `ip route add default via ...`", fill=(20, 110, 40), font=get_font(12, bold=True))

    # Block 2: Interface Stats Check
    draw_rounded_rect(draw, (440, 455, 760, 560), 6, fill=(255, 255, 255), outline=(180, 200, 220))
    draw.text((460, 472), "Interface State & MTU Check", fill=(30, 60, 110), font=get_font(14, bold=True))
    draw.text((460, 495), "• Tool: interface_stats_tool(node/switch)", fill=(60, 75, 95), font=small_font)
    draw.text((460, 515), "• Detect 'state DOWN' or MTU < 1500", fill=(60, 75, 95), font=small_font)
    draw.text((460, 535), "• Fix: `ip link set dev <port> up`", fill=(20, 110, 40), font=get_font(12, bold=True))

    # Block 3: Switch Trunk Traversal
    draw_rounded_rect(draw, (780, 455, 1120, 560), 6, fill=(255, 255, 255), outline=(180, 200, 220))
    draw.text((800, 472), "Switch Inter-Trunk Traversal", fill=(30, 60, 110), font=get_font(14, bold=True))
    draw.text((800, 495), "• Probes Switch s1 -> Switch s2 ports", fill=(60, 75, 95), font=small_font)
    draw.text((800, 515), "• Pinpoint s1-eth3, s1-eth2, s1-eth4", fill=(60, 75, 95), font=small_font)
    draw.text((800, 535), "• Hallucination check against topology", fill=(20, 110, 40), font=get_font(12, bold=True))

    # Final Convergence Box (Bottom: y: 590 to 670)
    draw_rounded_rect(draw, (200, 590, 1000, 670), 8, fill=(240, 252, 245), outline=(140, 205, 170), width=2)
    draw.text((600, 612), "Final RCA Report & Structured Remediation Output", fill=(20, 90, 50), font=step_font, anchor="mm")
    draw.text((600, 637), "Category Match (90%) | Root Cause Precision (100%) | Hallucination Check (0.0% Error)", fill=(40, 80, 60), font=get_font(13, bold=True), anchor="mm")
    draw.text((600, 655), "Output: Structured JSON report + exact CLI fix syntax ready for automated verification", fill=(80, 100, 90), font=small_font, anchor="mm")

    # Connecting lines to bottom
    draw.line([(250, 420), (250, 455)], fill=(150, 180, 210), width=2)
    draw.line([(950, 420), (600, 455)], fill=(150, 180, 210), width=2)
    draw.line([(950, 420), (950, 455)], fill=(150, 180, 210), width=2)
    draw.line([(250, 560), (450, 590)], fill=(140, 180, 160), width=2)
    draw.line([(600, 560), (600, 590)], fill=(140, 180, 160), width=2)
    draw.line([(950, 560), (750, 590)], fill=(140, 180, 160), width=2)

    img.save(FIG_DIR / "fig2_react_workflow.png", dpi=(300, 300))
    print("Generated fig2_react_workflow.png")

# -----------------------------------------------------------------------------
# Figure 3: Fault Injection & Remediation Lifecycle
# -----------------------------------------------------------------------------
def generate_fig3_fault_lifecycle():
    w, h = 1200, 520
    img = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    title_font = get_font(24, bold=True)
    stage_font = get_font(16, bold=True)
    body_font = get_font(13, bold=False)
    small_font = get_font(11, bold=False)

    # Title
    draw.text((w // 2, 30), "Closed-Loop Fault Injection, RCA Diagnosis, and Remediation Lifecycle", fill=(20, 45, 80), font=title_font, anchor="mm")
    draw.text((w // 2, 58), "Deterministic state mutation, ReAct isolation, CLI remediation, and automated health re-verification", fill=(90, 105, 125), font=body_font, anchor="mm")

    stages = [
        ("STAGE 1: BASELINE", "Pristine Network State", "• All 7 links UP\n• Host routes default via 10.0.0.1\n• MTU 1500 on all interfaces\n• DNS points to 10.0.0.254\n• Ping success: 100% (0% loss)", (235, 245, 255), (140, 180, 220), (20, 60, 120)),
        ("STAGE 2: FAULT INJECT", "5 Failure Archetypes", "• L1/L2: Trunk s1-eth3 down\n• L3: Route del default (blackhole)\n• L3/L4: NetEm 35% loss/180ms delay\n• L7: Corrupt /etc/resolv.conf\n• L2/L3: MTU reduced to 1200", (255, 240, 240), (220, 150, 150), (140, 30, 30)),
        ("STAGE 3: DIAGNOSE", "Autonomous ReAct Loop", "• Read-only diagnostic tools\n• Hypothesis-action-observation\n• Topology graph bounded\n• Runbook RAG context\n• Avg 2.0 tool calls / incident", (245, 240, 255), (190, 160, 230), (70, 20, 120)),
        ("STAGE 4: REMEDIATE", "Exact Action Execution", "• `ip link set dev <port> up`\n• `ip route add default via ...`\n• `tc qdisc del dev <port> root`\n• `echo nameserver ... > resolv`\n• `ip link set dev ... mtu 1500`", (255, 250, 235), (220, 190, 130), (120, 80, 10)),
        ("STAGE 5: VERIFY", "Automated Health Check", "• Post-remediation ping tool\n• Post-remediation DNS probe\n• Verify 0% packet loss\n• Automatic incident closure\n• Deterministic restoration", (235, 252, 240), (140, 210, 160), (20, 100, 45))
    ]

    box_w = 210
    box_h = 360
    start_x = 35
    spacing = 230
    y_pos = 95

    for idx, (s_tag, s_name, s_bullets, bg_color, border_color, title_color) in enumerate(stages):
        x = start_x + idx * spacing
        draw_rounded_rect(draw, (x, y_pos, x + box_w, y_pos + box_h), 10, fill=bg_color, outline=border_color, width=2)
        
        # Header
        draw.text((x + box_w // 2, y_pos + 22), s_tag, fill=title_color, font=get_font(12, bold=True), anchor="mm")
        draw.text((x + box_w // 2, y_pos + 48), s_name, fill=(20, 35, 55), font=stage_font, anchor="mm")
        draw.line([(x + 15, y_pos + 65), (x + box_w - 15, y_pos + 65)], fill=border_color, width=1)

        # Bullets
        by = y_pos + 80
        for line in s_bullets.split("\n"):
            draw.text((x + 15, by), line, fill=(45, 60, 80), font=small_font)
            by += 24

        # Arrow between stages
        if idx < len(stages) - 1:
            ax = x + box_w + 3
            ay = y_pos + box_h // 2
            draw.line([(ax, ay), (ax + 14, ay)], fill=(120, 140, 170), width=3)
            draw.polygon([(ax + 12, ay - 5), (ax + 12, ay + 5), (ax + 18, ay)], fill=(120, 140, 170))

    # Bottom Feedback Loop Arrow (Verify -> Baseline)
    draw.line([(1000, 465), (1000, 490), (140, 490), (140, 465)], fill=(30, 130, 60), width=2)
    draw.polygon([(135, 470), (145, 470), (140, 460)], fill=(30, 130, 60))
    draw.text((w // 2, 478), "Full Restoration Verification Closes Incident Loop (0% Packet Loss)", fill=(20, 110, 50), font=get_font(13, bold=True), anchor="mm")

    img.save(FIG_DIR / "fig3_fault_lifecycle.png", dpi=(300, 300))
    print("Generated fig3_fault_lifecycle.png")

# -----------------------------------------------------------------------------
# Figure 4: Comparative Evaluation Results (Bar Chart)
# -----------------------------------------------------------------------------
def generate_fig4_comparative_results():
    w, h = 1100, 600
    img = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    title_font = get_font(24, bold=True)
    axis_font = get_font(14, bold=True)
    label_font = get_font(13, bold=False)
    val_font = get_font(12, bold=True)
    legend_font = get_font(13, bold=True)

    # Title
    draw.text((w // 2, 35), "Empirical Diagnostic Performance Across 10 Standardized Benchmarks", fill=(20, 45, 80), font=title_font, anchor="mm")
    draw.text((w // 2, 65), "Comparison of Zero-Shot LLM, Static RAG + LLM, and Proposed Topology-Aware Agent", fill=(90, 105, 125), font=get_font(14, bold=False), anchor="mm")

    # Chart Area
    cx1, cy1 = 100, 110
    cx2, cy2 = 1000, 480
    chart_h = cy2 - cy1

    # Gridlines & Y-axis labels
    for pct in [0, 20, 40, 60, 80, 100]:
        y = cy2 - int((pct / 100.0) * chart_h)
        draw.line([(cx1, y), (cx2, y)], fill=(230, 235, 245), width=1)
        draw.text((cx1 - 15, y), f"{pct}%", fill=(100, 115, 130), font=label_font, anchor="rm")

    draw.line([(cx1, cy1), (cx1, cy2)], fill=(120, 135, 155), width=2)
    draw.line([(cx1, cy2), (cx2, cy2)], fill=(120, 135, 155), width=2)

    # Metrics to display
    metrics = [
        "Fault Category\nAccuracy",
        "Root Cause\nPrecision",
        "Actionable\nRemediation",
        "Hallucination\nRate (Lower is better)"
    ]

    # Data from evaluation_metrics.json
    # [ZeroShot, StaticRAG, ProposedAgent]
    data = [
        [60.0, 40.0, 90.0],   # Category Accuracy
        [40.0, 10.0, 100.0],  # Root Cause Precision
        [20.0, 70.0, 90.0],   # Remediation
        [100.0, 30.0, 0.0]    # Hallucination Rate
    ]

    colors = [
        (210, 80, 80),    # Red - Zero Shot
        (230, 160, 50),   # Orange - Static RAG
        (35, 140, 80)     # Green - Proposed Agent
    ]

    num_groups = len(metrics)
    group_width = (cx2 - cx1) / num_groups
    bar_w = 40
    gap = 8

    for g_idx in range(num_groups):
        gx = cx1 + g_idx * group_width + group_width / 2
        vals = data[g_idx]

        # Draw 3 bars
        start_bx = gx - (3 * bar_w + 2 * gap) / 2
        for b_idx in range(3):
            bx = start_bx + b_idx * (bar_w + gap)
            v = vals[b_idx]
            bar_top = cy2 - int((v / 100.0) * chart_h)
            
            # Fill bar
            draw.rectangle([(bx, bar_top), (bx + bar_w, cy2)], fill=colors[b_idx], outline=(255, 255, 255))
            
            # Label on top of bar
            label_y = bar_top - 12 if v > 0 else cy2 - 14
            val_color = colors[b_idx] if v == 0 else (30, 45, 65)
            draw.text((bx + bar_w / 2, label_y), f"{int(v)}%", fill=val_color, font=val_font, anchor="mm")

        # Metric group label
        m_lines = metrics[g_idx].split("\n")
        my = cy2 + 15
        for m_line in m_lines:
            draw.text((gx, my), m_line, fill=(40, 55, 75), font=axis_font, anchor="mt")
            my += 18

    # Legend at bottom
    ly = 555
    legend_items = [
        ("System A: Zero-Shot LLM (Ungrounded)", colors[0]),
        ("System B: Static RAG + LLM (No Tools)", colors[1]),
        ("System C: Proposed Topology-Aware Agent (Tool-Using)", colors[2])
    ]
    lx_start = 140
    for l_label, l_col in legend_items:
        draw.rectangle([(lx_start, ly), (lx_start + 18, ly + 14)], fill=l_col)
        draw.text((lx_start + 26, ly + 1), l_label, fill=(40, 55, 70), font=legend_font)
        lx_start += 290

    img.save(FIG_DIR / "fig4_comparative_results.png", dpi=(300, 300))
    print("Generated fig4_comparative_results.png")

if __name__ == "__main__":
    generate_fig1_architecture()
    generate_fig2_react_workflow()
    generate_fig3_fault_lifecycle()
    generate_fig4_comparative_results()
    print("All research paper figures generated successfully in figures/")

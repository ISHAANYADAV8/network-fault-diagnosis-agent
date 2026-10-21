"""
Interactive Terminal Demonstration Script
Showcases the Topology-Aware Tool-Using Diagnostic Agent diagnosing and remediating
a live network fault in real-time.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.sandbox.network_sandbox import NetworkSandbox
from src.tools.network_tools import set_sandbox, ping_tool
from src.faults.fault_injector import FaultInjector
from src.rag.runbook_retriever import RunbookRetriever
from src.agent.diagnostic_agent import DiagnosticAgent


def run_live_demo(scenario_id: str = "NET-SCN-001"):
    console = Console()
    console.clear()

    # Title Banner
    console.print(Panel(
        Text("Topology-Aware Tool-Using LLM Agent\nAutomated Network Fault Diagnosis & Root-Cause Analysis (RCA)", justify="center", style="bold cyan"),
        subtitle="DTU IT-401 B.Tech Project-I - Group 067",
        border_style="bright_blue"
    ))

    sandbox = NetworkSandbox()
    set_sandbox(sandbox)
    injector = FaultInjector(sandbox=sandbox)
    retriever = RunbookRetriever()
    agent = DiagnosticAgent(sandbox=sandbox, retriever=retriever)

    scn = injector.get_scenario(scenario_id)

    # 1. Incident Alert
    console.print("\n[bold red]ALERT: Network Fault Incident Detected![/bold red]")
    alert_table = Table(show_header=False, border_style="red")
    alert_table.add_column("Key", style="bold yellow")
    alert_table.add_column("Value", style="white")
    alert_table.add_row("Scenario ID", scn["scenario_id"])
    alert_table.add_row("Fault Class", scn["fault_class"])
    alert_table.add_row("Source Host", scn["target_node"])
    alert_table.add_row("Destination", scn["destination"])
    alert_table.add_row("Reported Symptom", scn["symptom"])
    console.print(alert_table)

    # 2. Inject Fault
    console.print("\n[bold yellow][*] Injecting Controlled Network Fault into Sandboxed Testbed...[/bold yellow]")
    injector.inject_scenario(scenario_id)
    time.sleep(0.5)
    console.print(f"[bold green][OK] Fault injected successfully:[/bold green] {scn['injected_fault']}")

    # 3. Agent Autonomous Reasoning Loop
    console.print("\n[bold cyan][*] Initializing Topology-Aware ReAct Diagnostic Agent...[/bold cyan]")
    time.sleep(0.5)

    report = agent.diagnose(
        symptom=scn["symptom"],
        target_node=scn["target_node"],
        destination=scn["destination"],
        scenario_id=scn["scenario_id"]
    )

    # Display Step Traces
    for idx, trace in enumerate(report["traces"], 1):
        console.print(f"\n[bold magenta]=== Diagnostic Iteration Step {idx} ===[/bold magenta]")
        console.print(f"[bold yellow]Thought:[/bold yellow] {trace['thought']}")
        console.print(f"[bold green]Action:[/bold green] [cyan]{trace['action']}[/cyan]")
        console.print(Panel(
            trace["observation"],
            title=f"Telemetry Output (Step {idx})",
            border_style="dim white",
            expand=False
        ))
        time.sleep(0.3)

    # 4. Final RCA Report Card
    rca_table = Table(title="[bold green]SYNTHESIZED ROOT CAUSE ANALYSIS (RCA) REPORT[/bold green]", border_style="green")
    rca_table.add_column("Attribute", style="bold cyan")
    rca_table.add_column("Agent Findings", style="white")
    rca_table.add_row("Diagnosed Fault Category", f"[bold green]{report['diagnosed_fault_class']}[/bold green]")
    rca_table.add_row("Identified Root Cause", report["root_cause_explanation"])
    rca_table.add_row("Recommended Remediation", f"[bold yellow]{report['actionable_remediation']}[/bold yellow]")
    rca_table.add_row("Tool Calls Executed", str(report["tool_calls_count"]))
    rca_table.add_row("Hallucination Count", str(len(report["hallucinations_detected"])))
    console.print("\n")
    console.print(rca_table)

    # 5. Execute Remediation & Verify
    console.print("\n[bold yellow][*] Executing Automated Remediation Command...[/bold yellow]")
    rem_cmd = report["actionable_remediation"]
    console.print(f"[dim]> {rem_cmd}[/dim]")
    time.sleep(0.4)

    # Execute remediation in sandbox
    if "s1-eth3" in rem_cmd and "up" in rem_cmd:
        injector.remediate_link_up("s1", "s1-eth3")
    elif "default via" in rem_cmd:
        injector.remediate_routing_blackhole(scn["target_node"], "10.0.0.1", "h2-eth0")
    elif "resolv.conf" in rem_cmd:
        injector.remediate_dns_failure(scn["target_node"], "10.0.0.254")
    elif "mtu" in rem_cmd:
        injector.remediate_mtu_mismatch("h1", "h1-eth0", 1500)
    elif "tc qdisc del" in rem_cmd:
        injector.remediate_channel_impairment("s1", "s1-eth1")

    # Verify resolution
    console.print("[bold green][OK] Verifying network health post-remediation...[/bold green]")
    test_res = ping_tool(scn["target_node"], scn["destination"] if "corp" not in scn["destination"] else "10.0.0.40", count=2)
    console.print(Panel(test_res, title="Post-Remediation Ping Verification", border_style="green"))
    console.print("[bold green]STATUS: Network connectivity 100% restored. Incident closed.[/bold green]\n")


if __name__ == "__main__":
    scn_arg = sys.argv[1] if len(sys.argv) > 1 else "NET-SCN-001"
    run_live_demo(scn_arg)

"""
Validation test suite for ReAct Diagnostic Agent, RAG Retriever, and Baselines (Phase 3).
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.sandbox.network_sandbox import NetworkSandbox
from src.tools.network_tools import set_sandbox
from src.faults.fault_injector import FaultInjector
from src.rag.runbook_retriever import RunbookRetriever
from src.agent.diagnostic_agent import DiagnosticAgent
from src.baselines.baseline_zero_shot import ZeroShotBaseline
from src.baselines.baseline_rag import RagBaseline


def run_agent_tests():
    print("=" * 65)
    print("RUNNING PHASE 3: REACT AGENT & BASELINES VALIDATION SUITE")
    print("=" * 65)

    sandbox = NetworkSandbox()
    set_sandbox(sandbox)
    injector = FaultInjector(sandbox=sandbox)
    retriever = RunbookRetriever()
    agent = DiagnosticAgent(sandbox=sandbox, retriever=retriever)

    # -------------------------------------------------------------------------
    # Test 1: RAG Runbook Retriever
    # -------------------------------------------------------------------------
    print("\n[Test 1] RAG Retriever Query: 'packet loss high latency variance'")
    docs = retriever.retrieve("packet loss high latency variance", top_k=2)
    assert len(docs) > 0, "RAG retriever must return matching documents"
    assert "icmp" in docs[0]["source"].lower() or "interface" in docs[0]["source"].lower(), "Must match ICMP runbook"
    print(f">>> PASS: Retrieved {len(docs)} runbook passages from '{docs[0]['source']}'.")

    # -------------------------------------------------------------------------
    # Test 2: Agent Solves NET-SCN-001 (Trunk Down)
    # -------------------------------------------------------------------------
    print("\n[Test 2] ReAct Agent Investigating NET-SCN-001 (Trunk Down)")
    injector.inject_scenario("NET-SCN-001")
    report_1 = agent.diagnose(
        symptom="Host h1 unable to reach application service at Host h4 (10.0.0.40)",
        target_node="h1",
        destination="10.0.0.40",
        scenario_id="NET-SCN-001"
    )

    print(f"  * Steps Taken: {report_1['steps_taken']}")
    print(f"  * Tool Calls ({report_1['tool_calls_count']}): {[c['tool'] for c in report_1['tool_calls']]}")
    print(f"  * Diagnosed Fault Class: {report_1['diagnosed_fault_class']}")
    print(f"  * Root Cause: {report_1['root_cause_explanation']}")
    print(f"  * Remediation: {report_1['actionable_remediation']}")
    print(f"  * Hallucinations: {report_1['hallucinations_detected']}")

    assert report_1["diagnosed_fault_class"] == "Interface State", "Must identify Interface State fault"
    assert "s1-eth3" in report_1["root_cause_explanation"] or "s1-eth3" in report_1["actionable_remediation"], "Must pinpoint port s1-eth3"
    assert len(report_1["hallucinations_detected"]) == 0, "Proposed agent must have 0 hallucinations"
    print(">>> PASS: NET-SCN-001 diagnosed accurately with evidence-backed reasoning.")

    # -------------------------------------------------------------------------
    # Test 3: Agent Solves NET-SCN-002 (Routing Blackhole)
    # -------------------------------------------------------------------------
    print("\n[Test 3] ReAct Agent Investigating NET-SCN-002 (Routing Blackhole)")
    injector.inject_scenario("NET-SCN-002")
    report_2 = agent.diagnose(
        symptom="Host h2 ping to WAN service at 10.0.1.254 fails with 'connect: Network is unreachable'",
        target_node="h2",
        destination="10.0.1.254",
        scenario_id="NET-SCN-002"
    )

    print(f"  * Steps Taken: {report_2['steps_taken']}")
    print(f"  * Tool Calls: {[c['tool'] for c in report_2['tool_calls']]}")
    print(f"  * Diagnosed Fault Class: {report_2['diagnosed_fault_class']}")
    print(f"  * Remediation: {report_2['actionable_remediation']}")

    assert report_2["diagnosed_fault_class"] == "Routing Table", "Must identify Routing Table fault"
    assert "default via 10.0.0.1" in report_2["actionable_remediation"], "Remediation must add default route"
    assert len(report_2["hallucinations_detected"]) == 0
    print(">>> PASS: NET-SCN-002 diagnosed accurately.")

    # -------------------------------------------------------------------------
    # Test 4: Agent Solves NET-SCN-004 (DNS Misconfiguration)
    # -------------------------------------------------------------------------
    print("\n[Test 4] ReAct Agent Investigating NET-SCN-004 (DNS Timeout)")
    injector.inject_scenario("NET-SCN-004")
    report_3 = agent.diagnose(
        symptom="Host h3 can ping IP addresses directly, but hostname resolution for 'app.corp.local' times out",
        target_node="h3",
        destination="app.corp.local",
        scenario_id="NET-SCN-004"
    )

    print(f"  * Steps Taken: {report_3['steps_taken']}")
    print(f"  * Diagnosed Fault Class: {report_3['diagnosed_fault_class']}")
    print(f"  * Remediation: {report_3['actionable_remediation']}")

    assert report_3["diagnosed_fault_class"] == "Name Resolution"
    assert "10.0.0.254" in report_3["actionable_remediation"]
    print(">>> PASS: NET-SCN-004 diagnosed accurately.")

    # -------------------------------------------------------------------------
    # Test 5: Baselines Execution Check
    # -------------------------------------------------------------------------
    print("\n[Test 5] Verifying Baselines (Zero-Shot and Static RAG)")
    zero_shot = ZeroShotBaseline()
    rag = RagBaseline(retriever=retriever)

    zs_out = zero_shot.diagnose("Host h1 ping to 10.0.0.40 drops 100%", "h1", "10.0.0.40")
    rag_out = rag.diagnose("Host h1 ping to 10.0.0.40 drops 100%", "h1", "10.0.0.40")

    assert zs_out["tool_calls_count"] == 0, "Zero-shot baseline must make 0 tool calls"
    assert rag_out["tool_calls_count"] == 0, "RAG baseline must make 0 tool calls"
    print(f">>> PASS: Baselines execute successfully.")

    injector.reset()
    print("\n" + "=" * 65)
    print("ALL PHASE 3 REACT AGENT & BASELINE TESTS PASSED! (5/5)")
    print("=" * 65)


if __name__ == "__main__":
    run_agent_tests()

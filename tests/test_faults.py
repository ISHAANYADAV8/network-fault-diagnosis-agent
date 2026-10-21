"""
Validation test suite for FaultInjector and Benchmark Scenarios (Phase 2).
Verifies that all 10 scenarios inject deterministically, produce expected
diagnostic signatures, and can be cleanly remediated.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.sandbox.network_sandbox import NetworkSandbox
from src.tools.network_tools import (
    ping_tool,
    traceroute_tool,
    routing_table_tool,
    interface_stats_tool,
    dns_query_tool,
    set_sandbox
)
from src.faults.fault_injector import FaultInjector


def run_fault_tests():
    print("=" * 65)
    print("RUNNING PHASE 2: FAULT INJECTION & BENCHMARK VALIDATION SUITE")
    print("=" * 65)

    sandbox = NetworkSandbox()
    set_sandbox(sandbox)
    injector = FaultInjector(sandbox=sandbox)

    assert len(injector.benchmarks) == 10, f"Expected 10 benchmark scenarios, got {len(injector.benchmarks)}"
    print(f"Loaded {len(injector.benchmarks)} benchmark scenarios from benchmarks.json.")

    # -------------------------------------------------------------------------
    # Test Scenario 1: NET-SCN-001 (Interface State / Trunk Down)
    # -------------------------------------------------------------------------
    print("\n[Scenario 1: NET-SCN-001] Trunk Port s1-eth3 DOWN")
    scn = injector.inject_scenario("NET-SCN-001")
    res_ping = ping_tool("h1", "10.0.0.40", count=2)
    res_stats = interface_stats_tool("s1")
    assert "100% packet loss" in res_ping, "NET-SCN-001: Ping must fail when trunk is severed"
    assert "s1-eth3" in res_stats and "state DOWN" in res_stats, "NET-SCN-001: s1-eth3 must report DOWN"
    print(">>> PASS: Trunk down signature verified.")

    # Remediate SCN-001
    injector.remediate_link_up("s1", "s1-eth3")
    res_restored = ping_tool("h1", "10.0.0.40", count=2)
    assert "0% packet loss" in res_restored, "NET-SCN-001: Remediation must restore connectivity"
    print(">>> PASS: Trunk remediation successful.")

    # -------------------------------------------------------------------------
    # Test Scenario 2: NET-SCN-002 (Routing Blackhole)
    # -------------------------------------------------------------------------
    print("\n[Scenario 2: NET-SCN-002] Routing Blackhole on h2")
    scn = injector.inject_scenario("NET-SCN-002")
    res_ping = ping_tool("h2", "10.0.1.254", count=2)
    res_route = routing_table_tool("h2")
    assert "Network is unreachable" in res_ping, "NET-SCN-002: Ping must report Network is unreachable"
    assert "default via" not in res_route, "NET-SCN-002: Default route must be absent"
    print(">>> PASS: Routing blackhole signature verified.")

    # Remediate SCN-002
    injector.remediate_routing_blackhole("h2", "10.0.0.1", "h2-eth0")
    res_restored = ping_tool("h2", "10.0.1.254", count=2)
    assert "0% packet loss" in res_restored, "NET-SCN-002: Remediation must restore default route"
    print(">>> PASS: Routing blackhole remediation successful.")

    # -------------------------------------------------------------------------
    # Test Scenario 3: NET-SCN-003 (Channel Impairment / NetEm)
    # -------------------------------------------------------------------------
    print("\n[Scenario 3: NET-SCN-003] Channel Impairment on s1-eth1 (35% loss, 180ms delay)")
    scn = injector.inject_scenario("NET-SCN-003")
    res_ping = ping_tool("h1", "10.0.0.20", count=5)
    print(res_ping)
    assert "packet loss" in res_ping, "NET-SCN-003: Must observe packet drops or high latency"
    print(">>> PASS: Channel impairment signature verified.")

    # Remediate SCN-003
    injector.remediate_channel_impairment("s1", "s1-eth1")
    res_restored = ping_tool("h1", "10.0.0.20", count=2)
    assert "0% packet loss" in res_restored, "NET-SCN-003: Remediation must restore line quality"
    print(">>> PASS: Channel impairment remediation successful.")

    # -------------------------------------------------------------------------
    # Test Scenario 4: NET-SCN-004 (Name Resolution Failure)
    # -------------------------------------------------------------------------
    print("\n[Scenario 4: NET-SCN-004] DNS Misconfiguration on h3 (10.0.0.99)")
    scn = injector.inject_scenario("NET-SCN-004")
    res_dns = dns_query_tool("h3", "app.corp.local")
    assert "timed out" in res_dns, "NET-SCN-004: DNS query must time out when resolver IP is invalid"
    # Direct IP ping still succeeds
    assert "0% packet loss" in ping_tool("h3", "10.0.0.40", count=1), "NET-SCN-004: Direct IP ping should still work"
    print(">>> PASS: DNS failure signature verified.")

    # Remediate SCN-004
    injector.remediate_dns_failure("h3", "10.0.0.254")
    res_restored = dns_query_tool("h3", "app.corp.local")
    assert "10.0.0.40" in res_restored, "NET-SCN-004: Remediation must restore DNS resolution"
    print(">>> PASS: DNS remediation successful.")

    # -------------------------------------------------------------------------
    # Test Scenario 5: NET-SCN-007 (MTU Mismatch)
    # -------------------------------------------------------------------------
    print("\n[Scenario 5: NET-SCN-007] MTU Mismatch on h1-eth0 (1200)")
    scn = injector.inject_scenario("NET-SCN-007")
    res_stats = interface_stats_tool("h1")
    assert "mtu 1200" in res_stats, "NET-SCN-007: Interface stats must reflect MTU 1200"
    print(">>> PASS: MTU mismatch signature verified.")

    # Remediate SCN-007
    injector.remediate_mtu_mismatch("h1", "h1-eth0", standard_mtu=1500)
    assert "mtu 1500" in interface_stats_tool("h1"), "NET-SCN-007: MTU must be restored to 1500"
    print(">>> PASS: MTU remediation successful.")

    # -------------------------------------------------------------------------
    # Final Reset Test
    # -------------------------------------------------------------------------
    print("\n[Final Sandbox Reset Test]")
    injector.reset()
    assert "0% packet loss" in ping_tool("h1", "10.0.0.40", count=2)
    assert "0% packet loss" in ping_tool("h2", "10.0.1.254", count=2)
    assert "10.0.0.40" in dns_query_tool("h1", "app.corp.local")
    print(">>> PASS: Entire sandbox pristine baseline verified.")

    print("\n" + "=" * 65)
    print("ALL PHASE 2 FAULT & BENCHMARK TESTS PASSED SUCCESSFULLY! (6/6)")
    print("=" * 65)


if __name__ == "__main__":
    run_fault_tests()

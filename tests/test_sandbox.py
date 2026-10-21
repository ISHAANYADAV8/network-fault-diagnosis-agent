"""
Unit and integration tests for NetworkSandbox and NetworkTools (Phase 1).
Validates healthy state, tools, fault injection, and reset.
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


def run_tests():
    print("=" * 60)
    print("RUNNING PHASE 1 TESTBED VALIDATION SUITE")
    print("=" * 60)

    sandbox = NetworkSandbox()
    set_sandbox(sandbox)

    # Test 1: Intraswitch Ping: h1 -> h2 (10.0.0.20 on Switch 1)
    print("\n[Test 1] Intraswitch Ping: h1 -> h2 (10.0.0.20)")
    res = ping_tool("h1", "10.0.0.20", count=3)
    print(res)
    assert "0% packet loss" in res, "Failed: Intraswitch ping should succeed with 0% loss"
    print(">>> PASS: Intraswitch ping healthy.")

    # Test 2: Interswitch Trunk Ping: h1 -> h4 (10.0.0.40 on Switch 2 via trunk s1-eth3)
    print("\n[Test 2] Interswitch Trunk Ping: h1 -> h4 (10.0.0.40)")
    res = ping_tool("h1", "10.0.0.40", count=3)
    print(res)
    assert "0% packet loss" in res, "Failed: Interswitch trunk ping should succeed with 0% loss"
    print(">>> PASS: Interswitch trunk ping healthy.")

    # Test 3: Traceroute through Gateway to WAN (h1 -> 10.0.1.254)
    print("\n[Test 3] Traceroute: h1 -> 10.0.1.254 (External Service via gw1)")
    res = traceroute_tool("h1", "10.0.1.254")
    print(res)
    assert "10.0.0.1" in res and "10.0.1.254" in res, "Failed: Traceroute must show gateway and WAN target"
    print(">>> PASS: Traceroute traversal valid.")

    # Test 4: Routing Table Inspection (h1)
    print("\n[Test 4] Routing Table on h1")
    res = routing_table_tool("h1")
    print(res)
    assert "default via 10.0.0.1" in res, "Failed: h1 routing table must have default route"
    print(">>> PASS: Routing table accurate.")

    # Test 5: Interface Stats Inspection (s1)
    print("\n[Test 5] Interface Stats on Switch s1")
    res = interface_stats_tool("s1")
    print(res)
    assert "s1-eth1" in res and "s1-eth3" in res and "state UP" in res, "Failed: s1 must report active ports"
    print(">>> PASS: Interface telemetry accurate.")

    # Test 6: DNS Query (h1 -> app.corp.local)
    print("\n[Test 6] DNS Resolution for app.corp.local from h1")
    res = dns_query_tool("h1", "app.corp.local")
    print(res)
    assert "10.0.0.40" in res, "Failed: DNS must resolve app.corp.local to 10.0.0.40"
    print(">>> PASS: DNS resolution operational.")

    # Test 7: Simulated Failure - Trunk Port Down (s1-eth3 down)
    print("\n[Test 7] Fault Injection: Disabling trunk port s1-eth3")
    sandbox.set_interface_status("s1", "s1-eth3", "DOWN")
    res = ping_tool("h1", "10.0.0.40", count=2)
    print(res)
    assert "100% packet loss" in res, "Failed: Ping should drop packets when trunk link is down"
    
    # Check interface tool sees the DOWN state
    s1_stats = interface_stats_tool("s1")
    assert "s1-eth3" in s1_stats and "state DOWN" in s1_stats, "Failed: Interface tool must show state DOWN"
    print(">>> PASS: Trunk failure observed deterministically.")

    # Restore
    sandbox.reset_to_default()
    print("\n[Test 8] Reset to Default")
    res = ping_tool("h1", "10.0.0.40", count=2)
    assert "0% packet loss" in res, "Failed: Network must be fully restored"
    print(">>> PASS: Network state restored cleanly.")

    print("\n" + "=" * 60)
    print("ALL PHASE 1 TESTS PASSED SUCCESSFULLY! (8/8)")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()

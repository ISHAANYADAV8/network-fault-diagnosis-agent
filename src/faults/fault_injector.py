"""
Fault Injection Pipeline Module
Programmatically injects deterministic network failures across 5 archetypes:
1. Link State Failure (L1/L2)
2. Routing Blackhole (L3)
3. Channel Impairment / QoS (L3/L4)
4. Name Resolution Failure (L7)
5. Interface MTU Mismatch (L2/L3)

Supports Mode A (Simulated Sandbox) and Mode B (Live Mininet / Linux CLI).
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional
from src.sandbox.network_sandbox import NetworkSandbox
from src.tools.network_tools import get_sandbox


class FaultInjector:
    def __init__(
        self,
        sandbox: Optional[NetworkSandbox] = None,
        benchmarks_path: Optional[str | Path] = None
    ):
        self.sandbox = sandbox or get_sandbox()
        if benchmarks_path is None:
            benchmarks_path = Path(__file__).resolve().parent.parent.parent / "benchmarks" / "benchmarks.json"
        self.benchmarks_path = Path(benchmarks_path)
        self.benchmarks: List[Dict[str, Any]] = []
        self._load_benchmarks()
        self.mode = os.environ.get("NETWORK_DIAG_MODE", "simulated").lower()

    def _load_benchmarks(self) -> None:
        """Loads curated benchmark scenarios from benchmarks.json."""
        if self.benchmarks_path.exists():
            with open(self.benchmarks_path, "r", encoding="utf-8") as f:
                self.benchmarks = json.load(f)

    def _exec_mininet_cmd(self, node_id: str, cmd: str) -> str:
        """Executes a configuration or fault injection command in Mininet."""
        full_cmd = f"ip netns exec {node_id} {cmd}" if "netns" in node_id else f"m {node_id} {cmd}"
        try:
            res = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=5)
            return res.stdout.strip() if res.stdout else res.stderr.strip()
        except Exception as e:
            return f"Error executing Mininet command: {e}"

    # -------------------------------------------------------------------------
    # Fault Archetype 1: Link State Failure (L1/L2)
    # -------------------------------------------------------------------------

    def inject_link_down(self, node_id: str, port: str) -> Dict[str, Any]:
        """
        Administratively disables an interface or trunk link.
        Mininet Equivalent: ip link set dev <port> down
        """
        if self.mode == "mininet":
            self._exec_mininet_cmd(node_id, f"ip link set dev {port} down")
        self.sandbox.set_interface_status(node_id, port, "DOWN")
        return {
            "fault_class": "Interface State",
            "action": "inject",
            "target": f"{node_id}:{port}",
            "command": f"ip link set dev {port} down",
            "status": "injected"
        }

    def remediate_link_up(self, node_id: str, port: str) -> Dict[str, Any]:
        """
        Re-enables an interface or trunk link.
        Mininet Equivalent: ip link set dev <port> up
        """
        if self.mode == "mininet":
            self._exec_mininet_cmd(node_id, f"ip link set dev {port} up")
        self.sandbox.set_interface_status(node_id, port, "UP")
        return {
            "fault_class": "Interface State",
            "action": "remediate",
            "target": f"{node_id}:{port}",
            "command": f"ip link set dev {port} up",
            "status": "remediated"
        }

    # -------------------------------------------------------------------------
    # Fault Archetype 2: Routing Blackhole (L3)
    # -------------------------------------------------------------------------

    def inject_routing_blackhole(self, node_id: str) -> Dict[str, Any]:
        """
        Deletes or strips the default gateway from a node's routing table.
        Mininet Equivalent: ip route del default
        """
        if self.mode == "mininet":
            self._exec_mininet_cmd(node_id, "ip route del default")
        self.sandbox.set_default_gateway(node_id, None)
        return {
            "fault_class": "Routing Table",
            "action": "inject",
            "target": node_id,
            "command": "ip route del default",
            "status": "injected"
        }

    def remediate_routing_blackhole(self, node_id: str, gateway_ip: str, interface: str) -> Dict[str, Any]:
        """
        Restores the missing default route in a node's routing table.
        Mininet Equivalent: ip route add default via <gateway_ip> dev <interface>
        """
        if self.mode == "mininet":
            self._exec_mininet_cmd(node_id, f"ip route add default via {gateway_ip} dev {interface}")
        self.sandbox.set_default_gateway(node_id, gateway_ip)
        return {
            "fault_class": "Routing Table",
            "action": "remediate",
            "target": node_id,
            "command": f"ip route add default via {gateway_ip} dev {interface}",
            "status": "remediated"
        }

    # -------------------------------------------------------------------------
    # Fault Archetype 3: Channel Impairment / QoS Degradation (L3/L4)
    # -------------------------------------------------------------------------

    def inject_channel_impairment(
        self,
        node_a: str,
        port_a: str,
        loss_pct: float = 35.0,
        delay_ms: float = 180.0
    ) -> Dict[str, Any]:
        """
        Injects severe synthetic jitter and packet loss via NetEm.
        Mininet Equivalent: tc qdisc add dev <port> root netem loss <loss>% delay <delay>ms
        """
        if self.mode == "mininet":
            self._exec_mininet_cmd(node_a, f"tc qdisc add dev {port_a} root netem loss {loss_pct}% delay {delay_ms}ms")
        self.sandbox.set_link_impairment(node_a, port_a, loss_pct=loss_pct, delay_ms=delay_ms)
        return {
            "fault_class": "Channel Impairment",
            "action": "inject",
            "target": f"{node_a}:{port_a}",
            "command": f"tc qdisc add dev {port_a} root netem loss {loss_pct}% delay {delay_ms}ms",
            "status": "injected"
        }

    def remediate_channel_impairment(self, node_a: str, port_a: str) -> Dict[str, Any]:
        """
        Removes traffic control queuing discipline netem impairments.
        Mininet Equivalent: tc qdisc del dev <port> root
        """
        if self.mode == "mininet":
            self._exec_mininet_cmd(node_a, f"tc qdisc del dev {port_a} root")
        self.sandbox.set_link_impairment(node_a, port_a, loss_pct=0.0, delay_ms=1.0)
        return {
            "fault_class": "Channel Impairment",
            "action": "remediate",
            "target": f"{node_a}:{port_a}",
            "command": f"tc qdisc del dev {port_a} root",
            "status": "remediated"
        }

    # -------------------------------------------------------------------------
    # Fault Archetype 4: Name Resolution Failure (L7)
    # -------------------------------------------------------------------------

    def inject_dns_failure(self, node_id: str, invalid_ip: str = "10.0.0.99") -> Dict[str, Any]:
        """
        Points /etc/resolv.conf nameserver to an unreachable or non-existent IP address.
        Mininet Equivalent: echo "nameserver <invalid_ip>" > /etc/resolv.conf
        """
        if self.mode == "mininet":
            self._exec_mininet_cmd(node_id, f"echo 'nameserver {invalid_ip}' > /etc/resolv.conf")
        self.sandbox.set_dns_server(node_id, invalid_ip)
        return {
            "fault_class": "Name Resolution",
            "action": "inject",
            "target": node_id,
            "command": f"echo 'nameserver {invalid_ip}' > /etc/resolv.conf",
            "status": "injected"
        }

    def remediate_dns_failure(self, node_id: str, valid_ip: str = "10.0.0.254") -> Dict[str, Any]:
        """
        Restores valid corporate nameserver IP in /etc/resolv.conf.
        Mininet Equivalent: echo "nameserver <valid_ip>" > /etc/resolv.conf
        """
        if self.mode == "mininet":
            self._exec_mininet_cmd(node_id, f"echo 'nameserver {valid_ip}' > /etc/resolv.conf")
        self.sandbox.set_dns_server(node_id, valid_ip)
        return {
            "fault_class": "Name Resolution",
            "action": "remediate",
            "target": node_id,
            "command": f"echo 'nameserver {valid_ip}' > /etc/resolv.conf",
            "status": "remediated"
        }

    # -------------------------------------------------------------------------
    # Fault Archetype 5: Interface MTU Mismatch (L2/L3)
    # -------------------------------------------------------------------------

    def inject_mtu_mismatch(self, node_id: str, port: str, small_mtu: int = 1200) -> Dict[str, Any]:
        """
        Lowers MTU on a specific interface causing oversized frame packet drops.
        Mininet Equivalent: ip link set dev <port> mtu <small_mtu>
        """
        if self.mode == "mininet":
            self._exec_mininet_cmd(node_id, f"ip link set dev {port} mtu {small_mtu}")
        self.sandbox.set_interface_mtu(node_id, port, small_mtu)
        return {
            "fault_class": "MTU Mismatch",
            "action": "inject",
            "target": f"{node_id}:{port}",
            "command": f"ip link set dev {port} mtu {small_mtu}",
            "status": "injected"
        }

    def remediate_mtu_mismatch(self, node_id: str, port: str, standard_mtu: int = 1500) -> Dict[str, Any]:
        """
        Restores standard 1500 Ethernet MTU.
        Mininet Equivalent: ip link set dev <port> mtu <standard_mtu>
        """
        if self.mode == "mininet":
            self._exec_mininet_cmd(node_id, f"ip link set dev {port} mtu {standard_mtu}")
        self.sandbox.set_interface_mtu(node_id, port, standard_mtu)
        return {
            "fault_class": "MTU Mismatch",
            "action": "remediate",
            "target": f"{node_id}:{port}",
            "command": f"ip link set dev {port} mtu {standard_mtu}",
            "status": "remediated"
        }

    # -------------------------------------------------------------------------
    # Benchmark Scenario Execution Engine
    # -------------------------------------------------------------------------

    def get_scenario(self, scenario_id: str) -> Dict[str, Any]:
        """Retrieves scenario definition by ID."""
        for scn in self.benchmarks:
            if scn["scenario_id"] == scenario_id:
                return scn
        raise KeyError(f"Scenario '{scenario_id}' not found in benchmarks.json.")

    def inject_scenario(self, scenario_id: str) -> Dict[str, Any]:
        """
        Injects a complete benchmark scenario by its identifier.
        Resets the network state to pristine first, then injects the fault.
        """
        self.reset()
        scenario = self.get_scenario(scenario_id)
        f_type = scenario["fault_class"]
        params = scenario.get("fault_parameters", {})

        if f_type == "Interface State":
            self.inject_link_down(params["node_id"], params["port"])
        elif f_type == "Routing Table":
            self.inject_routing_blackhole(params["node_id"])
        elif f_type == "Channel Impairment":
            self.inject_channel_impairment(
                params["node_a"],
                params["port_a"],
                loss_pct=params.get("loss_pct", 35.0),
                delay_ms=params.get("delay_ms", 180.0)
            )
        elif f_type == "Name Resolution":
            self.inject_dns_failure(params["node_id"], invalid_ip=params.get("invalid_ip", "10.0.0.99"))
        elif f_type == "MTU Mismatch":
            self.inject_mtu_mismatch(params["node_id"], params["port"], small_mtu=params.get("small_mtu", 1200))
        else:
            raise ValueError(f"Unknown fault class '{f_type}' in scenario {scenario_id}.")

        return scenario

    def reset(self) -> None:
        """Restores the network sandbox to default pristine state."""
        self.sandbox.reset_to_default()

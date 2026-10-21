"""
Network Diagnostic Tool Wrappers
Standardized execution interface for LLM Agent tool-calling.
Supports Mode A (Simulated Sandbox) and Mode B (Live Mininet / Linux netns).
"""

from __future__ import annotations

import os
import subprocess
from typing import Any, Callable, Dict, List, Optional
from src.sandbox.network_sandbox import NetworkSandbox

# Global active sandbox instance (default to Mode A on Windows)
_ACTIVE_SANDBOX: Optional[NetworkSandbox] = None
_EXECUTION_MODE = os.environ.get("NETWORK_DIAG_MODE", "simulated").lower()  # "simulated" or "mininet"


def get_sandbox() -> NetworkSandbox:
    """Retrieves or initializes the global NetworkSandbox instance."""
    global _ACTIVE_SANDBOX
    if _ACTIVE_SANDBOX is None:
        _ACTIVE_SANDBOX = NetworkSandbox()
    return _ACTIVE_SANDBOX


def set_sandbox(sandbox: NetworkSandbox) -> None:
    """Sets the active sandbox instance."""
    global _ACTIVE_SANDBOX
    _ACTIVE_SANDBOX = sandbox


def set_execution_mode(mode: str) -> None:
    """Switch execution mode: 'simulated' (Mode A) or 'mininet' (Mode B)."""
    global _EXECUTION_MODE
    if mode not in ["simulated", "mininet"]:
        raise ValueError("Mode must be 'simulated' or 'mininet'")
    _EXECUTION_MODE = mode


def _exec_mininet_cmd(node_id: str, command: str, timeout: int = 6) -> str:
    """Executes a diagnostic command inside a live Linux Mininet node namespace."""
    full_cmd = f"ip netns exec {node_id} {command}" if "netns" in node_id else f"m {node_id} {command}"
    try:
        proc = subprocess.run(
            full_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        output = proc.stdout.strip() if proc.stdout else proc.stderr.strip()
        return output if output else "Command executed with no output."
    except subprocess.TimeoutExpired:
        return f"Error: Diagnostic tool '{command}' timed out after {timeout} seconds."
    except Exception as e:
        return f"Execution error: {str(e)}"


# -----------------------------------------------------------------------------
# Standardized Tool API
# -----------------------------------------------------------------------------

def ping_tool(src_node: str, target_ip: str, count: int = 3) -> str:
    """
    Probes end-to-end IP reachability with ICMP echo requests.
    Args:
        src_node: Originating host or router identifier (e.g., 'h1', 'h2')
        target_ip: Destination IPv4 address to ping (e.g., '10.0.1.40')
        count: Number of echo packets to transmit (default: 3)
    """
    if _EXECUTION_MODE == "mininet":
        return _exec_mininet_cmd(src_node, f"ping -c {count} -W 2 {target_ip}", timeout=5)
    return get_sandbox().exec_ping(src_node, target_ip, count=count)


def traceroute_tool(src_node: str, target_ip: str) -> str:
    """
    Traces the layer-3 path hops and identifies points of packet drops or loops.
    Args:
        src_node: Originating host or router identifier (e.g., 'h1')
        target_ip: Destination IPv4 address to trace path towards
    """
    if _EXECUTION_MODE == "mininet":
        return _exec_mininet_cmd(src_node, f"traceroute -n -w 2 -m 8 {target_ip}", timeout=6)
    return get_sandbox().exec_traceroute(src_node, target_ip, max_hops=8)


def routing_table_tool(node_id: str) -> str:
    """
    Extracts the kernel IP routing table entries from a host or router.
    Args:
        node_id: Node identifier whose routing table to inspect (e.g., 'h1', 'gw1')
    """
    if _EXECUTION_MODE == "mininet":
        return _exec_mininet_cmd(node_id, "ip route show", timeout=4)
    return get_sandbox().exec_ip_route(node_id)


def interface_stats_tool(node_id: str) -> str:
    """
    Retrieves interface administrative status, carrier flags, MTU, and TX/RX error statistics.
    Args:
        node_id: Switch, router, or host identifier (e.g., 's1', 's2', 'h1', 'gw1')
    """
    if _EXECUTION_MODE == "mininet":
        return _exec_mininet_cmd(node_id, "ip -s link", timeout=4)
    return get_sandbox().exec_ip_link(node_id)


def dns_query_tool(src_node: str, hostname: str) -> str:
    """
    Executes DNS resolution query against the node's configured nameserver.
    Args:
        src_node: Host from which to perform DNS lookup (e.g., 'h1')
        hostname: Fully qualified domain name to resolve (e.g., 'app.corp.local')
    """
    if _EXECUTION_MODE == "mininet":
        return _exec_mininet_cmd(src_node, f"nslookup {hostname}", timeout=5)
    return get_sandbox().exec_dns_query(src_node, hostname)


# -----------------------------------------------------------------------------
# Tool Schema Registry for LLM Function Calling
# -----------------------------------------------------------------------------

TOOL_REGISTRY: Dict[str, Callable[..., str]] = {
    "ping_tool": ping_tool,
    "traceroute_tool": traceroute_tool,
    "routing_table_tool": routing_table_tool,
    "interface_stats_tool": interface_stats_tool,
    "dns_query_tool": dns_query_tool,
}

TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        "name": "ping_tool",
        "description": "Send ICMP echo requests from a source node to a target IP to check connectivity and round-trip time.",
        "parameters": {
            "type": "object",
            "properties": {
                "src_node": {
                    "type": "string",
                    "description": "Source node name (e.g., 'h1', 'h2', 'gw1')"
                },
                "target_ip": {
                    "type": "string",
                    "description": "Target IPv4 address (e.g., '10.0.1.40')"
                },
                "count": {
                    "type": "integer",
                    "description": "Number of packets to send (default: 3)"
                }
            },
            "required": ["src_node", "target_ip"]
        }
    },
    {
        "name": "traceroute_tool",
        "description": "Trace network hops from a source node to a target IP to detect where packets are lost or routed.",
        "parameters": {
            "type": "object",
            "properties": {
                "src_node": {
                    "type": "string",
                    "description": "Source node name (e.g., 'h1')"
                },
                "target_ip": {
                    "type": "string",
                    "description": "Target IPv4 address (e.g., '10.0.1.40')"
                }
            },
            "required": ["src_node", "target_ip"]
        }
    },
    {
        "name": "routing_table_tool",
        "description": "Inspect the kernel routing table ('ip route show') of a host or router.",
        "parameters": {
            "type": "object",
            "properties": {
                "node_id": {
                    "type": "string",
                    "description": "Node name to query (e.g., 'h1', 'h2', 'gw1')"
                }
            },
            "required": ["node_id"]
        }
    },
    {
        "name": "interface_stats_tool",
        "description": "Inspect network interfaces, MTU, carrier state (UP/DOWN), and packet drop statistics ('ip -s link').",
        "parameters": {
            "type": "object",
            "properties": {
                "node_id": {
                    "type": "string",
                    "description": "Node name to query (e.g., 's1', 's2', 'h1', 'gw1')"
                }
            },
            "required": ["node_id"]
        }
    },
    {
        "name": "dns_query_tool",
        "description": "Perform DNS hostname lookup using the node's configured nameserver ('nslookup').",
        "parameters": {
            "type": "object",
            "properties": {
                "src_node": {
                    "type": "string",
                    "description": "Source host performing query (e.g., 'h1')"
                },
                "hostname": {
                    "type": "string",
                    "description": "Domain name to resolve (e.g., 'app.corp.local')"
                }
            },
            "required": ["src_node", "hostname"]
        }
    }
]

"""
Network Sandbox Engine
Simulates a deterministic virtual network testbed (Mode A) on Windows/Linux.
Maintains state for nodes, interfaces, routing tables, links, impairments, and DNS.
Produces realistic terminal outputs for diagnostic tools (ping, traceroute, ip route, ip link, nslookup).
"""

from __future__ import annotations

import copy
import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import networkx as nx


class NetworkSandbox:
    def __init__(self, topology_path: Optional[str | Path] = None):
        if topology_path is None:
            topology_path = Path(__file__).resolve().parent.parent.parent / "config" / "topology.json"
        self.topology_path = Path(topology_path)
        self.raw_topology: Dict[str, Any] = {}
        self.state: Dict[str, Any] = {}
        self.graph = nx.Graph()
        self.load_topology()

    def load_topology(self) -> None:
        """Loads and initializes the sandbox state from topology.json."""
        with open(self.topology_path, "r", encoding="utf-8") as f:
            self.raw_topology = json.load(f)
        self.reset_to_default()

    def reset_to_default(self) -> None:
        """Resets the network state to the healthy pristine baseline."""
        self.state = copy.deepcopy(self.raw_topology)
        self._rebuild_graph()

    def _rebuild_graph(self) -> None:
        """Reconstructs the internal networkx graph based on current link and interface states."""
        self.graph.clear()
        nodes = self.state.get("nodes", {})
        for node_id, data in nodes.items():
            self.graph.add_node(node_id, **data)

        for link in self.state.get("links", []):
            node_a = link["node_a"]
            port_a = link["port_a"]
            node_b = link["node_b"]
            port_b = link["port_b"]
            
            # Link is active only if the link itself is UP, and both connected interfaces are UP
            intf_a_up = nodes.get(node_a, {}).get("interfaces", {}).get(port_a, {}).get("status", "UP") == "UP"
            intf_b_up = nodes.get(node_b, {}).get("interfaces", {}).get(port_b, {}).get("status", "UP") == "UP"
            link_up = link.get("status", "UP") == "UP" and intf_a_up and intf_b_up

            self.graph.add_edge(
                node_a,
                node_b,
                port_a=port_a,
                port_b=port_b,
                status="UP" if link_up else "DOWN",
                delay_ms=link.get("delay_ms", 1.0),
                loss_pct=link.get("loss_pct", 0.0),
            )

    # -------------------------------------------------------------------------
    # Helper Queries
    # -------------------------------------------------------------------------

    def find_node_by_ip(self, ip: str) -> Optional[str]:
        """Returns the node_id that owns the specified IP address."""
        for node_id, node in self.state.get("nodes", {}).items():
            if node.get("ip") == ip:
                return node_id
            for intf in node.get("interfaces", {}).values():
                if intf.get("ip") == ip:
                    return node_id
        return None

    def get_node(self, node_id: str) -> Dict[str, Any]:
        """Returns the dictionary data for a node."""
        if node_id not in self.state.get("nodes", {}):
            raise KeyError(f"Node '{node_id}' does not exist in topology.")
        return self.state["nodes"][node_id]

    def get_topology_summary(self) -> Dict[str, Any]:
        """Returns a sanitized topology representation suitable for LLM context prompts."""
        summary = {
            "subnets": self.state.get("subnets", []),
            "nodes": {},
            "links": []
        }
        for nid, data in self.state.get("nodes", {}).items():
            summary["nodes"][nid] = {
                "type": data.get("type"),
                "ip": data.get("ip"),
                "subnet": data.get("subnet"),
                "default_gateway": data.get("default_gateway"),
                "interfaces": list(data.get("interfaces", {}).keys())
            }
        for link in self.state.get("links", []):
            summary["links"].append(f"{link['node_a']}:{link['port_a']} <---> {link['node_b']}:{link['port_b']}")
        return summary

    # -------------------------------------------------------------------------
    # Fault Injection Mutators
    # -------------------------------------------------------------------------

    def set_interface_status(self, node_id: str, port: str, status: str) -> bool:
        """Sets an interface status to 'UP' or 'DOWN'."""
        node = self.get_node(node_id)
        if port not in node.get("interfaces", {}):
            raise ValueError(f"Port '{port}' not found on node '{node_id}'.")
        node["interfaces"][port]["status"] = status.upper()
        self._rebuild_graph()
        return True

    def set_link_impairment(self, node_a: str, port_a: str, loss_pct: float, delay_ms: float) -> bool:
        """Sets NetEm style packet loss and delay on a link."""
        for link in self.state.get("links", []):
            if (link["node_a"] == node_a and link["port_a"] == port_a) or \
               (link["node_b"] == node_a and link["port_b"] == port_a):
                link["loss_pct"] = float(loss_pct)
                link["delay_ms"] = float(delay_ms)
                self._rebuild_graph()
                return True
        raise ValueError(f"Link matching {node_a}:{port_a} not found.")

    def set_default_gateway(self, node_id: str, gateway_ip: Optional[str]) -> bool:
        """Sets or deletes (if None or empty) the default gateway for a host."""
        node = self.get_node(node_id)
        node["default_gateway"] = gateway_ip
        return True

    def set_dns_server(self, node_id: str, dns_ip: str) -> bool:
        """Sets the nameserver IP configured in /etc/resolv.conf on a node."""
        node = self.get_node(node_id)
        node["dns_server"] = dns_ip
        return True

    def set_interface_mtu(self, node_id: str, port: str, mtu: int) -> bool:
        """Sets MTU for a specific interface."""
        node = self.get_node(node_id)
        if port not in node.get("interfaces", {}):
            raise ValueError(f"Port '{port}' not found on node '{node_id}'.")
        node["interfaces"][port]["mtu"] = mtu
        return True

    # -------------------------------------------------------------------------
    # Simulated Tool Executions
    # -------------------------------------------------------------------------

    def _resolve_l3_path(self, src_node: str, target_ip: str) -> Tuple[bool, List[str], str, float, float]:
        """
        Determines Layer-3 routing and path traversal from src_node to target_ip.
        Returns: (is_reachable, path_nodes, failure_reason, total_delay_ms, max_loss_pct)
        """
        src = self.get_node(src_node)
        dest_node = self.find_node_by_ip(target_ip)
        external_eps = self.state.get("external_endpoints", {})

        if not dest_node and target_ip not in external_eps:
            return False, [], "Destination IP not found in topology", 0.0, 100.0

        if src_node == dest_node:
            return True, [src_node], "Localhost loopback", 0.1, 0.0

        # Check local interface state
        for intf in src.get("interfaces", {}).values():
            if intf.get("status") == "DOWN":
                return False, [src_node], "Network is unreachable (Interface DOWN)", 0.0, 100.0

        try:
            active_subgraph = nx.Graph([
                (u, v, d) for u, v, d in self.graph.edges(data=True) if d.get("status") == "UP"
            ])

            # Case 1: External WAN Endpoint (e.g., 10.0.1.254 via default gateway)
            if target_ip in external_eps:
                gw_ip = src.get("default_gateway")
                if not gw_ip:
                    return False, [src_node], "Network is unreachable (No default gateway)", 0.0, 100.0

                gw_node = self.find_node_by_ip(gw_ip)
                if not gw_node or not nx.has_path(active_subgraph, src_node, gw_node):
                    return False, [], "Destination Host Unreachable (Cannot reach gateway)", 0.0, 100.0

                path_to_gw = nx.shortest_path(active_subgraph, src_node, gw_node)
                path = path_to_gw + [target_ip]
                ep_data = external_eps[target_ip]
                base_delay = ep_data.get("base_rtt_ms", 10.0)
                return True, path, "OK", base_delay, 0.0

            # Case 2: Internal LAN Node
            dest = self.get_node(dest_node)
            if not nx.has_path(active_subgraph, src_node, dest_node):
                return False, [], "Destination Host Unreachable (Link severed)", 0.0, 100.0

            path = nx.shortest_path(active_subgraph, src_node, dest_node)

            # Calculate cumulative latency & packet loss along path
            total_delay = 0.0
            accumulated_loss = 0.0
            for i in range(len(path) - 1):
                edge_data = active_subgraph.get_edge_data(path[i], path[i+1])
                total_delay += edge_data.get("delay_ms", 1.0)
                edge_loss = edge_data.get("loss_pct", 0.0)
                accumulated_loss = 1.0 - (1.0 - (accumulated_loss / 100.0)) * (1.0 - (edge_loss / 100.0))
                accumulated_loss *= 100.0

            return True, path, "OK", max(0.5, total_delay), accumulated_loss

        except Exception as e:
            return False, [], str(e), 0.0, 100.0

    def exec_ping(self, src_node: str, target_ip: str, count: int = 3) -> str:
        """Simulates standard Linux 'ping -c <count> -W 2 <target_ip>'."""
        reachable, path, reason, delay, loss_pct = self._resolve_l3_path(src_node, target_ip)

        if not reachable:
            if "Network is unreachable" in reason:
                return f"connect: Network is unreachable"
            lines = [f"PING {target_ip} ({target_ip}) 56(84) bytes of data."]
            for seq in range(1, count + 1):
                lines.append(f"From {target_ip} icmp_seq={seq} Destination Host Unreachable")
            lines.extend([
                f"\n--- {target_ip} ping statistics ---",
                f"{count} packets transmitted, 0 received, +{count} errors, 100% packet loss, time {count * 1000}ms"
            ])
            return "\n".join(lines)

        # Handle synthetic loss if impaired
        received = 0
        rtts: List[float] = []
        lines = [f"PING {target_ip} ({target_ip}) 56(84) bytes of data."]
        
        for seq in range(1, count + 1):
            # Check if this packet is dropped
            if loss_pct > 0 and (random.random() * 100.0) < loss_pct:
                continue
            
            # Slight jitter variance
            jitter = random.uniform(-0.15 * delay, 0.25 * delay)
            rtt = max(0.5, round(delay * 2 + jitter, 2))
            rtts.append(rtt)
            received += 1
            lines.append(f"64 bytes from {target_ip}: icmp_seq={seq} ttl=63 time={rtt:.2f} ms")

        actual_loss = int(((count - received) / count) * 100)
        lines.append(f"\n--- {target_ip} ping statistics ---")
        if received > 0:
            min_rtt = min(rtts)
            max_rtt = max(rtts)
            avg_rtt = sum(rtts) / len(rtts)
            mdev = (max_rtt - min_rtt) / 2.0
            lines.append(f"{count} packets transmitted, {received} received, {actual_loss}% packet loss, time {count * 1000}ms")
            lines.append(f"rtt min/avg/max/mdev = {min_rtt:.3f}/{avg_rtt:.3f}/{max_rtt:.3f}/{mdev:.3f} ms")
        else:
            lines.append(f"{count} packets transmitted, 0 received, 100% packet loss, time {count * 1000}ms")

        return "\n".join(lines)

    def exec_traceroute(self, src_node: str, target_ip: str, max_hops: int = 8) -> str:
        """Simulates standard Linux 'traceroute -n -w 2 -m <max_hops> <target_ip>'."""
        reachable, path, reason, delay, loss_pct = self._resolve_l3_path(src_node, target_ip)

        lines = [f"traceroute to {target_ip} ({target_ip}), {max_hops} hops max, 60 byte packets"]

        if not reachable and "Network is unreachable" in reason:
            return "connect: Network is unreachable"

        # L3 hops: Filter path to hosts and routers (switches are L2 transparent)
        l3_hops = []
        for node_id in path:
            if node_id in self.state.get("nodes", {}):
                node = self.get_node(node_id)
                if node.get("type") in ["host", "router"]:
                    ip = node.get("ip")
                    if not ip and "interfaces" in node:
                        for intf in node["interfaces"].values():
                            if intf.get("ip"):
                                ip = intf["ip"]
                                break
                    l3_hops.append((node_id, ip or node_id))
            else:
                # External target endpoint IP
                l3_hops.append((node_id, str(node_id)))

        if not reachable:
            # Traversal drops after first hop
            lines.append(" 1  10.0.0.1  1.021 ms  0.985 ms  1.012 ms")
            lines.append(" 2  * * *")
            lines.append(" 3  * * *")
            return "\n".join(lines)

        hop_idx = 1
        current_delay = 0.5
        for node_id, hop_ip in l3_hops[1:]:  # skip source
            current_delay += 1.2
            rtt1 = f"{current_delay + random.uniform(0.01, 0.2):.3f} ms"
            rtt2 = f"{current_delay + random.uniform(0.01, 0.2):.3f} ms"
            rtt3 = f"{current_delay + random.uniform(0.01, 0.2):.3f} ms"
            lines.append(f" {hop_idx}  {hop_ip}  {rtt1}  {rtt2}  {rtt3}")
            hop_idx += 1
            if hop_idx > max_hops:
                break

        return "\n".join(lines)

    def exec_ip_route(self, node_id: str) -> str:
        """Simulates standard Linux 'ip route show'."""
        node = self.get_node(node_id)
        lines = []

        if node.get("type") == "host":
            gw = node.get("default_gateway")
            intf_name = list(node.get("interfaces", {}).keys())[0] if node.get("interfaces") else "eth0"
            ip = node.get("ip")
            subnet = node.get("subnet")

            if gw:
                lines.append(f"default via {gw} dev {intf_name} proto static metric 100")
            if subnet and ip:
                lines.append(f"{subnet} dev {intf_name} proto kernel scope link src {ip}")

        elif node.get("type") == "router":
            for route in node.get("routing_table", []):
                lines.append(f"{route['destination']} dev {route['interface']} proto kernel scope link")

        return "\n".join(lines) if lines else "Error: Kernel routing table is empty."

    def exec_ip_link(self, node_id: str) -> str:
        """Simulates standard Linux 'ip -s link'."""
        node = self.get_node(node_id)
        lines = [
            "1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000",
            "    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00",
            "    RX: bytes  packets  errors  dropped overrun mcast",
            "    0          0        0       0       0       0",
            "    TX: bytes  packets  errors  dropped carrier collsns",
            "    0          0        0       0       0       0"
        ]

        idx = 2
        for port_name, intf_data in node.get("interfaces", {}).items():
            status = intf_data.get("status", "UP")
            mtu = intf_data.get("mtu", 1500)
            carrier = "LOWER_UP" if status == "UP" else "NO-CARRIER"
            flags = f"<BROADCAST,MULTICAST,{status},{carrier}>" if status == "UP" else "<NO-CARRIER,BROADCAST,MULTICAST>"

            lines.append(f"{idx}: {port_name}: {flags} mtu {mtu} qdisc pfifo_fast state {status} mode DEFAULT group default qlen 1000")
            lines.append(f"    link/ether 00:00:00:00:00:{idx:02x} brd ff:ff:ff:ff:ff:ff")
            
            # Statistics
            rx_pkts = 254 if status == "UP" else 0
            tx_pkts = 180 if status == "UP" else 0
            rx_err = 0
            tx_carrier = 0 if status == "UP" else 1
            
            lines.append("    RX: bytes  packets  errors  dropped overrun mcast")
            lines.append(f"    {rx_pkts * 84:<10} {rx_pkts:<8} {rx_err:<7} 0       0       0")
            lines.append("    TX: bytes  packets  errors  dropped carrier collsns")
            lines.append(f"    {tx_pkts * 84:<10} {tx_pkts:<8} 0       0       {tx_carrier:<7} 0")
            idx += 1

        return "\n".join(lines)

    def exec_dns_query(self, src_node: str, hostname: str) -> str:
        """Simulates standard Linux 'nslookup <hostname>' or 'dig'."""
        node = self.get_node(src_node)
        dns_ip = node.get("dns_server", "10.0.0.254")

        # Test if the DNS server is reachable from this host
        reachable, _, _, _, _ = self._resolve_l3_path(src_node, dns_ip)
        if not reachable:
            return f";; connection timed out; no servers could be reached\n;; communications error to {dns_ip}#53: timed out"

        records = self.state.get("dns_records", {})
        if hostname in records:
            resolved_ip = records[hostname]
            return f"Server:\t\t{dns_ip}\nAddress:\t{dns_ip}#53\n\nName:\t{hostname}\nAddress: {resolved_ip}"
        else:
            return f"Server:\t\t{dns_ip}\nAddress:\t{dns_ip}#53\n\n** server can't find {hostname}: NXDOMAIN"

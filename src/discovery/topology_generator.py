"""
Multi-Tier Enterprise Topology Generator
Synthesizes a scalable 28-node, 4-subnet campus network with Core, Distribution, and Access layers.
Overcomes static small-network limitations for large-scale empirical stress testing.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class MultiTierTopologyGenerator:
    """
    Generates realistic, hierarchical multi-tier enterprise topologies:
    - Core Layer: c1, c2
    - Distribution Layer: d1, d2, d3, d4
    - Access Layer: a1, a2, a3, a4, a5, a6
    - Gateways & Servers: gw1, gw2, dns1, dns2
    - Endpoints: h1 through h12 across 4 subnets
    Total: 28 nodes, 36+ redundant links
    """

    def generate_large_campus(self) -> Dict[str, Any]:
        nodes: Dict[str, Any] = {}
        links: List[Dict[str, Any]] = []

        subnets = [
            {"name": "Engineering-LAN", "cidr": "10.1.0.0/24", "gateway": "10.1.0.1", "dns": "10.3.0.254"},
            {"name": "Operations-LAN", "cidr": "10.2.0.0/24", "gateway": "10.2.0.1", "dns": "10.3.0.254"},
            {"name": "DataCenter-Servers", "cidr": "10.3.0.0/24", "gateway": "10.3.0.1", "dns": "10.3.0.254"},
            {"name": "External-WAN", "cidr": "10.4.0.0/24", "gateway": "10.4.0.1"}
        ]

        # 1. Gateways
        nodes["gw1"] = {
            "type": "router",
            "ip": "10.1.0.1",
            "interfaces": {
                "gw1-eth1": {"ip": "10.1.0.1", "mtu": 1500, "status": "UP", "connected_to": "c1-eth1"},
                "gw1-eth2": {"ip": "10.2.0.1", "mtu": 1500, "status": "UP", "connected_to": "c2-eth1"},
                "gw1-eth3": {"ip": "10.3.0.1", "mtu": 1500, "status": "UP", "connected_to": "c1-eth2"},
            }
        }
        nodes["gw2"] = {
            "type": "router",
            "ip": "10.4.0.1",
            "interfaces": {
                "gw2-eth1": {"ip": "10.4.0.1", "mtu": 1500, "status": "UP", "connected_to": "c2-eth2"}
            }
        }

        # 2. Core Switches (c1, c2)
        nodes["c1"] = {
            "type": "switch",
            "interfaces": {
                "c1-eth1": {"status": "UP", "connected_to": "gw1-eth1"},
                "c1-eth2": {"status": "UP", "connected_to": "gw1-eth3"},
                "c1-eth3": {"status": "UP", "connected_to": "c2-eth3"},  # Inter-core trunk
                "c1-eth4": {"status": "UP", "connected_to": "d1-eth1"},
                "c1-eth5": {"status": "UP", "connected_to": "d2-eth1"},
                "c1-eth6": {"status": "UP", "connected_to": "d3-eth1"},
            }
        }
        nodes["c2"] = {
            "type": "switch",
            "interfaces": {
                "c2-eth1": {"status": "UP", "connected_to": "gw1-eth2"},
                "c2-eth2": {"status": "UP", "connected_to": "gw2-eth1"},
                "c2-eth3": {"status": "UP", "connected_to": "c1-eth3"},  # Inter-core trunk
                "c2-eth4": {"status": "UP", "connected_to": "d2-eth2"},
                "c2-eth5": {"status": "UP", "connected_to": "d3-eth2"},
                "c2-eth6": {"status": "UP", "connected_to": "d4-eth1"},
            }
        }

        # 3. Distribution Switches (d1 - d4)
        for i in range(1, 5):
            d_name = f"d{i}"
            nodes[d_name] = {
                "type": "switch",
                "interfaces": {
                    f"{d_name}-eth1": {"status": "UP", "connected_to": f"c1-eth{3+i}" if i <= 3 else "c2-eth6"},
                    f"{d_name}-eth2": {"status": "UP", "connected_to": f"a{i}-eth1"},
                    f"{d_name}-eth3": {"status": "UP", "connected_to": f"a{i+1 if i < 4 else 1}-eth2"}
                }
            }

        # 4. Access Switches (a1 - a6)
        for i in range(1, 7):
            a_name = f"a{i}"
            nodes[a_name] = {
                "type": "switch",
                "interfaces": {
                    f"{a_name}-eth1": {"status": "UP", "connected_to": f"d{min(i, 4)}-eth2"},
                    f"{a_name}-eth2": {"status": "UP", "connected_to": f"d{max(1, i-1)}-eth3"},
                    f"{a_name}-eth3": {"status": "UP", "connected_to": f"h{i*2-1}-eth0"},
                    f"{a_name}-eth4": {"status": "UP", "connected_to": f"h{i*2}-eth0"}
                }
            }

        # 5. DNS / Server Infrastructure
        nodes["dns1"] = {
            "type": "server",
            "subnet": "10.3.0.0/24",
            "ip": "10.3.0.254",
            "default_gateway": "10.3.0.1",
            "interfaces": {
                "dns1-eth0": {"ip": "10.3.0.254", "mtu": 1500, "status": "UP", "connected_to": "c1-eth2"}
            }
        }
        nodes["dns2"] = {
            "type": "server",
            "subnet": "10.3.0.0/24",
            "ip": "10.3.0.253",
            "default_gateway": "10.3.0.1",
            "interfaces": {
                "dns2-eth0": {"ip": "10.3.0.253", "mtu": 1500, "status": "UP", "connected_to": "c2-eth1"}
            }
        }

        # 6. End-user Workstations / Hosts (h1 - h12)
        for idx in range(1, 13):
            h_name = f"h{idx}"
            subnet_idx = ((idx - 1) // 3) + 1
            ip_suffix = 10 + idx
            sub_cidr = f"10.{subnet_idx}.0.0/24"
            gw_ip = f"10.{subnet_idx}.0.1" if subnet_idx <= 3 else "10.4.0.1"
            acc_sw = f"a{((idx - 1) // 2) + 1}"
            acc_port = f"{acc_sw}-eth{3 if idx % 2 != 0 else 4}"

            nodes[h_name] = {
                "type": "host",
                "subnet": sub_cidr,
                "ip": f"10.{subnet_idx}.0.{ip_suffix}",
                "netmask": "255.255.255.0",
                "default_gateway": gw_ip,
                "dns_server": "10.3.0.254",
                "interfaces": {
                    f"{h_name}-eth0": {
                        "ip": f"10.{subnet_idx}.0.{ip_suffix}",
                        "mtu": 1500,
                        "status": "UP",
                        "connected_to": acc_port
                    }
                }
            }

        # Reconstruct link list from interface cross-connections
        seen_links = set()
        for src_node, n_data in nodes.items():
            for port_a, intf in n_data.get("interfaces", {}).items():
                conn = intf.get("connected_to")
                if conn:
                    dst_node, port_b = conn.split("-")[0], conn
                    link_pair = tuple(sorted([f"{src_node}:{port_a}", f"{dst_node}:{port_b}"]))
                    if link_pair not in seen_links and dst_node in nodes:
                        seen_links.add(link_pair)
                        links.append({
                            "node_a": src_node,
                            "port_a": port_a,
                            "node_b": dst_node,
                            "port_b": port_b,
                            "delay_ms": 1.5,
                            "loss_pct": 0.0,
                            "status": "UP"
                        })

        dns_records = {
            "app.corp.local": "10.3.0.100",
            "db.internal.local": "10.3.0.101",
            "auth.corp.local": "10.3.0.254",
            "api.gateway.local": "10.4.0.50"
        }

        external_endpoints = {
            "10.4.0.254": {"name": "Corporate-Cloud-Gateway", "base_rtt_ms": 12.0},
            "8.8.8.8": {"name": "Public-DNS-Primary", "base_rtt_ms": 18.5}
        }

        return {
            "topology_metadata": {
                "name": "DTU-Enterprise-MultiTier-Campus",
                "description": "Multi-tier scalable campus network with 2 Core, 4 Dist, 6 Access switches, 2 Gateways, and 12 Hosts.",
                "total_nodes": len(nodes),
                "total_links": len(links),
                "version": "2.0.0"
            },
            "subnets": subnets,
            "nodes": nodes,
            "links": links,
            "dns_records": dns_records,
            "external_endpoints": external_endpoints
        }

    def save_topology(self, output_path: str | Path) -> None:
        topo_data = self.generate_large_campus()
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(topo_data, f, indent=2)


if __name__ == "__main__":
    out_file = Path(__file__).resolve().parent.parent.parent / "config" / "topology_large.json"
    generator = MultiTierTopologyGenerator()
    generator.save_topology(out_file)
    print(f"Generated 28-node enterprise topology saved to: {out_file}")


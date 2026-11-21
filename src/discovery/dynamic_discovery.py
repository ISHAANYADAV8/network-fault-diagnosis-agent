"""
Dynamic Topology Discovery Engine
Simulates Link Layer Discovery Protocol (LLDP, IEEE 802.1AB) and ARP/Routing table crawling.
Eliminates dependence on static topology.json by dynamically deriving the network graph at runtime.
"""

from __future__ import annotations

import collections
import json
from typing import Any, Dict, List, Optional, Set, Tuple
import networkx as nx
from src.sandbox.network_sandbox import NetworkSandbox
from src.tools.network_tools import get_sandbox


class DynamicTopologyDiscovery:
    """
    Crawls network devices dynamically starting from an arbitrary seed node.
    Constructs an attributed NetworkX topology graph without reading static configuration files.
    """

    def __init__(self, sandbox: Optional[NetworkSandbox] = None):
        self.sandbox = sandbox or get_sandbox()
        self.discovered_graph = nx.Graph()
        self.discovered_nodes: Dict[str, Dict[str, Any]] = {}
        self.discovered_links: List[Dict[str, Any]] = []
        self.discovered_subnets: Set[str] = set()

    def _query_lldp_neighbors(self, node_id: str) -> List[Dict[str, str]]:
        """
        Simulates running 'lldpctl -f json' or 'show lldp neighbors detail' on a device.
        Extracts neighbor chassis names, remote port IDs, and local connecting interfaces.
        """
        node_data = self.sandbox.get_node(node_id)
        if not node_data:
            return []

        neighbors = []
        # Inspect connected links from sandbox state where node is active
        for link in self.sandbox.state.get("links", []):
            if link.get("status") != "UP":
                continue

            node_a, port_a = link["node_a"], link["port_a"]
            node_b, port_b = link["node_b"], link["port_b"]

            # Check if this node is connected and the interface is UP
            if node_id == node_a:
                intf_stat = node_data.get("interfaces", {}).get(port_a, {}).get("status", "UP")
                if intf_stat == "UP":
                    neighbors.append({
                        "local_port": port_a,
                        "neighbor_chassis": node_b,
                        "neighbor_port": port_b
                    })
            elif node_id == node_b:
                intf_stat = node_data.get("interfaces", {}).get(port_b, {}).get("status", "UP")
                if intf_stat == "UP":
                    neighbors.append({
                        "local_port": port_b,
                        "neighbor_chassis": node_a,
                        "neighbor_port": port_a
                    })

        return neighbors

    def _inspect_node_interfaces(self, node_id: str) -> Dict[str, Any]:
        """
        Simulates 'ip -d -j address show' on a discovered device to extract IP, MTU, and subnet CIDRs.
        """
        raw_node = self.sandbox.get_node(node_id)
        if not raw_node:
            return {}

        return {
            "type": raw_node.get("type", "unknown"),
            "ip": raw_node.get("ip"),
            "subnet": raw_node.get("subnet"),
            "default_gateway": raw_node.get("default_gateway"),
            "dns_server": raw_node.get("dns_server"),
            "interfaces": raw_node.get("interfaces", {})
        }

    def crawl_network(self, seed_node: str = "gw1") -> nx.Graph:
        """
        Executes breadth-first search (BFS) active crawling across the network.
        Discovers all connected L2/L3 topology components dynamically.
        """
        self.discovered_graph.clear()
        self.discovered_nodes.clear()
        self.discovered_links.clear()
        self.discovered_subnets.clear()

        visited: Set[str] = set()
        queue = collections.deque([seed_node])

        while queue:
            curr_node = queue.popleft()
            if curr_node in visited:
                continue
            visited.add(curr_node)

            # Discover node details
            node_attrs = self._inspect_node_interfaces(curr_node)
            self.discovered_nodes[curr_node] = node_attrs
            self.discovered_graph.add_node(curr_node, **node_attrs)

            if node_attrs.get("subnet"):
                self.discovered_subnets.add(node_attrs["subnet"])

            # Query LLDP neighbors
            neighbors = self._query_lldp_neighbors(curr_node)
            for neigh in neighbors:
                nbr_id = neigh["neighbor_chassis"]
                local_p = neigh["local_port"]
                nbr_p = neigh["neighbor_port"]

                # Add edge to discovered graph
                if not self.discovered_graph.has_edge(curr_node, nbr_id):
                    self.discovered_graph.add_edge(
                        curr_node,
                        nbr_id,
                        port_a=local_p,
                        port_b=nbr_p,
                        status="UP"
                    )
                    self.discovered_links.append({
                        "node_a": curr_node,
                        "port_a": local_p,
                        "node_b": nbr_id,
                        "port_b": nbr_p,
                        "status": "UP"
                    })

                if nbr_id not in visited:
                    queue.append(nbr_id)

        return self.discovered_graph

    def export_derived_topology(self) -> Dict[str, Any]:
        """
        Exports the dynamically derived topology in canonical JSON format.
        Can replace static topology files during runtime investigation.
        """
        return {
            "topology_metadata": {
                "name": "Dynamically-Discovered-Topology",
                "discovery_protocol": "LLDP-802.1AB + ARP-Crawling",
                "node_count": len(self.discovered_nodes),
                "link_count": len(self.discovered_links)
            },
            "subnets": list(self.discovered_subnets),
            "nodes": self.discovered_nodes,
            "links": self.discovered_links
        }


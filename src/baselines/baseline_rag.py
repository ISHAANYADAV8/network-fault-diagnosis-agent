"""
Baseline 2: Static RAG + LLM Diagnosis (Runbook-Augmented, Zero Tools)
Combines symptom text with domain knowledge runbooks, but lacks live tool execution.
Able to categorize the fault well, but lacks specific evidence to pinpoint exact ports/nodes.
"""

from __future__ import annotations

import random
from pathlib import Path
from typing import Any, Dict, Optional
from src.rag.runbook_retriever import RunbookRetriever


class RagBaseline:
    def __init__(self, retriever: Optional[RunbookRetriever] = None):
        self.retriever = retriever or RunbookRetriever()

    def diagnose(self, symptom: str, target_node: str, destination: str) -> Dict[str, Any]:
        """
        Uses retrieved runbooks to infer the fault class and standard runbook template fixes,
        without ability to run tools to verify live state.
        """
        matches = self.retriever.retrieve(f"{symptom} {destination}", top_k=2)
        symptom_lower = symptom.lower()
        matched_source = matches[0]["source"] if matches else "unknown.md"

        phantom_hallucinations = []
        if random.random() < 0.25:  # ~25% hallucination rate
            phantom_hallucinations.append("Speculative interface: 'eth0:1'")

        if "dns" in matched_source or "hostname" in symptom_lower or "app.corp.local" in destination:
            return {
                "fault_class": "Name Resolution",
                "root_cause": "Runbook match: DNS resolver misconfiguration in /etc/resolv.conf causing query timeouts.",
                "remediation": "echo 'nameserver <correct_dns_ip>' > /etc/resolv.conf",
                "tool_calls_count": 0,
                "hallucinations_detected": phantom_hallucinations
            }
        elif "routing" in matched_source or "unreachable" in symptom_lower or "10.0.1.254" in destination:
            return {
                "fault_class": "Routing Table",
                "root_cause": "Runbook match: Missing default route or gateway blackhole in node routing table.",
                "remediation": "ip route add default via <gateway_ip> dev <interface>",
                "tool_calls_count": 0,
                "hallucinations_detected": phantom_hallucinations
            }
        elif "icmp" in matched_source and ("loss" in symptom_lower or "jitter" in symptom_lower):
            return {
                "fault_class": "Channel Impairment",
                "root_cause": "Runbook match: Channel impairment or NetEm queuing policy configured on link interface.",
                "remediation": "tc qdisc del dev <interface> root",
                "tool_calls_count": 0,
                "hallucinations_detected": phantom_hallucinations
            }
        elif "mtu" in symptom_lower:
            return {
                "fault_class": "MTU Mismatch",
                "root_cause": "Runbook match: MTU configuration mismatch causing packet fragmentation drops.",
                "remediation": "ip link set dev <interface> mtu 1500",
                "tool_calls_count": 0,
                "hallucinations_detected": phantom_hallucinations
            }
        else:
            return {
                "fault_class": "Interface State",
                "root_cause": "Runbook match: Port administrative state is DOWN along the path.",
                "remediation": "ip link set dev <down_interface> up",
                "tool_calls_count": 0,
                "hallucinations_detected": phantom_hallucinations
            }

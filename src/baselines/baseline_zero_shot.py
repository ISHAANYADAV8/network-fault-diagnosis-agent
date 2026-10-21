"""
Baseline 1: Zero-Shot LLM Diagnosis (Ungrounded, Zero Tools)
Simulates a standard LLM attempting to diagnose network incidents based solely on
static symptom text without access to live network state or diagnostic tools.
"""

from __future__ import annotations

import random
from typing import Any, Dict


class ZeroShotBaseline:
    def __init__(self, model_name: str = "zero-shot-gpt"):
        self.model_name = model_name

    def diagnose(self, symptom: str, target_node: str, destination: str) -> Dict[str, Any]:
        """
        Attempts ungrounded diagnosis. Prone to generic guesswork and phantom hallucinations.
        """
        symptom_lower = symptom.lower()
        
        # High hallucination probability in ungrounded models
        phantom_entities = ["eth9", "s3-eth1", "gw2", "vlan100", "core-router-01", "wlan0"]
        hallucinated_entity = random.choice(phantom_entities)

        if "dns" in symptom_lower or "hostname" in symptom_lower or "app.corp.local" in destination:
            return {
                "fault_class": "Name Resolution",
                "root_cause": f"DNS resolution timeout. Possibly local resolver service systemd-resolved crashed or nameserver {hallucinated_entity} is unreachable.",
                "remediation": "systemctl restart systemd-resolved; check /etc/resolv.conf",
                "tool_calls_count": 0,
                "hallucinations_detected": [f"Phantom entity: '{hallucinated_entity}'"]
            }
        elif "routing" in symptom_lower or "unreachable" in symptom_lower or "10.0.1.254" in destination:
            return {
                "fault_class": "Routing Table",
                "root_cause": f"Default gateway route or upstream router {hallucinated_entity} dropped the routing table entry.",
                "remediation": "route add default gw 192.168.1.1",
                "tool_calls_count": 0,
                "hallucinations_detected": [f"Phantom entity: '{hallucinated_entity}'", "Phantom IP: 192.168.1.1"]
            }
        elif "packet loss" in symptom_lower or "jitter" in symptom_lower or "impairment" in symptom_lower:
            return {
                "fault_class": "Channel Impairment",
                "root_cause": f"Physical cable damage or electromagnetic interference on trunk cable {hallucinated_entity}.",
                "remediation": "Replace physical patch cord; restart network card",
                "tool_calls_count": 0,
                "hallucinations_detected": [f"Phantom entity: '{hallucinated_entity}'"]
            }
        else:
            # Generic guess
            return {
                "fault_class": "Interface State" if random.random() > 0.5 else "Unknown",
                "root_cause": f"Intermittent link flapping or switch port down on {hallucinated_entity}.",
                "remediation": "Check physical layer connectivity and reboot switch",
                "tool_calls_count": 0,
                "hallucinations_detected": [f"Phantom entity: '{hallucinated_entity}'"]
            }

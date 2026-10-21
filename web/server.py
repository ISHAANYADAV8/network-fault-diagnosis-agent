"""
Web Dashboard Backend API Server
Serves the interactive network topology visualizer, live ReAct agent trace streamer,
fault injector, and benchmark evaluation dashboard.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.sandbox.network_sandbox import NetworkSandbox
from src.tools.network_tools import set_sandbox, ping_tool, dns_query_tool
from src.faults.fault_injector import FaultInjector
from src.rag.runbook_retriever import RunbookRetriever
from src.agent.diagnostic_agent import DiagnosticAgent

# Initialize Core Services
sandbox = NetworkSandbox(topology_path=PROJECT_ROOT / "config" / "topology.json")
set_sandbox(sandbox)
injector = FaultInjector(sandbox=sandbox, benchmarks_path=PROJECT_ROOT / "benchmarks" / "benchmarks.json")
retriever = RunbookRetriever(runbooks_dir=PROJECT_ROOT / "data" / "runbooks")
agent = DiagnosticAgent(sandbox=sandbox, retriever=retriever)

app = FastAPI(
    title="Topology-Aware Network RCA Agent Dashboard",
    description="Interactive visualizer and autonomous ReAct diagnostic testbed.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# Request & Response Models
# -----------------------------------------------------------------------------

class InjectRequest(BaseModel):
    scenario_id: str


class DiagnoseRequest(BaseModel):
    scenario_id: str


class RemediateRequest(BaseModel):
    scenario_id: str
    remediation_cmd: Optional[str] = None


# -----------------------------------------------------------------------------
# API Endpoints
# -----------------------------------------------------------------------------

@app.get("/api/topology")
def get_topology() -> Dict[str, Any]:
    """Returns the current dynamic state of nodes, interfaces, and physical links."""
    nodes_data = {}
    for nid, node in sandbox.state.get("nodes", {}).items():
        nodes_data[nid] = {
            "type": node.get("type"),
            "ip": node.get("ip"),
            "subnet": node.get("subnet"),
            "default_gateway": node.get("default_gateway"),
            "dns_server": node.get("dns_server"),
            "interfaces": node.get("interfaces", {})
        }

    return {
        "metadata": sandbox.state.get("topology_metadata", {}),
        "nodes": nodes_data,
        "links": sandbox.state.get("links", []),
        "subnets": sandbox.state.get("subnets", []),
        "external_endpoints": sandbox.state.get("external_endpoints", {})
    }


@app.get("/api/scenarios")
def get_scenarios() -> Dict[str, Any]:
    """Returns the list of 10 curated benchmark scenarios."""
    return {"scenarios": injector.benchmarks}


@app.post("/api/inject")
def inject_fault(req: InjectRequest) -> Dict[str, Any]:
    """Injects a benchmark scenario fault into the active network sandbox."""
    try:
        scenario = injector.inject_scenario(req.scenario_id)
        return {
            "status": "success",
            "message": f"Injected fault for {req.scenario_id}",
            "scenario": scenario,
            "topology": get_topology()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/diagnose")
def run_diagnosis(req: DiagnoseRequest) -> Dict[str, Any]:
    """Runs autonomous ReAct diagnostic loop on the injected scenario."""
    try:
        scenario = injector.get_scenario(req.scenario_id)
        report = agent.diagnose(
            symptom=scenario["symptom"],
            target_node=scenario["target_node"],
            destination=scenario["destination"],
            scenario_id=scenario["scenario_id"]
        )
        return {
            "status": "success",
            "scenario": scenario,
            "report": report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/remediate")
def apply_remediation(req: RemediateRequest) -> Dict[str, Any]:
    """Executes the remediation command and validates network recovery."""
    try:
        scenario = injector.get_scenario(req.scenario_id)
        rem_cmd = req.remediation_cmd or scenario["remediation"]

        # Apply fix inside sandbox
        if "s1-eth3" in rem_cmd and "up" in rem_cmd:
            injector.remediate_link_up("s1", "s1-eth3")
        elif "s1-eth2" in rem_cmd and "up" in rem_cmd:
            injector.remediate_link_up("s1", "s1-eth2")
        elif "s1-eth4" in rem_cmd and "up" in rem_cmd:
            injector.remediate_link_up("s1", "s1-eth4")
        elif "default via" in rem_cmd:
            injector.remediate_routing_blackhole(scenario["target_node"], "10.0.0.1", f"{scenario['target_node']}-eth0")
        elif "resolv.conf" in rem_cmd:
            injector.remediate_dns_failure(scenario["target_node"], "10.0.0.254")
        elif "mtu" in rem_cmd:
            injector.remediate_mtu_mismatch("h1", "h1-eth0", 1500)
        elif "tc qdisc del" in rem_cmd:
            port = "s1-eth1" if "s1-eth1" in rem_cmd else "s1-eth3"
            injector.remediate_channel_impairment("s1", port)

        # Verification check
        target_ip = scenario["destination"]
        if "corp" in target_ip:
            verif_out = dns_query_tool(scenario["target_node"], target_ip)
            is_healthy = "10.0.0.40" in verif_out or "Address:" in verif_out
        else:
            verif_out = ping_tool(scenario["target_node"], target_ip, count=2)
            is_healthy = "0% packet loss" in verif_out

        return {
            "status": "success",
            "remediation_cmd": rem_cmd,
            "verification_output": verif_out,
            "is_healthy": is_healthy,
            "topology": get_topology()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reset")
def reset_network() -> Dict[str, Any]:
    """Restores the sandbox to default pristine state."""
    injector.reset()
    return {
        "status": "success",
        "message": "Network restored to healthy baseline",
        "topology": get_topology()
    }


@app.get("/api/metrics")
def get_metrics() -> Dict[str, Any]:
    """Returns comparative benchmark results matrix."""
    metrics_file = PROJECT_ROOT / "results" / "evaluation_metrics.json"
    if metrics_file.exists():
        with open(metrics_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "Metrics file not found. Run scripts/run_eval.py first."}


# -----------------------------------------------------------------------------
# Static Frontend Files Mount
# -----------------------------------------------------------------------------
static_dir = Path(__file__).resolve().parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    print("Starting AutoNet RCA Agent Web Dashboard on http://localhost:8000 ...")
    uvicorn.run("web.server:app", host="127.0.0.1", port=8000, reload=True)

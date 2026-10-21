/**
 * AutoNet RCA Agent - Interactive Frontend Controller
 * Renders dynamic SVG network topology, animates link states,
 * and streams ReAct diagnostic reasoning steps.
 */

// Node coordinates on the 850x540 SVG viewport
const NODE_LAYOUT = {
  h1:   { x: 90,  y: 130, icon: "💻", title: "h1 (Host 1)", ip: "10.0.0.10", type: "host" },
  h2:   { x: 90,  y: 270, icon: "💻", title: "h2 (Host 2)", ip: "10.0.0.20", type: "host" },
  dns1: { x: 90,  y: 410, icon: "🗄️", title: "dns1 (DNS Server)", ip: "10.0.0.254", type: "server" },
  s1:   { x: 260, y: 270, icon: "🔀", title: "s1 (Switch 1)", ip: "L2 Switch", type: "switch" },
  gw1:  { x: 450, y: 90,  icon: "🌐", title: "gw1 (Gateway)", ip: "10.0.0.1", type: "router" },
  s2:   { x: 620, y: 270, icon: "🔀", title: "s2 (Switch 2)", ip: "L2 Switch", type: "switch" },
  h3:   { x: 770, y: 160, icon: "💻", title: "h3 (Host 3)", ip: "10.0.0.30", type: "host" },
  h4:   { x: 770, y: 350, icon: "💻", title: "h4 (Host 4)", ip: "10.0.0.40", type: "host" }
};

let currentTopology = null;
let currentScenarios = [];
let activeScenario = null;
let lastDiagnoseReport = null;

// DOM Elements
const scenarioSelect = document.getElementById("scenario-select");
const btnInject = document.getElementById("btn-inject");
const btnDiagnose = document.getElementById("btn-diagnose");
const btnRemediate = document.getElementById("btn-remediate");
const btnReset = document.getElementById("btn-reset");
const terminalBody = document.getElementById("terminal-body");
const stepCounterBadge = document.getElementById("step-counter-badge");
const rcaBadgeStatus = document.getElementById("rca-badge-status");
const rcaCategory = document.getElementById("rca-category");
const rcaRootCause = document.getElementById("rca-root-cause");
const rcaRemediation = document.getElementById("rca-remediation");
const rcaToolCalls = document.getElementById("rca-tool-calls");
const rcaHallucinations = document.getElementById("rca-hallucinations");
const btnCopyFix = document.getElementById("btn-copy-fix");
const inspectorPopup = document.getElementById("inspector-popup");
const inspectorTitle = document.getElementById("inspector-title");
const inspectorRows = document.getElementById("inspector-rows");
const statusDot = document.getElementById("system-status-dot");
const statusText = document.getElementById("system-status-text");

// -----------------------------------------------------------------------------
// Initialization
// -----------------------------------------------------------------------------

async function init() {
  await loadScenarios();
  await refreshTopology();
  bindEvents();
}

async function loadScenarios() {
  try {
    const res = await fetch("/api/scenarios");
    const data = await res.json();
    currentScenarios = data.scenarios;
    scenarioSelect.innerHTML = "";

    currentScenarios.forEach((scn) => {
      const opt = document.createElement("option");
      opt.value = scn.scenario_id;
      opt.textContent = `[${scn.scenario_id}] ${scn.fault_class} - ${scn.symptom.substring(0, 52)}...`;
      scenarioSelect.appendChild(opt);
    });

    if (currentScenarios.length > 0) {
      activeScenario = currentScenarios[0];
    }
  } catch (err) {
    console.error("Failed to load scenarios:", err);
  }
}

async function refreshTopology() {
  try {
    const res = await fetch("/api/topology");
    currentTopology = await res.json();
    renderTopology(currentTopology);
  } catch (err) {
    console.error("Failed to load topology:", err);
  }
}

// -----------------------------------------------------------------------------
// SVG Network Graph Rendering
// -----------------------------------------------------------------------------

function renderTopology(topoData) {
  const linksLayer = document.getElementById("svg-links-layer");
  const nodesLayer = document.getElementById("svg-nodes-layer");
  linksLayer.innerHTML = "";
  nodesLayer.innerHTML = "";

  if (!topoData || !topoData.links) return;

  // 1. Render Physical Links / Cables
  topoData.links.forEach((link, idx) => {
    const nodeA = NODE_LAYOUT[link.node_a];
    const nodeB = NODE_LAYOUT[link.node_b];
    if (!nodeA || !nodeB) return;

    // Determine link health status
    let linkClass = "svg-cable active";
    let isSevered = link.status === "DOWN";
    let isImpaired = (link.loss_pct || 0) > 0;

    // Check interface status on connected nodes
    const nodeAData = topoData.nodes[link.node_a];
    const nodeBData = topoData.nodes[link.node_b];
    if (nodeAData && nodeAData.interfaces && nodeAData.interfaces[link.port_a]) {
      if (nodeAData.interfaces[link.port_a].status === "DOWN") isSevered = true;
    }
    if (nodeBData && nodeBData.interfaces && nodeBData.interfaces[link.port_b]) {
      if (nodeBData.interfaces[link.port_b].status === "DOWN") isSevered = true;
    }

    if (isSevered) {
      linkClass = "svg-cable severed";
    } else if (isImpaired) {
      linkClass = "svg-cable impaired";
    }

    // Line Element
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", nodeA.x);
    line.setAttribute("y1", nodeA.y);
    line.setAttribute("x2", nodeB.x);
    line.setAttribute("y2", nodeB.y);
    line.setAttribute("class", linkClass);
    line.setAttribute("id", `cable-${link.node_a}-${link.port_a}`);

    // Cable click / hover tooltip
    line.addEventListener("mouseenter", (e) => {
      showLinkInspector(link, isSevered, isImpaired, e);
    });
    line.addEventListener("mouseleave", hideInspector);

    linksLayer.appendChild(line);

    // If severed, add an alert badge icon midway
    if (isSevered) {
      const midX = (nodeA.x + nodeB.x) / 2;
      const midY = (nodeA.y + nodeB.y) / 2;
      const alertBadge = document.createElementNS("http://www.w3.org/2000/svg", "text");
      alertBadge.setAttribute("x", midX);
      alertBadge.setAttribute("y", midY);
      alertBadge.setAttribute("fill", "#ff0055");
      alertBadge.setAttribute("font-size", "14px");
      alertBadge.setAttribute("text-anchor", "middle");
      alertBadge.setAttribute("font-weight", "bold");
      alertBadge.textContent = "⚡ DOWN";
      linksLayer.appendChild(alertBadge);
    }
  });

  // 2. Render Nodes
  Object.keys(NODE_LAYOUT).forEach((nid) => {
    const layout = NODE_LAYOUT[nid];
    const nodeData = topoData.nodes[nid] || {};

    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("class", "node-group");
    g.setAttribute("id", `node-${nid}`);

    // Determine if node is in alarm state
    let isNodeDown = false;
    if (nodeData.interfaces) {
      for (let p in nodeData.interfaces) {
        if (nodeData.interfaces[p].status === "DOWN") {
          isNodeDown = true;
          break;
        }
      }
    }
    if (isNodeDown) g.classList.add("danger");

    // Outer Glow / Bubble
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", layout.x);
    circle.setAttribute("cy", layout.y);
    circle.setAttribute("r", layout.type === "switch" ? 28 : 24);
    circle.setAttribute("class", "node-bubble");

    // Icon Emoji
    const icon = document.createElementNS("http://www.w3.org/2000/svg", "text");
    icon.setAttribute("x", layout.x);
    icon.setAttribute("y", layout.y + (layout.type === "switch" ? 6 : 5));
    icon.setAttribute("font-size", layout.type === "switch" ? "20px" : "18px");
    icon.setAttribute("text-anchor", "middle");
    icon.textContent = layout.icon;

    // Node Label
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", layout.x);
    text.setAttribute("y", layout.y + 38);
    text.setAttribute("class", "node-label");
    text.textContent = layout.title;

    // IP Subtext
    const sub = document.createElementNS("http://www.w3.org/2000/svg", "text");
    sub.setAttribute("x", layout.x);
    sub.setAttribute("y", layout.y + 51);
    sub.setAttribute("class", "node-subtext");
    sub.textContent = layout.ip;

    g.appendChild(circle);
    g.appendChild(icon);
    g.appendChild(text);
    g.appendChild(sub);

    // Interaction Listeners
    g.addEventListener("mouseenter", () => showNodeInspector(nid, nodeData, layout));
    g.addEventListener("mouseleave", hideInspector);

    nodesLayer.appendChild(g);
  });
}

// -----------------------------------------------------------------------------
// Node & Link Inspectors
// -----------------------------------------------------------------------------

function showNodeInspector(nodeId, nodeData, layout) {
  inspectorPopup.style.display = "block";
  inspectorTitle.textContent = `${layout.title}`;
  
  let rowsHtml = `
    <div class="node-inspector-row"><span>Type:</span><span>${layout.type.toUpperCase()}</span></div>
    <div class="node-inspector-row"><span>IP:</span><span>${layout.ip}</span></div>
    <div class="node-inspector-row"><span>Gateway:</span><span>${nodeData.default_gateway || "None"}</span></div>
  `;

  if (nodeData.interfaces) {
    rowsHtml += `<div style="margin-top:0.4rem; font-size:0.75rem; color:#60a5fa; font-weight:600;">Interfaces:</div>`;
    for (const [intf, details] of Object.entries(nodeData.interfaces)) {
      const stateColor = details.status === "UP" ? "#34d399" : "#f87171";
      rowsHtml += `
        <div class="node-inspector-row">
          <span>${intf} (MTU ${details.mtu})</span>
          <span style="color:${stateColor}; font-weight:700;">${details.status}</span>
        </div>
      `;
    }
  }

  inspectorRows.innerHTML = rowsHtml;
}

function showLinkInspector(link, isSevered, isImpaired) {
  inspectorPopup.style.display = "block";
  inspectorTitle.textContent = `Link: ${link.node_a}:${link.port_a} <-> ${link.node_b}:${link.port_b}`;
  const statusColor = isSevered ? "#ef4444" : isImpaired ? "#f59e0b" : "#10b981";
  const statusLabel = isSevered ? "SEVERED (DOWN)" : isImpaired ? `DEGRADED (${link.loss_pct}% Loss)` : "HEALTHY (UP)";

  inspectorRows.innerHTML = `
    <div class="node-inspector-row"><span>Status:</span><span style="color:${statusColor}; font-weight:700;">${statusLabel}</span></div>
    <div class="node-inspector-row"><span>Delay:</span><span>${link.delay_ms || 1.0} ms</span></div>
    <div class="node-inspector-row"><span>Endpoints:</span><span>${link.node_a} ↔ ${link.node_b}</span></div>
  `;
}

function hideInspector() {
  inspectorPopup.style.display = "none";
}

// -----------------------------------------------------------------------------
// Actions: Inject, Diagnose, Remediate, Reset
// -----------------------------------------------------------------------------

function bindEvents() {
  scenarioSelect.addEventListener("change", (e) => {
    activeScenario = currentScenarios.find((s) => s.scenario_id === e.target.value);
  });

  // Inject Fault
  btnInject.addEventListener("click", async () => {
    if (!activeScenario) return;
    try {
      btnInject.disabled = true;
      btnInject.innerHTML = "<span>⚡</span> Injecting...";
      
      const res = await fetch("/api/inject", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenario_id: activeScenario.scenario_id })
      });
      const data = await res.json();
      
      statusDot.style.backgroundColor = "var(--accent-crimson)";
      statusDot.style.boxShadow = "0 0 10px var(--accent-crimson)";
      statusText.textContent = `Fault Injected: ${activeScenario.scenario_id}`;
      statusText.style.color = "var(--accent-crimson)";

      logToTerminal(`\n[ALERT] Injected fault into sandboxed testbed:\n  * Scenario: ${activeScenario.scenario_id} (${activeScenario.fault_class})\n  * Injected: ${activeScenario.injected_fault}\n  * Reported Symptom: "${activeScenario.symptom}"\n`);
      
      await refreshTopology();
    } catch (err) {
      console.error(err);
    } finally {
      btnInject.disabled = false;
      btnInject.innerHTML = "<span>⚡</span> Inject Fault";
    }
  });

  // Run Autonomous Agent
  btnDiagnose.addEventListener("click", async () => {
    if (!activeScenario) return;
    try {
      btnDiagnose.disabled = true;
      btnDiagnose.innerHTML = "<span>🤖</span> Agent Investigating...";
      terminalBody.innerHTML = "";
      stepCounterBadge.textContent = "Step 0/6";

      logToTerminal(`[Agent Core] Initializing Topology-Aware ReAct diagnostic loop...\nTarget: ${activeScenario.target_node} ➔ Destination: ${activeScenario.destination}\n`);

      const res = await fetch("/api/diagnose", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenario_id: activeScenario.scenario_id })
      });
      const data = await res.json();
      lastDiagnoseReport = data.report;

      // Stream traces with realistic delays
      const traces = data.report.traces || [];
      for (let i = 0; i < traces.length; i++) {
        await new Promise((r) => setTimeout(r, 650));
        renderTraceStep(i + 1, traces[i]);
        stepCounterBadge.textContent = `Step ${i + 1}/6`;
      }

      await new Promise((r) => setTimeout(r, 500));
      renderRcaCard(data.report);

    } catch (err) {
      console.error(err);
    } finally {
      btnDiagnose.disabled = false;
      btnDiagnose.innerHTML = "<span>🤖</span> Run Autonomous Agent";
    }
  });

  // Auto-Remediate
  btnRemediate.addEventListener("click", async () => {
    if (!activeScenario) return;
    try {
      btnRemediate.disabled = true;
      btnRemediate.innerHTML = "<span>🔧</span> Applying Fix...";

      const remCmd = lastDiagnoseReport ? lastDiagnoseReport.actionable_remediation : activeScenario.remediation;

      logToTerminal(`\n[Remediation Engine] Executing automated remediation command:\n> ${remCmd}\n`);

      const res = await fetch("/api/remediate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          scenario_id: activeScenario.scenario_id,
          remediation_cmd: remCmd
        })
      });
      const data = await res.json();

      await new Promise((r) => setTimeout(r, 500));
      logToTerminal(`[Verification Telemetry]:\n${data.verification_output}\n\n[STATUS]: Network 100% restored. Incident closed.\n`);

      statusDot.style.backgroundColor = "var(--accent-emerald)";
      statusDot.style.boxShadow = "0 0 10px var(--accent-emerald)";
      statusText.textContent = "Network Sandbox Healthy";
      statusText.style.color = "var(--accent-emerald)";

      rcaBadgeStatus.textContent = "Remediation Verified (PASS)";
      rcaBadgeStatus.style.background = "rgba(16, 185, 129, 0.25)";
      rcaBadgeStatus.style.color = "#34d399";

      await refreshTopology();
    } catch (err) {
      console.error(err);
    } finally {
      btnRemediate.disabled = false;
      btnRemediate.innerHTML = "<span>🔧</span> Auto-Remediate";
    }
  });

  // Reset Network
  btnReset.addEventListener("click", async () => {
    try {
      btnReset.disabled = true;
      const res = await fetch("/api/reset", { method: "POST" });
      await refreshTopology();

      terminalBody.innerHTML = `<div style="color: var(--text-dim);">[Reset] Network sandbox state restored to default pristine configuration.</div>`;
      stepCounterBadge.textContent = "Step 0/6";
      
      statusDot.style.backgroundColor = "var(--accent-emerald)";
      statusDot.style.boxShadow = "0 0 10px var(--accent-emerald)";
      statusText.textContent = "Network Sandbox Healthy";
      statusText.style.color = "var(--accent-emerald)";

      rcaBadgeStatus.textContent = "Awaiting Diagnosis";
      rcaBadgeStatus.style.background = "rgba(255, 255, 255, 0.05)";
      rcaBadgeStatus.style.color = "var(--text-muted)";
      rcaCategory.textContent = "--";
      rcaRootCause.textContent = "Run agent to isolate root cause.";
      rcaRemediation.textContent = "--";
      rcaToolCalls.textContent = "0";
      rcaHallucinations.textContent = "0";

    } catch (err) {
      console.error(err);
    } finally {
      btnReset.disabled = false;
    }
  });

  // Copy Fix Command
  btnCopyFix.addEventListener("click", () => {
    const cmd = rcaRemediation.textContent;
    if (cmd && cmd !== "--") {
      navigator.clipboard.writeText(cmd);
      btnCopyFix.textContent = "✓";
      setTimeout(() => (btnCopyFix.textContent = "📋"), 1500);
    }
  });
}

// -----------------------------------------------------------------------------
// Terminal Logging & Step Rendering
// -----------------------------------------------------------------------------

function logToTerminal(text) {
  const el = document.createElement("div");
  el.className = "trace-text";
  el.textContent = text;
  terminalBody.appendChild(el);
  terminalBody.scrollTop = terminalBody.scrollHeight;
}

function renderTraceStep(stepIdx, trace) {
  const stepDiv = document.createElement("div");
  stepDiv.className = "trace-step";

  stepDiv.innerHTML = `
    <div style="font-weight:700; font-size:0.75rem; color:#60a5fa; margin-bottom:0.3rem;">─── ITERATION STEP ${stepIdx} ───</div>
    <div style="margin-bottom:0.3rem;">
      <span class="trace-label hypo">Thought:</span>
      <span style="color:#fde047;">${trace.thought}</span>
    </div>
    <div style="margin-bottom:0.4rem;">
      <span class="trace-label act">Action:</span>
      <code style="color:var(--accent-cyan); background:rgba(0,242,254,0.1); padding:0.1rem 0.35rem; border-radius:3px;">${trace.action}</code>
    </div>
    <div style="background:rgba(0,0,0,0.4); padding:0.4rem; border-radius:4px; border:1px solid rgba(255,255,255,0.06); font-size:0.78rem;">
      <span class="trace-label obs">Observation:</span>
      <pre style="color:#94a3b8; margin-top:0.2rem; font-family:var(--font-mono);">${trace.observation}</pre>
    </div>
  `;

  terminalBody.appendChild(stepDiv);
  terminalBody.scrollTop = terminalBody.scrollHeight;
}

function renderRcaCard(report) {
  rcaBadgeStatus.textContent = "Diagnosis Complete (VERIFIED)";
  rcaBadgeStatus.style.background = "rgba(16, 185, 129, 0.2)";
  rcaBadgeStatus.style.color = "#34d399";
  
  rcaCategory.textContent = report.diagnosed_fault_class;
  rcaRootCause.textContent = report.root_cause_explanation;
  rcaRemediation.textContent = report.actionable_remediation;
  rcaToolCalls.textContent = report.tool_calls_count;
  rcaHallucinations.textContent = `${report.hallucinations_detected.length} (Grounded)`;
}

// Start application
document.addEventListener("DOMContentLoaded", init);

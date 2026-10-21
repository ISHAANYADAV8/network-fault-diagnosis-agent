# Runbook: ICMP & Connectivity Troubleshooting

## Overview
ICMP Echo (ping) and traceroute are the primary Layer 3/4 reachability diagnostics.

## Diagnostic Signatures
1. **Total Packet Drop (100% loss) with "Destination Host Unreachable":**
   - Typically indicates an intermediate link or port along the path is administratively DOWN or physically disconnected.
   - Action: Inspect interface status (`ip -s link`) on intermediate switches and routers along the path.

2. **Immediate Failure with "connect: Network is unreachable":**
   - Originating host has no route to the destination IP address.
   - Usually caused by a missing default gateway in the routing table.
   - Action: Check `ip route show` on the source host.

3. **High Latency Variance, Jitter, or Partial Packet Loss (e.g., 20% - 40% loss):**
   - Indicates synthetic or physical link degradation, queuing congestion, or NetEm configuration (`tc qdisc`).
   - Action: Inspect ping RTT min/avg/max and look for `tc` traffic control disciplines on switch interfaces.

4. **Traceroute Drops Mid-Path (`* * *` after hop N):**
   - Hop N is the last responsive router or node. The link between hop N and hop N+1 is broken or dropping packets.

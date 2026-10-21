# Runbook: Routing Table Triage & Blackhole Diagnosis

## Overview
Hosts and routers use kernel routing tables (`ip route show`) to determine the next hop for outgoing packets.

## Key Rules & Signatures
1. **Intra-subnet Routing:**
   - Packets targeted to IP addresses within the local subnet (e.g. `10.0.0.0/24`) do not use the default gateway.
   - They rely on the link-scope kernel route (`10.0.0.0/24 dev eth0 proto kernel scope link`).

2. **Inter-subnet / WAN Routing:**
   - Packets targeted outside the local subnet (e.g. `10.0.1.254`) require a default gateway (`default via <gateway-ip>`).
   - If the default route is missing or corrupted, the Linux network stack aborts with:
     `connect: Network is unreachable`.

3. **Remediation Syntax:**
   - Restoring a default gateway route:
     `ip route add default via <gateway_ip> dev <interface>`
     Example: `ip route add default via 10.0.0.1 dev h1-eth0`

# Runbook: Interface State & MTU Mismatch Diagnosis

## Overview
Network interfaces (`ip -s link`) report physical carrier status, administrative state, MTU size, and packet error/drop counters.

## Diagnostic Signatures
1. **Administrative or Carrier State DOWN:**
   - Output shows `<NO-CARRIER,BROADCAST,MULTICAST>` and `state DOWN`.
   - TX/RX counters remain static.
   - Remediation: `ip link set dev <interface> up`

2. **Inter-Switch Trunk Links:**
   - In modular topologies, switch-to-switch trunk ports (e.g. `s1-eth3`) carry aggregated VLAN/subnet traffic between switch domains.
   - If a trunk port goes `DOWN`, traffic between hosts on opposite switches drops completely.
   - Remediation: `ip link set dev <trunk_port> up`

3. **MTU Mismatch & Fragmentation Drops:**
   - Standard Ethernet MTU is 1500 bytes.
   - If an interface is misconfigured with an MTU below standard (e.g. 1200), large packets with the Don't Fragment (DF) flag set are dropped.
   - Remediation: `ip link set dev <interface> mtu 1500`

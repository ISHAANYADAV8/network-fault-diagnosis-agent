# Runbook: Domain Name Resolution (DNS) Triage

## Overview
DNS translates human-readable hostnames (e.g. `app.corp.local`) into routable IPv4 addresses using nameservers configured in `/etc/resolv.conf`.

## Diagnostic Signatures
1. **Connection Timeout to Port 53:**
   - Output shows `;; connection timed out; no servers could be reached` or `timed out`.
   - Direct IP ping to destination succeeds, but hostname resolution fails.
   - Root Cause: Host is configured with an unreachable, erroneous, or non-existent nameserver IP.
   - Action: Inspect `/etc/resolv.conf` on the querying node.
   - Remediation: `echo "nameserver <valid_dns_ip>" > /etc/resolv.conf` (e.g. `10.0.0.254`).

2. **NXDOMAIN Error:**
   - Server responds but returns `** server can't find <hostname>: NXDOMAIN`.
   - Root Cause: Domain name does not exist on the authoritative DNS server.

---
name: godmode-network
description: Network diagnostics via GODMODE MCP — ping, port scanning, DNS lookup (A/MX/NS/TXT), WHOIS, IP info, and network interface listing. Tools — ping, port_scan, dns_lookup, whois_lookup, ip_info, network_interfaces.
allowed-tools: Read, Bash
---

# Godmode Network Tools

Network diagnostics via GODMODE MCP.

## Tools

| Tool | Args | Description |
|------|------|-------------|
| `ping` | `host`, `count?` | Ping a host |
| `port_scan` | `host`, `ports` | Check open ports |
| `dns_lookup` | `domain`, `record_type?` (A/AAAA/MX/NS/TXT/CNAME/SOA) | DNS lookup |
| `whois_lookup` | `domain` | WHOIS info |
| `ip_info` | `ip?` | IP details (or public IP) |
| `network_interfaces` | — | List interfaces and IPs |

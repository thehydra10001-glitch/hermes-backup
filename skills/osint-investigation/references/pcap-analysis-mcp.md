# PCAP Analysis via MCP + Wireshark/tcpdump

**Context:** Network forensics & OSINT — analyze packet captures using AI-driven MCP servers and traditional CLI tools.

## Pre-installed Tooling

| Tool | Path | Version |
|------|------|---------|
| Wireshark | `wireshark` | 4.6.0 |
| tshark | `tshark` | 4.6.0 |
| tcpdump | `tcpdump` | 4.99.5 |
| capinfos | `capinfos` | ✓ |
| mergecap | `mergecap` | ✓ |
| editcap | `editcap` | ✓ |
| dumpcap | `dumpcap` | ✓ |
| text2pcap | `text2pcap` | ✓ |

User is in the `wireshark` group — no sudo needed for captures via dumpcap.

## MCP Servers Installed

### Primary: bx33661/Wireshark-MCP (47 tools)
```
pip install wireshark-mcp
```
Registered in Hermes as MCP server `wireshark` via:
```bash
hermes mcp add wireshark --command wireshark-mcp --args serve
```

**Key tools (prefixed `wireshark_` in Hermes):**

| Category | Tools |
|----------|-------|
| Entry | `wireshark_open_file` — open pcap, recommend relevant tools |
| Agent | `wireshark_quick_analysis`, `wireshark_security_audit` |
| Packet | `wireshark_get_packet_list`, `wireshark_get_packet_details`, `wireshark_get_packet_bytes`, `wireshark_get_packet_context` |
| Stream | `wireshark_follow_stream` (TCP/UDP) |
| Stats | `wireshark_stats_protocol_hierarchy`, `wireshark_stats_endpoints`, `wireshark_stats_conversations`, `wireshark_stats_io_graph`, `wireshark_stats_expert_info` |
| Extract | `wireshark_extract_http_requests`, `wireshark_extract_dns_queries`, `wireshark_extract_tls_handshakes`, `wireshark_extract_dhcp_info`, `wireshark_extract_credentials`, `wireshark_extract_smtp_emails` |
| Security | `wireshark_detect_port_scan`, `wireshark_detect_dos_attack`, `wireshark_detect_dns_tunnel`, `wireshark_detect_arp_spoofing`, `wireshark_check_threats`, `wireshark_analyze_suspicious_traffic`, `wireshark_analyze_tcp_health` |
| File | `wireshark_capture` (live), `wireshark_filter_save`, `wireshark_merge_pcaps`, `wireshark_get_file_info` |
| Edit | `wireshark_editcap_trim`, `wireshark_editcap_split`, `wireshark_editcap_deduplicate`, `wireshark_text2pcap_import` |
| Viz | `wireshark_plot_traffic`, `wireshark_plot_protocols`, `wireshark_decode_payload` |

### Alternative: khuynh22/mcp-wireshark (14 tools, simpler)
```
pip install mcp-wireshark
```
Tools: `check_installation`, `list_interfaces`, `read_pcap`, `display_filter`, `summarize_pcap`, `stats_by_proto`, `follow_tcp`, `follow_udp`, `expert_info`, `decode_protocol`, `protocol_stats`, `analyze_iec61850`, `live_capture`, `export_json`.

## Quick Usage

### From Hermes (in-session)
The 47 MCP tools auto-register on next session start (`/reset` or new session). Tools are available as `wireshark_*` prefixed names.

**Typical workflow:**
```
1. wireshark_open_file(pcap_file="/path/to/capture.pcap")  — opens & analyzes
2. wireshark_quick_analysis(pcap_file=...)                   — one-call overview
3. wireshark_security_audit(pcap_file=...)                   — full security audit
4. wireshark_get_packet_list(pcap_file=..., limit=50)       — examine packets
5. wireshark_extract_http_requests(pcap_file=...)           — extract HTTP
6. wireshark_extract_dns_queries(pcap_file=...)             — extract DNS
```

### Direct CLI (tshark)
```bash
# Protocol hierarchy
tshark -r capture.pcap -q -z io,phs

# Top talkers
tshark -r capture.pcap -q -z endpoints,ip

# Conversations
tshark -r capture.pcap -q -z conv,tcp

# Extract specific fields
tshark -r capture.pcap -T fields -e ip.src -e ip.dst -e http.host -Y http.request

# Expert info (anomalies)
tshark -r capture.pcap -q -z expert
```

### Live Capture
```bash
# Using dumpcap (no root needed)
dumpcap -i eth0 -w /tmp/capture.pcap -s 65535

# Using tcpdump
sudo tcpdump -i eth0 -w /tmp/capture.pcap

# Via MCP: wireshark_capture(interface="eth0", packet_count=100)
```

## Sample PCAPs for Testing

| File | Contents |
|------|----------|
| `/tmp/ipv4frags.pcap` | IPv4 fragments, 3 packets, ICMP echo |
| `/tmp/ping.pcap` | Single ICMP echo (created via text2pcap) |

More samples: https://wiki.wireshark.org/SampleCaptures

## GitHub MCP Servers Discovered

| Repo | Focus |
|------|-------|
| [mixelpixx/Wireshark-MCP](https://github.com/mixelpixx/Wireshark-MCP) | Most feature-rich — Wireshark + nmap + threat intel (AbuseIPDB, URLhaus). `pip install wireshark-mcp-server` |
| [bx33661/Wireshark-MCP](https://github.com/bx33661/Wireshark-MCP) | Clean pcap analysis focus, 47 tools, auto-configures clients. **Installed.** |
| [khuynh22/mcp-wireshark](https://github.com/khuynh22/mcp-wireshark) | Simpler, 14 tools, community-maintained. **Also installed.** |
| [0xKoda/WireMCP](https://github.com/0xKoda/WireMCP) | Real-time capture focus, tshark-powered |

## Pitfalls

- **Some online pcap sources return HTML** — GitHub raw URLs, wiki attachments, etc. may return error pages. Verify with `file` and `capinfos` before analysis.
- **File permissions** — user is already in `wireshark` group; captures work without sudo via dumpcap.
- **tshark display filters** — Use Wireshark display filter syntax (e.g. `http.request`, `dns.flags.response == 0`, `tcp.port == 443`).
- **MCP tools need /reset** — MCP server tools only appear after starting a new session (`/reset` in Hermes). The `hermes mcp add` command confirmed the tools exist but the current session won't see them until next start.
- **`wireshark-mcp` param name** — The tool parameter for pcap files is `pcap_file`, NOT `filepath` or `filename`.

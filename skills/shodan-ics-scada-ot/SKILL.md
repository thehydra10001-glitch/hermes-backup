---
name: shodan-ics-scada-ot
description: "SCADA/ICS/OT Hacking & Offensive OSINT via Shodan — 50+ Shodan dorks, Shodan alternatives for IoT/ICS discovery, protocol-specific search filters, and responsible disclosure guidelines"
version: 1.0
author: hermes-agent
platforms: [linux]
metadata:
  hermes:
    tags: [shodan, ics, scada, ot, industrial, offensive-osint, iot]
    category: security
trigger: /skill shodan-ics-scada-ot
---

# SCADA/ICS/OT Hacking Using Shodan — Offensive OSINT

**Author:** HERMES Agent (based on TryHackBox/Open-source-intelligence content, AustrianEnergyCERT, EC-429/Shodan_ICS, and vespersec Shodan cheat sheet)

**Purpose:** Identify publicly exposed SCADA/ICS/OT systems connected to the internet using Shodan and alternative search engines for offensive OSINT recon.

---

## Overview

SCADA (Supervisory Control and Data Acquisition) and ICS (Industrial Control Systems) devices control critical infrastructure — power grids, water treatment, manufacturing plants, pipelines, HVAC, nuclear facilities. Many of these systems are directly connected to the internet with weak or no authentication.

Shodan (shodan.io) is a search engine for internet-connected devices. It indexes banners, services, and protocol responses. Combined with **Shodan dorks** (specialized search queries), you can find exposed SCADA/ICS/OT systems.

---

## ⚠️ Ethical & Legal Warning

> **Responsible use only.** Unauthorized scanning or testing of SCADA/ICS systems controlling critical infrastructure may violate computer fraud and abuse laws in your jurisdiction. Only test systems you own or have explicit written authorization to test. Shodan's data is publicly indexed, but **actively probing** discovered systems without permission constitutes unauthorized access in many countries.

---

## Shodan Search Filters & Operators

| Filter | Description | Example |
|--------|-------------|---------|
| `port:` | Filter by port number | `port:502` |
| `product:` | Filter by product/software | `product:"Modbus"` |
| `title:` | Filter by HTTP title | `title:"SCADA"` |
| `html:` | Filter by HTML content | `html:"PLC"` |
| `country:` | Filter by country code | `country:IN` |
| `city:` | Filter by city | `city:"Mumbai"` |
| `org:` | Filter by ISP/org | `org:"Bharti Airtel"` |
| `os:` | Filter by operating system | `os:"Windows"` |
| `hostname:` | Filter by hostname | `hostname:"powerplant"` |
| `net:` | Filter by IP range | `net:203.0.113.0/24` |
| `before:/after:` | Date filter | `before:2024-01-01` |
| `has_vuln:` | Known vulnerabilities | `has_vuln:true` |
| `tag:ics` | Shodan-assigned ICS tag | `tag:ics` |

Combine filters: `port:502 country:IN has_vuln:true`

---

## SCADA/ICS/OT Shodan Dorks — Master List

### ABB Products
```
ABB AC 800M
ABB RTU560
ABB RTU-Helpdesk
ABB SREA-01
ABB Webmodule
```

### Protocol & Port-Based (High Value)
| Dork | Protocol | Common Use |
|------|----------|------------|
| `port:502` | **Modbus** | PLC communication, no auth by default |
| `port:44818` | **EtherNet/IP** | Rockwell/Allen-Bradley PLCs |
| `port:20000` | **DNP3** | Power grid SCADA |
| `port:47808` | **BACnet** | Building automation/HVAC |
| `port:5094 hart-ip` | **HART-IP** | Process automation |
| `port:102` | **Siemens S7** | Siemens SIMATIC PLCs |
| `port:2404 asdu address` | **IEC 60870-5-104** | Power utility SCADA |
| `port:1911,4911 product:Niagara` | **Niagara AX** | Tridium building mgmt |
| `port:1962 PLC` | **PCWorx** | PLC programming |
| `port:20547 PLC` | **ProConOS** | PLC runtime |
| `port:5006,5007 product:mitsubishi` | **Mitsubishi PLC** | Factory automation |
| `port:2455 operating system` | **CODESYS** | 3S-Smart Software PLC runtime |
| `port:18245,18246 product:"general electric"` | **GE SRTP** | GE PLCs |
| `port:9600 response code` | **OMRON FINS** | OMRON PLCs |
| `port:789 product:"Red Lion Controls"` | **Red Lion** | Industrial routers/PLCs |
| `port:3011` | **MELSEC** | Mitsubishi communication |

### Product/Banner-Based Dorks
```
AKCP Embedded Web Server
A440 Wireless Modem
A850 Telemetry Gateway
addUPI Server
addVANTAGE
title:adcon
IPC@CHIP
Cimetrics Eplus Web Server
ISC SCADA Service HTTPserv:00001
Webvisu
Visu Remote Login
3S-Smart Software Solutions
DELTA enteliTOUCH
i.LON
CIMPLICITY WebView
CIMPLICITY-HttpSvr
ProficyPortal
GoAhead-Webs InitialPage.asp
Modbus Bridge
ModbusGW
PLC type
PLC name
Powerlink
SCADA
webSCADA
HMS AnyBus-S WebServer
eiPortal
EnergyICT RTU
lantronix
lantronix port:9999
port:30718 lantronix
Moscad ACE
MovWebClientX
ioLogik Web Server
port:4800 'Moxa Nport'
title:'NPort web console'
MoxaHttp
port:4800 'OnCell'
```

### Vendor-Specific Dorks
```
# Siemens
port:102 siemens
port:161 simatic
siemens S7

# Schneider Electric / Modicon
schneider modicon
Building Operation Automation Server Schneider Electric

# Rockwell / Allen-Bradley
rockwell allen-bradley
CIP

# Honeywell
honeywell scada

# GE
port:18245,18246 product:"general electric"
GE SRTP

# Mitsubishi
port:5006,5007 product:mitsubishi
mitsubishi melsec

# Omron
port:9600 response code
omron fins

# Moxa
moxa nport
MoxaHttp

# Tridium / Niagara
product:Niagara
niagara ax

# Building Automation / BACnet
port:47808 bacnet
Cimetrics
Delta enteliTOUCH
```

### Category-Based Searches
```
# All Shodan ICS-tagged devices
tag:ics

# Web-based SCADA interfaces
title:"SCADA"
title:"webSCADA"
title:"PLC"
title:"HMI"
"Server: SCADA"

# Default credentials on SCADA systems
"password" "admin" port:502
"admin" "1234" "login" port:80
```

---

## Shodan Alternatives for ICS/IoT/OT OSINT

| Engine | URL | Free Tier | Best For |
|--------|-----|-----------|----------|
| **Shodan** | shodan.io | 100 queries/mo | General ICS/IoT discovery |
| **Censys** | censys.io | 250 queries/mo | Cert research, SSL/TLS, ASM |
| **ZoomEye** | zoomeye.org | Partial free | Asian infrastructure (China) |
| **FOFA** | fofa.info | 100+ rules | Favicon pivots, asset discovery |
| **Netlas** | netlas.io | Free tier | Passive DNS, cert research |
| **GreyNoise** | viz.greynoise.io | Free | Noise reduction, alert enrichment |
| **Criminal IP** | criminalip.io | Freemium | Threat intel, ASM |
| **ScanSearch** | scansearch.net | Free | Real-time active scanning |
| **BinaryEdge** | binaryedge.io | Limited free | Exposed services, data leak monitor |
| **ONYPHE** | onyphe.io | Limited free | Cyber defense, honeypot detection |
| **FullHunt** | fullhunt.io | Limited free | Attack surface monitoring |
| **Hunter (how)** | hunter.how | Limited free | IoT/ICS focused scanning |
| **Shodan ICS Explore** | shodan.io/explore/category/industrial-control-systems | Free | Curated ICS categories |

### Cross-Engine Pivoting Workflow

```
Shodan find → Censys verify → Netlas DNS → FOFA favicon pivot → GreyNoise noise filter
```

Each engine indexes differently — cross-check findings across 2+ sources before reporting.

---

## Quick Start Commands

### Shodan CLI (requires API key)
```bash
# Install
pip install shodan --break-system-packages

# Basic search
shodan search --fields ip_str,port,org,hostnames "port:502 country:IN"

# Count results
shodan count "port:502"

# Download results
shodan download scada_results "tag:ics" --limit 1000

# Parse downloaded file
shodan parse --fields ip_str,port,org scada_results.json.gz

# Host details
shodan host <IP_ADDRESS>

# Scan IP
shodan scan submit <IP_ADDRESS>

# My IP
shodan myip
```

### Curl-based Shodan API (free tier)
```bash
# Search (1 query = 1 credit)
SHODAN_KEY="YOUR_KEY"
curl -s "https://api.shodan.io/shodan/host/search?key=$SHODAN_KEY&query=port:502&facets={}"

# Single host lookup
curl -s "https://api.shodan.io/shodan/host/<IP>?key=$SHODAN_KEY"

# Count
curl -s "https://api.shodan.io/shodan/host/count?key=$SHODAN_KEY&query=port:502"

# Shodan ExploitDB
curl -s "https://exploits.shodan.io/api/search?key=$SHODAN_KEY&query=scada"
```

### Censys CLI
```bash
pip install censys
censys search "services.service_name: MODBUS" --pages 2
censys search "services.service_name: BACNET" --pages 2
censys view <IP>
```

---

## ICS Protocol Deep-Dive

### Modbus (port 502)
The most common ICS protocol. No authentication by default.
```
Shodan: port:502
Censys: services.service_name: MODBUS
ZoomEye: port:502
```
**Risk:** Full read/write to coils and registers — can change setpoints, stop processes.

### DNP3 (port 20000)
Used in electrical grid SCADA.
```
Shodan: port:20000 source address
```
**Risk:** Can issue control commands if no authentication.

### BACnet (port 47808)
Building automation — HVAC, lighting, fire systems.
```
Shodan: port:47808
```
**Risk:** Read/write building management points.

### Siemens S7 (port 102)
```
Shodan: port:102 siemens SIMATIC S7
```
**Risk:** Can upload/download PLC programs, force I/O.

### EtherNet/IP (port 44818)
Allen-Bradley / Rockwell ControlLogix.
```
Shodan: port:44818
```
**Risk:** CIP protocol allows tag read/write, potentially remote stop.

---

## Offensive OSINT Workflow

### Phase 1 — Discovery
```
1. Search Shodan for target protocol + country + org
2. Cross-check results on Censys/ZoomEye/FOFA
3. Filter out honeypots with GreyNoise
4. Save IP list to target.txt
```

### Phase 2 — Verification
```bash
# Quick port scan (no aggressive -A to stay low-noise)
nmap -sT -T3 -p 502,20000,44818,47808,102,161 <target>

# Grab banners
nmap -sV --version-intensity 5 -p 502 <target>

# Check modbus
modbus-cli <target>  # or: pip install pymodbus
```

### Phase 3 — Enumeration
```bash
# Find webboxes / HTTP SCADA interfaces
curl -sIk http://<target>:80 | grep -i "server:\|shodan\|scada\|login"

# Check for default passwords
# Common: admin/admin, admin/1234, root/root, admin/password
```

---

## Tools for ICS/SCADA Recon

```bash
# Modbus
pip install pymodbus
pip install modbus-cli

# s7scan — Siemens S7 discovery
pip install s7scan
s7scan <IP_RANGE>

# PLCScan
git clone https://github.com/meir555/PLCScan.git
cd PLCScan && python3 plcscan.py <target>

# Modscan
pip install modscan

# ICS Vulnerability Scanner
git clone https://github.com/EC-429/Shodan_ICS.git
cd Shodan_ICS && python3 shodan_ics.py

# Nuclei ICS templates
nuclei -u <target> -tags ics,scada,modbus

# NMAP NSE scripts for ICS
nmap --script modbus-discover.nse -p 502 <target>
nmap --script s7-info.nse -p 102 <target>
nmap --script bacnet-info.nse -p 47808 <target>
nmap --script enip-info.nse -p 44818 <target>
```

---

## References

- **TryHackBox/Open-source-intelligence** — github.com/TryHackBox/Open-source-intelligence
- **AustrianEnergyCERT/ICS_IoT_Shodan_Dorks** — github.com/AustrianEnergyCERT/ICS_IoT_Shodan_Dorks
- **EC-429/Shodan_ICS** — github.com/EC-429/Shodan_ICS
- **dootss/shodan-dorks** — github.com/dootss/shodan-dorks (auto-updating dorks)
- **nullfuzz-pentest/shodan-dorks** — github.com/nullfuzz-pentest/shodan-dorks
- **Shodan ICS Explore** — shodan.io/explore/category/industrial-control-systems
- **Vespersec Shodan Cheat Sheet** — vespersec.net/docs/osint-reconnaissance/shodan-search-queries-cheat-sheet
- **OSINT Team 2026 Free Tier Comparison** — osintteam.blog (Shodan vs Censys vs ZoomEye vs FOFA)
- **Scada/ICS/OT Hacking Using Shodan Offensive OSINT** (Muhammad Raheem / espyerx) — espyerx.medium.com
- **vanimpe.eu — What is Shodan telling us about ICS in Belgium?** — vanimpe.eu

## Pitfalls

- **Honeypots** — Many ICS Shodan results are **honeypots** (especially Conpot). Cross-verify on GreyNoise before reporting.
- **Rate limits** — Shodan free tier = 100 queries/mo. Use .facet queries for broad counts before detail lookups.
- **False positives** — Products like `GoAhead-Webs` appear on many non-ICS devices. Combine with port filters.
- **Legal** — `nmap -sV` on SCADA systems can cause crashes (some PLCs are famously fragile). Use only with authorization.
- **API keys** — Shodan CLI/API requires a paid tier for meaningful output. Free tier can browse the web UI manually.
- **Censys free tier** — 250 queries/mo in 2026, but only returns 50 results per query. Combine with pagination.
- **FOFA** — Chinese interface. Use Google Translate. Best for Asian infrastructure pivoting.

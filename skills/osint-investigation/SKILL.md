---
name: osint-investigation
description: "HERMES OSINT framework — multi-phase open-source intelligence investigation with 25 tools, structured reporting, and free API integrations"
version: 1.4
author: hermes-agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [osint, security, investigation, reconnaissance, social-media]
    category: security
---

# HERMES OSINT Investigation Framework

**Deploy target:** Kali Linux | **Python env:** `~/osint-env` | **25 tools installed**

## When to Use

- User asks to investigate a person, username, email, domain, IP, phone, or image using OSINT
- User provides a target and wants online presence, breach data, or digital footprint
- User wants a structured OSINT report with sourced findings
- Quick scan or deep investigation — both supported

## Reference Files

- `references/investigation-kuldipsinhmori-20260710.md` — Real investigation case study with tool performance metrics and pitfalls discovered
- `references/telegram-bot-api.md` — Sending messages to arbitrary Telegram chat IDs via bot API (for delivery)
- `references/github-api-recon.md` — GitHub API recon: user profiles, repos, identity correlation, pivot patterns
- `references/indian-phone-prefixes.md` — Indian mobile number prefix-to-operator/circle mapping (free lookup without APIs)
- `references/pcap-analysis-mcp.md` — PCAP/network forensics via Wireshark MCP server (47 tools) + tcpdump/tshark CLI; MCP server setup, key tools table, quick commands, sample pcaps, and pitfalls
- `scripts/generate_osint_report.py` — fpdf2-based PDF report generator template (customize TARGET_NAME, IDENTITIES, PLATFORMS, etc.)

## Tool Path Setup

**Always activate venv before Python OSINT tools (maigret, holehe, socialscan, phoneinfoga, h8mail, sublist3r, metagoofil):**
```bash
source ~/osint-env/bin/activate
```

**System tools** (whois, nmap, dig, etc.) are in `/usr/bin/`. Sherlock is at `~/.local/bin/sherlock` (add `export PATH="$HOME/.local/bin:$PATH"` to `.bashrc` if needed).

---

## Quick Commands

| User says | Action |
|---|---|
| `INVESTIGATE: <target>` | Full OSINT, all 5 phases |
| `QUICK SCAN: <target>` | Phase 1 passive only, 5 min |
| `USERNAME: <handle>` | Sherlock + Maigret + WhatsMyName |
| `EMAIL: <email>` | Holehe + HIBP + breach check |
| `DOMAIN: <domain>` | DNS + WHOIS + subdomains + certs |
| `IP: <addr>` | Shodan + nmap + geolocation + ASN |
| `PHONE: <num>` | PhoneInfoga + NumVerify + TrueCaller |
| `IMAGE: <file/url>` | ExifTool + reverse image + geolocation |
| `FRACTAL: <domain/CIDR>` | Full fractal recon loop (passive → DNS → masscan → nmap → SAN extract → re-loop) |
| `ASN: <ASN>` | BGP + Shodan + Censys passive footprinting by ASN |
| `RECON-LOOP: <domain> <CIDR>` | Run recon-loop.sh automation script |
| `REPORT` | Generate full report from session data |

---

## Tool Arsenal (25 tools)

### Username / Social Footprint
```bash
# Sherlock: fast (~10s), checks ~100 sites, finds ~8 results
sherlock <user> --print-found --timeout 10 --output /tmp/sherlock_<user>.txt

# Maigret: slower (~48s), checks 509 sites, finds ~11 results
# ⚠️ -J is JSON TYPE (simple/ndjson), NOT output file!
# Output goes to --folderoutput directory as report_<user>_simple.json
maigret <user> -J simple --folderoutput /tmp/maigret_out

# Run BOTH for comprehensive coverage — they complement each other
socialscan <user>
```

**Holehe output format:** `[+]` = found/registered, `[-]` = not found, `[x]` = error/unknown

### Email Intelligence
```bash
holehe <email>
h8mail -t <email>
theHarvester -d <domain> -b all
```

### Domain / DNS Recon
```bash
whois <domain> && dig <domain> ANY
dnsrecon -d <domain> && dnsenum <domain>
fierce -domain <domain>
sublist3r -d <domain>
amass enum -d <domain>
```

### Network / IP
```bash
nmap -sV -sC -O <target>
masscan <range> -p 1-65535
traceroute <target>
whatweb <url>
```

### Web App Recon
```bash
nikto -h <url>
gobuster dir -u <url> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
wafw00f <url>
```

### Metadata
```bash
exiftool <file>
metagoofil -d <domain> -t pdf,doc,xls -o /tmp/meta/
strings <binary>
```

### Phone Number Investigation
```bash
# PhoneInfoga (requires venv activation)
source ~/osint-env/bin/activate
cd ~/PhoneInfoga && python3 phoneinfoga.py -n +91XXXXXXXXXX

# NumVerify API (requires free API key from numverify.com)
curl -s "http://apilayer.net/api/validate?access_key=YOUR_KEY&number=XXXXXXXXXX&country_code=IN"

# Indian mobile prefix lookup (no API needed)
# First 4-5 digits determine operator and circle — see references/indian-phone-prefixes.md
```

**⚠️ PhoneInfoga syntax:** Use `-n <number>` NOT `scan -n <number>` — the `scan` subcommand doesn't exist in current version.

**Indian number format:** 10 digits, starts with 6/7/8/9. Prefix `+91` for international.

### Frameworks
```bash
recon-ng
spiderfoot --target <target>
```

### GitHub / Developer Recon (API, no auth needed)
```bash
# User profile — name, bio, repos, followers, creation date
curl -s "https://api.github.com/users/<username>" | python3 -m json.tool

# Repos list — names, languages, descriptions, last updated
curl -s "https://api.github.com/users/<username>/repos?per_page=30&sort=updated" | python3 -c "import sys,json; [print(f'{r[\"name\"]} | {r.get(\"language\",\"N/A\")} | {r.get(\"updated_at\",\"N/A\")}') for r in json.load(sys.stdin)]"
```
See `references/github-api-recon.md` for full patterns and field mapping.

Also see script `scripts/generate_osint_report.py` for fpdf2 report generation.

## 📦 Ultimate OSINT Resource — Awesome OSINT Arsenal

**751+ tools · 50 categories · 1-click installer**
```bash
git clone https://github.com/rawfilejson/awesome-osint-arsenal
cd awesome-osint-arsenal
sudo bash osint.sh          # OSINT tools only (recommended)
# OR full install:
sudo bash install.sh
```
Includes: Username/Social OSINT · Email/Phone/Domain/IP · Geolocation · Image/Face · Breach/Leaks · Dark Web · Web App · Red/Blue Team · Forensics · Termux Android · **Georgia OSINT (500+ resources)** · Google Dorking per country · AI OSINT · and more.

## 🤖 Automated OSINT with n8n Workflows

n8n (free, open-source) can auto-pilot multi-source OSINT investigations:

| Workflow | ID | What it does | APIs needed |
|:---------|:---|:-------------|:------------|
| **Org Research** | `12506` | 6-phase org OSINT — court + legislation + news → GPT-5 analysis | CourtListener, LegiScan, Serper, Jina AI, OpenRouter |
| **LinkedIn Discovery** | `6508` | Find LinkedIn profiles by role (CISO, CEO) via Google CSE → Google Sheet | Google CSE + Sheets |
| **Person Profile** | `12507` | Personality + email + legal + web → GPT-5 synthesis report | Humantic AI, Hunter, CourtListener, LegiScan, Serper |

**Install n8n:**
```bash
sudo apt install nodejs npm && sudo npm install n8n -g
n8n start  # UI at http://localhost:5678
```

## Free OSINT APIs

| Category | Tool | URL | Free Tier |
|---|---|---|---|
| Search | Shodan | https://shodan.io | 100/mo |
| Search | Censys | https://censys.io | 250/mo |
| Search | GreyNoise | https://viz.greynoise.io | Free |
| Search | URLScan | https://urlscan.io/api/v1/ | Free |
| Search | VirusTotal | https://virustotal.com/api/v3/ | 500/day |
| Dark Web | IntelligenceX | https://intelx.io | Limited |
| Email | HIBP | https://haveibeenpwned.com/api/v3/ | Free |
| Email | Hunter.io | https://hunter.io/api/v2/ | 25/mo |
| Email | EmailRep | https://emailrep.io/ | Free |
| Person | WhatsMyName | https://whatsmyname.app | Free |
| Person | GitHub API | https://api.github.com/users/<user> | 60/hr |
| DNS | crt.sh | https://crt.sh | Free |
| DNS | ViewDNS | https://viewdns.info/api/ | 1500/mo |
| DNS | SecurityTrails | https://securitytrails.com | 50/mo |
| DNS | Wayback | https://archive.org/wayback/ | Free |
| IP | IP-API | https://ip-api.com/json/ | 45/min |
| IP | ipinfo.io | https://ipinfo.io/ | 50k/mo |
| Phone | NumVerify | https://numverify.com/api | 100/mo |
| Dark Web | Ahmia | https://ahmia.fi | Free |
| Dark Web | BreachDirectory | https://breachdirectory.org | Free |

---

## 5-Phase Investigation Workflow

### Phase 0 — Mission Brief
```
TARGET:       [input]
TARGET TYPE:  [person / username / email / domain / IP / org / phone / image]
MISSION:      [what operator wants to find]
STARTED:      [timestamp UTC]
```

### Phase 1 — Passive Recon
- WHOIS / DNS records
- Historical snapshots (Wayback Machine)
- SSL certificate transparency (crt.sh)
- Public social profiles
- Search engine dorking (site:, filetype:, cache:, related:)
- Breach database checks

### Phase 2 — Active Enumeration
- Port scanning (nmap)
- Subdomain enumeration (sublist3r, amass, fierce)
- Directory brute-forcing (gobuster)
- Email harvesting (theHarvester)
- Username hunting (sherlock, maigret)
- Tech fingerprinting (whatweb, builtwith)

### Phase 3 — Correlation & Pivoting
```
email → breach check → accounts → social → phone → location
domain → subdomains → IPs → ASN → related → owner
username → platforms → bios → emails → real identity
```

### Phase 4 — Verification
- Cross-check every finding with 2+ independent sources
- Flag unverified data as `[UNVERIFIED]`

### Phase 5 — Report
Use structured report template with sections: Target Profile, Findings (Identity, Digital Footprint, Email, Network, Geolocation, Breach, Timeline), Pivot Map, Evidence Log, Analyst Notes, Tool Log.

---

## Sherlock Fix Protocol

If sherlock fails or hangs:
1. **Maigret** fallback: `maigret <user> -J simple --folderoutput /tmp/maigret_out`
2. **GitHub API** (if target is a developer): see `references/github-api-recon.md` — returns name, bio, repos, followers, creation date
3. **WhatsMyName API**: `curl -s "https://whatsmyname.app/api/search?q=<user>" | python3 -m json.tool`
4. **Manual verify**: instantusername.com, namechk.com

⚠️ **Both Sherlock AND Maigret can timeout** on Kali (60s+ hangs). If both fail, pivot to GitHub API + web_search immediately — don't retry tools that already timed out.

Only report sites confirmed by 2+ sources.

---

## ORCID Public API (no key needed)

For researcher verification, the ORCID public API works without authentication:
```bash
# Search by name
curl -s "https://pub.orcid.org/v3.0/search/?q=family-name:Mori+AND+given-names:Kuldipsinh" \
  -H "Accept: application/json"

# Get full record by ORCID iD
curl -s "https://pub.orcid.org/v3.0/0009-0008-3093-7095" \
  -H "Accept: application/json"
```
Response includes: name, keywords, biography, employments, educations, works (publications).
Cross-verify ORCID keywords against LinkedIn bio for identity confirmation.

## Breach Check Limitations (2026)

⚠️ All major breach APIs now require paid API keys:
- **HIBP** — requires `hibp-api-key` header (paid: https://haveibeenpwned.com/API/Key)
- **EmailRep** — unauthenticated API disabled; needs API key
- **BreachDirectory** — Cloudflare challenge blocks automated access

**Workaround:** Direct operator to manual browser check at https://haveibeenpwned.com
For automated checks, obtain a HIBP API key and store in `.env` as `HIBP_API_KEY`.

## PDF Report Generation

See `scripts/generate_osint_report.py` for a complete fpdf2-based PDF report template.
Key rules:
- Use ASCII fallback chars (`-`, `[OK]`) instead of Unicode symbols — Helvetica is Latin-1 only
- For Unicode content, use `pdf.add_font()` with TTF files
- Custom FPDF subclass with `header()`, `footer()`, `section_title()`, `table_row()` methods
- Save output to `~/.hermes/pastes/` for easy retrieval

## Pitfalls

- **PEP 668** — always `source ~/osint-env/bin/activate` before pip-installed tools (maigret, holehe, socialscan, phoneinfoga, h8mail, sublist3r, metagoofil)
- **Symlink setup** — after venv install, symlink tools to `~/.local/bin/` and add to PATH in `.bashrc`
- **Sherlock** — add `--timeout 10` to avoid hangs; use `--output` to save results
- **Sherlock+Maigret timeout** — BOTH can hang on Kali (60s+). Don't retry; pivot to GitHub API + web_search immediately
- **Maigret `-J` flag** — `-J` is JSON TYPE (simple/ndjson), NOT output file path! Use `--folderoutput /dir` for output directory. File is auto-named `report_<user>_simple.json`
- **Maigret errors** — 11% "Access denied" is normal; use `--cloudflare-bypass` if worse
- **Amass** — passive mode fast, active needs wordlists; use `-passive` for quick scans
- **Holehe** — needs valid email; returns false if service blocks probing
- **Gobuster** — use `-x` for extensions, `-t 50` for threads
- **web_extract** — DuckDuckGo backend can only search, NOT extract URLs. For URL content, set `web.extract_backend` to firecrawl, tavily, exa, or parallel
- **Jina AI Reader (Cloudflare bypass)** — When DuckDuckGo is the only backend and a target URL is behind Cloudflare (Medium, etc.), use `curl -H "Accept: text/plain" "https://r.jina.ai/http://<url>"` to extract clean markdown. Jina's reader proxy bypasses Medium/CF paywalls and returns formatted content. No API key needed for moderate usage. Free tier is generous. This is a zero-config alternative to switching extract_backend.
- **DOCX extraction** — Use `python-docx` for .docx files (parses actual structure, far better than OCR). Install: `pip install python-docx --break-system-packages`
- **Breach APIs** — HIBP, EmailRep, BreachDirectory all require API keys in 2026; fall back to manual browser check
- **fpdf2 Unicode** — Helvetica font is Latin-1 only; use ASCII fallbacks (`-`, `[OK]`) or add TTF font for Unicode
- **Evidence** — save tool output to `/tmp/` or `~/.hermes/pastes/` before session ends
- **Browser tools** — camofox may not be running; if `browser_navigate` fails, pivot to `curl` + `web_search`/`web_extract` for web content
- **Legal** — only publicly available OSINT; no unauthorized access; operator responsible for compliance

---

## ⚡ Fractal Recon Methodology (from @utaah — Jul 2026)

**Source:** https://medium.com/@utaah/bug-bounty-automation-elite-recon-pipeline-bonus-script-7fd94ad62d84
**Core insight:** Reconnaissance is NOT a linear checklist — it's a **continuous feedback loop**. Every discovery seeds the next round. A network is a fractal, not a flat surface.

### The 5-Phase Fractal Loop

#### Phase 1 — Passive Footprinting (Perimeter Mapping)
Do NOT touch the target network. Query third-party aggregators that have already mapped it.

```bash
# Shodan — search by ASN/subnet (no packets to target)
shodan search --fields ip_str,port,org,hostnames net:198.51.0.0/16

# Censys — web search UI
# https://platform.censys.io/search?q=host.ip%3A%22198.51.0.0%2F16%22

# BGP ASN lookup
dig +short 198.51.0.0/16.origin.asn.cymru.com txt
```

**Goal:** Reveal historical records, forgotten subnets, and architecture shape without triggering a single IDS alert.

#### Phase 2 — DNS Structure Mapping (Horizontal Expansion)
Pivot from **network layer** (IPs) to **application layer** (DNS). Extract the logical map.

```bash
# Observation → Extraction → Discovery → Pivot
# 1. See HTTP/S on port 443
# 2. Pull SSL cert for domain names
openssl s_client -connect 198.51.x.x:443 </dev/null 2>/dev/null | openssl x509 -noout -text | grep DNS

# Authoritative interrogation
dig NS acme-corp.com +short

# Zone Transfer Hail Mary (AXFR)
dig axfr @ns1.acme-corp.com acme-corp.com

# Horizontal brute-forcing
dnsrecon -d targetcompany.com -D /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -t brt
```

> **🥇 The Lindy Effect of Infrastructure:** A server named `api-v3` is modern and likely patched. A server named `legacy-vpn-2015` or `test-oracle` has survived in the shadows for years — these are the fragile nodes.

#### Phase 3 — Kinetic Filtration (The Sweep)
Only NOW touch the target's physical IP space. Use a **two-pass strategy**:

1. **Wide & Shallow** (15 min → hot targets immediately):
   ```bash
   masscan -p21,22,53,80,443,445,3389,8443 -U:53,161 198.51.0.0/16 --rate=10000 --wait 0
   ```
2. **Deep & Thorough** (background — 6h window):
   ```bash
   masscan -p1-65535 198.51.0.0/16
   ```

#### Phase 4 — Deep Enumeration (Probing for Fragility)
Shift from **broad discovery** to **deep analysis** on the hot targets.

```bash
# Parse masscan output for target list
grep "open" masscan_results.gnmap | awk '{print $2":"$3}' | cut -d/ -f1 | sort -u > targets.txt

# Precision interrogation — version + scripts + OS
nmap -sV -sC -Pn -T4 -O -iL targets.txt -oA targeted_deep_analysis

# TLS certificate domain extraction
cat liveips.txt | tlsx -san -cn -silent > extracted_domains.txt

# Alternative — full sweep ping
nmap -sn 198.51.0.0/16 -T4 --min-parallelism 100 -oG liveips.gnmap
nmap -sS -p- --min-rate 1000 -iL liveips -oG open_ports.gnmap
```

#### Phase 5 — The Fractal Return (Closing the Loop)
**THE most important phase that amateurs miss.** Recon is a **continuous feedback loop**.

When Nmap's `-sC` extracts an SSL/TLS certificate, the **Subject Alternative Name (SAN)** field may reveal domains you never knew existed:

```bash
# Extract SAN domains from Nmap XML output
grep -h "subjectAltName" final_deep_analysis.xml | grep -oE "[a-zA-Z0-9.-]+\.[a-z]{2,}" | sort -u > new_domains.txt
```

**FEED BACK INTO THE LOOP** — take `new_domains.txt` and run through Phase 2-4 again:
```bash
# Resolve IPs
for d in $(cat new_domains.txt); do host $d; done

# Brute-force subdomains on newly discovered domains
subfinder -d $d -o subdomains.txt
dnsrecon -d $d -D /usr/share/wordlists/subdomains.txt -t brt

# Sweep new IPs through masscan → nmap pipeline
```

> **You are never "done" with recon. You are just waiting for the next piece of data to force you back to the start.**

### Bonus: `recon-loop.sh` — Full Automation Script

Save as `~/recon-loop.sh` and run with `bash recon-loop.sh <domain> <CIDR>`:

```bash
#!/bin/bash
DOMAIN=$1
SCOPE=$2
TIMESTAMP=$(date +%s)
WORKDIR="recon_${DOMAIN}_${TIMESTAMP}"
mkdir -p $WORKDIR && cd $WORKDIR

echo "[+] Phase 1 & 2: DNS & Scope Setup"
echo "Targeting: $DOMAIN | Scope: $SCOPE" > scope_info.txt
dig NS $DOMAIN +short > nameservers.txt

echo "[+] Phase 3: Kinetic Filtration (Sweep)"
masscan -p21,22,53,80,443,445,3389,8443 -U:53,161 $SCOPE --rate=10000 --wait 0 -oG masscan_results.gnmap
grep "open" masscan_results.gnmap | awk '{print $2":"$3}' | cut -d/ -f1 | sort -u > targets.txt

echo "[+] Phase 4: Precision Interrogation"
nmap -sV -sC -Pn -T4 -iL targets.txt -oA nmap_deep_scan

echo "[+] Phase 5: Feedback Loop Extraction"
grep -h "subjectAltName" nmap_deep_scan.xml 2>/dev/null | grep -oE "[a-zA-Z0-9.-]+\.[a-z]{2,}" | sort -u > new_domains_found.txt

echo "[!] Recon Cycle Complete. Findings saved in: $WORKDIR"
echo "[!] New potential domains discovered: $(wc -l < new_domains_found.txt)"
```

### Integration with Existing OSINT Workflow

| Existing OSINT Phase | Fractal Recon Equivalent |
|---|---|
| Phase 0 (Mission Brief) | Define scope + ASN/CIDR |
| Phase 1 (Passive Recon) | Phase 1 (Shodan/Censys/BGP) + Phase 2 (DNS structure) |
| Phase 2 (Active Enumeration) | Phase 3 (masscan sweep) + Phase 4 (nmap deep) |
| Phase 3 (Correlation) | Phase 5 (SAN extraction → loop back) |
| Phase 4 (Verification) | Cross-check with Censys passive data |
| Phase 5 (Report) | Document fractal loop iterations |

### Key Tools Added

| Tool | Purpose |
|---|---|
| `masscan` | Rapid port scanning (100k pps) — Wide/Shallow + Deep/Thorough |
| `tlsx` | TLS certificate SAN/CN extraction (ProjectDiscovery) |
| `openssl s_client` | Manual SSL cert inspection |
| `dnsrecon -t brt` | DNS brute-forcing with wordlists |
| `dig axfr` | Zone transfer testing (Hail Mary) |

### Pitfalls

- **masscan rate too high** — `--rate=10000` may trigger target DDoS thresholds. Start at `--rate=1000` and ramp up if needed
- **AXFR rarely works** — Zone transfers are almost always disabled. Don't spend more than 30s testing; pivot to dnsrecon brute-force immediately
- **tlsx not installed** — Install with `go install github.com/projectdiscovery/tlsx/cmd/tlsx@latest`
- **SAN extraction misses wildcard certs** — `subjectAltName` grep only finds explicit SAN entries. Also check `CN=` in certificate output
- **Fractal loop = infinite** — Set a loop limit (3 iterations max) or time limit (4h) or you'll never exit recon to exploitation
- **Live host ≠ exploitable** — Phase 4 nmap results may still show false positives from CDN/WAF. Verify with `curl -I` before reporting

---

### Phone Lookup Limitations
- **PhoneInfoga urllib3 error** — `AttributeError: module 'urllib3.util.ssl_' has no attribute 'DEFAULT_CIPHERS'` on Python 3.12+/urllib3 2.x. Workaround: downgrade urllib3 to 1.26.x in venv (`pip install urllib3==1.26.18`)
- **NumVerify demo key** — returns `invalid_access_key`; must register free account at numverify.com
- **Web scraping phone sites** — Truecaller, IndiaTrace, Varic, FindAndTrace all use Cloudflare protection or require auth; curl-based approaches fail
- **Indian phone prefix analysis** — Free fallback method (no API needed): first 4-5 digits determine operator + circle. See `references/indian-phone-prefixes.md`

## Communication Style

- `[HERMES ACTIVATED]` — begin investigation
- `[HERMES REPORT COMPLETE]` — end investigation
- `► Running: <cmd>` → `✓ Result:` or `✗ Failed:`
- `↪️ Pivoting from [A] → [B]`
- `[HIGH/MED/LOW]` confidence on every finding
- `[FOUND: YYYY-MM-DD HH:MM UTC]` timestamp on data points

## Self-Improvement Debrief (after every session)
```
Tools worked:    [list]
Tools failed:    [list + reason]
APIs returned:   [list]
APIs failed:     [list + reason]
Data gaps:       [what was missing]
Next run:        [what to try]
```

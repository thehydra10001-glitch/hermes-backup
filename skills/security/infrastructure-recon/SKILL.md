---
name: infrastructure-recon
description: >
  External infrastructure reconnaissance — scanning DNS, email security (SPF/DKIM/DMARC),
  exposed database services (MySQL/MariaDB), phpMyAdmin assessment, SSH/mail server
  fingerprinting, and multi-hosting provider detection. Companion to the
  bug-bounty skill for surface-level attack discovery.
version: 1.0
author: hermes-agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [recon, infrastructure, email, database, phpmyadmin, dns]
    category: security
    trigger: recon
---

# Infrastructure Reconnaissance

This skill covers the **external infrastructure layer** — services and
configurations that sit outside the web application itself but form part
of the overall attack surface: DNS, email, databases, phpMyAdmin, SSH,
and mail servers.

---

## Email Security Recon (SPF/DKIM/DMARC)

**Trigger:** Any target with MX records or custom domain email.

### Quick 3-Command Check
```bash
dig TXT <domain> +short | grep "v=spf"
dig TXT _dmarc.<domain> +short
dig TXT default._domainkey.<domain> +short
```

### Severity Matrix

| SPF | DKIM | DMARC | Verdict |
|---|---|---|---|
| `-all` (hardfail) | ✅ Configured | `p=reject` | 🟢 Secure |
| `~all` (softfail) | ❌ Missing | `p=none` | 🔴 SPOOFABLE |
| Missing | Missing | Missing | 🔴 SPOOFABLE |
| `-all` | Missing | `p=none` | 🟡 Weak |
| `~all` | ✅ Configured | `p=quarantine` | 🟡 Partial |

### Spoofability Rule
If SPF is `~all` (softfail) or missing, AND DMARC is `p=none` or missing,
the domain **CAN be spoofed** regardless of DKIM. This is a valid
HIGH/MEDIUM finding for any program whose domain sends
transactional/business emails — attackers can phish clients/vendors.

### Spoofing Attack Scenario (copy-paste for report)

```
From: ceo@victim.com
To: target@client.com
Body: Urgent — transfer funds to account X

→ SPF: ~all softfail → does NOT block delivery
→ DKIM: no record → no signature to verify
→ DMARC: p=none → takes NO action on auth failure
→ Result: EMAIL LANDS IN INBOX, no warnings
```

### Remediation Block (copy-paste ready for report)

**SPF fix:** Change `~all` → `-all`:
```
v=spf1 include:_spf.mail.hostinger.com -all
```

**DKIM fix:** Generate via Hostinger cPanel → Email → Email Deliverability → DKIM → Generate key. Or manually add DNS TXT record with the DKIM public key provided by your mail provider.

**DMARC fix (phase 1 — monitor):**
```
v=DMARC1; p=quarantine; rua=mailto:dmarc@victim.com; pct=100
```
**DMARC fix (phase 2 — enforce after 2 weeks of monitoring):**
```
v=DMARC1; p=reject; rua=mailto:dmarc@victim.com; ruf=mailto:dmarc@victim.com; pct=100
```

### SMTP Service Checks (Port 25 Open)

**Open relay check:**
```bash
echo -e "EHLO tester.com\nMAIL FROM:<test@tester.com>\nRCPT TO:<test@victim.com>\nQUIT" | nc -nv -w 5 <ip> 25
```
Response `250 OK` to both MAIL FROM and RCPT TO = open relay (CRITICAL).
Response `550 Rejected` or `550 Relay denied` = not an open relay ✅.

**User enumeration via VRFY/EXPN:**
```bash
echo -e "EHLO tester.com\nVRFY root\nVRFY admin\nEXPN root\nQUIT" | nc -nv -w 5 <ip> 25
```
`252 Administrative prohibition` = VRFY disabled ✅.
`250 <user>` or `252 <user>` = user exists (info disclosure).

**AUTH detection:**
SMTP that doesn't advertise `STARTTLS` in EHLO response → plaintext
authentication (MEDIUM finding if credentials are exchanged).

**PITFALL:** Multiple sequential failed checks at SMTP level (VRFY, RCPT, MAIL FROM)
can trigger Spamhaus-based temporary blocks from providers like Hostinger/OVH.
Wait 30-60s between manual SMTP testing phases.

**PITFALL:** SMTP servers may ban your IP after repeated failed attempts
(Spamhaus, `max_connect_errors`). Do email checks early in the engagement.

**PITFALL:** MariaDB's `max_connect_errors` (default ~10) blocks your IP after
5+ failed auth attempts. The server returns: `Host 'X.X.X.X' is blocked because
of many connection errors; unblock with 'mariadb-admin flush-hosts'`. Recovery
requires either a trusted IP to run `FLUSH HOSTS;` or a server restart. The block
is per-IP and persists until manually cleared. Run aggressive brute force from a
fresh IP or proxy.

**PITFALL:** Sub-company pages often live on **separate apex domains**, not
subdomains. For Heaven Group, `heaveninfra.heavengroup.in` returned NXDOMAIN,
but `heaveninterior.in` was the real site. When a subdomain returns NXDOMAIN,
check `dig +short <company-name>.in A`, `dig +short <company-name>.com A`, and
related TLD variations. Also check WHOIS on the parent domain for related
registrations — GoDaddy often groups related domains under the same account.

---

## phpMyAdmin Assessment

**Trigger:** `phpmyadmin/` directory found on a web target, or known
MySQL/MariaDB host.

### Version Detection
```bash
curl -s "https://target.com/phpmyadmin/" | grep -oP 'version:"[^"]*"'
# Or check the URL pattern /phpmyadmin/index.php?route=/
```

### CVE Lookup Pattern
Check the phpMyAdmin security announcements page for the version:
- https://www.phpmyadmin.net/security/PMASA-YYYY-N/
- PMASA-2025-2 (CVE-2025-24529): XSS in Insert tab — fixed in 5.2.2
- PMASA-2025-3 (CVE-2024-2961): glibc/iconv — fixed in 5.2.2

### Quick Security Checklist
| Check | Command | Good |
|---|---|---|
| Setup dir removed? | `curl -sI /phpmyadmin/setup/` | 404 |
| Directory listing off? | `curl -sI /phpmyadmin/js/` | 403 |
| Git exposed? | `curl -sI /phpmyadmin/.git/HEAD` | 404 |
| Readme accessible? | `curl -sI /phpmyadmin/readme.php` | 404 |
| CHANGELOG accessible? | `curl -sI /phpmyadmin/CHANGELOG` | 404 |
| Security headers? | Check CSP, X-Frame-Options | Present |
| Open redirect via url.php? | `curl -sI /phpmyadmin/url.php?url=https://evil.com` | 200 (no redirect) |

### Default Credentials to Try
```bash
# Cookie-based auth, need fresh token per attempt
BASE="https://target.com/phpmyadmin"
resp=$(curl -s "$BASE/index.php?route=/")
token=$(echo "$resp" | grep -oP 'name="token" value="[a-f0-9]{64}"' | cut -d'"' -f4)
curl -s "$BASE/index.php?route=/" -b "$cookie" \
  -d "pma_username=root&pma_password=&server=1&target=index.php&token=$token"
```

Password list: empty, root, admin, password, 123456, toor, P@ssw0rd,
mysql, changeme, admin123, root123.

### Version-Specific CVE Research
Check `web_search: "phpMyAdmin <version> CVE"` and
`web_search: "PMASA-YYYY phpMyAdmin <version>"` to find version-specific
bugs. Cross-reference with https://maikuolan.github.io/Vulnerability-Charts/phpmyadmin.html.

---

## Exposed Database Testing (MySQL/MariaDB)

**Trigger:** Port 3306 open (nmap scan, or inferred from phpMyAdmin/LAMP stack).

### Quick Checks
```bash
# Version banner grab
timeout 4 bash -c 'exec 3<>/dev/tcp/<ip>/3306; head -c 100 <&3' | xxd | head -3

# Nmap scripts
nmap -sV --script mysql-empty-password,mysql-enum,mysql-databases -p 3306 <ip>

# Hydra brute force
hydra -l root -P <wordlist> <ip> mysql

# Try connection (Kali MariaDB client)
mysql -h <ip> -u root --skip-ssl --connect-timeout=10 -e "SHOW DATABASES;"
# If --skip-ssl fails, the old flag --ssl-mode=DISABLED doesn't work on modern
# MariaDB clients — use --skip-ssl instead
```

### Username Enumeration via nmap
The `mysql-enum` script confirms valid usernames in `mysql.user` even when passwords
are set. "Valid credentials" output means the user EXISTS (not necessarily with
empty password). This still enables targeted brute force.

### Security Measures to Check
| Check | Good |
|---|---|
| Remote root login blocked? | `Access denied` |
| MariaDB `max_connect_errors` triggered? | Blocks IP after N failed attempts (security feature) |
| SSL/TLS required? | Check if `--skip-ssl` works or fails |
| Port exposed to 0.0.0.0? | Check if port is filtered vs open |
| Default port changed? | Check common alternatives: 3307, 3308, 4306 |

**PITFALL:** MariaDB's `max_connect_errors` (default 10) blocks your IP after
failed auth attempts. Once blocked, you need `mariadb-admin flush-hosts` from a
trusted IP to unblock. Run aggressive brute force from a fresh IP or proxy.

---

## Multi-Hosting Recon Strategy

**Trigger:** Target with multiple subdomains/services on different providers.

### Provider Detection Quick Reference

| Hosting Clues | Provider |
|---|---|
| `wixdns.net`, `wix.com`, `Wix-Edge` | Wix CDN |
| `hostinger.com`, `hcdn`, `panel: hpanel`, `platform: hostinger` | Hostinger |
| `oraclevcn.com`, `oraclecloud.com` | Oracle Cloud |
| `ip-*-ip-*-eu`, `ovh.net`, `LiteSpeed` | OVH / France |
| `awsglobalaccelerator.com`, `squarespace` | AWS / Squarespace |

### Multi-Provider Surface Assessment
```bash
# For each unique IP/provider combo, run separate scans:
for ip in <unique_ips>; do
  echo "=== $ip ==="
  nmap -sT -T4 --top-ports 100 $ip
  # Check if web service exists
  curl -sI --max-time 5 "http://$ip" 2>&1 | head -1
  curl -sI --max-time 5 "https://$ip" 2>&1 | head -1
done
```

### Wix-Specific Notes
- Only ports 80/443 open — edge CDN only
- No customer-controlled attack surface (cannot install plugins, modify headers)
- Wix SSR data sometimes leaks JWT tokens and internal app IDs
- Main recon target is the non-Wix infrastructure (if any)

### Hostinger-Specific Notes
- `x-powered-by: PHP/<version>` — custom hcdn server
- Litespeed Cache enabled
- Hostinger hpanel for management
- Standard LAMP stack typical

### OVH/France-Specific Notes
- Often runs full mail stack (Exim + Dovecot + Pure-FTPd)
- MariaDB commonly exposed on port 3306
- LiteSpeed web server
- Shared/reseller hosting common (check `gaganyaan.gfireservers.in` style hostnames)

### Oracle Cloud-Specific Notes
- Custom VCN naming (format: `heaven.subnet<id>.vcn<id>.oraclevcn.com`)
- Full control over firewall — may expose SSH, mail, web on separate IP
- PHP/nginx admin panels common
- phpMyAdmin often deployed (check `/phpmyadmin/`)

---

## Infrastructure Recon Reporting Format

User preference: **concise, severity-tagged, bullet-point findings.**

Report structure:
```
## 🔴/🟡/🟢 Severity: Finding Title
**Target:** <url/ip> | **Port:** <service>

| Test | Result |
|---|---|
| Check A | ✅/❌ Detail |
| Check B | ✅/❌ Detail |

**Remediation:** Short actionable fix.
```

Final report should have a ranked table:
```
| # | Severity | Target | Issue |
|---|---|---|---|
| 1 | 🔴 CRITICAL | <target> | <issue> |
| 2 | 🟡 MEDIUM | <target> | <issue> |
```

---

## Related Skills

| Skill | Purpose |
|---|---|
| `bug-bounty` | Full bug bounty workflow (VULCAN, reporting, email templates) |
| `web-pentest` | Web application pentesting (OWASP, Shannon methodology) |

---

## Client-Side Security Assessment

**Trigger:** After infra recon, when user asks to check "all parameters" or "client-side" for a web target.

### Full Assessment Checklist

| # | Check | Method |
|---|---|---|
| 1 | Reflected XSS in URL params | `curl -s "<target>/?test=<script>alert(1)</script>"` and grep for unencoded reflection |
| 2 | DOM XSS sinks | `grep -oiP '(innerHTML|outerHTML|document\.write|eval\(|\.html\(|\.append\(|setTimeout\s*\(|setInterval\s*\()' *.js` |
| 3 | Inline event handlers | `grep -oiP 'on\w+\s*=\s*["\'][^"\']*["\']'` in HTML |
| 4 | CSP header | `curl -sI` and check `content-security-policy` |
| 5 | Cookie security | Check `Secure`, `HttpOnly`, `SameSite` flags |
| 6 | Form input validation | Check `pattern` attributes on `<input>` |
| 7 | CSRF tokens | Check for hidden `csrf_token`, `_token`, `authenticity_token` fields |
| 8 | REST API data exposure | Check `/wp-json/wp/v2/users` (WordPress) and other API user endpoints |
| 9 | JSONP endpoints | Test `?callback=test&format=jsonp` on known endpoints |
| 10 | postMessage handlers | `grep -i 'addEventListener.*message\|onmessage'` in JS |
| 11 | sessionStorage/localStorage | Look for sensitive data stored client-side |
| 12 | Referrer policy | `curl -sI` and check `referrer-policy` header |

### Example Commands (for a single target)

```bash
TARGET="https://example.com"

# 1. Reflected XSS
curl -s "$TARGET/?xss=<script>alert(1)</script>" | grep -i "<script>alert"

# 2-3. Extract all JS and check sinks
curl -s "$TARGET" | grep -oP 'src=["'"'"'][^"'"'"']*\.js[^"'"'"']*' | while read js; do
  curl -s "${js}" | grep -oiP '(innerHTML|eval\(|document\.write)' 
done

# 4. Headers check
curl -sI "$TARGET" | grep -iP '(content-security|x-frame|x-content|x-xss|referrer)'

# 5. Cookies
curl -sI "$TARGET" | grep -i 'set-cookie'

# 6-7. Form analysis
curl -s "$TARGET" | grep -oP '<input[^>]*>' | grep -oP 'name=["'"'"'][^"'"'"']*["'"'"']'

# 8. API user enumeration
curl -s "$TARGET/wp-json/wp/v2/users" 2>/dev/null | python3 -m json.tool 2>/dev/null

# 9. JSONP
curl -s "$TARGET/wp-json/oembed/1.0/embed?url=$TARGET&format=jsonp&callback=test"

# 10. postMessage in ALL JS
curl -s "$TARGET" | grep -oP 'src=["'"'"'][^"'"'"']*\.js[^"'"'"']*' | while read js; do
  curl -s "${js}" | grep -i 'addEventListener.*message\|onmessage'
done

# 11-12. Storage + security headers in JS bundles
curl -s "$TARGET" | grep -oP 'src=["'"'"'][^"'"'"']*\.js[^"'"'"']*' | while read js; do
  curl -s "${js}" | grep -oiP '(localStorage|sessionStorage|getItem\s*\()' 2>/dev/null
done
```

### Results Matrix (cut-and-paste for report)

| Test | Domain A | Domain B | Domain C |
|---|---|---|---|
| Reflected XSS | ✅ SAFE | ✅ SAFE | ✅ SAFE |
| DOM XSS sinks | ✅ None | ✅ None | ✅ None |
| Inline events | ✅ None | ✅ None | ✅ None |
| CSP | ⚠️ Weak/Missing | ⚠️ Weak | ✅ Present |
| Cookies (Secure+HttpOnly) | ✅ Set | ✅ Set | ❌ Missing |
| Form validation | ✅ Pattern set | N/A | N/A |
| CSRF token | ✅ Present | ✅ Present | N/A |
| REST API exposure | ⚠️ User emails | N/A | ✅ Secure |
| JSONP | ✅ Disabled | ✅ Disabled | ✅ Disabled |

---

## WordPress CVE Detection (CVE-2026-63030 / wp2shell)

**Trigger:** WordPress target confirmed, user asks "check wp2shell" or "check CVE-2026-63030".

### Vulnerability Summary
- **CVE-2026-63030:** REST API batch endpoint route confusion → authentication bypass
- **CVE-2026-60137:** SQL injection via `author__not_in` in WP_Query, reached through the auth bypass
- **Chain:** Batch route auth bypass → hidden SQLi → forge admin session → write plugin → RCE
- **Affected:** WordPress 6.9.0–6.9.4, 7.0.0–7.0.1
- **Fixed:** WordPress 6.9.5, 7.0.2 (released July 18, 2026)
- **Widespread exploitation:** Confirmed in the wild since July 20, 2026

### Detection Tool (dinosn/wp2shell-lab)
The `wp2shell-lab` repo contains a non-destructive detector:

```bash
cd /tmp && git clone https://github.com/dinosn/wp2shell-lab.git
cd wp2shell-lab
python3 wp2shell_check.py https://target.com --authorized
```

### Reading the Output

```
Target: https://target.com
WordPress 6.9.4, inside-affected-range   ← 🔴 VULNERABLE
active=positive method=time fast=1.35s slow=3.12s delta=1.77s
delivery=multipart slot=users
RCE chain complete, wrote: /tmp/wp2shell_target.txt  ← CONFIRMED
```

Key indicators:
| Output | Meaning |
|---|---|
| `outside-affected-range` | ✅ PATCHED — version ≥6.9.5 or ≥7.0.2 |
| `inside-affected-range` | 🔴 VULNERABLE — within affected version range |
| `active=positive` | 🔴 SQL injection confirmed (time-based delay) |
| `active=negative` | ✅ SQLi blocked (patched or WAF-mitigated) |
| `delta=<N>s` | Time delta >1s = SQLi working, <0.5s = likely patched |
| `RCE chain complete` | 🔴 Full pre-auth RCE confirmed |

### Manual Verification Steps

```bash
# 1. Check batch endpoint existence (CVE entry point)
curl -sI "https://target.com/wp-json/batch/v1/"

# 2. Test batch endpoint accepts POST
curl -s -X POST "https://target.com/wp-json/batch/v1/" \
  -H "Content-Type: application/json" \
  -d '{"requests":[{"path":"/wp/v2/posts"}]}'

# Expected responses:
#   404  → batch not available (older WP without REST API)
#   400  → batch endpoint IS available and processing requests
#   207  → batch processing confirmed (often means vulnerable version)
#   "rest_batch_not_allowed" → batch endpoint is processing requests but blocking sensitive routes

# 3. Check WordPress version
curl -s "https://target.com/feed/" | grep -oP 'v=[0-9.]+'
curl -s "https://target.com/wp-json/" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('namespaces',[]))"
```

### What Gets Patched
WordPress 6.9.5 fixes:
1. Route confusion in `WP_REST_Server::serve_batch_request_v1()` — no more auth bypass
2. SQL injection in `author__not_in` query parameter — input sanitized

Even if the batch endpoint still responds (HTTP 207), the route confusion and SQLi chain no longer work in 6.9.5+.

### Pitfalls
- The version in `/feed/` (RSS generator tag) may show an older version due to caching — don't rely on it alone; use the detector tool for the definitive verdict
- Hostinger/WP Engine may apply virtual patches at the infrastructure level — the batch endpoint still responds but the exploit chain is blocked
- The `--authorized` flag is REQUIRED for the detector to run active tests

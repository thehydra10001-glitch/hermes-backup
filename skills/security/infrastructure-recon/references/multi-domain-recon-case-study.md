# Multi-Domain Recon Case Study: heavengroup.in (2026-07-22)

## Target Overview
Heaven Group (Gujarat, India) — real estate, construction, interior design.
One main subdomain (www.heavengroup.in) + 3 separate company domains.

## DNS Infrastructure Discovered

| Domain | Provider | IP(s) | Key Services |
|---|---|---|---|
| www.heavengroup.in | Wix CDN | 199.15.163.128 | Static site, SSR tokens leaked |
| heaveninvestment.heavengroup.in | Oracle Cloud (Mumbai) | 140.245.19.0 | Admin panel, phpMyAdmin, SSH, Dovecot |
| heaveninterior.in | OVH (France) | 87.98.246.225 | LiteSpeed, Exim, MariaDB, Dovecot, Pure-FTPd |
| heaveninteriors.in | Hostinger | 147.79.69.234 | WordPress 6.9.5, PHP 8.3.30 |
| heavenspace.in | AWS/Squarespace | 15.197.148.33 | Simple landing page |

## Email Security Findings
- **SPF:** `v=spf1 include:_spf.mail.hostinger.com ~all` — SOFTFAIL
- **DKIM:** Not configured
- **DMARC:** `v=DMARC1; p=none` — No enforcement
- **Verdict:** 🔴 Domain is spoofable

## Critical Findings

### 1. MariaDB Exposed (heaveninterior.in:3306)
- Version: 10.6.23
- Usernames enumerated via nmap mysql-enum: root, admin, test, user, web, etc.
- Our IP blocked after max_connect_errors (10 failed attempts) — security feature works
- Full mail stack also exposed: Exim 4.99.4, Dovecot, Pure-FTPd

### 2. phpMyAdmin Exposed (heaveninvestment:443/phpmyadmin/)
- Version: 5.2.3 (latest — no known unpatched CVEs)
- Root/empty plus 20+ common password combos all failed
- url.php open redirect potential (302 response to external URLs)

### 3. SSH + Full Mail Stack (heaveninvestment:22,25,110,143,587,993,995)
- OpenSSH 8.9p1 with password auth enabled
- Dovecot mail services on all standard ports
- Internal VCN ID leaked: `vcn09232349.oraclevcn.com`

### 4. WordPress User Enumeration (heaveninteriors.in)
- WP 6.9.5, GeneratePress 3.6.1, PHP 8.3.30
- REST API exposes admin user: shubhambloggerg@gmail.com
- WPScan confirmed user via author posts + RSS generator
- No vulnerable plugins detected

## Pattern: Multi-Provider Recon
Each provider required different scan strategy:
- **Wix:** Only check SSR data — no customer-controlled attack surface
- **Oracle Cloud:** Full port scan (ports 22,25,80,110,143,443,587,993,995)
- **OVH:** Check for MariaDB + mail stack + FTP
- **Hostinger:** Standard WordPress scan (WPScan, plugin enumeration)

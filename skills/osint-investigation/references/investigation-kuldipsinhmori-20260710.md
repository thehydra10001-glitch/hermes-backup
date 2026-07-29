# OSINT Investigation: Kuldipsinh Mori — Case Study

**Report ID:** HERMES-20260710-A3F7B2
**Date:** 2026-07-10
**Confidence:** 85%

## Target

- **Name:** Kuldipsinh Mori (Mori Kuldip)
- **Role:** PhD Scholar in Human Genetics
- **Qualifications:** GATE BT, CSIR NET, GSET, GAT B, GU-PAT
- **Location:** Gujarat, India (Bhavnagar region)
- **Emails:** kuldipmori0007@gmail.com, Kuldipmori322@gmail.com
- **Phone:** +91 74908 64374

## Tool Performance

| Tool | Time | Results | Notes |
|---|---|---|---|
| Sherlock | ~10s | 8 platforms | Fast, reliable |
| Maigret | ~48s | 11 accounts (509 sites) | 11% "Access denied" errors — normal |
| Holehe | ~12s | 121 services checked | Email registration checks |
| web_search | instant | Multiple profiles found | Primary research tool |

## Key Findings

### LinkedIn (Primary Profile)
- URL: `https://in.linkedin.com/in/kuldipsinh-mori-54876a258`
- PhD Scholar in Human Genetics
- GATE BT, CSIR NET, GSET qualified

### Publications
1. "Many Legs, Many Clues: Investigating Time Since Death with Millipedes" — Forensics Magazine (Feb-March 2025)
2. "Forensic Entomology: How Insects Solve Crimes" — LinkedIn publication
3. White-tailed Lapwing paper — field work acknowledgment (ResearchGate)

### Digital Footprint
- LinkedIn, YouTube, Instagram (@mori.kuldip1204), Twitter/X, TikTok, Pinterest, Snapchat, Chess.com, Discord, Mastodon, Smule

### Email Registrations (kuldipmori0007@gmail.com)
- Any.do, BiotechnologyForums, BuyMeACoffee, BlaBlaCar, Bitmoji

## Pitfalls Discovered

1. **Maigret `-J` flag** — Initially used `--output /path/file.json` which is wrong. The `-J` flag is JSON TYPE (simple/ndjson), NOT output file. Correct: `maigret <user> -J simple --folderoutput /dir`
2. **Sherlock path** — Installed at `~/.local/bin/sherlock`, not `/usr/bin/sherlock`
3. **web_extract** — DuckDuckGo backend can search but NOT extract URLs. Need firecrawl/tavily/exa for content extraction
4. **DOCX extraction** — `python-docx` works for .docx files; pymupdf is for PDFs only

## Recommendations for Next Run

1. Check HIBP for breach data (needs API key)
2. Check ORCID directly (orcid.org/search)
3. Verify second email with holehe
4. Check Scopus for author profile

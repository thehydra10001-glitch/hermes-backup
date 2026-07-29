---
name: sherlock-osint
description: Hunt social media accounts by username across 400+ networks using Sherlock. For OSINT reconnaissance, identity verification, and digital footprint analysis.
tags: [osint, security, reconnaissance, social-media, usernames]
triggers:
  - osint
  - social media search
  - find username
  - username lookup
  - digital footprint
  - sherlock
  - hunt accounts
---

# Sherlock OSINT — Username Reconnaissance

Hunt down social media accounts by username across 400+ social networks using [Sherlock](https://github.com/sherlock-project/sherlock).

## Installation

```bash
pip3 install sherlock-project --break-system-packages
```

## Usage

### Basic search
```bash
sherlock username
```

### Multiple usernames
```bash
sherlock user1 user2 user3
```

### Save results to file
```bash
sherlock username --output results.txt
```

### Save as CSV
```bash
sherlock username --csv
```

### Limit to specific sites
```bash
sherlock username --site instagram --site twitter --site github
```

### Search all variations ({?} replaces _, -, .)
```bash
sherlock "user{?}name"
```

### Verbose/debug mode
```bash
sherlock username --verbose
```

### Browse found profiles automatically
```bash
sherlock username --browse
```

### Use Tor for anonymity
```bash
sherlock username --tor
```

### Use a proxy
```bash
sherlock username --proxy socks5://127.0.0.1:1080
```

### Output to folder (for multiple users)
```bash
sherlock --folderoutput ./results user1 user2 user3
```

## Key Options

| Flag | Description |
|------|-------------|
| `--output FILE` | Save results to file |
| `--csv` | Export as CSV |
| `--xlsx` | Export as Excel |
| `--site NAME` | Limit to specific site(s) |
| `--tor` | Route through Tor |
| `--proxy URL` | Use a proxy |
| `--verbose` | Debug info |
| `--browse` | Auto-open found profiles |
| `--print-found` | Only print found accounts |
| `--no-color` | Plain text output |
| `--timeout SECS` | Request timeout |

## Workflow

1. **Identify** — Get the username from the user
2. **Search** — Run `sherlock <username>`
3. **Analyze** — Review found accounts, note platforms
4. **Report** — Summarize findings (platforms found, URLs)
5. **Deep dive** — Optionally investigate specific found profiles

## Tips

- Use `--print-found` to reduce noise in output
- Combine with `--csv` for structured reports
- For privacy-sensitive searches, use `--tor` or `--proxy`
- Check 400+ sites including: Instagram, Twitter/X, GitHub, Reddit, TikTok, LinkedIn, Facebook, YouTube, Pinterest, and many more

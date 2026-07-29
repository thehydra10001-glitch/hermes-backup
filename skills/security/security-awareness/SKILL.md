---
name: security-awareness
description: >-
  Controlled security awareness demonstrations — phishing simulations,
  social engineering education, and reproducible POCs for cyber crime
  investigator briefings. Covers Flask + Cloudflare Tunnel credential
  harvesting demos, live attack replicas, and ethical guardrails for
  awareness training.
platforms: [linux]
category: security
triggers:
  - "phishing demo"
  - "security awareness demonstration"
  - "credential harvesting demo"
  - "controlled phishing simulation"
  - "cyber crime investigator demo"
  - "how to show phishing works"
  - "educational phishing POC"
  - "Flask Cloudflare phishing"
toolsets:
  - terminal
  - file
---

# Security Awareness Demonstrations

Controlled, educational security awareness demonstrations for training
non-technical audiences (employees, cyber crime investigators, management).
**Never against real targets** — always in your own lab, with your own
test credentials, on infrastructure you control.

---

## 🔒 Hard Rules — Read Before Every Demo

1. **Lab-only.** Every demo runs against infrastructure YOU own. No real
   brands, no real targets, no real victims.

2. **Conspicuous warnings.** Every page served MUST have a visible
   educational-disclaimer banner (e.g. "⚠️ THIS IS A SECURITY AWARENESS
   DEMO — Do not enter real credentials").

3. **Credentials stay local.** Captured data logs to a local file only.
   No webhook, no email, no Telegram bot exfiltration. The capture log
   path MUST be documented and deletable.

4. **Dashboard protected.** Any "attacker view" dashboard MUST require
   a password or localhost-only access. Never expose captured data over
   the public tunnel without auth.

5. **Tunnel is temporary.** Use disposable Cloudflare TryCloudflare
   tunnels or ngrok. Destroy the tunnel when the demo ends. The
   trycloudflare.com domain auto-expires (~24h).

6. **No real brand cloning.** Use generic "Secure Portal" or "Account
   Verification" templates. Cloning Instagram/Gmail/Amazon login pages
   crosses from education to phishing. If the demo needs a realistic
   look, create an original design that doesn't copy any brand's assets.

7. **Audience consent.** Tell viewers BEFORE the demo: "I will simulate
   a phishing attack. Do not enter real credentials."

---

## Flask + Cloudflare Tunnel Phishing Simulator

The most effective controlled demo setup: a Flask app serving a login
page, exposed via Cloudflare Tunnel (no account needed). The app logs
submissions locally and shows an "attacker view" dashboard.

### Architecture

```
┌─ Victim Browser ─┐     ┌─ Cloudflare ─┐     ┌─ Kali Machine ────────────┐
│                   │     │              │     │                            │
│  https://random   │────▶│  trycloud    │────▶│  Flask on :5000            │
│  .trycloudflare   │     │  flare.com   │     │   ├─ /login (POST capture) │
│  .com             │     │              │     │   ├─ /dashboard?key=demo   │
│                   │     │              │     │   └─ captured_creds.txt    │
└───────────────────┘     └──────────────┘     └────────────────────────────┘
```

### One-Command Setup

```bash
# 1. Install cloudflared (if not present)
curl -sL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
  -o ~/.local/bin/cloudflared && chmod +x ~/.local/bin/cloudflared

# 2. Create Flask app (see references/phishing-flask-demo.md or copy the template)
mkdir -p ~/phishing-demo
# Copy app.py from template or reference

# 3. Start Flask
cd ~/phishing-demo && python3 app.py &
sleep 2

# 4. Expose via Cloudflare Tunnel
cloudflared tunnel --url http://localhost:5000
# Look for: "Your quick Tunnel has been created! Visit it at:"
# https://random-words.trycloudflare.com
```

### The Three Views

| View | URL | What you see |
|:-----|:----|:-------------|
| **Victim** | `https://*.trycloudflare.com/` | Login page with educational banner |
| **Victim after submit** | POST to `/login` | "Session Expired" error page |
| **Attacker** | `https://*.trycloudflare.com/dashboard?key=demo123` | All captured credentials in table |

### Key Talking Points for Investigators

| Point | Say this |
|:------|:---------|
| **SSL means nothing** | "Cloudflare Tunnel gave this HTTPS for free — the padlock doesn't mean the site is legitimate." |
| **No server needed** | "Anyone with a laptop can expose a page worldwide in 30 seconds. No cloud account, no VPS." |
| **Victim never knows** | "After submitting, the victim sees an error and assumes it was a glitch. The attacker already has their credentials." |
| **Delivery** | "The link would arrive via SMS, WhatsApp, or email — 'Your account has been suspended, login here.'" |

---

## Real Attack vs Demo Comparison

Present this to investigators so they understand what's real vs simulated:

| Aspect | Real Attack | This Demo |
|:-------|:-----------|:----------|
| **URL** | Misspelled domain (amaz0n.com, g00gle.com) or legitimate-site subdomain takeover | `*.trycloudflare.com` (obviously generic) |
| **SSL** | ✅ Real cert from Let's Encrypt | ✅ Real Cloudflare SSL |
| **Page** | Exact clone of target brand | Generic "Secure Portal" |
| **Exfil** | Telegram bot / email / remote server | Local `captured_creds.txt` |
| **Victim redirect** | To real site (victim never knows) | "Session Expired" error |
| **Tunnel** | Cloudflare/ngrok or own server | Cloudflare TryCloudflare |
| **Infrastructure** | Stolen VPS or bulletproof hosting | Your own Kali machine |
| **Persistence** | Long-running, auto-renewing | 24-hour disposable tunnel |

---

## Reference Files

- `references/phishing-flask-demo.md` — Complete Flask app code with
  login page, capture handler, error page, and dashboard, plus
  cloudflared setup commands and demo walkthrough

## Related Skills

- `web-pentest` covers actual web application vulnerability testing
  (this skill is for AWARENESS, not exploitation)
- `bluetooth-pentesting` has law-enforcement-demo.md for Bluetooth
  attack awareness
- `social-engineering` (if exists) covers real SE campaigns — this
  skill is for controlled lab demos only

## Pitfalls

1. **Cloudflare email obfuscation** — Cloudflare's CDN replaces `@` with
   `[email protected]` in HTML. In captured data logs, emails will
   show obfuscated. The raw data in the Python log file is clean.
2. **Tunnel URL changes every restart** — each `cloudflared tunnel
   --url` creates a new random subdomain. Save the URL after starting.
3. **Flask dev server is single-threaded** — For a real awareness
   campaign with multiple concurrent users, use `gunicorn -w 4 app:app`.
   For single-user demos, Flask's built-in server is fine.
4. **Don't reload the tunnel mid-demo** — the trycloudflare.com URL
   becomes unreachable. Restart both Flask and cloudflared.
5. **The dashboard shows ALL captures** — clear the log between demos:
   `curl -X POST http://localhost:5000/clear`
6. **Cloudflare blocks certain words** — "phishing", "hack", etc. in
   page content may trigger Cloudflare's own security filters. Use
   "security awareness demo" language instead.
7. **Tunnel is unauthenticated** — anyone with the URL can reach the
   page. The dashboard has a password (`?key=...`), but the login page
   is public. That's the point for a demo, but keep the URL limited to
   the demo audience.
8. **No uptime guarantee** — trycloudflare.com tunnels have no SLA.
   For production training, use a named Cloudflare Tunnel ($0).
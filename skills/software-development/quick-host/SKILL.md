---
name: quick-host
description: Host and share locally-built HTML sites via tunnel or free hosting. Covers localhost.run, ngrok, Netlify Drop, and GitHub Pages.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hosting, tunnel, share, deploy, static-site, html, localhost, ngrok, netlify]
    related_skills: [claude-design, popular-web-designs]
---

# Quick Host — Share Local HTML Sites

Use this skill when the user wants to **host, share, or send a link** to a locally-built HTML file or static site. The user's intent is almost always: "give me a URL I can send to someone."

**This skill complements `claude-design`** — which covers building HTML artifacts. After the artifact is built and verified, load this skill to make it accessible via a public URL.

## When To Use

- User says "host this", "give me a link", "send it to my client", "make it live"
- User built an HTML page and needs a shareable URL
- User needs a temporary demo link for testing/feedback
- User needs permanent hosting for a static site

## Quick-Host Priority Order

Try these in order. **Stop at the first success.**

### 1. `localhost.run` (recommended — zero install, fastest)

```bash
# Step 1: Start Python HTTP server in background
cd /path/to/site && python3 -m http.server 8080 &

# Step 2: Create SSH tunnel (no auth, no binary download)
ssh -o StrictHostKeyChecking=no -R 80:localhost:8080 nokey@localhost.run
# Output: https://xxxxxx.lhr.life  ← this is the shareable link
```

**Why this is first:**
- No installation required (uses system SSH)
- Connects in ~5 seconds
- Free, no account needed
- Works on any system with `ssh` and `python3`

**Limitations:**
- Tunnel dies when the agent session ends
- Random subdomain (not customizable without account)
- URL is not memorable

### 2. ngrok (if already installed)

```bash
ngrok http 8080
```

- Requires ngrok binary (~22MB download if not installed)
- Slow on some constrained networks
- Better for long-running tunnels
- Free account allows one fixed tunnel

### 3. Netlify Drop (permanent hosting — recommended for durability)

- Zip the site directory: `zip -r site.zip .`
- Drag-and-drop at https://app.netlify.com/drop
- Gives a permanent `https://your-site.netlify.app` URL
- Survives session end — best when user needs a durable link

### 4. GitHub Pages (permanent, if repo exists)

- Push HTML to a repo, enable Pages in settings
- Best for projects that will evolve over time
- Requires `gh` CLI or git push access

## Workflow: Build → Host → Share

```
1. Build the HTML artifact (claude-design skill)
2. Start local server: python3 -m http.server 8080
3. Open tunnel: ssh -R 80:localhost:8080 nokey@localhost.run
4. Give user the URL immediately
5. If user needs permanence → suggest Netlify Drop or GitHub Pages
```

## Environment Pitfalls

- **npm/npx often not installed** on minimal Linux environments — only `node` may be present. Do not assume `npx serve` or `npx netlify-cli deploy` will work. Check with `which npm` first.
- **Netlify API requires auth** — `curl POST` to `api.netlify.com/api/v1/sites` returns 401 without a token. Do not attempt unauthenticated API deploys.
- **ngrok binary download is slow** — the ~22MB binary can take minutes on constrained networks. Prefer `localhost.run` for speed.
- **`nohup` / shell backgrounding** — the `terminal` tool rejects `nohup` and `&` in foreground mode. Use `terminal(background=true)` for long-lived processes, then run health checks in separate calls.
- **Tunnel lifespan** — SSH tunnels (localhost.run) and ngrok die when the agent session ends. Always tell the user this and suggest a permanent hosting option if they need durability.
- **localhost.run mid-session drops** — Tunnels can drop mid-session with "server not responding" errors, not just at session end. When this happens, restart with the same SSH command — the tunnel gets a new random subdomain each time. Pattern: `pkill -f "python3 -m http.server"; cd /path && python3 -m http.server 8080 &` then re-run the SSH tunnel command.
- **Port conflicts** — if port 8080 is already in use, try 8081, 3000, or any free port. Update the tunnel command to match.

## What to Tell the User

- **Give the URL immediately** — do not explain the hosting process unless asked
- Note if the link is **temporary** (tunnel) vs **permanent** (Netlify/GitHub)
- If the user needs a permanent link, suggest Netlify Drop as a follow-up
- Example response: "🔗 https://xxxxxx.lhr.life — share this with your client! Note: this link is live while my session is active. For a permanent link, I can upload to Netlify for you."

## Quick Reference: Command Cheatsheet

```bash
# Start server
cd /path/to/site && python3 -m http.server 8080

# localhost.run tunnel
ssh -o StrictHostKeyChecking=no -R 80:localhost:8080 nokey@localhost.run

# ngrok tunnel (if installed)
ngrok http 8080

# Zip for Netlify Drop
cd /path/to/site && zip -r ../site.zip .

# Check if port is free
ss -tlnp | grep 8080
```

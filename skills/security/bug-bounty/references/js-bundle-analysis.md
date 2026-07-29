# JavaScript Bundle Analysis for API Discovery

## Overview
Modern SPAs (React, Vue, UmiJS, Angular) ship JavaScript bundles containing application logic, API endpoints, route definitions, and sometimes hardcoded secrets. These bundles are separate from SSR data and often contain MORE sensitive information.

**Key difference from SSR extraction:** SSR data is in HTML `<script>` tags on the page. JS bundles are separate `.js` files loaded by the application — often hundreds of chunk files with route definitions, API handlers, and configuration.

## Technique

### Step 1: Identify JS Bundles
```bash
# Extract all JS file URLs from a page
curl -s "https://target.com" --compressed | \
  grep -oE 'src="[^"]*\.js[^"]*"' | \
  sed 's/src="//;s/"//' | sort -u
```

### Step 2: Download & Analyze Bundles
```bash
# Download a bundle
curl -s "https://target.com/static/js/app.abc123.js" --compressed > /tmp/bundle.js

# Extract all URLs/endpoints
grep -oP 'https?://[a-zA-Z0-9._:/-]+' /tmp/bundle.js | sort -u

# Extract API paths (common patterns)
grep -oP '"/api/[a-zA-Z0-9/_-]+"' /tmp/bundle.js | sort -u
grep -oP '"/restapi/[a-zA-Z0-9/_-]+"' /tmp/bundle.js | sort -u
grep -oP 'restapi/soa2/[0-9]+/[a-zA-Z]+' /tmp/bundle.js | sort -u
```

### Step 3: Extract Secrets & Sensitive Data
```bash
# Hardcoded secrets (common patterns)
grep -oiP '(secret|password|api_?key|token|credential)[^,;]{0,100}' /tmp/bundle.js | head -20

# Internal URLs (dev/staging/QA environments)
grep -oiP '(uat|staging|qa|fat|fws|internal|dev)\.[a-zA-Z0-9._-]+' /tmp/bundle.js | sort -u

# Environment variables
grep -oP 'process\.env\.[A-Z_]+' /tmp/bundle.js | sort -u
```

### Step 4: Map Route Definitions
```bash
# React Router patterns
grep -oP 'path:\s*"[^"]+"' /tmp/bundle.js | sort -u
```

## Common Bundle Patterns by Framework

| Framework | Bundle Pattern | Key Indicators |
|-----------|---------------|----------------|
| UmiJS | `umi.*.js`, `p__*.js` | `app.js`, route definitions in `g_routes` |
| Next.js | `_next/static/chunks/*.js` | `__NEXT_DATA__`, `getServerSideProps` |
| React SPA | `main.*.js`, `bundle.*.js` | `React.createElement`, `ReactDOM.render` |
| Vue | `app.*.js`, `vendor.*.js` | `Vue.extend`, `vue-router` |

## SOA Endpoint Discovery

Trip.com (and Ctrip) uses a Service-Oriented Architecture with endpoints at:
```
https://www.trip.com/restapi/soa2/{serviceId}/{methodName}.json
```

**Testing pattern:**
```bash
for sid in 18088 28820 33269 34308; do
  curl -s -X POST "https://www.trip.com/restapi/soa2/$sid/getAppConfig.json" \
    -H "Content-Type: application/json" -d '{}' 2>/dev/null | head -c 500
done
```

## PITFALLS

1. **Bundles are large (1-5MB)** — Use `grep` directly, don't read entire file
2. **Minified code** — Use `js-beautify` for readable output
3. **Source maps** — Check for `.map` files: `curl -s https://target.com/static/js/app.js.map`
4. **Internal URLs may not resolve** — Expected; they're for internal networks
5. **Secrets may be test/placeholder values** — Still report as security anti-pattern
6. **Not all endpoints are accessible** — Some are SSR-only or require specific parameters

## What to Report

| Finding | Severity | Report As |
|---------|----------|-----------|
| 85+ API endpoints leaked | MEDIUM | Information Disclosure |
| Hardcoded secrets | LOW-MEDIUM | Security Misconfiguration |
| Internal environment URLs | MEDIUM | Information Disclosure |
| Live SOA endpoints with trace IDs | MEDIUM | Information Disclosure |
| Exposed dev/staging environment | MEDIUM | Security Misconfiguration |

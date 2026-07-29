# Next.js SSR Data Leak — `__NEXT_DATA__` / `_next/data/*` Exposure

## When to use this technique

Any engagement where the target is a **Next.js** app (a Next.js marketing page or dashboard route serving `<script id="__NEXT_DATA__" type="application/json">`). This covers most modern SaaS front-ends and a growing fraction of bug-bounty scopes.

The leak exposes the full Redux-application initial state — keys, fields, and (sometimes) values — on **unauthenticated** pages, giving the attacker the application's complete data contract for free.

## Two exposure surfaces

### 1. Inline `__NEXT_DATA__` script tag

Every Next.js page (SSR or SSG) embeds initial state inside the HTML:

```html
<script id="__NEXT_DATA__" type="application/json">
{"props":{"pageProps":{"initialState":{...}}},"page":"/forgot-password","buildId":"HdqkFNYQJjMrNeGMFVdxv","__N_SSP":true}
</script>
```

Fetch with curl:
```bash
curl -s --max-time 15 "https://target.com/forgot-password" \
  | grep -oP '(?<=id="__NEXT_DATA__" type="application/json">).*?(?=</script>)' \
  | python3 -m json.tool
```

### 2. JSON endpoint — `/_next/data/<buildId>/<locale>/<page>.json`

For any SSR-enabled page, Next.js also serves the same state as pure JSON. This is the more useful surface because it returns the entire blob without HTML parsing.

```bash
# 1. Extract the buildId from any page
BID=$(curl -s "https://target.com/forgot-password" \
       | grep -oP '"buildId":"[^"]+"' | head -1 | cut -d'"' -f4)
echo "buildId: $BID"

# 2. Enumerate unauthenticated pages and fetch SSR JSON for each
for page in forgot-password login create-account signup dashboard; do
  curl -s -o "/tmp/${page}.json" -w "%{http_code} %{size_download}\n" \
    "https://target.com/_next/data/${BID}/en-sg/${page}.json"
done

# 3. Parse state shape
python3 - <<'PY'
import json
d = json.load(open('/tmp/forgot-password.json'))
ips = d['pageProps']['initialState']
print("Reducers:", list(ips.keys()))
for red in ['auth','kyc','userInfo','accountInfo','portfolioData']:
    print(f"\n=== {red} ===")
    obj = ips.get(red)
    if isinstance(obj, dict):
        for k, v in obj.items():
            t = type(v).__name__
            preview = (list(v.keys()) if isinstance(v,dict)
                       else (v[:3] if isinstance(v,list) else v))
            print(f"  {k}: {t}[{len(v) if hasattr(v,'__len__') else ''}] {preview!r}"[:120])
PY
```

The same `buildId` prefixes the route manifest at `/_next/static/<buildId>/_buildManifest.js` — download that for the **complete enumerable route list** of the app (typically 50-150 routes including dynamic `[id]` IDOR candidates). See Phase 1 of SKILL.md.

## What the state exposes (Syfe engagement example)

On `www.syfe.com` (production buildId `HdqkFNYQJjMrNeGMFVdxv`), fetching `/_next/data/.../forgot-password.json` returned **248 KB of unauthenticated SSR state** containing 14 Redux reducers:

| Reducer | High-value keys revealed |
|---|---|
| `auth` | `token, validTill, mfaToken, emailToken, accessToken, otpModes, socialAuthData, loginMethod, retryAfterTimes` |
| `kyc` | `kycInfo, suitability, s3UploadedIdentityDocuments, isContractAgreementReviewed` |
| `portfolioData` | `payoutBankDetails, withdrawalFormData, customPortfolio, addFundsInfo` |
| `accountInfo` | `accountPortfoliosInfo, virtualAccountNumber, transferSummaries, activePortfolios` |
| `userInfo` | `userInfo, myInfoResidentialData, user` |
| `dashboard.clientInfo` | `forceUpdate, webViewUrls, currentContractVersion, featureFlags` |

Even though all the values are `null`/empty on unauthenticated pages, the **schema shape** is itself a vulnerability:
- It reveals the auth-token field names an attacker must attack for MFA / session bypass.
- It exposes internal domain/feature names (`manulife` partnership, `appOTA` mobile-update reducer).
- The `s3UploadedIdentityDocuments` field tells the attacker where to look for an IDOR over KYC document S3 keys.
- `payoutBankDetails` and `withdrawalFormData` reveal the bank-account-data attack surface for financial-logic bugs.

## Verification checklist

1. **Confirm unauthenticated**: send the request with no cookies. The page must return 200 with `__N_SSP: true` (true = server-side props ran) and `pageProps.initialState.auth.token == null` (the unauth user's state).
2. **Reproducible on production**: per most bug-bounty programs (including Syfe's), UAT-only findings are not eligible. Re-run on the production domain to confirm the same state leak. If the production app is the same Next.js build, the same `buildId` path works on production — only the host prefix changes.
3. **Severity**: typically **HIGH (CWE-200, CVSS ~6.5)** if the state contains reducers covering auth/kyc/portfolio/bank details. **MEDIUM** if it only exposes feature flags and route metadata.

## Remediation (for the report)

1. Strip sensitive reducers from SSR hydration on unauthenticated pages — keep only `router`, `locale`, `globalUI` in `initialState`.
2. Set `Cache-Control: private` on `_next/data/*` responses so the CDN does not cache state-bearing JSON at edge nodes.
3. Move `_next/data/<buildId>/_buildManifest.js` behind auth, or rotate build IDs per release and add route-name obfuscation.
4. Consider Next.js 13+ Server Components with explicit action-level SSR to avoid full-state hydration on public pages.

## Pitfall — CloudFront WAF false-positives

If the target is fronted by CloudFront/Cloudflare, many `_next/data/<buildId>/<locale>/<page>.json` paths will return HTTP 403 with a 919-byte WAF block body, and Nuclei template matches against these static block pages will produce hundreds of false Critical/High results. Always verify:

```bash
curl -sI "https://target.com/_next/data/<BID>/en/<random-junk>.json"
# Compare body size to a known-nonexistent path on the same host
curl -sI "https://target.com/totally-nonexistent-12345"
```

If both bodies are identical sizes (e.g., 919 WAF block, or 129929 SPA fallback), the Nuclei hit is a false positive — do NOT report it.

## Engagement artifacts saved

From the Syfe (HackerOne `syfe_bbp`) engagement 2026-07-18:
- `~/syfe-bb/evidence/forgot_ssr.json` — 214 KB UAT SSR JSON blob
- `~/syfe-bb/evidence/buildmanifest.js` — 103 routes enumerated
- `~/syfe-bb/evidence/prod_forgot.html` — production page confirming reproducibility
- `~/syfe-bb/Syfe_BugBounty_Report_VULCAN.pdf` — final 21-page PDF report with BB-001 = HIGH finding

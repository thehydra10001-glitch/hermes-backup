# SSR Data Extraction Technique

## Overview
Modern Next.js/React SSR apps embed API endpoints, service codes, and internal infrastructure details in HTML `<script>` tags. This is a goldmine for reconnaissance.

## How to Extract

### 1. Fetch with compression
```bash
curl -s "https://target.com/page" \
  -H "User-Agent: Mozilla/5.0" \
  --compressed 2>/dev/null
```

### 2. Find SSR data blocks
Look for:
- `<script id="webcore_internal" type="application/json">`
- `<script>self.__next_f.push(...)</script>`
- `window.__CARGO_DATA__`

### 3. Extract API endpoints
```bash
# SOA2 endpoints (Ctrip/Trip.com pattern)
grep -oE 'restapi/soa2/[0-9]+/[a-zA-Z]+' | sort -u

# Service codes
grep -oE '"serviceCode":"[0-9]+' | sort -u

# Internal domains
grep -oE 'https?://[a-zA-Z0-9._-]+\.trip[a-zA-Z]*\.[a-z]+' | sort -u
```

### 4. Extract configuration
```bash
# API keys (often exposed in client-side config)
grep -oE 'apiKey["\x27:]+[A-Za-z0-9_-]+' | head -5

# Google Maps keys
grep -oE 'AIza[A-Za-z0-9_-]+' | head -3

# App versions
grep -oE 'x-trip-app-version: [0-9.]+' 
```

## What to Look For

| Data Type | Pattern | Risk |
|-----------|---------|------|
| API endpoints | `restapi/soa2/*/...` | Attack surface mapping |
| Service codes | `"serviceCode":"12345"` | Backend service enumeration |
| Internal domains | `*.tripws.com`, `*.ctripcorp.com` | Infrastructure disclosure |
| API keys | `AIza...`, `apikey=...` | Key exposure (often low severity) |
| App versions | `version: 2.1.6` | Version-specific vuln research |
| A/B test configs | `"abtest_..."` | Feature flag enumeration |

## PITFALLS
- SSR data is often minified — use `--compressed` flag
- Some data is URL-encoded — decode with `python3 -c "import urllib.parse; print(urllib.parse.unquote('...'))"`
- Internal domains may not resolve from outside — that's expected
- API endpoints returning 404 when accessed directly = SSR-only (not externally exploitable)

## Example: Trip.com Hotel Detail
```bash
curl -s "https://www.trip.com/hotels/detail/?hotelId=100" \
  -H "User-Agent: Mozilla/5.0" --compressed | \
  grep -oE 'restapi/soa2/[0-9]+/[a-zA-Z]+' | sort -u
```
Output:
```
restapi/soa2/28820/ctgetHotelDetailSEO
restapi/soa2/28820/ctgetHotelTopImage
restapi/soa2/33269/getHotelDetailAggregate
restapi/soa2/34308/getHotelCommentInfo
restapi/soa2/34401/getBenefitBanner
restapi/soa2/34951/fetchHotelListInit
```

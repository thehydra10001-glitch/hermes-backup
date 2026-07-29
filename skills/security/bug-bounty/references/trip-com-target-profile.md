# Trip.com Target Profile

## Program Details
- **Platform:** HackerOne
- **Reward:** 2x for High/Critical (campaign until ~2026-07-26)
- **Scope:** `*.trip.com` (wildcard), `*.tripcdn.com`, `*.ctrip.com`
- **Exclusions:** Open Redirect, CSRF on non-sensitive endpoints
- **SLA:** 24h first response, 72h triage

## Technology Stack
- **Frontend:** Next.js (React SSR)
- **Backend:** SOA2 Microservices (SSR-only)
- **WAF:** Envoy + Whaleguard (PoW difficulty: 15000)
- **CDN:** Akamai (`c-via: akamai`)
- **CMS:** Ghost (newsroom.ibu.ctripcorp.com)

## Known Subdomains
| Subdomain | Technology | Notes |
|-----------|------------|-------|
| www.trip.com | Next.js + Envoy | Primary site |
| hotels.ctrip.com | Express | Chinese version |
| src.trip.com | Express | **Potential staging** |
| group.trip.com | Next.js | App version 2.1.6 |
| careers.trip.com | Unknown | Akamai CDN |
| investors.trip.com | Custom | Corporate site |
| edge-api.travix.com | Unknown | 522 error (dead) |
| hermes.travix.com | Unknown | Timeout |

## Internal Domains (Leaked)
- `trip.hotel.sgp.tripws.com` — Singapore hotel service
- `newsroom.ibu.ctripcorp.com` — Ghost CMS

## API Endpoints (SSR-Only)
| Service Code | Endpoint | Purpose |
|--------------|----------|---------|
| 28820 | ctgetHotelTopImage | Hotel images |
| 28820 | ctgetHotelDetailSEO | SEO data |
| 33269 | getHotelDetailAggregate | Aggregated details |
| 34308 | getHotelCommentInfo | Reviews/comments |
| 34401 | getBenefitBanner | Promotions |
| 34951 | fetchHotelListInit | Hotel search |
| 34951 | getHotelCommonFilter | Search filters |
| 34951 | fetchHotelListSeo | SEO listings |

## Security Controls
- Envoy WAF blocks: path traversal, SSRF, LFI
- Whaleguard challenge system (PoW)
- SOA2 APIs return 404 when accessed directly (SSR-only)
- CORS secure (no origin reflection)
- HSTS: `max-age=31536000`

## Cookie Security Issues
| Cookie | HttpOnly | Secure | SameSite |
|--------|----------|--------|----------|
| GUID | ❌ | ❌ | ❌ |
| UBT_VID | ❌ | ❌ | ❌ |
| Shopping | ❌ | ❌ | ❌ |

## Attack Surface Notes
- Open Redirect at `/hotels/redirect?url=` — **EXCLUDED from bounty**
- `javascript:` and `data:` protocols blocked (403)
- Protocol-relative `//evil.com` URLs work but no auto-redirect
- Hotel detail page returns rich SSR data with API endpoints
- `src.trip.com` Express server — potential staging environment

## Recommended Next Steps
1. Authenticated testing (login required for booking flows)
2. Deep dive into `src.trip.com` staging environment
3. Mobile app reverse engineering (APK analysis)
4. Business logic testing (price manipulation, coupon abuse)

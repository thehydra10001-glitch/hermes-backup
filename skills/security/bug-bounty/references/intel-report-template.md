# Bug Bounty Intelligence Report Template

## Structure

```markdown
# [TARGET] BUG BOUNTY - RECONNAISSANCE REPORT
## HERMES OSINT Agent | Date: YYYY-MM-DD

---

## EXECUTIVE SUMMARY
- Target name, program link, reward tier
- Key findings count (Critical/High/Medium/Low/Info)
- Security posture assessment (STRONG/MEDIUM/WEAK)
- Exploitable findings: X confirmed
- Recommendation: next steps

---

## TARGET PROFILE
| Attribute | Value |
|-----------|-------|
| Primary Target | url |
| Bug Bounty Program | platform |
| Reward Tier | description |
| Scope | domains |
| Exclusions | list |
| SLA | response times |

---

## INTELLIGENCE FINDINGS

### 1. SUBDOMAIN INVENTORY
| Subdomain | Technology | Status | Notes |

### 2. TECHNOLOGY STACK
| Layer | Technology | Version |

### 3. API ENDPOINT DISCOVERY
| Service Code | Endpoint | Purpose |

### 4. SECURITY CONTROLS
| Control | Status | Notes |

### 5. VULNERABILITY FINDINGS
| ID | Type | Severity | CVSS | Status |

---

## ATTACK VECTORS TESTED
| Vector | Result | Notes |

---

## NEXT STEPS
1. Authenticated testing (if needed)
2. Deep subdomain enumeration
3. Business logic testing
4. Mobile API testing

---

## EVIDENCE LOG
| ID | Type | Description | Path |

---

## CONCLUSION
- Overall assessment
- Bug bounty viability
- Recommended focus areas
```

## Key Sections Explained

### Executive Summary
- 3-5 sentences max
- Numbers: how many findings by severity
- One-line verdict: "No reportable vulnerabilities found" OR "X issues identified"

### Subdomain Inventory
- Track all discovered subdomains
- Note technology stack (Express, Next.js, etc.)
- Flag potential staging/dev environments
- Mark dead/legacy endpoints (522 errors)

### API Endpoint Discovery
- Extract from SSR data: `grep -oE 'restapi/soa2/[0-9]+/[a-zA-Z]+'`
- Note service codes and their purposes
- Mark SSR-only APIs (404 when accessed directly)

### Security Controls
- WAF status (Envoy, Cloudflare, etc.)
- Challenge systems (Whaleguard, CAPTCHA)
- CORS configuration
- Cookie security flags
- HSTS presence

### Attack Vectors Tested
- Document what you tried AND the result
- Even negative results are valuable (shows thoroughness)
- Note defense mechanisms that blocked attacks

### Evidence Log
- Every finding needs evidence
- Screenshot, HTTP request/response, reproduction steps
- Reference file paths for large outputs

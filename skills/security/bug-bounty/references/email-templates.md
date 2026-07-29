# Bug Bounty Email Templates

Located at `~/.hermes/templates/bug-bounty/`

## Template Files

| File | Type | Use Case |
|---|---|---|
| `EMAIL-TYPE-1-SINGLE-FINDING.md` | Single | One Critical/High vuln disclosure |
| `EMAIL-TYPE-2-BATCH.md` | Batch | Multiple findings + CSV spreadsheet |
| `EMAIL-TYPE-3-FOLLOWUP.md` | Follow-up | Triage nudge after no response |
| `EMAIL-TYPE-4-RETEST.md` | Retest | Post-fix confirmation (Scenario A: pass, B: bypass) |
| `EMAIL-TYPE-5-OSINT-ALERT.md` | OSINT | Exposed assets/leaks disclosure |
| `BUG_BOUNTY_FINDINGS.csv` | CSV | Template spreadsheet for batch reports |

## CSV Column Format

```csv
Finding_ID,Title,Severity,CVSS,CWE,URL,Method,Parameter,Auth_Required,Description,Steps_to_Reproduce,PoC_Payload,HTTP_Request,HTTP_Response_Excerpt,Impact,Remediation,Confidence,Discovered_Date
```

## Workflow

1. Identify email type from user command
2. Load template from `~/.hermes/templates/bug-bounty/`
3. Fill all `[PLACEHOLDER]` values from session findings
4. Generate CSV if batch mode
5. Output filled email ready to send

## Subject Line Format

```
[SECURITY REPORT] [SEVERITY] — [Vuln Type] in [Affected Endpoint] | [Program Name]
```

Example:
```
[SECURITY REPORT] HIGH — Stored XSS in /profile/bio allows Account Takeover | AcmeCorp Bug Bounty
```

## Key Rules

- Never paste actual credentials/secrets in email body — reference attachments
- Redact captured tokens to last 6 chars in chat history
- Attach all screenshots from /evidence/ folder
- Attach Burp Suite exports from /burp/ folder
- Always include responsible disclosure statement

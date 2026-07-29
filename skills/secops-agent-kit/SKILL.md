---
name: secops-agent-kit
description: Security Operations Agent Kit — 25+ security skills for AI coding agents covering AppSec (SAST/DAST), DevSecOps, threat modeling, incident response, offensive security, and compliance.
metadata:
  source: https://github.com/AgentSecOps/SecOpsAgentKit
  stars: 181
  version: 1.0
---

# SecOpsAgentKit — Security Operations Skills

Security operations toolkit for AI coding agents. 25+ skills to catch vulnerabilities, scan containers, detect secrets, enforce policies — shift-left security for the AI era.

## Skill Categories

### 🔒 Application Security (appsec)
| Skill | Tool | What it does |
|-------|------|-------------|
| api-mitmproxy | mitmproxy | Interactive HTTPS proxy for API security testing |
| api-spectral | Spectral | API spec linting & security validation (OpenAPI/AsyncAPI) |
| dast-ffuf | ffuf | Fast web fuzzer — directory enumeration & param fuzzing |
| dast-nuclei | Nuclei | Template-based vulnerability scanning (ProjectDiscovery) |
| dast-zap | OWASP ZAP | Dynamic application security testing |
| sast-bandit | Bandit | Python SAST with CWE & OWASP mappings |
| sast-semgrep | Semgrep | Multi-language static analysis |
| sca-blackduck | Black Duck | Software Composition Analysis |

### ⚙️ DevSecOps
| Skill | Tool | What it does |
|-------|------|-------------|
| container-grype | Grype | Container vuln scanning with CVSS/EPSS/KEV |
| container-hadolint | Hadolint | Dockerfile linting & best practices |
| iac-checkov | Checkov | IaC security scanning (750+ policies) |
| sca-trivy | Trivy | SCA + container vuln scanning |
| secrets-gitleaks | Gitleaks | Hardcoded secret detection in git repos |
| vuln-defectdojo | DefectDojo | Vulnerability management & findings aggregation |

### 📋 Secure SDLC
| Skill | Tool | What it does |
|-------|------|-------------|
| reviewdog | reviewdog | Automated code review for CI/CD |
| sast-horusec | Horusec | Multi-language SAST (18+ langs, 20+ tools) |
| sbom-syft | Syft | SBOM generation for container images/filesystems |

### 🏛️ Compliance
| Skill | Tool | What it does |
|-------|------|-------------|
| policy-opa | OPA | Policy-as-code enforcement (Open Policy Agent) |

### 🧠 Threat Modeling
| Skill | Tool | What it does |
|-------|------|-------------|
| pytm | pytm | Python-based threat modeling with STRIDE & DFD |

### 🚨 Incident Response
| Skill | Tool | What it does |
|-------|------|-------------|
| detection-sigma | Sigma | Universal SIEM detection rule creation |
| forensics-osquery | osquery | SQL-powered forensic investigation |
| ir-velociraptor | Velociraptor | Endpoint forensics & IR at scale |

### ⚔️ Offensive Security
| Skill | Tool | What it does |
|-------|------|-------------|
| pentest-metasploit | Metasploit | Exploit development & vuln validation |
| recon-nmap | Nmap | Network recon & port scanning |
| network-netcat | Netcat | TCP/UDP network utility |
| ot-security-assessment | Nmap+MSF | OT/ICS device discovery & assessment |
| analysis-tshark | tshark | Network protocol analysis & packet capture |
| webapp-sqlmap | SQLMap | Automated SQL injection detection |
| webapp-nikto | Nikto | Web server vulnerability scanning |
| crack-hashcat | Hashcat | Advanced password recovery |
| privesc-linpeas | LinPEAS | Linux privilege escalation enumeration |

## Frameworks Referenced
OWASP · CWE · MITRE ATT&CK · NIST · SOC2 · PCI-DSS · GDPR

## Install Individual Skills
```bash
# Claude Code plugin install
/plugin marketplace add https://github.com/AgentSecOps/SecOpsAgentKit.git

# Or skills.sh
npx skills add AgentSecOps/SecOpsAgentKit
```

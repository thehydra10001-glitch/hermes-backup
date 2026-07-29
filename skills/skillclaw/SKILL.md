---
name: skillclaw
description: SkillClaw — Collective Skill Evolution for AI Agents. A client proxy + evolve server that automatically deduplicates, improves, and evolves Hermes skills from real session data.
metadata:
  source: https://github.com/AMAP-ML/SkillClaw
  version: 1.0
---

# SkillClaw — Collective Skill Evolution

SkillClaw makes LLM agents progressively better by evolving reusable skills from real session data. It has two components:

1. **Client Proxy** — A local API proxy that intercepts agent requests, records session artifacts, and manages your local skill library.
2. **Evolve Server** — An optional service that reads session data from shared storage, evolves or creates skills, and writes them back.

## Quick Install

```bash
git clone https://github.com/AMAP-ML/SkillClaw.git && cd SkillClaw
bash scripts/install_skillclaw.sh
source .venv/bin/activate
skillclaw setup
skillclaw start --daemon
```

## Hermes Integration

1. Run `skillclaw setup` and choose `hermes` for CLI agent
2. SkillClaw rewrites `~/.hermes/config.yaml` to point Hermes at the local proxy
3. Hermes uses `~/.hermes/skills` as the local skill library

## Key Features

- **Auto-evolve** — Skills improve from every session, every interaction
- **Auto-deduplicate** — Same knowledge stored once
- **Multi-device** — Skills unify across Home, School, Work Hermes instances
- **Team sharing** — Multiple users feed the same evolution loop
- **OpenClaw, Codex, Claude Code** — Also supported natively

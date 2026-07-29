# Bulk Import Example — 16 Repos (2026-07-26)

Concrete example of a bulk import session. All 16 repos were probed, categorized, and installed in a single conversation.

## Category A — Direct Agent Skills (7)

Copied existing SKILL.md files directly (from root or skills/ subdirectory):

| Hermes Name | Source | SKILL.md Location | Size |
|---|---|---|---|
| humanizer | blader/humanizer | root | 29,632 B |
| detect-skill | resemble-ai/detect-skill | root (master branch) | 18,640 B |
| browser-harness | browser-use/browser-harness | root | 7,795 B |
| youtube | ZeroPointRepo/youtube-skills | skills/youtube-full/SKILL.md | 8,480 B |
| composio | composio-community/skills | skills/composio/SKILL.md | 2,184 B |
| make-interfaces-feel-better | jakubkrehel/make-interfaces-feel-better | skills/make-interfaces-feel-better/SKILL.md | 11,818 B |
| loopy | Forward-Future/loopy | skills/loopy/SKILL.md | 15,519 B |

## Category B — Multi-Skill Libraries (3)

Created wrapper/catalog SKILL.md (not copying all sub-skills):

| Hermes Name | Source | Sub-Skills |
|---|---|---|
| addyosmani-agent-skills | addyosmani/agent-skills | 24 skills (spec, plan, build, test, review, ship...) |
| mattpocock-skills | mattpocock/skills | 15+ skills (grill-me, tdd, code-review, wayfinder...) |
| anthropic-cybersecurity-skills | mukul975/Anthropic-Cybersecurity-Skills | 817 skills across 29 security domains |

## Category C — Software Tools (6)

Created custom SKILL.md with install commands and usage:

| Hermes Name | Source | Type | Install Command |
|---|---|---|---|
| skillclaw | AMAP-ML/SkillClaw | Python daemon | git clone + bash install_skillclaw.sh |
| defuddle | kepano/defuddle | npm package | npm install -g defuddle |
| codebase-memory-mcp | DeusData/codebase-memory-mcp | Binary MCP server | curl ... install.sh \| bash |
| agent-reach | Panniantong/Agent-Reach | Python CLI + MCP | pip install agent-reach |
| minions | agent37-platform/minions | Node.js server | npx minionsai |
| oh-my-hermes | witt3rd/oh-my-hermes | Hermes plugins | git clone + configure |

## Probing Technique Used

For each repo, the following probes were run:

```bash
# 1. Get repo description (GitHub API)
curl -sL "https://api.github.com/repos/<owner>/<repo>" | python3 -c "... print(d['description'], d.get('topics',[]))"

# 2. Fetch README
curl -sL https://raw.githubusercontent.com/<owner>/<repo>/main/README.md | head -200

# 3. Check for SKILL.md at root
curl -sLo /dev/null -w "%{http_code}" https://raw.githubusercontent.com/<owner>/<repo>/main/SKILL.md

# 4. Probe skills/ subdirectory structure
curl -sL "https://api.github.com/repos/<owner>/<repo>/contents/skills" | python3 -c "..."

# 5. Branch fallback
curl -sLo /dev/null -w "%{http_code}" https://raw.githubusercontent.com/<owner>/<repo>/master/SKILL.md

# 6. List root contents for unknown structures
curl -sL "https://api.github.com/repos/<owner>/<repo>/contents" | python3 -c "..."
```

## Key Discoveries During This Session

1. **resemble-ai/detect-skill** — SKILL.md lives on `master` branch, not `main` (old repo). Always branch-fallback.
2. **mattpocock/skills** — Skills organized under `skills/engineering/` and `skills/productivity/`. Has `/setup-matt-pocock-skills` as a setup command.
3. **witt3rd/oh-my-hermes** — No standard SKILL.md. Uses `.omh/` directory with `plugins/`, `plans/`, `research/`. Hermes-specific format.
4. **browser-use/browser-harness** — Both a SKILL.md AND a software tool with `install.md`. Category hybrid — copy SKILL.md, note the install path separately.
5. **mukul975/Anthropic-Cybersecurity-Skills** — 817 skills. No root SKILL.md or AGENTS.md. Wrapper only.
6. **Forward-Future/loopy** — `skills/loopy/` and `skills/loop-library/` directories. Choose the primary (loopy) for the Hermes skill name.

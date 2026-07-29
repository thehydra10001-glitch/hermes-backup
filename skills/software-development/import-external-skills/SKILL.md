---
name: import-external-skills
description: "Import third-party agent skill repos into Hermes — probe repo structure, categorize by type (direct SKILL.md / multi-skill library / software tool), install as Hermes skills under ~/.hermes/skills/<name>/."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, skills, import, installation, workflow, github]
    related_skills: [hermes-agent-skill-authoring, plan]
---

# Importing External Skills into Hermes

Importing agent skills from GitHub repos into `~/.hermes/skills/<name>/SKILL.md`. This is a sister activity to **authoring** new skills (covered by `hermes-agent-skill-authoring`) — it focuses on converting pre-existing skills and tools into Hermes-usable format.

## When to Use

- User drops a list of GitHub URLs and says "install these as skills"
- User asks you to clone or set up a specific agent-skill repo from GitHub
- User wants to make an npm/pip tool (defuddle, codebase-memory-mcp, etc.) available as a Hermes skill
- User has a skills.sh-compatible repo they want available in Hermes' skill loader

## Three-Phase Workflow

### Phase 1: Probe the Repo

Fetch the README and inspect the repo structure to understand what you're dealing with:

```bash
# 1. Fetch README (raw.githubusercontent.com, not the GitHub web page)
curl -sL https://raw.githubusercontent.com/<owner>/<repo>/main/README.md | head -150

# 2. Check for SKILL.md at root (direct agent skill)
curl -sLo /dev/null -w "%{http_code}" https://raw.githubusercontent.com/<owner>/<repo>/main/SKILL.md

# 3. Check for skills/ subdirectory (multi-skill library)
# GitHub API returns JSON with type (file/dir) for each item
curl -sL "https://api.github.com/repos/<owner>/<repo>/contents/skills" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if isinstance(data, list):
        for f in data:
            print(f['name'], f['type'])
    else:
        print('no skills/ dir')
except: pass
"

# 4. Check for AGENTS.md (alternate skill format)
curl -sLo /dev/null -w "%{http_code}" https://raw.githubusercontent.com/<owner>/<repo>/main/AGENTS.md

# 5. Branch fallback — some repos use master instead of main
curl -sLo /dev/null -w "%{http_code}" https://raw.githubusercontent.com/<owner>/<repo>/master/SKILL.md
```

### Phase 2: Categorize

Determine which of three categories the repo falls into, based on what Phase 1 reveals:

| Category | Hallmarks | Action |
|----------|-----------|--------|
| **A — Direct Agent Skill** | SKILL.md at root or in skills/<name>/ | Copy SKILL.md directly |
| **B — Multi-Skill Library** | skills/ dir with 5+ sub-skills, no single SKILL.md | Create a wrapper/catalog SKILL.md |
| **C — Software Tool** | npm package, pip package, binary, MCP server, no SKILL.md | Create a custom SKILL.md with install + usage |

**Edge cases to watch for:**
- `main` vs `master` branch (some old repos use master)
- SKILL.md exists but uses relative `references/` links — these break if you only copy SKILL.md
- Repo has both a SKILL.md AND is a software tool (e.g. browser-harness) — copy SKILL.md but also note install path
- Repo is Hermes-specific (e.g. oh-my-hermes with `.omh/` dir) — create a custom wrapper

### Phase 3: Install

#### Category A — Direct Agent Skill

```bash
mkdir -p ~/.hermes/skills/<name>
curl -sL https://raw.githubusercontent.com/<owner>/<repo>/main/SKILL.md > ~/.hermes/skills/<name>/SKILL.md
```

For skills in a subdirectory (e.g. `skills/youtube-full/SKILL.md`):
```bash
curl -sL https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<subdir>/SKILL.md > ~/.hermes/skills/<name>/SKILL.md
```

For repos with additional reference files, copy the full directory structure when feasible (use `write_file` or `terminal cp` for each supporting file).

#### Category B — Multi-Skill Library

Write a **wrapper SKILL.md** that serves as a catalog rather than mirroring all sub-skills:

```
~/.hermes/skills/<name>/SKILL.md
```

The wrapper should include:
- **Overview** — what the library covers and its scope
- **Bulleted list** of all sub-skills with one-line description of each
- **Install command** (`npx skills add <owner>/<repo>`) for native agents
- **Category table** grouping related sub-skills (e.g. engineering vs productivity)
- **Note** that individual sub-skills aren't pre-loaded as Hermes skills — the wrapper teaches the agent what exists so it can delegate to the full install

Example excerpt:
```markdown
## Sub-Skills (24 total)

### Engineering Lifecycle
- **spec-driven-development** — Define scope before writing code
- **test-driven-development** — Red-green-refactor cycle
- **code-review-and-quality** — Five-axis review before merge
- **incremental-implementation** — One vertical slice at a time
```

#### Category C — Software Tool

Write a **custom SKILL.md** that teaches the agent what the tool is and how to use it:

```markdown
---
name: <name>
description: "One-line: what the tool does for agents"
metadata:
  source: https://github.com/<owner>/<repo>
---

# <Tool Name>

Brief overview (2-3 sentences explaining what the tool does and why an agent should know about it).

## Quick Install
```bash
# npm
npm install -g <package>

# pip
pip install <package>

# Binary
curl -fsSL https://install.sh | bash
```

## CLI Usage
Key commands the agent would invoke, with examples:
```bash
<command> --option <arg>
```

## Key Features
- Point-form list of relevant capabilities

## Integration
How the agent can use this tool — as a skill reference, a terminal tool, an MCP server, etc.
```

## Pitfalls

1. **`main` vs `master` branch.** Always check both. `curl -sLo /dev/null -w "%{http_code}" https://raw.githubusercontent.com/<owner>/<repo>/master/SKILL.md` when `main` returns 404.

2. **Relative path dependencies.** Many SKILL.md files link to `references/*.md`, assets, or scripts via relative paths. These break if you only copy SKILL.md. Options:
   - Copy the entire repo directory structure
   - Inline key referenced content into SKILL.md
   - Add a note in SKILL.md that references exist upstream

3. **Massive libraries (100+ skills).** e.g. Anthropic-Cybersecurity-Skills (817 skills). Do NOT create 817 individual Hermes skills. A single wrapper/catalog SKILL.md with categorized tables is the right approach — compact, scannable, and keeps `~/.hermes/skills/` manageable.

4. **Hermes-specific repos** like `oh-my-hermes` with `.omh/` directories. These are not standard SKILL.md repos — they use Hermes plugin/plan/research directories. Create a wrapper SKILL.md that describes the structure and points the agent to the right subdirectories.

5. **NPM tools used as skills** (e.g. defuddle). `npx defuddle parse` works via terminal but isn't a native skill. The custom SKILL.md approach is best — it registers the tool's existence so the agent knows to call it, without trying to make it a real SKILL.md.

6. **GitHub API rate limits.** Unauthenticated requests to `api.github.com` are limited to 60/hr. If probing many repos, batch the checks efficiently (one curl per repo) rather than separate calls for each path check.

7. **Unicode in fpdf2/Helvetica.** If creating skill content that mentions fpdf2 reports, remember Helvetica only supports Latin-1. Use ASCII fallbacks or note the TTF font workaround.

## Verification Checklist

- [ ] `~/.hermes/skills/<name>/SKILL.md` exists and is non-empty
- [ ] SKILL.md has valid frontmatter (`name`, `description`, etc.)
- [ ] For Category A: SKILL.md is the original or a properly attributed copy
- [ ] For Category B: wrapper lists all sub-skills and includes `npx skills add` command
- [ ] For Category C: custom SKILL.md has accurate install commands and usage examples
- [ ] No PR numbers, session IDs, or one-off names in skill names
- [ ] Skill is listed: `ls ~/.hermes/skills/<name>/`
- [ ] `skill_view(name='<name>')` returns the content (note: may need new session)

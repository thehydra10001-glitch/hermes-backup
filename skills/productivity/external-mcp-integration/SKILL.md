---
name: external-mcp-integration
description: "Connect third-party MCP servers to Hermes — SSE transport servers (Zapier, custom endpoints), app authentication flow, and tool discovery. Covers adding, testing, and using external MCP services in Hermes sessions."
version: 1.2
author: hermes-agent
created_by: agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mcp, integration, zapier, sse, external-services, automation]
    category: productivity
---

# External MCP Integration

Connect third-party MCP (Model Context Protocol) servers to Hermes. This covers SSE-transport servers (like Zapier MCP), which differ from the more common stdio-based local MCP servers.

## Transport Types

| Transport | Usage | Example |
|-----------|-------|---------|
| **stdio** | Local processes spawned by Hermes | Local file-server MCP, database MCP |
| **SSE** (Server-Sent Events) | Remote cloud-hosted endpoints | Zapier MCP, custom cloud MCPs |

## Adding an SSE MCP Server

```bash
hermes mcp add <name> --url "https://example.com/mcp/connect?token=YOUR_TOKEN"
```

SSE endpoints often prompt interactively:
- **Authentication** → Usually **n** (token is in the URL)
- **Enable all tools?** → **Y** to use everything

For non-interactive setup (scripts, automation):
```bash
echo -e "\n\nY\n" | hermes mcp add <name> --url "https://example.com/mcp/connect?token=YOUR_TOKEN"
```

## Lifecycle Commands

```bash
hermes mcp add NAME --url URL    # Add an SSE MCP server
hermes mcp list                   # List configured servers
hermes mcp test NAME              # Test connection
hermes mcp remove NAME            # Remove a server
hermes mcp configure NAME         # Toggle which tools are enabled
```

In-session: `/reload-mcp` to refresh all MCP connections after adding/removing.

## MCP Authentication Patterns

Remote MCP servers use one of three auth patterns. Know which one you're dealing with before connecting:

| Pattern | Works With | How to connect | Example |
|---------|-----------|----------------|---------|
| **URL-embedded token** | `hermes mcp add --url` | Token is in the URL itself; answer **n** (no) when asked "Does this server require authentication?" | Zapier MCP (`?token=...`) |
| **Bearer token / API key** | `hermes mcp add --url` + headers | Add `Authorization: Bearer <key>` header, or paste token when prompted (answer **Y**) | GitHub MCP, custom APIs |
| **OAuth 2.0 (CIMD / PKCE)** | `hermes mcp add --url` (limited) | Requires browser-based OAuth flow. Clients like Claude Desktop, Cursor handle this natively. Hermes `mcp add` does NOT have an interactive browser-OAuth flow — use Composio as a gateway (handles OAuth for you) or get a token manually via Canva Developer Portal | Canva MCP (`https://mcp.canva.com/mcp`) |

For OAuth-based MCP servers, **Composio** is the recommended bridge — it handles OAuth, token refresh, and rate limits:

```bash
# Install Composio CLI
curl -fsSL https://composio.dev/install | bash

# In a Hermes session: "Connect me to Composio" → browser auth
# Then: "Connect me to Canva" → browser auth for Canva OAuth
# Free tier: 20,000 tool calls/month, no credit card
```

## Zapier MCP (Example: 15 Tools)

Zapier MCP bridges 9,000+ apps (Gmail, Google Sheets, Slack, GitHub, Notion, etc.) into Hermes.

### Connection
**In Hermes (SSE transport):**
```bash
hermes mcp add zapier --url "https://mcp.zapier.com/api/v1/connect?token=YOUR_TOKEN"
```

**In Claude Code (HTTP transport):**
```bash
claude mcp add --transport http "Zapier-MCP" https://mcp.zapier.com/api/v1/connect
```
Then restart Claude and prompt: `Zapier-MCP onboard me` to auto-configure.

Accepts `text/event-stream` SSE protocol. Free Zapier tier works.

### First-Time Setup
1. **Call `get_configuration_url`** inside a Hermes session (this is an MCP tool, not a CLI command):
   ```
   In a Hermes session, ask: "Call get_configuration_url from zapier MCP"
   ```
2. Open the returned URL in browser → log into app accounts (Gmail, Slack, GitHub, etc.)
3. Return to Hermes — the connection persists between sessions

### Usage Flow
```
list_enabled_zapier_actions    → what's already connected
discover_zapier_actions(...)   → find actions across 9K+ apps
enable_zapier_action(...)      → connect an app
execute_zapier_read_action(...)  → read/search data
execute_zapier_write_action(...) → create/write data
```

### Concrete Example: Send Email via Gmail

```bash
# 1. Get the config URL (inside a Hermes session)
# -> Opens browser to connect Gmail account

# 2. Discover Gmail actions
discover_zapier_actions(query="gmail send email")

# 3. Enable Gmail
enable_zapier_action(app_id="gmail")

# 4. List enabled to verify
list_enabled_zapier_actions

# 5. Send email (natural language in session)
"Send an email to amansangani5@gmail.com with subject 'Test' and body 'Hello from Hermes via Zapier MCP'"
```

### All 15 Zapier MCP Tools

| Tool | Purpose |
|------|---------|
| `discover_zapier_actions` | Search 9,000+ apps for connectable actions |
| `enable_zapier_action` | Enable an app's actions on this MCP server |
| `disable_zapier_action` | Remove a connected app |
| `list_enabled_zapier_actions` | Call first — see active connections |
| `execute_zapier_read_action` | Read/search data from connected apps |
| `execute_zapier_write_action` | Create/write data in connected apps |
| `auto_provision_mcp` | Auto-setup from existing Zapier usage |
| `list_zapier_skills` / `get_zapier_skill` | Manage saved workflow definitions |
| `create_zapier_skill` / `delete_zapier_skill` | Save/remove reusable workflows |
| `update_zapier_skill` | Edit a saved workflow definition |
| `write_code_action` | Custom code action for an app |
| `send_feedback` | Report experience to Zapier |
| `get_configuration_url` | URL to connect app accounts |

### Limits
- Rate-limited to ~3 req/s
- Free tier has action/task caps — check at the configuration URL

## Canva MCP (Free Design Generation)

Canva MCP connects AI assistants to Canva's design capabilities — create designs, edit, search library, export to multiple formats (PNG, PDF, PPTX, MP4), add comments, upload assets.

### Free Tier Access (3 paths)

| Path | Auth Needed | Best For | Setup |
|------|-------------|----------|-------|
| **Via Composio gateway** | OAuth (handled for you) | Hermes users — easiest path | `curl -fsSL https://composio.dev/install \| bash` → in session: "Connect me to Canva" |
| **Direct URL** (`https://mcp.canva.com/mcp`) | OAuth 2.0 (CIMD) — needs Bearer token | Clients with native OAuth support (Claude Desktop, Cursor) | Add as remote MCP server, auth via browser |
| **Stdio via npm** (`npx -y @canva/cli@latest mcp`) | Canva Dev account | Canva app developers building integrations | `hermes mcp add canva --command "npx -y @canva/cli@latest mcp"` |

**Composio** is the recommended path for Hermes — free tier gives 20,000 tool calls/month with managed OAuth. No credit card needed.

### What's Available (Free Plan)

The Canva MCP exposes tools for:

- **Design creation** — generate designs from text descriptions using templates or from scratch
- **Design editing** — modify existing designs via natural language
- **Design discovery** — search and retrieve designs, pages, and folders
- **Design export** — export in multiple formats (PDF, PNG, JPG, PPTX, MP4)
- **Design resizing** — resize designs for different channels
- **Comments** — add feedback loops to design workflows
- **Asset management** — upload and manage brand assets

Free plan works for most operations. Some Pro features (brand kits, premium templates, background removal) are gated.

### Setup via Composio (Hermes-friendly)

```bash
# 1. Install Composio
curl -fsSL https://composio.dev/install | bash

# 2. In a Hermes session:
"Connect me to Composio"
→ Opens browser for Composio OAuth

# 3. Then:
"Connect me to Canva"
→ Opens browser for Canva OAuth

# 4. Start designing:
"Create a social media post in Canva with title 'Hello from Hermes'"
```

### Direct URL (if you have a token)

```bash
hermes mcp add canva --url "https://mcp.canva.com/mcp"
# Say 'y' to auth → paste Bearer token when prompted
```

To get a Canva Bearer token: create an app at canva.com/developers → get Client ID + Secret → exchange via OAuth 2.0 for an access token.

### Built-in in Claude Desktop

Canva MCP is a built-in connector under Claude Desktop Settings → Developer → Connectors. No config file needed — just click "Connect" and OAuth in the browser.

## Testing MCP Servers

```bash
# Quick connectivity test
hermes mcp test <name>

# In-session: after adding, reload
/reload-mcp

# Verify tools are available — the server's tools appear
# as native Hermes tools after a successful add
```

## Pitfalls

- **SSE endpoints stay open** as long-lived streams — this is normal, not a timeout
- **Token in URL** is considered a credential — don't share the URL, don't log it
- **`/reload-mcp`** is required in-session after adding a new server (does NOT auto-detect)
- **Interactive prompts** on `hermes mcp add` can block automation — use the echo-pipe workaround:
  ```bash
  echo -e "\\n\\nY\\n" | hermes mcp add zapier --url "https://..."
  ```
  The prompts are: (1) "Does this server require authentication?" → press Enter (no), (2) "Enable all N tools?" → type Y + Enter
- **SSE headers** — Zapier requires `Accept: text/event-stream`. Sending `Accept: application/json` returns a `-32000` error: "Not Acceptable"
- **MCP tools are session-only** — they can't be called from terminal directly; they require a Hermes chat session to dispatch
- **Configuration URL is ephemeral** — once the browser window connects, the URL doesn't need to be re-fetched; the config persists

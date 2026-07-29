---
name: hermes-extending
description: "Add features to Hermes Agent — slash commands, tools, gateway handlers, CLI commands. Covers the 4-file pattern for slash commands, tool registration, and the codebase layout."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, development, extension, slash-commands, tools, gateway]
    homepage: https://github.com/NousResearch/hermes-agent
---

# Extending Hermes Agent

How to add features to the Hermes Agent codebase: slash commands, tools, gateway handlers, CLI commands. Source lives at `~/.hermes/hermes-agent/`.

## Source Layout

```
hermes-agent/
├── hermes_cli/
│   ├── commands.py       # CommandDef registry (single source of truth for all slash commands)
│   ├── config.py         # DEFAULT_CONFIG, env var definitions
│   └── main.py           # CLI entry point, argparse
├── cli.py                # Interactive CLI (HermesCLI class) — process_command() dispatches slash commands
├── gateway/
│   ├── run.py            # GatewayRunner — main gateway dispatch loop, command routing
│   └── slash_commands.py # Gateway slash-command handlers (mixin inherited by GatewayRunner)
├── tools/                # One file per tool + registry.py
│   └── registry.py       # Central tool registry (register() calls)
├── toolsets.py           # Toolset definitions (_HERMES_CORE_TOOLS, TOOLSETS dict)
├── agent/                # Prompt builder, context compression, memory, model routing
└── tests/                # pytest suite
```

## Adding a Slash Command (4-File Pattern)

Every slash command touches **exactly 4 files**. All consumers (help text, autocomplete, Telegram menu, Slack mapping, `/help`) derive from the central registry.

### Step 1: Register — `hermes_cli/commands.py`

Add a `CommandDef` to `COMMAND_REGISTRY`:

```python
CommandDef(
    "resources",                           # name (without /)
    "Show system resources",               # description
    "Info",                                # category: "Session", "Configuration", "Tools & Skills", "Info", "Exit"
    aliases=("res",),                      # optional aliases
    args_hint="[detail]",                  # optional argument placeholder
    subcommands=("cpu", "ram"),            # optional tab-completable subcommands
    cli_only=True,                         # optional: only available in CLI
    gateway_only=True,                     # optional: only available in gateway
    gateway_config_gate="some.config.key", # optional: config dotpath that gates availability
)
```

**Placement:** group by category section. Info commands go near `/platforms`, `/version`.

**ACTIVE_SESSION_BYPASS_COMMANDS:** If the command should work even while an agent is running (like `/status`, `/stop`, `/help`), add its name to the `ACTIVE_SESSION_BYPASS_COMMANDS` frozenset in the same file. Commands NOT in this set get the "Agent is running — can't run mid-turn" catch-all.

### Step 2: Gateway Handler — `gateway/slash_commands.py`

Add an `async def _handle_<name>_command(self, event: MessageEvent) -> str` method to the `SlashCommandMixin` class. This is a mixin that `GatewayRunner` inherits.

Key patterns:
- `event.get_command_args()` — raw arguments after the command name
- `event.source` — platform/user/chat info
- Return a plain string (the reply text)
- Use `t()` for i18n strings, but plain strings are fine for new commands

Place new handlers after related existing handlers (e.g., after `_handle_status_command` for info commands).

### Step 3: Dispatch — `gateway/run.py`

Add a dispatch entry in the `_handle_message` method's command routing section:

```python
if canonical == "resources":
    return await self._handle_resources_command(event)
```

Place it near similar commands. The `canonical` variable is the resolved command name (no slash).

### Step 4: CLI Handler — `cli.py`

Add two things:
1. A dispatch entry in `process_command()`:
   ```python
   elif canonical == "resources":
       self._show_resources()
   ```
2. The handler method on the `HermesCLI` class:
   ```python
   def _show_resources(self):
       """Show system resource usage."""
       # ... implementation ...
       self._console_print("\n".join(lines), highlight=False, markup=False)
   ```

## Adding a Tool (2-File Pattern)

### File 1: `tools/your_tool.py`

```python
import json, os
from tools.registry import registry

def check_requirements() -> bool:
    return True  # or check for required env vars / binaries

def your_tool(param: str) -> str:
    return json.dumps({"success": True, "data": "..."})

registry.register(
    name="your_tool",
    toolset="core",            # which toolset this belongs to
    schema={...},              # OpenAI function-calling schema
    handler=lambda args, **kw: your_tool(param=args.get("param", "")),
    check_fn=check_requirements,
    requires_env=["YOUR_API_KEY"],  # optional
)
```

### File 2: `toolsets.py`

Add the tool name to the appropriate toolset in `TOOLSETS` dict or `_HERMES_CORE_TOOLS`.

## Concrete Example

See `references/slash-command-example-resources.md` for a complete working implementation of the 4-file pattern (the `/resources` command showing CPU, RAM, storage, battery).

## Pitfalls

- **`/personality` is built-in.** Don't create a new slash command for personalities. The `/personality` command already exists and reads from `config.yaml → agent.personalities`. Just add a new entry there with `system_prompt`, `description`, `tone`, and `style` fields. Takes effect on the next message — no restart needed.
- **Cron drift-protection.** When a cron job is created with `no_agent=False` (LLM-driven), the system snapshots the model/provider at creation time. If the global config later changes, the job fails with "Skipped to prevent unintended spend: global inference config drifted". Fix: use `no_agent=True` for script-only jobs, or recreate the job to reset the baseline.
- **Prompt caching is sacred.** Never change the system prompt, tool schemas, or context mid-conversation. New commands that alter agent behavior must take effect on `/reset`, not mid-turn.
- **Message role alternation.** Never produce two assistant or two user messages in a row. Commands that fall through to agent processing (like `/learn`) rewrite `event.text` and let the agent respond — preserving alternation.
- **Gateway handlers are async.** Use `async def` and `await` for adapter calls.
- **CLI handlers are sync.** Use `self._console_print()` for output, not `print()`.
- **`psutil` is a dependency** but lazy-import it inside handlers to avoid import-time side effects.
- **Battery percentage** from `psutil.sensors_battery()` returns a float — use `round()` for clean display.

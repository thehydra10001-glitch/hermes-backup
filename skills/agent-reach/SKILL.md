---
name: agent-reach
description: Give your AI agent internet capabilities — browse YouTube, Twitter, Reddit, Bilibili, GitHub, search the web, read any page. One command to install all channels.
metadata:
  source: https://github.com/Panniantong/Agent-Reach
  version: 1.0
---

# Agent Reach — Internet Capabilities for AI Agents

Give your AI agent one-click internet access — read web pages, YouTube transcripts, Twitter, Reddit, Bilibili, GitHub, RSS, web search, and more.

## Quick Install

Copy this to your agent:
```
帮我安装 Agent Reach：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
```

## Supported Platforms

| Platform | Zero Config | After Config |
|----------|------------|-------------|
| Web pages | Jina Reader | — |
| YouTube | Subtitles + Search | — |
| RSS | Any RSS/Atom feed | — |
| Web Search | — | Exa via MCP (free) |
| GitHub | Public repos + Search | Private, Issues, PRs |
| Twitter/X | Read single tweet | Search, timeline |
| Bilibili | Search + video details | Subtitles |
| Reddit | — | Search + read posts |
| Xiaohongshu | — | Search + read |

## Features
- Zero-effort install — one paste, agent does the rest
- Self-diagnosis: `agent-reach doctor` checks every channel
- Multi-backend routing per platform (auto-switch on failure)
- Privacy-first: cookies stay local, code is open source

# Hermes Agent Backup

Automated backup of Hermes AI agent configuration, skills, MCP servers, and custom scripts.

## Structure

- skills/ — All installed skills by category
- mcp-servers/ — MCP server configs and source
- config/ — Hermes config.yaml, .env template
- scripts/ — Custom helper scripts
- plugins/ — Custom Hermes plugins
- cron/ — Cron job definitions

## Restore

1. Clone: `git clone https://github.com/thehydra10001-glitch/hermes-backup.git`
2. Symlink skills: `ln -sf ~/hermes-backup/skills/* ~/.hermes/skills/`
3. Copy config: `cp ~/hermes-backup/config/config.yaml ~/.hermes/config.yaml`

Backup created: 2026-07-29

## How to Backup

- Manual: ./backup.sh
- Cron auto: Add `0 6 * * 0 cd ~/hermes-backup && ./backup.sh` for weekly

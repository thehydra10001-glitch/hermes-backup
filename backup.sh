#!/bin/bash
# Hermes Agent Backup Script
# Run: bash backup.sh
# Schedule: bash -c "cd ~/hermes-backup && git pull --rebase && bash backup.sh && git push"

set -e

BACKUP_DIR="$(cd "$(dirname "$0")" && pwd)"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo "=== Hermes Backup @ $TIMESTAMP ==="

# 1. Skills
echo "[1/5] Backing up skills..."
rsync -a --delete "$HERMES_HOME/skills/" "$BACKUP_DIR/skills/" 2>/dev/null || \
  cp -ru "$HERMES_HOME/skills/"* "$BACKUP_DIR/skills/" 2>/dev/null || true
echo "  Skills: $(find "$BACKUP_DIR/skills" -name 'SKILL.md' | wc -l)"

# 2. Config (redact secrets)
echo "[2/5] Backing up config..."
cp "$HERMES_HOME/config.yaml" "$BACKUP_DIR/config/config.yaml"
# Create redacted env template
if [ -f "$HERMES_HOME/.env" ]; then
  grep -v "^#" "$HERMES_HOME/.env" 2>/dev/null | sed 's/=.*/=/' > "$BACKUP_DIR/config/.env.template"
  echo "  .env template created (secrets redacted)"
fi

# 3. MCP Servers
echo "[3/5] Backing up MCP servers..."
for mcp_src in ~/MetasploitMCP ~/GhidraMCP; do
  dir=$(basename "$mcp_src")
  if [ -d "$mcp_src" ]; then
    cp -r "$mcp_src" "$BACKUP_DIR/mcp-servers/$dir" 2>/dev/null || true
    echo "  ✓ $dir"
  fi
done

# 4. Cron jobs
echo "[4/5] Backing up cron jobs..."
crontab -l > "$BACKUP_DIR/cron/crontab.txt" 2>/dev/null || echo "# No crontab" > "$BACKUP_DIR/cron/crontab.txt"
echo "  Crontab saved"

# 5. README timestamp
echo "[5/5] Updating README..."
sed -i "s/Backup created: .*/Backup created: $(date -u +%Y-%m-%d)/" "$BACKUP_DIR/README.md" 2>/dev/null || true

# Git
cd "$BACKUP_DIR"
if [ -z "$(git status --porcelain)" ]; then
  echo "✦ No changes to commit"
else
  git add -A
  git commit -m "backup: $TIMESTAMP"
  git push origin main 2>&1 || echo "  ⚠ Push failed — check remote"
  echo "✦ Backup pushed to GitHub"
fi

echo "=== Backup Complete ==="

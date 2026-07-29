---
name: scheduled-content
description: "Set up recurring content delivery via cron jobs - daily quotes, digests, reminders, reports. Pattern: Python generator script + Hermes cronjob tool."
tags: [cron, scheduled, daily, content, delivery, automation, recurring]
triggers:
  - daily
  - every day
  - schedule
  - cron
  - recurring
  - send me at
  - remind me
  - daily quote
  - daily shloka
  - daily digest
---

# Scheduled Content Delivery

Set up recurring content delivery using a **Python generator script** + **Hermes cronjob tool**. This covers daily quotes, digests, reminders, reports, or any date-indexed content.

## Workflow

### 1. Create the Content Generator Script

Place in `~/.hermes/scripts/<name>.py`. The script must:

- **Print the final message to stdout** (cronjob tool delivers this)
- **Be self-contained** - no external dependencies beyond stdlib
- **Never repeat** - use date-based indexing into a curated list
- **Optionally save files** - HTML status images, CSVs, etc.

```python
#!/usr/bin/env python3
"""Template for daily content generation."""
import datetime
import os

CONTENT_LIST = [
    # Each item is a dict with all fields needed for one day
    {"title": "...", "body": "...", "translation": "..."},
    # ... enough items to cover rotation without repeats
]

def get_content_for_date(date=None):
    if date is None:
        date = datetime.date.today()
    index = date.timetuple().tm_yday % len(CONTENT_LIST)
    return CONTENT_LIST[index]

if __name__ == "__main__":
    today = datetime.date.today()
    item = get_content_for_date(today)
    # Print the formatted message - this is what gets delivered
    print(f"📅 {today.strftime('%d %B %Y')}\n\n{item['title']}\n\n{item['body']}")
```

### 2. Test the Script

```bash
python3 ~/.hermes/scripts/<name>.py
```

Verify output looks correct. Fix formatting before scheduling.

### 3. Schedule via Cronjob Tool

```python
cronjob(
    action="create",
    name="Daily <Content Type>",
    schedule="0 7 * * *",          # cron expression
    script="<name>.py",             # relative path under ~/.hermes/scripts/
    prompt="Run the script and send its output to the user."
)
```

**Schedule format reference:**
| Schedule | Meaning |
|----------|---------|
| `0 7 * * *` | Daily at 7:00 AM |
| `0 9 * * 1-5` | Weekdays at 9:00 AM |
| `0 * * * *` | Every hour |
| `30 8 * * 1` | Mondays at 8:30 AM |

### 4. Manage Existing Jobs

```python
cronjob(action="list")              # See all jobs with IDs
cronjob(action="pause", job_id="x") # Temporarily stop
cronjob(action="resume", job_id="x") # Resume
cronjob(action="remove", job_id="x") # Delete permanently
cronjob(action="run", job_id="x")    # Trigger immediately (test)
```

## Multi-Target Delivery

By default, cron jobs deliver to the chat that created them (`origin`). To send to **multiple Telegram chats**, set the `deliver` field:

```python
cronjob(
    action="update",
    job_id="<job_id>",
    deliver="origin,telegram:5784206319"  # origin + specific chat
)
```

**Delivery format reference:**
| Value | Meaning |
|-------|---------|
| `origin` (or omit) | The chat that created the job |
| `telegram:<chat_id>` | Specific Telegram user/group |
| `telegram:<chat_id>:<thread_id>` | Specific Telegram topic/thread |
| `discord:#channel` | Discord channel |
| `all` | Every connected home channel |
| `origin,telegram:123` | Fan out to multiple targets |

**Finding Telegram chat IDs:** Ask the user to forward a message to `@userinfobot` or `@getidsbot` on Telegram. For groups, add `@raw_data_bot` and forward a message.

**Sending messages outside cron** (from scripts or ad-hoc):
```bash
hermes send --to telegram:5784206319 "Hello from the bot!"
```
⚠️ Do NOT use raw `curl` to the Telegram API — you won't have the bot token readily available. Always use `hermes send`.

## Pitfalls

- **Cron drift-protection** — When the global inference config (provider/model) changes, jobs with `no_agent=False` (LLM-driven) get SKIPPED with: "Skipped to prevent unintended spend: global inference config drifted since this job was created". **Fix:** For script-only jobs that don't need AI reasoning, use `no_agent=True` with `script=` parameter. This bypasses drift-protection entirely since no LLM is used. Example: `cronjob(action="create", no_agent=True, script="daily_gita.py", ...)`. The `prompt` field is ignored when `no_agent=True`.
- **Script path must be relative** - `daily_gita.py`, not `~/.hermes/scripts/daily_gita.py`. The tool resolves it automatically.
- **Script must print to stdout** - the cronjob tool captures stdout and delivers it. Use `print()`, not file writes.
- **No interactive input** - scripts run unattended. No `input()` calls.
- **List rotation math** - use `date.timetuple().tm_yday % len(list)` for annual rotation. For weekly rotation, use `date.weekday() % len(list)`.
- **Dependencies** - scripts run in the active venv. Only use stdlib or pre-installed packages.
- **Timezone** - cron schedule uses the system timezone. Verify with `date` command.

## Example: Daily Gita Shloka

```python
#!/usr/bin/env python3
import datetime, os

SHLOKAS = [
    {"chapter": 2, "verse": 47, "sanskrit": "...", "gujarati": "...", "english": "..."},
    # ... 20+ shlokas for rotation
]

def get_shloka(date=None):
    if date is None:
        date = datetime.date.today()
    return SHLOKAS[date.timetuple().tm_yday % len(SHLOKAS)]

if __name__ == "__main__":
    shloka = get_shloka()
    print(f"🕉 *Bhagavad Gita {shloka['chapter']}.{shloka['verse']}*\n\n"
          f"*Sanskrit:* {shloka['sanskrit']}\n\n"
          f"*Gujarati:* {shloka['gujarati']}\n\n"
          f"*English:* {shloka['english']}")
```

## Example: Daily Motivation Quote

```python
#!/usr/bin/env python3
import datetime, random

QUOTES = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
    # ... add more
]

if __name__ == "__main__":
    today = datetime.date.today()
    idx = today.timetuple().tm_yday % len(QUOTES)
    quote, author = QUOTES[idx]
    print(f"💪 *Daily Motivation*\n\n_{quote}_\n\n— {author}")
```

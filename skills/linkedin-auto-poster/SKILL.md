---
name: linkedin-auto-poster
description: Automated LinkedIn posting using free tools — RSS feeds for news, local AI templates for post generation, Pollinations.ai for images. No API keys required.
category: social-media
---

# LinkedIn Auto-Poster

## Overview
Automated LinkedIn posting system that fetches cyber security news, generates AI-powered posts using local templates, creates images, and prepares content for manual posting. 100% free — no API keys needed.

## Architecture

```
RSS Feeds (TheHackerNews, SecurityWeek, KrebsOnSecurity, BleepingComputer)
    ↓
NewsFetcher - Parse and deduplicate articles
    ↓
AIPostGenerator - Template-based post creation (no external AI API)
    ↓
ImageGenerator - Pollinations.ai (free, no API key)
    ↓
LinkedInPoster - Save to file + clipboard
    ↓
PostLogger - JSON log for history
```

## Dependencies

```bash
pip3 install feedparser requests schedule --break-system-packages
```

## Configuration

```python
CONFIG = {
    "RSS_FEEDS": [
        "https://feeds.feedburner.com/TheHackersNews",
        "https://www.securityweek.com/feed",
        "https://krebsonsecurity.com/feed/",
        "https://www.bleepingcomputer.com/feed/",
    ],
    "IMAGE_WIDTH": 1200,
    "IMAGE_HEIGHT": 627,
    "SCHEDULE_DAYS": 2,
    "SCHEDULE_HOUR": 2,
}
```

## Post Categories

| Category | Trigger Words | Style |
|----------|--------------|-------|
| breaking | breaking, urgent, alert, critical | Urgent, call to action |
| warning | attack, breach, hack, ransomware | Security alert, immediate actions |
| analysis | study, research, report, trend | Deep dive, implications |
| educational | how to, guide, tips, learn | Teaching, awareness |
| default | (everything else) | General news, professional |

## Template Pattern

```python
POST_TEMPLATES = {
    "breaking": [
        "🚨 BREAKING: {title}\n\n{summary}\n\nThis is a developing story...\n\n#CyberSecurity #InfoSec",
    ],
    "warning": [
        "⚠️ SECURITY WARNING:\n\n{title}\n\n{summary}\n\nImmediate actions...\n\n#CyberSecurity #ThreatAlert",
    ],
    # ... more categories
}
```

## Image Generation (Pollinations.ai)

```python
# Free, no API key
url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
params = {"width": 1200, "height": 627, "model": "flux", "seed": random.randint(1, 1000000)}
response = requests.get(url, params=params, timeout=120, stream=True)
```

## Output Files

| File | Content |
|------|---------|
| `linkedin_posts.txt` | Ready-to-copy post text |
| `post_image_*.png` | Generated image |
| `posts_log.json` | Full post history |

## Usage

```python
from linkedin_poster import LinkedInAutomation, CONFIG

automation = LinkedInAutomation(CONFIG)
automation.run_once()  # Run once
automation.schedule_automation()  # Run every 2 days
```

## Pitfalls

1. **RSS feeds may change URLs** — verify feed URLs periodically
2. **Pollinations.ai may be slow** — set timeout=120, use stream=True
3. **LinkedIn blocks bots** — use manual posting approach (save to file)
4. **Template repetition** — random.choice() helps, but rotate templates
5. **Image quality varies** — seed parameter helps, but not deterministic

## Cron Job Setup

```bash
# Run every 2 days at 2 AM
0 2 */2 * * cd /home/kali/linkedin-auto-poster && python3 linkedin_poster.py --once
```

## Alternative: Hermes Cron

```python
# Use Hermes cronjob tool for managed scheduling
cronjob(action="create", schedule="0 2 */2 * *", prompt="Run LinkedIn auto-poster...")
```

## Extensions

- Add more RSS feeds for broader coverage
- Implement LinkedIn API for auto-posting (requires OAuth)
- Add sentiment analysis for better categorization
- Create image templates with text overlay
- Add Google Sheets logging (requires service account)

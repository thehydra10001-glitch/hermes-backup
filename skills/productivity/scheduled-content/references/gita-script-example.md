# Daily Bhagavad Gita Shloka Script

Working example of a content generator script. Tested and deployed as a cron job.

## Script Location
`~/.hermes/scripts/daily_gita.py`

## Key Features
- 20 unique shlokas rotating by day-of-year
- Sanskrit + Gujarati + English translations
- Generates HTML WhatsApp status image file
- Telegram-compatible markdown formatting

## Rotation Logic
```python
index = date.timetuple().tm_yday % len(SHLOKAS)
```
- `tm_yday` = day of year (1-366)
- Modulo by list length = never repeats within the cycle
- 20 shlokas = repeats every 20 days

## HTML Status Image
The script also saves an HTML file at:
`~/.hermes/scripts/gita-status-YYYY-MM-DD.html`

This HTML is a 1080x1920 (9:16) WhatsApp status image with:
- Dark gradient background
- Devanagari + Gujarati + English text
- Google Fonts for multilingual support
- CSS-only design (no JS needed)

## Deployment
```
cronjob create:
  name: "Daily Bhagavad Gita Shloka"
  schedule: "0 7 * * *"
  script: "daily_gita.py"
```

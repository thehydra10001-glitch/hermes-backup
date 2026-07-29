# Telegram Bot API — Sending Messages to Arbitrary Chat IDs

## When to Use

- Delivering OSINT findings to specific users via Telegram
- Cron job delivery to specific chat IDs
- Bot-initiated messages (not responses to user messages)

## Prerequisites

- Bot token in `~/.hermes/.env` as `TELEGRAM_BOT_TOKEN`
- Target's chat ID (numeric, e.g. `5784206319`)
- User must have started a conversation with the bot (sent `/start`)

## How to Get a Chat ID

1. User messages `@userinfobot` or `@RawDataBot` on Telegram
2. Bot replies with numeric chat ID
3. For groups: add `@RawDataBot` to the group, it replies with group chat ID

## Send Message via curl

```bash
TOKEN=$(awk -F= '/^TELEGRAM_BOT_TOKEN=/{print $2; exit}' ~/.hermes/.env)
CHAT="<chat_id>"

curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=${CHAT}" \
  --data-urlencode "text=${MSG}" \
  -d "parse_mode=Markdown"
```

## Notes

- `parse_mode=Markdown` supports `*bold*`, `_italic_`, `` `code` ``
- `parse_mode=HTML` supports `<b>bold</b>`, `<i>italic</i>`
- Use `--data-urlencode "text=..."` for messages with special chars
- Bot token is masked in `.env` display but readable via awk/grep
- Response `"ok": true` confirms delivery

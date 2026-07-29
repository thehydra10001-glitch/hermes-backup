#!/usr/bin/env python3
"""
TEMPLATE: Daily Content Generator Script
Copy this to ~/.hermes/scripts/<your-content>.py and customize.

The script must:
1. Print the final message to stdout (cronjob delivers this)
2. Use date-based indexing for unique daily content
3. Be self-contained (stdlib only)
"""
import datetime
import os

# === CONFIGURATION ===
CONTENT_LIST = [
    {
        "title": "Title for Item 1",
        "body": "Content body text here...",
        "translation": "Optional translation or alternative text",
    },
    {
        "title": "Title for Item 2",
        "body": "Content body text here...",
        "translation": "Optional translation or alternative text",
    },
    # Add enough items to cover your rotation period
    # For daily: 7 items = weekly rotation, 30 = monthly, 365 = yearly
]

# === DATE-BASED SELECTION ===
def get_content_for_date(date=None):
    """Select content based on day of year. Never repeats within list length."""
    if date is None:
        date = datetime.date.today()
    index = date.timetuple().tm_yday % len(CONTENT_LIST)
    return CONTENT_LIST[index]

# === OPTIONAL: Save files (HTML status, CSV, etc.) ===
def save_html_status(item, date):
    """Example: Save an HTML status image file."""
    output_dir = os.path.expanduser("~/.hermes/scripts")
    filename = f"status-{date.strftime('%Y-%m-%d')}.html"
    filepath = os.path.join(output_dir, filename)
    
    html = f"""<!DOCTYPE html>
<html>
<head><style>
body {{ width: 1080px; height: 1920px; background: #1a1a2e; color: white; 
       display: flex; align-items: center; justify-content: center; 
       font-family: sans-serif; text-align: center; padding: 60px; }}
</style></head>
<body>
<h1>{item['title']}</h1>
<p>{item['body']}</p>
</body>
</html>"""
    
    with open(filepath, "w") as f:
        f.write(html)
    return filepath

# === MAIN ===
if __name__ == "__main__":
    today = datetime.date.today()
    item = get_content_for_date(today)
    
    # Format the message (Telegram markdown)
    message = f"""📅 *{today.strftime('%d %B %Y')}*

*{item['title']}*

{item['body']}

{item['translation']}"""
    
    # Print to stdout - cronjob tool delivers this
    print(message)
    
    # Optional: save HTML status
    # save_html_status(item, today)

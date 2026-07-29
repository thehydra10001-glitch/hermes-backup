# Hosting Command Reference — Tested Patterns

## localhost.run — Tested on Kali Linux (2024+)

```bash
# Server start (background via terminal tool)
terminal(command="cd /path/to/site && python3 -m http.server 8080", background=true, notify_on_complete=false)

# Tunnel start (background via terminal tool)
terminal(command="ssh -o StrictHostKeyChecking=no -R 80:localhost:8080 nokey@localhost.run", background=true, notify_on_complete=true)

# Health check
terminal(command="curl -s -o /dev/null -w '%{http_code}' http://localhost:8080")
# Expected: 200
```

### Tunnel URL extraction
The URL appears in the SSH output after "authenticated as anonymous user":
```
cadc19adba6c65.lhr.life tunneled with tls termination, https://cadc19adba6c65.lhr.life
```
Parse the `https://xxxxx.lhr.life` part.

## Environment: Kali Linux 6.x (amd64)

- `python3` available at `/usr/bin/python3` (3.11+)
- `node` available at `/usr/bin/node` (v20+)
- `npm` NOT installed by default — only `node` binary
- `npx` NOT available without npm
- `ngrok` NOT pre-installed
- `cloudflared` NOT pre-installed
- SSH available at `/usr/bin/ssh`
- `pyngrok` installable via pip but requires ngrok binary download

## Common Failures

### npm not found
```
$ npm install -g surge
/usr/bin/bash: line 3: npm: command not found
```
**Fix:** Do not rely on npm. Use python3 HTTP server + SSH tunnel instead.

### Netlify API 401
```
$ curl -X POST "https://api.netlify.com/api/v1/sites" ...
{"code": 401, "message": "Access Denied"}
```
**Fix:** Netlify API requires auth token. Use Netlify Drop (browser drag-and-drop) instead.

### ngrok download timeout
The ngrok binary (~22MB) downloads slowly on constrained networks.
**Fix:** Use `localhost.run` instead — no binary download needed.

### terminal tool rejects nohup/&
```
Foreground command uses '&' backgrounding. Use terminal(background=true)
```
**Fix:** Use `terminal(background=true)` for long-lived processes.

# WordPress.org Passive Recon Case Study — 2026-07-19

## Target
- URL: `https://wordpress.org/`
- Program: HackerOne `hackerone.com/wordpress`
- Scope: `wordpress.org`, `*.wordpress.org`

## Recon Results

### DNS
```
A: 66.6.42.252
AAAA: 2620:109:b00a::4206:2afc
MX: smtp2-dca.wordpress.org, smtp1-dca.wordpress.org
NS: ns1-4.wordpress.org
```

### Subdomains
| Subdomain | IP | Notes |
|-----------|----|-------|
| api.wordpress.org | 66.6.42.251 | Different IP — API endpoint |
| mail.wordpress.org | 66.6.42.147 | Different IP — Mail server |
| staging/admin/login/beta/test | → CNAME to wordpress.org | All point to main site |

### HTTP Headers
```
server: nginx
strict-transport-security: max-age=3600
x-frame-options: SAMEORIGIN
x-olaf: ⛄
x-nc: HIT dca 1
link: <https://wordpress.org/wp-json/>; rel="https://api.w.org/"
```

### Missing Security Headers
- X-Content-Type-Options ❌
- Content-Security-Policy ❌
- Referrer-Policy ❌
- Permissions-Policy ❌

### Technology
- CMS: WordPress 7.1-beta2 (generator meta tag)
- Server: nginx
- CDN: Varnish/CDN (x-nc: HIT dca)
- Sitemap: Jetpack 15.8
- Themes: wporg-parent-2021, wporg-main-2022
- Plugins: Gutenberg 23.5.3, pub-sync (MU-plugin)

### XML-RPC
- `/xmlrpc.php` → HTTP 405 (Method Not Allowed) — disabled/blocked ✓

### REST API (HIGH finding)
- `/wp-json/wp/v2/users` → Exposes usernames, display names, profile URLs, Gravatar hashes
- `/wp-json/wp/v2/pages` → Exposes page content, author IDs
- Thousands of users enumerable without authentication

### Sitemaps
- `sitemap.xml` → Jetpack-generated, 3 sub-sitemaps (pages, images, videos)
- Additional sitemaps: themes, plugins, news, showcase, documentation, patterns, photos

## Key Takeaway
Passive recon (curl + dig only, zero active scanning) found a HIGH-severity REST API user enumeration leak. Always run passive recon first.

# GitHub API Recon Reference

No authentication needed for public profiles. Rate limit: 60 req/hr (unauthenticated).

## User Profile

```bash
curl -s "https://api.github.com/users/<username>" | python3 -m json.tool
```

**Key fields:**
| Field | Description |
|---|---|
| `login` | Username |
| `name` | Display name |
| `bio` | User bio (may contain email, links) |
| `location` | Self-reported location |
| `email` | Public email (if set) |
| `blog` | Website URL |
| `twitter_username` | Twitter handle |
| `public_repos` | Total public repos |
| `followers` / `following` | Follower/following count |
| `created_at` | Account creation date |
| `updated_at` | Last profile update |

## Repos List

```bash
curl -s "https://api.github.com/users/<username>/repos?per_page=30&sort=updated" \
  | python3 -c "import sys,json; repos=json.load(sys.stdin); \
    [print(f'{r[\"name\"]} | {r.get(\"language\",\"N/A\")} | {r.get(\"description\",\"N/A\")} | Stars:{r.get(\"stargazers_count\",0)} | Updated:{r.get(\"updated_at\",\"N/A\")}') for r in repos]"
```

**Key fields per repo:**
| Field | Description |
|---|---|
| `name` | Repository name |
| `language` | Primary language |
| `description` | Repo description |
| `stargazers_count` | Stars (popularity signal) |
| `forks_count` | Forks |
| `created_at` | When created |
| `updated_at` | Last activity |
| `topics` | Tagged topics (if any) |

## Identity Correlation

- `name` field → cross-reference with LinkedIn/other profiles
- `bio` field → may contain email, social handles, company
- `location` → geolocation pivot
- `blog` → personal website pivot
- `twitter_username` → Twitter/X pivot
- Repo names/topics → interest/skill inference

## Pivot Patterns

```
GitHub username → LinkedIn (via name + location match)
GitHub repos → skills/interests → professional profile
GitHub bio → email/social handles → breach checks
GitHub orgs → employer verification
GitHub activity timeline → employment timeline correlation
```

## Limitations

- Private repos not visible
- Email only visible if user set it as public
- Location is self-reported (may be vague)
- Bio may be empty
- No phone number exposed

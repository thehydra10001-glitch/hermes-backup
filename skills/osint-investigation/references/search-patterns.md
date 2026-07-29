# OSINT Platform Search Patterns

## GitHub API Lookup

```bash
# Direct API check
curl -s "https://api.github.com/users/<username>" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for k in ['login','name','bio','location','company','blog','email','public_repos','followers','following','created_at']:
    print(f'{k}: {data.get(k, \"N/A\")}')
"
```

## Web Search Patterns

### General Person Search
```
web_search(query="\"Full Name\" LinkedIn OR ResearchGate OR ORCID")
web_search(query="\"Full Name\" Instagram OR Facebook OR Twitter")
```

### Platform-Specific
```
web_search(query="site:linkedin.com/in/ \"Name\"")
web_search(query="site:researchgate.net \"Name\"")
web_search=query="site:orcid.org \"Name\"")
web_search(query="site:scholar.google.com \"Name\"")
web_search(query="site:github.com \"Name\"")
```

### Email Breach Check
```
web_search(query="\"email@domain.com\" breach data")
```

## Common Username Patterns

For a person named "John Doe":
- `johndoe`
- `john_doe`
- `johndoe123`
- `doejohn`
- `john.doe`
- `j_doe`
- `jd123`

## Researcher-Specific Platforms

| Platform | URL Pattern | Data Available |
|----------|-------------|----------------|
| ORCID | orcid.org/0000-0000-0000-0000 | Publications, employment |
| ResearchGate | researchgate.net/profile/Name | Papers, citations, RG Score |
| Google Scholar | scholar.google.com/citations?user=ID | Citations, h-index |
| Scopus | scopus.com/authid/detail.uri?authorId=ID | Publications, metrics |
| IRMA | irma-international.org/affiliate/ | Professional membership |

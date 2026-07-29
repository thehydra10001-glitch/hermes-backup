---
name: defuddle
description: Extract main content from web pages — removes clutter (comments, sidebars, headers, footers) and returns cleaned HTML or Markdown. A replacement for Mozilla Readability.
metadata:
  source: https://github.com/kepano/defuddle
  version: 1.0
---

# Defuddle — Web Content Extraction

Defuddle extracts the main content from web pages. It cleans up web pages by removing clutter like comments, sidebars, headers, footers, and other non-essential elements, leaving only the primary content.

## Usage

### CLI
```bash
# Parse a URL
npx defuddle parse https://example.com/article

# Output as markdown
npx defuddle parse page.html --markdown

# Output as JSON with metadata
npx defuddle parse page.html --json

# Extract a specific property
npx defuddle parse page.html --property title
```

### Node.js
```javascript
import { parseHTML } from 'linkedom';
import { Defuddle } from 'defuddle/node';

const { document } = parseHTML(html);
const result = await Defuddle(document, 'https://example.com/article', {
  markdown: true
});
console.log(result.content);
```

## Key Features
- More forgiving than Mozilla Readability — removes fewer uncertain elements
- Consistent output for footnotes, math, code blocks
- Uses mobile styles to guess at unnecessary elements
- Extracts schema.org metadata
- Multiple output formats: HTML, Markdown, JSON, frontmatter
- Debug mode for understanding what gets removed

## Installation
```bash
npm install -g defuddle
```

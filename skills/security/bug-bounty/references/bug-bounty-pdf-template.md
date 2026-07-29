# Bug Bounty PDF Report Template (fpdf2)

## Overview
Professional PDF report generator for bug bounty findings. Uses fpdf2 with custom FPDF subclass for consistent styling.

## Proven Code Pattern

```python
#!/usr/bin/env python3
"""Bug Bounty PDF Report Generator using fpdf2."""
from fpdf import FPDF
from datetime import datetime

class BugBountyReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(255, 0, 0)
        self.cell(0, 8, 'BUG BOUNTY REPORT - CONFIDENTIAL', align='C')
        self.set_draw_color(255, 0, 0)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}} | HERMES OSINT Agent | {datetime.now().strftime("%Y-%m-%d")}', align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(255, 0, 0)
        self.set_fill_color(30, 30, 30)
        self.cell(0, 8, f'  {title}', new_x='LMARGIN', new_y='NEXT', fill=True)
        self.ln(3)

    def finding_header(self, num, title, severity):
        colors = {'CRITICAL': (255,0,0), 'HIGH': (255,100,0), 'MEDIUM': (255,165,0), 'LOW': (0,128,0)}
        r, g, b = colors.get(severity, (128, 128, 128))
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(r, g, b)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 7, f'Finding #{num}: {title} [{severity}]', new_x='LMARGIN', new_y='NEXT', fill=True)
        self.ln(2)

    def kv_line(self, key, value):
        self.set_font('Helvetica', 'B', 9)
        self.cell(50, 5, f'{key}:')
        self.set_font('Helvetica', '', 9)
        self.cell(0, 5, value, new_x='LMARGIN', new_y='NEXT')

    def body_text(self, text):
        self.set_font('Helvetica', '', 9)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def code_block(self, text):
        self.set_font('Courier', '', 8)
        self.set_fill_color(245, 245, 245)
        for line in text.split('\n'):
            self.cell(0, 4, f'  {line}', new_x='LMARGIN', new_y='NEXT', fill=True)
        self.ln(2)

# Usage:
pdf = BugBountyReport()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()
# ... add findings ...
pdf.output('report.pdf')
```

## CRITICAL: Data Sanitization

**ALWAYS sanitize data strings before passing to PDF methods:**

```python
def sanitize_for_pdf(text):
    """Remove non-Latin-1 characters (Chinese, Japanese, etc.)"""
    return text.encode('ascii', 'ignore').decode('ascii')

# Example: API response with Chinese characters
raw_response = '{"code":"400","message":"请求体不能为空，且必须为JSON格式"}'
clean = sanitize_for_pdf(raw_response)
# Result: '{"code":"400","message":""}'  -- Chinese removed
```

## Common Pitfalls

1. **`cell()` + `multi_cell()` crash:** Never call `multi_cell()` immediately after `cell()` at same horizontal position. Use `set_x()` + `multi_cell(width)` instead.

2. **Chinese/CJK characters:** Core fonts (Helvetica, Courier) are Latin-1 only. Non-ASCII characters cause `FPDFUnicodeEncodingException`. Sanitize with `.encode('ascii','ignore')`.

3. **`ln` parameter deprecated:** Use `new_x='LMARGIN', new_y='NEXT'` instead of `ln=1`. Use `new_x='RIGHT', new_y='TOP'` instead of `ln=0`.

4. **Code block width:** Keep lines < 70 chars for Courier 8pt. Longer lines cause "Not enough horizontal space" error.

## Recommended Structure

1. **Cover Page** — Target, date, report ID, classification
2. **Table of Contents** — Manual listing
3. **Executive Summary** — 3-5 sentences, finding counts
4. **Scope & Methodology** — Program details, tools used
5. **Reconnaissance Results** — Subdomains, tech stack, DNS
6. **Vulnerability Findings** — One section per finding with severity, description, evidence, remediation
7. **Positive Security Controls** — What's working (WAF, DDoS, etc.)
8. **Vulnerability Summary Matrix** — Table with all findings
9. **Technical Evidence** — Raw requests/responses
10. **Remediation** — Priority 1/2/3 actions
11. **Tool Execution Log** — Timestamped tool runs
12. **Conclusion** — Summary and next steps

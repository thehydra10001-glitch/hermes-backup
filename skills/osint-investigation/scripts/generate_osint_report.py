#!/usr/bin/env python3
"""HERMES OSINT PDF Report Generator — fpdf2-based template.
Generates a professional multi-page PDF with clickable links, tables, and metadata.

Usage: python3 generate_osint_report.py
Output: ~/.hermes/pastes/OSINT-Report-<TargetName>-<date>.pdf

Customize: Modify the data dicts below (identities, platforms, timeline, etc.)
for each investigation. The report structure is reusable across all OSINT cases.

Key rules:
- ASCII fallback chars only (Helvetica is Latin-1, no Unicode)
- Custom FPDF subclass for consistent header/footer
- Clickable URLs via fpdf2 link parameter
- Alternating row colors for readability
"""
from fpdf import FPDF
import datetime

class OSINTReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, 'HERMES OSINT Investigation Report | CONFIDENTIAL', 0, 0, 'L')
        self.cell(0, 6, f'Report ID: HERMES-YYYYMMDD-XXXXXX', 0, 1, 'R')
        self.line(10, 14, 200, 14)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'HERMES OSINT Agent v1.1 | Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_draw_color(0, 51, 102)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def subsection(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(0, 80, 130)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(1)

    def field(self, label, value):
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(60, 60, 60)
        self.cell(50, 6, label + ':', 0, 0)
        self.set_font('Helvetica', '', 9)
        self.set_text_color(0, 0, 0)
        self.cell(0, 6, str(value), 0, 1)

    def link_item(self, label, url):
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(0, 51, 102)
        self.cell(5, 5, '-', 0, 0)
        self.cell(40, 5, label + ':', 0, 0)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(0, 102, 204)
        self.cell(0, 5, url, 0, 1, 'L', link=url)

    def table_header(self, cols, widths):
        self.set_font('Helvetica', 'B', 8)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 7, col, 1, 0, 'C', fill=True)
        self.ln()

    def table_row(self, cols, widths, fill=False):
        self.set_font('Helvetica', '', 8)
        self.set_text_color(0, 0, 0)
        if fill:
            self.set_fill_color(240, 245, 250)
        for i, col in enumerate(cols):
            self.cell(widths[i], 6, str(col)[:50], 1, 0, 'L', fill=fill)
        self.ln()


# ===== CUSTOMIZE THESE =====
TARGET_NAME = "Kuldipsinh R. Mori"
TARGET_ROLE = "Human Genetics Researcher | PhD Scholar"
TARGET_UNI = "Gujarat University, India"
REPORT_ID = "HERMES-20260710-A3F7B2"
RISK_LEVEL = "LOW"
CONFIDENCE = "92%"

IDENTITIES = [
    ("LinkedIn (Researcher)", "https://in.linkedin.com/in/kuldipsinh-mori-54876a258"),
    ("ORCID", "https://orcid.org/0009-0008-3093-7095"),
    ("IRMA International", "https://www.irma-international.org/affiliate/kuldipsinh-r-mori/513157/"),
    ("UrbanPro", "https://www.urbanpro.com/jodhpur/kuldipsinh"),
]

PLATFORMS = [
    ("LinkedIn", "kuldipsinh-mori-54876a258", "Active"),
    ("ORCID", "0009-0008-3093-7095", "Active"),
    ("YouTube", "@kuldipsinhmori", "Active"),
    ("Instagram", "@mori.kuldip1204", "Active"),
    ("Twitter/X", "@kuldipsinhmori", "Active"),
]

TIMELINE = [
    ("2017-08", "Twitter/X account created"),
    ("2025-02", "Forensics Magazine article published"),
    ("2026", "PhD Scholar in Human Genetics (current)"),
    ("2026-07-10", "This OSINT investigation"),
]

ALL_LINKS = [
    ("LinkedIn", "https://in.linkedin.com/in/kuldipsinh-mori-54876a258"),
    ("ORCID", "https://orcid.org/0009-0008-3093-7095"),
    ("IRMA", "https://www.irma-international.org/affiliate/kuldipsinh-r-mori/513157/"),
]

# ===== GENERATE =====
pdf = OSINTReport()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# Cover
pdf.ln(20)
pdf.set_font('Helvetica', 'B', 28)
pdf.set_text_color(0, 51, 102)
pdf.cell(0, 15, 'HERMES OSINT', 0, 1, 'C')
pdf.set_font('Helvetica', '', 18)
pdf.set_text_color(60, 60, 60)
pdf.cell(0, 10, 'Investigation Report', 0, 1, 'C')
pdf.ln(5)
pdf.set_draw_color(0, 51, 102)
pdf.line(60, pdf.get_y(), 150, pdf.get_y())
pdf.ln(10)
pdf.set_font('Helvetica', 'B', 14)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 10, f'Target: {TARGET_NAME}', 0, 1, 'C')
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, TARGET_ROLE, 0, 1, 'C')
pdf.cell(0, 8, TARGET_UNI, 0, 1, 'C')
pdf.ln(15)

# Metadata
pdf.set_font('Helvetica', '', 10)
pdf.set_fill_color(245, 248, 252)
pdf.set_draw_color(200, 210, 220)
y_start = pdf.get_y()
pdf.rect(30, y_start, 150, 45, 'DF')
pdf.set_xy(35, y_start + 5)
pdf.set_text_color(60, 60, 60)
for label, value in [('Classification', 'CONFIDENTIAL'), ('Report ID', REPORT_ID),
                     ('Generated By', 'HERMES OSINT Agent v1.1'), ('Confidence', CONFIDENCE)]:
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(45, 6, label + ':', 0, 0)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 6, value, 0, 1)

# Findings
pdf.add_page()
pdf.section_title('1. IDENTITIES FOUND')
for name, url in IDENTITIES:
    pdf.link_item(name, url)
    pdf.ln(1)

pdf.ln(5)
pdf.section_title('2. DIGITAL FOOTPRINT')
widths = [45, 95, 40]
pdf.table_header(['Platform', 'Handle', 'Status'], widths)
for i, (plat, handle, status) in enumerate(PLATFORMS):
    pdf.table_row([plat, handle, status], widths, fill=(i % 2 == 0))

pdf.ln(5)
pdf.section_title('3. TIMELINE')
widths4 = [30, 140]
pdf.table_header(['Date', 'Event'], widths4)
for i, (date, event) in enumerate(TIMELINE):
    pdf.table_row([date, event], widths4, fill=(i % 2 == 0))

pdf.add_page()
pdf.section_title('4. ALL LINKS')
widths5 = [50, 130]
pdf.table_header(['Platform', 'URL (clickable)'], widths5)
for i, (name, url) in enumerate(ALL_LINKS):
    pdf.set_font('Helvetica', '', 7)
    fill = (i % 2 == 0)
    if fill:
        pdf.set_fill_color(240, 245, 250)
    pdf.cell(50, 5, name, 1, 0, 'L', fill=fill)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(130, 5, url[:60], 1, 1, 'L', link=url, fill=fill)
pdf.set_text_color(0, 0, 0)

# End
pdf.ln(10)
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(0, 51, 102)
pdf.cell(0, 10, 'END OF REPORT', 0, 1, 'C')

# Save
today = datetime.date.today().strftime('%Y%m%d')
safe_name = TARGET_NAME.replace(' ', '').replace('.', '')
output_path = f'/home/kali/.hermes/pastes/OSINT-Report-{safe_name}-{today}.pdf'
pdf.output(output_path)
print(f"PDF saved to: {output_path}")
print(f"Pages: {pdf.pages_count}")

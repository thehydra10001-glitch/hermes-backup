# fpdf2 PDF Generation Pattern

## Proven Code Template

```python
#!/usr/bin/env python3
"""Generate styled PDF using fpdf2."""
from fpdf import FPDF

class StyledPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'Document Title', align='C')
        self.ln(5)
        self.set_draw_color(180, 180, 180)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def code_block(self, code):
        self.set_font('Courier', '', 9)
        self.set_fill_color(245, 245, 245)
        x = self.get_x()
        y = self.get_y()
        lines = code.strip().split('\n')
        block_height = len(lines) * 5 + 8
        self.rect(x, y, 190, block_height, 'DF')
        self.ln(3)
        for line in lines:
            self.set_x(x + 3)
            self.cell(0, 5, line, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def bullet(self, text, indent=10):
        self.set_font('Helvetica', '', 10)
        x = self.get_x()
        self.set_x(x + indent)
        self.cell(5, 6, '-')
        self.multi_cell(0, 6, text)
        self.ln(1)

pdf = StyledPDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()
# ... add content ...
pdf.output('output.pdf')
```

## Common Pitfalls
1. **Unicode bullets fail:** `chr(8226)` (.) not supported by Helvetica. Use `-` instead.
2. **`ln=True` deprecated:** Use `new_x='LMARGIN', new_y='NEXT'` instead.
3. **Text encoding -- CRITICAL:** Core fonts (Helvetica, Courier, Times) are **Latin-1 only**. ANY character outside U+0080-U+00FF crashes with `FPDFUnicodeEncodingException`. This includes em dashes, curly quotes, ellipsis, bullets, and CJK/Cyrillic.
   - **Fix A -- Register a TTF font:**
     ```python
     pdf.add_font('Mono', '', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')
     pdf.add_font('Mono', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf')
     pdf.set_font('Mono', '', 8)
     ```
     Common paths: DejaVu Sans Mono, Liberation Mono under `/usr/share/fonts/truetype/`.
   - **Fix B -- Sanitize all text** (when stuck with core fonts):
     ```python
     def _clean(t):
         return t.replace('\u2014', '--').replace('\u2013', '-') \
                 .replace('\u2018', "'").replace('\u2019', "'") \
                 .replace('\u201c', '"').replace('\u201d', '"') \
                 .replace('\u2026', '...').replace('\u2022', '*') \
                 .replace('\u00a0', ' ')
     ```
4. **`uni=True` deprecated in fpdf2 v2.5.1+:** `add_font('Mono', '', 'font.ttf', uni=True)` generates a DeprecationWarning. The `uni` parameter is no longer accepted. Simply omit it.
5. **Page breaks:** Set `set_auto_page_break(auto=True, margin=20)` early.
6. **cell() + multi_cell() crash:** Calling `multi_cell()` immediately after `cell()` on the same line causes "Not enough horizontal space to render a single character". Fix: put label and value on separate lines — never mix cell+multi_cell in same horizontal position.
7. **Long strings overflow:** SHA256 hashes and long URLs in `cell()` can overflow. Use `cell(0, 5, ...)` with width=0 for auto-width, or break across lines.
8. **ASCII art lines too wide:** When using `multi_cell()` with code blocks containing ASCII art, each line must be < ~70 chars for Courier 7pt. Longer lines (especially waveforms with `/\\` patterns) cause "Not enough horizontal space". Fix: shorten lines, use smaller font (Courier 6pt), or simplify diagrams.
9. **Unicode in data strings:** Non-ASCII characters (Chinese, Japanese, etc.) in data strings cause errors when using standard fonts (Helvetica, Courier). Fix: sanitize all data strings with `.encode('ascii', 'ignore').decode('ascii')` or replace non-ASCII chars before passing to PDF methods.

## Table Pattern
```python
# Header
pdf.set_font('Helvetica', 'B', 9)
pdf.set_fill_color(60, 60, 60)
pdf.set_text_color(255, 255, 255)
pdf.cell(30, 8, 'Column 1', border=1, fill=True)
pdf.cell(50, 8, 'Column 2', border=1, fill=True)
pdf.ln()

# Rows
pdf.set_font('Helvetica', '', 9)
pdf.set_text_color(40, 40, 40)
for row in data:
    pdf.cell(30, 7, row[0], border=1)
    pdf.cell(50, 7, row[1], border=1)
    pdf.ln()
```

## Circuit Diagram Patterns

### Resistor (Zigzag)
```python
def draw_resistor(self, x, y, label="R"):
    self.set_draw_color(0, 0, 0)
    self.set_line_width(0.5)
    self.line(x, y, x+10, y)
    points = [(x+10, y)]
    for i in range(6):
        px = x + 10 + (i+1) * 5
        py = y + (5 if i % 2 == 0 else -5)
        points.append((px, py))
    points.append((x+50, y))
    for i in range(len(points)-1):
        self.line(points[i][0], points[i][1], points[i+1][0], points[i+1][1])
    self.line(x+50, y, x+60, y)
    self.set_font('Helvetica', '', 8)
    self.text(x+20, y-10, label)
```

### Capacitor (Parallel Lines)
```python
def draw_capacitor(self, x, y, label="C"):
    self.set_draw_color(0, 0, 0)
    self.set_line_width(0.5)
    self.line(x, y, x+20, y)
    self.line(x+20, y-10, x+20, y+10)
    self.line(x+25, y-10, x+25, y+10)
    self.line(x+25, y, x+45, y)
    self.set_font('Helvetica', '', 8)
    self.text(x+15, y-12, label)
```

### LED (Triangle + Arrows)
```python
def draw_led(self, x, y, label="LED"):
    self.set_draw_color(0, 0, 0)
    self.set_line_width(0.5)
    self.line(x, y, x+15, y-10)
    self.line(x, y, x+15, y+10)
    self.line(x+15, y-10, x+15, y+10)
    self.line(x+15, y, x+30, y)
    self.line(x+20, y-15, x+25, y-20)
    self.line(x+22, y-12, x+27, y-17)
    self.set_font('Helvetica', '', 8)
    self.text(x+5, y+15, label)
```

### Transistor (NPN)
```python
def draw_transistor(self, x, y, label="NPN"):
    self.set_draw_color(0, 0, 0)
    self.set_line_width(0.5)
    self.line(x, y, x+15, y)  # Base
    self.line(x+15, y-15, x+15, y+15)  # Vertical
    self.line(x+15, y-10, x+30, y-20)  # Collector
    self.line(x+30, y-20, x+30, y-30)
    self.line(x+15, y+10, x+30, y+20)  # Emitter
    self.line(x+30, y+20, x+30, y+30)
    self.line(x+22, y+14, x+28, y+18)  # Arrow
    self.set_font('Helvetica', '', 8)
    self.text(x+5, y+35, label)
```

### Board Outline (Arduino/ESP32/RPi)
```python
def draw_board(self, x, y, name, color, pins=7):
    self.set_draw_color(*color)
    self.set_line_width(1)
    self.rect(x, y, 50, 70)
    self.set_font('Helvetica', 'B', 7)
    self.set_text_color(*color)
    self.text(x + 5, y + 10, name)
    for i in range(pins):
        self.set_fill_color(0, 0, 0)
        self.rect(x + 3, y + 15 + i * 7, 3, 3, 'F')
        self.rect(x + 44, y + 15 + i * 7, 3, 3, 'F')
```

### Layout: Diagram Left, Text Right
```python
# Place diagram on left
pdf.draw_resistor(20, 40, "R1")
# Place text on right
pdf.set_font('Helvetica', 'B', 10)
pdf.text(90, 45, "Resistor (R1):")
pdf.set_font('Helvetica', '', 9)
pdf.text(90, 55, "Value: 220 ohm")
```

## Key Lesson: Diagrams + Formatting Balance

**Problem:** V1 had good diagrams but text overlapped. V2 fixed overlap but lost diagrams.

**Solution:** Keep diagrams AND use smaller fonts:
- Code blocks: Courier 7-8pt (NEVER larger)
- Body text: Helvetica 9pt
- Diagram labels: Helvetica 7-8pt
- Line height: 4-5pt

## Colored Box Variants (Warning/Danger/Tip/Success/Note)

Extend the info_box pattern with semantic color coding:

```python
def warning_box(self, text):
    """Yellow background - caution, not critical."""
    self.set_fill_color(255, 243, 205)
    self.set_draw_color(255, 193, 7)
    self.set_font('Helvetica', 'B', 10)
    self.set_text_color(133, 100, 4)
    self.multi_cell(0, 6, f"WARNING: {text}", border=1, fill=True)
    self.set_text_color(0, 0, 0)
    self.ln(4)

def danger_box(self, text):
    """Red background - critical safety or legal warning."""
    self.set_fill_color(248, 215, 218)
    self.set_draw_color(220, 53, 69)
    self.set_font('Helvetica', 'B', 10)
    self.set_text_color(114, 28, 36)
    self.multi_cell(0, 6, f"DANGER: {text}", border=1, fill=True)
    self.set_text_color(0, 0, 0)
    self.ln(4)

def tip_box(self, text):
    """Cyan background - helpful hint or best practice."""
    self.set_fill_color(209, 236, 241)
    self.set_draw_color(0, 184, 214)
    self.set_font('Helvetica', 'I', 10)
    self.set_text_color(12, 84, 96)
    self.multi_cell(0, 6, f"TIP: {text}", border=1, fill=True)
    self.set_text_color(0, 0, 0)
    self.ln(4)

def success_box(self, text):
    """Green background - confirmation, milestone reached."""
    self.set_fill_color(212, 237, 218)
    self.set_draw_color(40, 167, 69)
    self.set_font('Helvetica', 'B', 10)
    self.set_text_color(21, 87, 36)
    self.multi_cell(0, 6, f"SUCCESS: {text}", border=1, fill=True)
    self.set_text_color(0, 0, 0)
    self.ln(4)

def note_box(self, text):
    """Gray background - neutral informational note."""
    self.set_fill_color(226, 227, 229)
    self.set_draw_color(108, 117, 125)
    self.set_font('Helvetica', '', 10)
    self.set_text_color(73, 80, 87)
    self.multi_cell(0, 6, f"NOTE: {text}", border=1, fill=True)
    self.set_text_color(0, 0, 0)
    self.ln(4)
```

**Key pattern:** All boxes use `multi_cell(0, 6, text, border=1, fill=True)` — width=0 fills the available horizontal space, border=1 draws the colored outline, fill=True applies the background. Always reset `set_text_color(0, 0, 0)` after to avoid leaking color into subsequent content.

## UI Element Label Pattern

For labeling interface elements in tutorials:

```python
def ui_element(self, label, desc):
    self.set_font('Courier', 'B', 10)
    self.set_text_color(0, 102, 204)
    self.cell(50, 6, f'  [{label}]')
    self.set_font('Helvetica', '', 10)
    self.set_text_color(0, 0, 0)
    self.multi_cell(0, 6, desc)
    self.ln(1)
```

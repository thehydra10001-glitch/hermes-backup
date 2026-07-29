---
name: electronics-pdf
description: Generate electronics & microcontroller reference PDFs with clean formatting AND circuit diagrams
category: productivity
---

# Electronics PDF Generator

## Best Practice
Combine V1 diagrams + V2 clean formatting for perfect output.

## Key Lessons Learned

### V1 Strengths (Keep)
- Drew actual circuit diagrams (resistor zigzag, capacitor parallel lines, LED triangle, transistor, MOSFET, relay symbols)
- Drew board outlines (Arduino, ESP32, Raspberry Pi) with pin markers
- Drew multimeter with dial and probes
- Drew sensor boxes

### V2 Strengths (Keep)
- No text overlap on any page
- Smaller fonts for code blocks (Courier 8pt)
- Better line spacing (5-6pt body, 4pt code)
- Clean section separation
- Proper page breaks

### V1 Weaknesses (Avoid)
- Text overlapped on pages 7, 8, 13, 15, 17, 26
- Unicode characters caused errors (use DejaVu Sans Mono instead — see Unicode Font Approach section)

### V2 Weaknesses (Avoid)
- Lost all circuit diagrams - became text-only
- No visual board representations

## Template Structure

```python
# 1. Use fpdf2 with custom class
# 2. Draw methods for each component:
#    - draw_resistor(x, y, label) - zigzag pattern
#    - draw_capacitor(x, y, label) - parallel lines
#    - draw_led(x, y, label) - triangle + arrows
#    - draw_transistor(x, y, label) - NPN/PNP symbol
#    - draw_mosfet(x, y, label) - gate/channel/drain/source
#    - draw_relay(x, y, label) - coil + contacts
#    - draw_board(x, y, name, color, pins) - board outline
#    - draw_multimeter(x, y) - body + dial + probes
#    - draw_sensor(x, y, label) - box with pins
# 3. Font sizes:
#    - Chapter title: Helvetica Bold 14
#    - Section title: Helvetica Bold 10
#    - Body text: Helvetica 9
#    - Code blocks: Courier 7-8pt (NEVER larger)
#    - Diagram labels: Helvetica 7-8pt
# 4. Spacing:
#    - Line height body: 5pt
#    - Line height code: 4pt
#    - After section: 3pt
#    - After code block: 4pt
# 5. Unicode via DejaVu Sans Mono (see section below) — avoid only if file size is critical
```

## Unicode Font Approach (Preferred — New in v2.8+)

Instead of replacing Unicode characters with ASCII equivalents, **use DejaVu Sans Mono** (or another Unicode TTF) via `add_font()`:

```python
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdf.add_font("M", "", os.path.join(FONT_DIR, "DejaVuSansMono.ttf"))  # regular
pdf.add_font("M", "B", os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf"))  # bold
pdf.add_font("M", "I", os.path.join(FONT_DIR, "DejaVuSansMono-Oblique.ttf"))  # italic
pdf.add_font("M", "BI", os.path.join(FONT_DIR, "DejaVuSansMono-BoldOblique.ttf"))  # bold italic
```

Then use `pdf.set_font("M", "B", 10)` instead of `"Courier"`.

### Font Paths (Kali Linux / Debian)
| Variant | Path |
|:--------|:-----|
| Regular | `/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf` |
| Bold | `/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf` |
| Oblique | `/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Oblique.ttf` |
| Bold Oblique | `/usr/share/fonts/truetype/dejavu/DejaVuSansMono-BoldOblique.ttf` |

### Add a Unicode Safety Sanitizer
Even DejaVu doesn't cover EVERY Unicode character. Add a `_clean()` static method
as a fallback to catch stragglers:

```python
@staticmethod
def _clean(t):
    return t.replace("\u2014", "--").replace("\u2013", "-") \
            .replace("\u2018", "'").replace("\u2019", "'") \
            .replace("\u201c", '"').replace("\u201d", '"') \
            .replace("\u2026", "...").replace("\u2022", "*") \
            .replace("\u00a0", " ") \
            .replace("\u2713", "V").replace("\u2717", "X")
```

Call `txt = self._clean(txt)` before `multi_cell()` on every text/body method.

### Deprecation Warning
In fpdf2 ≥ v2.5.1, `add_font(..., uni=True)` is deprecated. Just omit the
`uni` parameter — TrueType fonts are always treated as Unicode.

### Font Size Comparison
DejaVu Sans Mono is slightly WIDER than Courier at the same pt size.
- Use 6.5pt instead of 7pt for body text
- Use 6pt instead of 6.5pt for code blocks
- Use 10pt instead of 11pt for chapter titles

### When to Use Which
- **DejaVu Sans Mono (Unicode approach):** Any PDF that needs em dashes, proper
  quotes, degree symbols, or international characters. Preferred for all new work.
- **Built-in Courier (ASCII approach):** When file size matters (no font embedding)
  or maximum compatibility with legacy fpdf2 versions.

## ASCII Fallback: Unicode Replacement Table
(Only when NOT using DejaVu — see Unicode Font Approach above for the modern way)
- Ω → R or ohm
- µ → u
- τ → tau
- ± → +/-
- ° → deg
- → → ->
- ≥ → >=
- ≤ → <=

## Page Layout Rules
1. Max 2-3 diagrams per page
2. Diagrams on left (x=20), text on right (x=90+)
3. Code blocks: full width (190mm)
4. Tables: proper column widths with borders
5. Auto page break at margin=20

## Reference Files
- `references/circuit-diagrams.md` — Complete draw methods for all components (resistor, capacitor, LED, transistor, MOSFET, relay, boards, ground, VCC)

## Verification Checklist
- [ ] No text overlapping on any page
- [ ] All circuit diagrams present
- [ ] Board outlines visible
- [ ] Code blocks properly formatted
- [ ] Tables aligned correctly
- [ ] Page numbers working
- [ ] No Unicode errors

## Key Lesson from Session
User explicitly said: "v1 good for diagram but not good v2 in diagram"
- V1 had actual drawn circuit symbols (zigzag resistors, parallel capacitor lines, transistor arrows)
- V2 removed diagrams to fix overlap, became text-only boring
- SOLUTION: Keep V1 diagrams AND use V2's font sizes/spacing to prevent overlap
- Never sacrifice visual diagrams for text formatting — find the balance
- Courier 7-8pt prevents text overlap in diagram-heavy PDFs

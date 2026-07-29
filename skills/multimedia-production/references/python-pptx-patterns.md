# python-pptx Pattern Reference

## Quick Setup
```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(5.625)  # 16:9 aspect ratio
```

## Theme Configuration Pattern
```python
THEMES = {
    "business": {
        "primary": RGBColor(0x1E, 0x3A, 0x5F),    # Navy
        "secondary": RGBColor(0x3D, 0x7E, 0xAA),  # Medium blue
        "accent": RGBColor(0xE8, 0xB8, 0x4E),      # Gold
        "bg_light": RGBColor(0xF8, 0xF9, 0xFA),    # Off-white
        "bg_dark": RGBColor(0x1A, 0x1A, 0x2E),     # Dark navy
        "text_light": RGBColor(0xFF, 0xFF, 0xFF),
        "text_dark": RGBColor(0x33, 0x33, 0x33),
    },
    # Add more themes...
}
```

## Slide Builder Patterns

### Title Slide (Full Background)
```python
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = theme["bg_dark"]

# Title text
title_box = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(1.5))
p = title_box.text_frame.paragraphs[0]
p.text = "Title"
p.font.size = Pt(44)
p.font.bold = True
p.font.color.rgb = theme["text_light"]
p.alignment = PP_ALIGN.CENTER
```

### Content Slide (Accent Bar + Bullets)
```python
# Accent bar on left
accent_bar = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    Inches(0), Inches(0), Inches(0.15), Inches(1.2)
)
accent_bar.fill.solid()
accent_bar.fill.fore_color.rgb = theme["primary"]
accent_bar.line.fill.background()

# Header
header_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(8.5), Inches(0.8))
p = header_box.text_frame.paragraphs[0]
p.text = "Section Title"
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = theme["primary"]

# Bullet points
bullet_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.2), Inches(4.5))
for i, bullet in enumerate(bullets):
    p = bullet_box.text_frame.paragraphs[0] if i == 0 else bullet_box.text_frame.add_paragraph()
    p.text = f"▸  {bullet}"
    p.font.size = Pt(18)
    p.font.color.rgb = theme["text_dark"]
    p.space_after = Pt(12)
```

### Two-Column Slide
```python
# Left column (colored box)
left_col = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.5), Inches(1.5), Inches(4.2), Inches(3.8)
)
left_col.fill.solid()
left_col.fill.fore_color.rgb = theme["primary"]
left_col.line.fill.background()

# Right column (text only)
right_box = slide.shapes.add_textbox(Inches(5.2), Inches(1.7), Inches(4.2), Inches(3.4))
```

## Common Shapes
```python
# Rectangle
shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)

# Rounded rectangle
shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)

# Fill and remove border
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(r, g, b)
shape.line.fill.background()  # No border
```

## Text Formatting
```python
# Font properties
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
p.alignment = PP_ALIGN.CENTER  # or PP_ALIGN.LEFT, PP_ALIGN.RIGHT

# Spacing
p.space_after = Pt(12)
p.space_before = Pt(6)
```

## Content Generation Pattern
```python
def generate_content(topic: str, num_slides: int = 8):
    sections = [
        ("Introduction", f"Welcome to our presentation on {topic}."),
        ("Key Concepts", f"Let's explore the fundamental principles."),
        ("Current Trends", f"The landscape is constantly changing."),
        ("Challenges", f"Understanding obstacles is the first step."),
        ("Opportunities", f"Where there are challenges, there are opportunities."),
        ("Best Practices", f"Learn from industry leaders."),
        ("Future Outlook", f"What does the future hold?"),
        ("Key Takeaways", f"The most important points to remember."),
    ]
    
    num_content = max(num_slides - 2, 4)  # Minus title and ending
    selected = random.sample(sections, min(num_content, len(sections)))
    
    return {
        "title": topic,
        "subtitle": f"A Comprehensive Overview of {topic}",
        "sections": selected,
        "bullets": {title: [f"Point {i}" for i in range(1, 4)] for title, _ in selected},
    }
```

## File Output
```python
prs.save("output.pptx")
print(f"Saved {len(prs.slides)} slides")
```

## Table Pattern
```python
# Create table
table_data = [
    ["Feature", "Option A", "Option B"],
    ["Power", "15-40W", "40-60W"],
    ["Best For", "SMD", "Through-hole"],
]

rows = len(table_data)
cols = len(table_data[0])
table_shape = slide.shapes.add_table(rows, cols, Inches(0.3), Inches(1.2), Inches(9.4), Inches(4))
table = table_shape.table

for r in range(rows):
    for c in range(cols):
        cell = table.cell(r, c)
        cell.text = table_data[r][c]
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(11)
            paragraph.alignment = PP_ALIGN.CENTER
            if r == 0:
                paragraph.font.bold = True
                paragraph.font.color.rgb = THEME["text_light"]
            else:
                paragraph.font.color.rgb = THEME["text_dark"]
        # Header row styling
        if r == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = THEME["primary"]
        elif r % 2 == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = THEME["bg_light"]
        else:
            cell.fill.solid()
            cell.fill.fore_color.rgb = THEME["text_light"]
```

## Multi-Card Layout Pattern
```python
# Create multiple themed cards side by side
cards = [
    ("Card 1", "Description 1", THEME["green"]),
    ("Card 2", "Description 2", THEME["accent"]),
    ("Card 3", "Description 3", THEME["red"]),
]

for i, (title, desc, color) in enumerate(cards):
    left = 0.4 + (i * 3.15)  # Spacing between cards
    
    # Card background
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(1.3), Inches(2.9), Inches(3.8))
    card.fill.solid()
    card.fill.fore_color.rgb = THEME["text_light"]
    card.line.color.rgb = color
    card.line.width = Pt(2)
    
    # Color accent bar at top
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.3), Inches(2.9), Inches(0.15))
    accent.fill.solid()
    accent.fill.fore_color.rgb = color
    accent.line.fill.background()
    
    # Title
    add_text_box(slide, left + 0.15, 1.55, 2.6, 0.4, title, 16, True, THEME["primary"])
    # Description
    add_text_box(slide, left + 0.15, 2.8, 2.6, 2, desc, 12, False, THEME["text_dark"])
```

## Colored Range Display Pattern
```python
# Display temperature/power ranges with colored boxes
ranges = [
    ("200-250°C", "Low range use case", THEME["green"]),
    ("250-320°C", "Medium range use case", THEME["accent"]),
    ("320-380°C", "High range use case", THEME["orange"]),
    ("380-450°C", "Maximum range use case", THEME["red"]),
]

for i, (label, use_case, color) in enumerate(ranges):
    top = 1.3 + (i * 0.95)
    
    # Colored box
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(top), Inches(2), Inches(0.8))
    box.fill.solid()
    box.fill.fore_color.rgb = color
    box.line.fill.background()
    
    # Label in box
    add_text_box(slide, 0.6, top + 0.15, 1.8, 0.5, label, 18, True, THEME["text_light"], PP_ALIGN.CENTER)
    # Description next to box
    add_text_box(slide, 2.8, top + 0.2, 6.5, 0.4, use_case, 14, False, THEME["text_dark"])
```

## Tips
- Use `slide_layouts[6]` (blank) for full control
- 16:9 widescreen: `Inches(10) x Inches(5.625)`
- RGBColor takes hex values: `RGBColor(0x1E, 0x3A, 0x5F)`
- Set `line.fill.background()` to remove shape borders
- Use `word_wrap = True` on text frames for long text
- For tables, use `add_table()` method and style cells in loops
- For multi-card layouts, calculate `left = start + (i * spacing)` for even distribution
- Watch for mismatched parentheses when building THEME dict lookups

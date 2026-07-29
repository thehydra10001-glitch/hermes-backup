---
name: multimedia-production
description: "Generate videos, PDFs, and images with fallback chains. Covers manim→moviepy video fallback, fpdf2 PDF generation, and PIL text rendering."
version: 1.0.0
platforms: [linux, macos, windows]
---

# Multimedia Production

## When to use
User requests: video creation, PDF generation, image creation, document formatting, explainer videos, slide-to-PDF conversion, or any multimedia output from text/code content.

## Video Creation Fallback Chain

### Primary: Manim CE (rich animations)
```bash
# Check prerequisites first
pkg-config --cflags pango 2>/dev/null && echo "OK" || echo "MISSING"
pip install manim 2>&1 | tail -5
```
**Requires:** `libpango1.0-dev`, `libcairo2-dev`, `pkg-config` system packages.
If manim fails to install (manimpango wheel build error), fall back immediately.

### Fallback: Moviepy + PIL (simple explainer videos)
```bash
pip install moviepy pillow
```
**Pattern:** Pre-generate frames with PIL/Pillow, compose into video with moviepy.
- Use PIL for text rendering (manim's TextClip requires ImageMagick which may also be missing)
- Generate all frames first, then create VideoClip from frame array
- Optimize: lower resolution (720x1280), lower FPS (15), shorter scenes (3s)
- Export: `write_videofile(output, fps=15, codec='libx264', audio=False)`

**Speed optimization:** Generate frames once, reuse for static scenes. Avoid per-frame computation.

## PDF Generation

### Tool: fpdf2
```bash
pip install fpdf2
```

**Pattern:** Create a custom FPDF subclass for consistent styling.
- Define `header()`, `footer()`, `chapter_title()`, `body_text()`, `code_block()`, `bullet()` methods
- Use `multi_cell()` for wrapped text, `cell()` for single-line
- Code blocks: use Courier font, light gray fill background
- Tables: manual cell placement with borders
- Avoid Unicode bullet characters (chr(8226)) — use `-` instead, Helvetica doesn't support them

**Font limitation:** fpdf2 core fonts (Helvetica, Courier, Times) are Latin-1 only. For Unicode content, use `pdf.add_font()` with TTF files.

**API Response Sanitization:** When embedding API responses (especially from Chinese services), always sanitize first:
```python
def sanitize_for_pdf(text):
    """Remove non-Latin-1 characters from API responses."""
    return text.encode('ascii', 'ignore').decode('ascii')

# Example: Chinese error message in API response
raw = '{"code":"400","message":"请求体不能为空"}'
clean = sanitize_for_pdf(raw)
# Result: '{"code":"400","message":""}' -- Chinese removed safely
```

**ASCII art in code blocks:** Keep lines < 70 chars for Courier 7pt. Longer lines cause "Not enough horizontal space" errors. See [references/fpdf2-pattern.md](references/fpdf2-pattern.md) for details.

## Sudo Restriction Workaround

Hermes blocks `sudo -S` password piping for security. When sudo is needed:
1. Create a shell script with the commands
2. Give user the path to run manually: `bash /path/to/script.sh`
3. Script should include verification commands to confirm success

## PowerPoint Generation

### Tool: python-pptx
```bash
pip install python-pptx
```

**Pattern:** Define themes as dicts with RGBColor values, generate content from topic, build slides programmatically.

**Key settings:**
```python
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(5.625)  # 16:9 widescreen
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
```

**Reference:** See [references/python-pptx-patterns.md](references/python-pptx-patterns.md) for theme configs, slide builders, and content generation templates.

**Note:** For more advanced PPT needs (templates, editing existing decks, visual QA), use the `powerpoint` skill.

## Cross-Platform Notes

- **Linux:** Check `apt` packages before pip installs that need C extensions
- **Windows:** Use `fpdf2` (not reportlab) for simpler setup
- **macOS:** May need `brew install pkg-config pango` for manim

## PEP 668 / Managed Python Workaround

On systems with PEP 668 (externally-managed-environment), `pip install` fails with "This environment is externally managed". Always use a temporary venv:

```bash
python3 -m venv /tmp/media-venv
/tmp/media-venv/bin/pip install fpdf2 youtube-transcript-api pillow
# Then run scripts with:
/tmp/media-venv/bin/python3 your_script.py
```

This applies to Kali, Ubuntu 23.04+, Debian 12+, Fedora, and Arch. Check with `python3 -c "import sys; print(sys.prefix)"` — if it's `/usr`, you need a venv.

---
name: document-extraction-fallbacks
description: "Fallback chains for extracting text from documents when primary tools fail — legacy .doc, scanned PDFs without OCR, and PEP 668 workarounds."
version: 1.0.0
author: Hermes Agent
platforms: [linux, macos, windows]
---

# Document Extraction Fallbacks

Use this skill when the primary extraction tools (pypdf, pymupdf, python-docx, marker-pdf) return empty text, fail to install, or the document is in a format they don't support.

## Decision Tree

```
Document received
├── URL available? → web_extract(urls=[...])
├── Native text PDF? → pypdf or pymupdf
├── DOCX file? → python-docx
├── Legacy .doc (Word 97-2003)? → See §Legacy .doc
├── Scanned PDF (0 chars from pymupdf/pypdf)? → See §Scanned PDF
├── EPUB? → pymupdf (native support)
└── Unknown binary? → file command to detect format first
```

## Step 1: Identify the Format

Always run `file` on the document first — the extension may lie:

```bash
file document.xyz
# Output: "Composite Document File V2" = legacy .doc
# Output: "PDF document" = PDF (but may be scanned)
# Output: "XML Document" = could be DOCX (ZIP-based)
```

## Step 2: Legacy .doc (Word 97-2003)

python-docx CANNOT read legacy .doc files (OLE Compound Document format). Use one of:

### Method A: `strings` (Quick, No Install)

Works for mostly-text documents. Captures readable ASCII content:

```bash
strings "document.doc" | head -200
```

Also reveals metadata (title, author, creation date, character/word counts).

### Method B: `catdoc` (Better Formatting)

```bash
# Install
sudo apt install catdoc    # Debian/Ubuntu/Kali
brew install catdoc         # macOS

# Extract
catdoc document.doc
```

### Method C: `antiword` (Layout Preservation)

```bash
sudo apt install antiword
antiword document.doc
```

### Method D: LibreOffice Headless (Best Fidelity)

```bash
# Convert to DOCX first, then use python-docx
libreoffice --headless --convert-to docx document.doc
python3 -c "
from docx import Document
doc = Document('document.docx')
for p in doc.paragraphs:
    if p.text.strip():
        print(p.text)
"
```

## Step 3: Scanned PDF (Image-Only, No Embedde Text)

When pymupdf or pypdf return 0 characters for every page, the PDF is scanned images. Extraction options:

### Option A: Ghostscript → ImageMagick → vision_analyze

No OCR needed — use the agent's vision Model:

```bash
# 1. Convert PDF pages to PNG images with Ghostscript
mkdir -p /tmp/pdf_pages
gs -dNOPAUSE -dBATCH -sDEVICE=png16m -r300 \
   -sOutputFile=/tmp/pdf_pages/page_%d.png document.pdf

# 2. Resize smaller with ImageMagick (vision APIs have size limits)
mkdir -p /tmp/pdf_small
for i in 1 2 3 4 5 6 7; do
  convert /tmp/pdf_pages/page_${i}.png \
    -resize 50% -quality 85 /tmp/pdf_small/page_${i}.jpg
done

# 3. Pass each page to vision_analyze
vision_analyze(
    image_url="file:///tmp/pdf_small/page_1.jpg",
    question="Extract ALL text from this document page word-for-word."
)
```

**Pitfalls:**
- vision_analyze may reject large images → resize to 25% or JPEG quality 70
- Base64 data URIs can exceed API limits → use `file://` paths instead
- Vision APIs have rate limits → send one page at a time
- Some models lack native vision → falls back to aux vision model which may fail

### Option B: Install Tesseract OCR (System)

Best for batch/automated extraction:

```bash
sudo apt install tesseract-ocr tesseract-ocr-eng  # Debian/Ubuntu/Kali
pip3 install --break-system-packages pytesseract    # PEP 668 systems
```

```python
import pytesseract
from PIL import Image
for i in range(1, 8):
    text = pytesseract.image_to_string(Image.open(f"/tmp/pdf_pages/page_{i}.png"))
    print(f"--- Page {i} ---\n{text}")
```

### Option C: marker-pdf (High-Quality, ~3-5GB)

When the document has complex layout (tables, equations, multi-column):

```bash
pip install marker-pdf
marker_single document.pdf --output_dir ./output
```

See the `ocr-and-documents` skill for full marker-pdf usage.

## Step 4: PEP 668 (Python Package Protection)

On Kali, Debian 12+, and other modern distros, `pip install` is blocked for system Python:

```
error: externally-managed-environment
× This environment is externally managed
```

**Solution A** — `--break-system-packages` (safe on single-user systems):
```bash
pip3 install --break-system-packages pymupdf pytesseract
```

**Solution B** — Use a virtual environment:
```bash
python3 -m venv /tmp/pdf_venv
source /tmp/pdf_venv/bin/activate
pip install pymupdf pytesseract
```

**Solution C** — System packages (`apt`):
```bash
sudo apt install python3-pymupdf tesseract-ocr  # if available
```

## Reference Files

- `references/q-codes.md` — Compiled Q-code reference table (from extracted .doc)
- `references/asoc-exam-sample.md` — ASOC exam sample questions (100 Q&A)

## Verification

After extraction, always verify:
- [ ] Total character count > 0 (text was actually extracted)
- [ ] Page-by-page content matches expected document structure
- [ ] No encoding artifacts (garbled Unicode, repeated strings from binary data)
- [ ] For scanned docs: compare a sample against the visual page
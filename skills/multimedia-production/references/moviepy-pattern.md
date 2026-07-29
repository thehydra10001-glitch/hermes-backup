# Moviepy + PIL Video Creation Pattern

## Proven Code Template

```python
#!/usr/bin/env python3
"""Create explainer video using moviepy + PIL for text rendering."""
from moviepy import VideoClip, concatenate_videoclips
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 720, 1280  # Vertical (9:16)
FPS = 15
SCENE_DURATION = 3  # seconds per scene

BG_COLOR = (15, 15, 35)
GOLD = (200, 169, 81)
WHITE = (255, 255, 255)
CYAN = (0, 245, 255)

def get_font(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in paths:
        try: return ImageFont.truetype(path, size)
        except: continue
    return ImageFont.load_default()

def create_frame(lines, font_sizes=None, colors=None, bg_color=BG_COLOR):
    img = Image.new('RGB', (WIDTH, HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)
    if font_sizes is None: font_sizes = [50] * len(lines)
    if colors is None: colors = [WHITE] * len(lines)
    
    total_height = 0
    line_data = []
    for line, size, color in zip(lines, font_sizes, colors):
        font = get_font(size)
        bbox = draw.textbbox((0, 0), line, font=font)
        text_height = bbox[3] - bbox[1]
        line_data.append((line, font, color, text_height))
        total_height += text_height + 15
    
    y = (HEIGHT - total_height) // 2
    for line, font, color, text_height in line_data:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        draw.text((x, y), line, fill=color, font=font)
        y += text_height + 15
    return np.array(img)

# Pre-generate all frames (once)
frames = {
    'title': create_frame(["TITLE", "SUBTITLE"], font_sizes=[60, 40], colors=[GOLD, WHITE]),
    'content': create_frame(["Line 1", "Line 2"], font_sizes=[40, 35], colors=[WHITE, CYAN]),
}

# Create clips
clips = [
    VideoClip(lambda t: frames['title'], duration=SCENE_DURATION).with_fps(FPS),
    VideoClip(lambda t: frames['content'], duration=SCENE_DURATION).with_fps(FPS),
]

final = concatenate_videoclips(clips)
final.write_videofile("output.mp4", fps=FPS, codec='libx264', audio=False)
```

## Key Optimizations
1. Pre-generate all frames before creating clips
2. Use static lambda: `lambda t: frames[name]` (no per-frame computation)
3. Lower resolution (720x1280) and FPS (15) for speed
4. Short scenes (3s) reduce total frame count
5. PIL handles text rendering (no ImageMagick dependency)

## Font Fallback Chain
1. DejaVuSans-Bold.ttf (best)
2. DejaVuSans.ttf (fallback)
3. ImageFont.load_default() (last resort, tiny)

## Resolution Presets
| Use Case | Width | Height | FPS |
|----------|-------|--------|-----|
| WhatsApp status | 720 | 1280 | 15 |
| Instagram reel | 1080 | 1920 | 30 |
| YouTube short | 1080 | 1920 | 30 |
| Landscape demo | 1280 | 720 | 15 |

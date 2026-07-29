---
name: video-creation
description: Create videos programmatically using moviepy. Fallback when manim can't be installed due to missing system dependencies.
tags: [video, moviepy, animation, media]
triggers:
  - create video
  - make video
  - animate
  - explainer video
  - video production
---

# Video Creation with moviepy

Use when manim can't be installed (missing pango/cairo dev headers, no root access) but the user needs a programmatic video.

## When to Use

- Manim installation fails with `Failed to build manimpango`
- User needs a simple text-based explainer video
- No LaTeX math rendering required
- Quick title cards, motion graphics, or text animations

## Installation

```bash
pip3 install moviepy --break-system-packages
```

## Basic Pattern

```python
from moviepy import VideoClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import numpy as np

WIDTH, HEIGHT = 720, 1280  # Vertical (9:16)
FPS = 15

def create_frame(text, font_size=50, color=(255,255,255), bg_color=(15,15,35)):
    img = Image.new('RGB', (WIDTH, HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (WIDTH - (bbox[2] - bbox[0])) // 2
    y = (HEIGHT - (bbox[3] - bbox[1])) // 2
    draw.text((x, y), text, fill=color, font=font)
    return np.array(img)

# Pre-generate frames
frame1 = create_frame("Title", font_size=70, color=(200,169,81))
frame2 = create_frame("Content", font_size=50)

# Create clips
clip1 = VideoClip(lambda t: frame1, duration=3).with_fps(FPS)
clip2 = VideoClip(lambda t: frame2, duration=3).with_fps(FPS)

# Concatenate and export
final = concatenate_videoclips([clip1, clip2])
final.write_videofile("output.mp4", fps=FPS, codec='libx264', audio=False)
```

## PIL Font Fallback

```python
def get_font(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()
```

## Tips

- Pre-generate all frames before creating clips (faster than generating on-the-fly)
- Use `logger=None` in `write_videofile` to suppress verbose output
- Lower FPS (15) and resolution (720x1280) for faster rendering
- moviepy has no LaTeX support — use PIL for all text rendering

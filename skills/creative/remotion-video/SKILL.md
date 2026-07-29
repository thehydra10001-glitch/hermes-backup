---
name: remotion-video
description: "Create programmatic videos with React using Remotion — install, scaffold, preview, render, and export MP4/MOV/GIF."
tags: [video, react, animation, remotion, render]
---

# Remotion — Programmatic Videos with React

## What is Remotion?
Remotion lets you create videos using React components. You write JSX, it renders frame-by-frame into MP4, MOV, GIF, or image sequences.

## Prerequisites
- Node.js >= 18 (install via `apt install nodejs npm` if missing)
- ffmpeg (for rendering): `sudo apt install ffmpeg`

## Quick Start (new project)

```bash
npx create-video@latest --yes --blank my-video
cd my-video
npm install
npm run dev        # Opens Remotion Studio in browser
```

## Add Remotion Skills (LLM-friendly presets)

```bash
npx -y skills@latest add remotion-dev/skills -g -y
npx remotion skills add
```

This adds pre-built components (subtitles, transitions, animations, etc.) to your project.

## Project Structure

```
my-video/
  src/
    Root.tsx          # Composition registration
    MyComposition.tsx # Your video component
  public/             # Static assets (images, fonts)
  remotion.config.ts  # Remotion config
```

## Key Commands

| Command | What it does |
|---------|-------------|
| `npm run dev` | Start Remotion Studio (browser preview) |
| `npx remotion render src/index.ts MyComp out/video.mp4` | Render to MP4 |
| `npx remotion render src/index.ts MyComp out/video.gif --image-format=png` | Render to GIF |
| `npx remotion still src/index.ts MyComp out/frame.png --frame=0` | Render single frame |
| `npx remotion upgrade` | Upgrade all Remotion packages |

## Creating a Composition

```tsx
// src/MyComposition.tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';

export const MyComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const opacity = interpolate(frame, [0, 30], [0, 1]);
  const scale = spring({ frame, fps, config: { damping: 10 } });
  
  return (
    <AbsoluteFill style={{ backgroundColor: '#111', justifyContent: 'center', alignItems: 'center' }}>
      <h1 style={{ color: 'white', fontSize: 80, opacity, transform: `scale(${scale})` }}>
        Hello Remotion!
      </h1>
    </AbsoluteFill>
  );
};
```

Register in Root.tsx:
```tsx
import { Composition } from 'remotion';
import { MyComposition } from './MyComposition';

export const RemotionRoot: React.FC = () => (
  <Composition id="MyComp" component={MyComposition} durationInFrames={150} fps={30} width={1920} height={1080} />
);
```

## Rendering Tips

- **MP4**: requires `ffmpeg` installed on the system
- **GIF**: use `--image-format=png` for transparency support
- **Frames**: `--frames=0-30` to render a subset
- **Concurrency**: `--concurrency=4` to speed up rendering
- **Codec**: `--codec=h264` (default) or `--codec=vp8` for webm

## Common Pitfalls

1. **ffmpeg not found** → `sudo apt install ffmpeg`
2. **White screen in Studio** → check browser console for React errors
3. **Slow rendering** → reduce resolution or use `--concurrency`
4. **Memory issues** → render in chunks with `--frames`
5. **Font loading** → use `@remotion/google-fonts` or load via CSS `@font-face`

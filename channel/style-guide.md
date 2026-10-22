# Visual Style Guide

Every frame of every video follows this guide. The content agent reads it before making anything.

## Format

- **YouTube Shorts only:** vertical **9:16**, **1080 × 1920 px**, 30 fps, under 60 seconds.
- **Safe zones:** YouTube's interface covers parts of the screen, so keep text and key subjects inside the safe area:
  - Top 250 px: avoid (search bar, channel name)
  - Bottom 420 px: avoid (title, description, music tag)
  - Right 140 px: avoid (like, comment and share buttons)
  - **Safe area:** x 60–940, y 250–1500

## Look: cozy lo-fi anime illustration

Hand-painted 2D anime illustration in a cozy "lo-fi study" mood, inspired by Studio Ghibli backgrounds and lo-fi
music artwork.

- **Lighting is the star.** Most scenes are at night or dusk. One **warm practical light source** (a desk lamp,
  a window glow, a screen, a candle) lights the subject in amber. Everything else falls into soft blue-teal shadow.
  Warm light against cool shadow is the signature of the look.
- **Rendering:** clean dark-brown line art (not black), flat **cel shading** with one or two shadow tones,
  soft painted gradients in skies and backgrounds, and a subtle paper-grain texture. No 3D, no photorealism,
  no glossy digital airbrushing.
- **Cozy, lived-in detail:** plants, mugs, books, pencils, sticky notes, posters and a sleepy cat. Rooms feel
  real and slightly cluttered. Science subjects appear **inside this world**, for example a glowing brain model
  on the desk, a microscope by the window, or stars and planets seen through the glass.
- **Characters:** simple anime proportions, soft rounded faces, small noses, expressive eyebrows,
  calm or curious expressions, cozy clothes (knits, scarves, hoodies) in muted colours.
- **Mood:** calm, curious, a little melancholic. Never loud, never neon.

## Colour palette

Muted, warm and slightly desaturated, like an old poster under a lamp.

| Role | Colour | Hex |
|---|---|---|
| Night sky / deep shadow | Ink blue | `#1E2433` |
| Mid shadow | Slate teal | `#33495A` |
| Lamp light / highlights | Warm amber | `#F2B66D` |
| Window lights | Soft yellow | `#F4D27A` |
| Wood, warm metal | Copper | `#C8653A` |
| Clothing, plants | Forest green | `#2F5D50` |
| Accents (scarf, books) | Brick red | `#B5443B` |
| Cat, warm accents | Tabby orange | `#E07B39` |
| Paper, mugs | Cream | `#EFE3C8` |
| Line art, hair | Dark brown | `#3B2A24` |

Rule: about 60% cool shadow tones, 30% mid tones, and 10% warm light. The warm light is what pulls the eye.

## Our recurring character: Atlas (proposal, see `channel/character.md`)

The channel needs **one original host character** who appears in every Short, studying, wondering and discovering.
Design them once, write the description here, and reuse it word for word in every prompt for consistency.

> **Do not copy the Lofi Girl.** She is a trademarked character. Avoid her combination of brown ponytail,
> big headphones, red scarf, green sweater, an orange cat in the window, and the desk-at-the-window
> composition. Our character and room must be clearly our own.

## Typography (on-screen text)

- **Font:** a soft, slightly hand-made display font, e.g. *Fredoka SemiBold*, *Quicksand Bold* or *Comfortaa Bold*.
  CapCut and Canva both have these.
- **Hook text:** 90–110 px, **cream** `#EFE3C8`, max **6 words**, 1–2 lines, centred within the safe area.
- Highlight one key word in **amber** `#F2B66D`.
- Add a soft dark shadow or a semi-transparent ink-blue box behind the text so it reads over detailed art.
- Captions during narration: 60–70 px, same treatment, placed at y ≈ 1250–1450.

## The first frame (the hook frame)

The first frame decides whether people swipe past. It must:
1. Show the topic's **main subject** clearly within half a second. Light it with the warm light.
2. Carry the **hook text** (max 6 words) that creates curiosity or stakes.
3. Contain **something unexpected inside the cozy scene**, e.g. the desk lamp lighting a brain that is
   rinsing itself, or a tiny black hole in the coffee mug.
4. Look good **as a still**, because it also works as the Shorts cover image.

## AI generation prompt base (Higgsfield)

Start every image prompt with this base, then add the character description and the scene:

> Cozy lo-fi anime illustration, hand-painted 2D, Studio Ghibli inspired background art, clean dark-brown line art,
> soft cel shading, subtle paper grain texture, nighttime, a single warm amber desk lamp glow (#F2B66D)
> contrasting with deep blue-teal shadows (#1E2433, #33495A), muted earthy palette of copper, forest green,
> brick red and cream, lived-in cozy details, calm contemplative mood, vertical 9:16 composition,
> main subject in the upper-middle area, no text, no watermark, no 3D, not photorealistic,

Add on-screen text later in the editor or as an overlay, not in the AI image, because AI-generated text is unreliable.

**Originality:** the style is *inspired by* lo-fi and Ghibli-style art. Never recreate the Lofi Girl, Ghibli
characters, or any other existing character, logo or specific scene.

## Without Higgsfield

This painted style can't be drawn convincingly with code. If Higgsfield is unavailable, the agent may only make a
**layout sketch** (`tools/render_frame.py`) showing where the subject, light and text go. It must label it as a
sketch, not a style preview, and it does not count as an approved first frame.

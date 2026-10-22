# Visual Style Guide

Every frame of every video follows this guide. The content agent reads it before making anything.

**Master reference:** `channel/reference/atlas-reference.webp`, approved by the creator. When this text and the
reference image disagree, the image wins. Attach it as a reference image whenever the generator supports it.

## Format

- **YouTube Shorts only:** vertical **9:16**, **1080 × 1920 px**, 30 fps, under 60 seconds.
- **Safe zones:** YouTube's interface covers parts of the screen, so keep text and key subjects inside the safe area:
  - Top 250 px: avoid (search bar, channel name)
  - Bottom 420 px: avoid (title, description, music tag)
  - Right 140 px: avoid (like, comment and share buttons)
  - **Safe area:** x 60–940, y 250–1500

## Look: cozy cinematic storybook

Richly detailed, **painterly storybook illustration with a cinematic, lightly 3D feel**, like a high-end animated
film's concept art. Think a warm mountain-cabin observatory at night under a sky full of stars.

- **Lighting is the star.** Night or dusk. **Warm lantern and candle light** (golden, flickering) lights the subject.
  It contrasts with a **deep blue-violet starry sky** and cool blue shadows. Small practical lights (oil lanterns,
  a glowing mug, distant cabin windows) add depth.
- **Rendering:** soft painterly detail with real texture: **individual fur strands**, chunky knit wool, worn leather,
  aged brass, old paper. Gentle depth of field (soft background bokeh). Rich, glowing, but never glossy plastic CGI.
- **Sky:** a dense star field with the **Milky Way**, the occasional shooting star, and dusk gradients of magenta,
  orange and violet over mountain silhouettes.
- **World:** a timber **cabin observatory** high in the mountains, with big windows looking over pine forest, a lake
  and a few twinkling town lights far below. Inside: a brass telescope, leather-bound books, star charts and
  constellation sketches pinned to the walls, a brass armillary globe, oil lanterns, plants, quills and parchment.
- **Science subjects live inside this world.** They appear on the desk, through the telescope, inside a glass dome,
  or in the journal's sketches, lit by the same warm light.
- **Mood:** cozy, curious, wonder-filled. Calm, never loud or neon.

## Colour palette

| Role | Colour | Hex |
|---|---|---|
| Night sky (deep) | Midnight navy | `#141A2E` |
| Night sky (Milky Way) | Star violet | `#4B3F72` |
| Lantern light / highlights | Lantern gold | `#FFB347` |
| Warm glow, flames | Ember orange | `#E8892B` |
| Atlas's cardigan | Mustard | `#D4A021` |
| Atlas's scarf, pines | Pine green | `#2E4A2F` |
| Leather, wood | Saddle brown | `#6B4226` |
| Telescope, glasses, instruments | Aged brass | `#B08D57` |
| Dusk sky accent | Dusk rose | `#C2577A` |
| Paper, star charts | Parchment | `#E9DCC0` |

Rule: about 60% deep night tones, 30% warm wood and fabric mid-tones, and 10% bright lantern gold. The gold pulls the eye.

## Our recurring character: Atlas

Atlas is our approved host. See `channel/character.md` for his exact description and props. Use that description
word for word in every prompt where he appears.

## Typography (on-screen text)

- **Font:** a warm storybook serif or a soft rounded display font, e.g. *Fraunces Bold*, *Recoleta* or *Quicksand Bold*.
  CapCut and Canva have similar fonts.
- **Hook text:** 90–110 px, **parchment** `#E9DCC0`, max **6 words**, 1–2 lines, centred within the safe area.
- Highlight one key word in **lantern gold** `#FFB347`.
- Add a soft dark shadow or a semi-transparent midnight-navy box behind the text so it reads over detailed art.
- Captions during narration: 60–70 px, same treatment, placed at y ≈ 1250–1450.

## The first frame (the hook frame)

The first frame decides whether people swipe past. It must:
1. Show the topic's **main subject** clearly within half a second, lit by lantern light.
2. Carry the **hook text** (max 6 words) that creates curiosity or stakes.
3. Contain **something unexpected inside the cozy scene**, e.g. a crystal with a heartbeat under a glass dome,
   or a tiny black hole swirling inside Atlas's mug.
4. Look good **as a still**, because it also works as the Shorts cover image.

## AI generation prompt base (Higgsfield)

Start every image or video prompt with this base, then add Atlas's description (if he's in the shot) and the scene:

> Cozy cinematic storybook illustration, richly detailed painterly style with a soft 3D animated-film feel,
> detailed fur and fabric textures, warm golden oil-lantern light (#FFB347) contrasting with a deep navy and violet
> starry night sky with the Milky Way (#141A2E, #4B3F72), timber mountain cabin observatory, aged brass instruments,
> leather-bound books and star charts, gentle depth of field, magical calm mood, vertical 9:16 composition,
> main subject in the upper-middle area,

**Negative prompt:** text, letters, words, watermark, logo, subtitles, flat vector, cel shading, anime, harsh
lighting, neon colours, glossy plastic CGI, photorealistic photo, extra limbs, distorted paws, extra fingers,
blurry face, morphing objects, fast camera movement

Add on-screen text later in the editor or as an overlay, not in the AI image, because AI-generated text is unreliable.

**Originality:** never recreate existing characters (e.g. Rocket Raccoon, the Lofi Girl, other channels' mascots),
logos or specific scenes from films.

## Consistency tips

- Always attach `channel/reference/atlas-reference.webp` (or the approved first frame) as a reference image when the model allows it.
- Keep Atlas's outfit identical in every shot: mustard cardigan, brown elbow patches, green scarf, brass glasses, satchel.
- Keep the same home base so the world feels continuous: the cabin observatory, the telescope and the lanterns.

## Without Higgsfield

This detailed style can't be drawn convincingly with code. If Higgsfield is unavailable, the agent may only make a
**layout sketch** (`tools/render_frame.py`) showing where the subject, light and text go. It must label it as a
sketch, not a style preview, and it does not count as an approved first frame.

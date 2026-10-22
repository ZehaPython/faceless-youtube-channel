# time-crystals: first frame and opening shot (v2)

Replaces v1 (lo-fi anime style, no character). Matches the approved reference `channel/reference/atlas-reference.webp`.

## Step 1: still image (the first frame) on the Higgsfield website
- Model: **Nano Banana Pro** (or another image model that accepts a reference image)
- Reference image: upload `channel/reference/atlas-reference.webp`
- Aspect ratio: **9:16**

### Prompt
Cozy cinematic storybook illustration, richly detailed painterly style with a soft 3D animated-film feel,
detailed fur and fabric textures, warm golden oil-lantern light contrasting with a deep navy and violet starry night
sky with the Milky Way, timber mountain cabin observatory, aged brass instruments, leather-bound books and star charts,
gentle depth of field, magical calm mood, vertical 9:16 composition, main subject in the upper-middle area.
Atlas, a stocky middle-aged raccoon astronomer with soft, detailed grey and brown fur, a dark eye mask, warm brown eyes
and a kind, slightly smug smile, wearing thin round gold wire-rimmed glasses, a chunky mustard-yellow cable-knit
cardigan with brown leather elbow patches and wooden buttons, a thick knitted pine-green scarf, and a worn brown
leather satchel on a strap across his body. Big fluffy ringed tail.
Atlas leans over his wooden desk, eyes wide with wonder, gazing at a small glass dome. Inside the dome floats a tiny
crystal made of glowing points of light arranged in a neat lattice, pulsing teal and gold, lighting his face and
glasses from below. On the desk: a brass oil lantern, a steaming navy enamel mug with a white pine-tree pattern,
an open leather-bound star atlas with a quill, and an old brass pocket watch with a cracked glass face.
Behind him, a large window shows snowy mountains, a dark pine forest, a lake and the Milky Way with a shooting star.

### Negative prompt
text, letters, words, watermark, logo, subtitles, flat vector, cel shading, anime, harsh lighting, neon colours,
glossy plastic CGI, photorealistic photo, extra limbs, distorted paws, extra fingers, blurry face

## Step 2: animate the approved still (opening shot, 5 s)
- Model: **Kling 3.0, image-to-video**, using the approved still from step 1
- Aspect ratio 9:16 · Duration 5 s · Audio off

### Motion prompt
The crystal inside the glass dome pulses in a slow, perfectly steady rhythm like a heartbeat, its light points
flipping between teal and gold. Atlas blinks slowly and leans a little closer, his glasses reflecting the pulses.
The lantern flame flickers softly, steam rises from the mug, stars twinkle outside the window.
Slow, gentle camera push-in toward the dome. Atlas's appearance stays exactly the same.

### Negative prompt
morphing, changing outfit, extra limbs, distorted paws, flickering face, text, watermark, fast camera movement

## Hook text (added in the editor)
"This Crystal Has a **Heartbeat**": 5 words, "Heartbeat" in lantern gold #FFB347.

"""Assemble a finished Short: clips + voiceover + hook text + burned-in captions -> MP4.

Reads scenes.json and captions.json from the production folder. The voiceover is sped up
by scenes.json's voice_speed (to fit under 60 s), and every scene and caption time is
scaled to match. Clips shorter than their scene are slowed down to fit; longer ones are trimmed.

Usage:
    python tools/assemble_short.py production/time-crystals [--out final/time-crystals-v1.mp4]
"""

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

W, H, FPS = 1080, 1920, 30
MAX_WORDS = 5
CLOUD_CHROMIUM = "/opt/pw-browsers/chromium"

# Same treatment as the approved first frame (channel/style-guide.md).
TEXT_HTML = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,800&display=block" rel="stylesheet">
<style>
html,body{{margin:0;width:{w}px;height:{h}px;background:transparent;overflow:hidden}}
.shade{{position:absolute;left:0;right:0;top:{shade_top}px;height:{shade_h}px;
  background:linear-gradient(to bottom,rgba(20,26,46,0),rgba(20,26,46,.72) 30%,rgba(20,26,46,.72) 75%,rgba(20,26,46,0))}}
.t{{position:absolute;left:60px;width:880px;top:{top}px;text-align:center;font-family:'Fraunces',Georgia,serif;
  font-weight:800;font-size:{size}px;line-height:1.1;color:#E9DCC0;text-shadow:0 4px 18px rgba(0,0,0,.7)}}
.t b{{color:#FFB347}}
</style></head><body><div class="shade"></div><div class="t">{text}</div></body></html>"""


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def chunk_phrase(start, end, text):
    """Split a phrase into captions of at most MAX_WORDS words, timed by word count."""
    words, bold, tagged = text.split(), False, []
    for w in words:
        opens, closes = w.startswith("<b>"), w.endswith("</b>")
        plain = w.replace("<b>", "").replace("</b>", "")
        bold = bold or opens
        tagged.append((plain, bold))
        if closes:
            bold = False
    n = max(1, -(-len(tagged) // MAX_WORDS))
    size = -(-len(tagged) // n)  # balance chunk sizes
    chunks, t = [], start
    per_word = (end - start) / len(tagged)
    for i in range(0, len(tagged), size):
        part = tagged[i:i + size]
        html = " ".join(f"<b>{w}</b>" if b else w for w, b in part)
        chunks.append([t, t + per_word * len(part), html])
        t += per_word * len(part)
    return chunks


def render_pngs(items, folder):
    """Render each (html_text, kind) to a transparent 1080x1920 PNG."""
    paths = []
    with sync_playwright() as p:
        launch = {"executable_path": CLOUD_CHROMIUM} if Path(CLOUD_CHROMIUM).is_file() else {}
        browser = p.chromium.launch(**launch)
        page = browser.new_page(viewport={"width": W, "height": H})
        for i, (text, kind) in enumerate(items):
            if kind == "hook":
                html = TEXT_HTML.format(w=W, h=H, shade_top=1180, shade_h=420, top=1270, size=104, text=text)
            else:
                html = TEXT_HTML.format(w=W, h=H, shade_top=1230, shade_h=300, top=1300, size=72, text=text)
            page.set_content(html)
            page.wait_for_load_state("networkidle")
            path = folder / f"text-{i:03d}.png"
            page.screenshot(path=str(path), omit_background=True)
            paths.append(path)
        browser.close()
    return paths


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("folder")
    p.add_argument("--out")
    args = p.parse_args()

    root = Path(args.folder)
    plan = json.loads((root / "scenes.json").read_text(encoding="utf-8"))
    caps = json.loads((root / "captions.json").read_text(encoding="utf-8"))
    speed = plan["voice_speed"]
    voice = root / plan["voiceover"]
    total = duration(voice) / speed
    out = root / (args.out or f"final/{plan['slug']}-v1.mp4")
    out.parent.mkdir(parents=True, exist_ok=True)

    # Scene windows in final (sped-up) time; each scene runs until the next one starts.
    scenes = plan["scenes"]
    starts = [s["start"] / speed for s in scenes] + [total]
    inputs, filters = [], []
    for i, s in enumerate(scenes):
        clip = root / "clips" / f"{s['id']}.mp4"
        want = starts[i + 1] - starts[i]
        have = duration(clip)
        stretch = max(1.0, want / have)  # slow down short clips; never speed up
        inputs += ["-i", str(clip)]
        filters.append(f"[{i}:v]setpts={stretch:.4f}*(PTS-STARTPTS),fps={FPS},"
                       f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
                       f"trim=duration={want:.3f},setpts=PTS-STARTPTS[v{i}]")
    filters.append("".join(f"[v{i}]" for i in range(len(scenes))) + f"concat=n={len(scenes)}:v=1:a=0[base]")

    # Text overlays: hook first, then captions. Each caption holds until the next one (max +0.6 s).
    items = [(caps["hook"]["text"], "hook", 0.0, caps["hook"]["end"] / speed)]
    chunks = [c for ph in caps["phrases"] for c in chunk_phrase(*ph)]
    for j, (a, b, text) in enumerate(chunks):
        nxt = chunks[j + 1][0] if j + 1 < len(chunks) else total * speed
        items.append((text, "caption", a / speed, min(nxt, b + 0.6) / speed))

    with tempfile.TemporaryDirectory() as tmp:
        pngs = render_pngs([(t, k) for t, k, _, _ in items], Path(tmp))
        last = "base"
        for k, (png, (_, _, a, b)) in enumerate(zip(pngs, items)):
            idx = len(scenes) + k
            inputs += ["-i", str(png)]
            filters.append(f"[{last}][{idx}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[o{k}]")
            last = f"o{k}"
        fade_start = max(0.0, total - 0.6)
        filters.append(f"[{last}]fade=t=out:st={fade_start:.3f}:d=0.6[vout]")
        audio_idx = len(scenes) + len(pngs)
        inputs += ["-i", str(voice)]
        filters.append(f"[{audio_idx}:a]atempo={speed},apad[aout]")

        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
               "-filter_complex", ";".join(filters), "-map", "[vout]", "-map", "[aout]",
               "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)]
        subprocess.run(cmd, check=True)
    print(f"Wrote {out} ({duration(out):.2f} s)")


if __name__ == "__main__":
    main()

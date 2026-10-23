"""Generate scene images and animated clips for a Short from its scenes.json.

Images: Qwen Image 3 Edit with the style references (Atlas reference + approved first frame).
Clips:  Kling 3.0 image-to-video, one per scene, length matched to the narration.
Files that already exist are skipped, so the run can be resumed. Billable requests.

Usage:
    python tools/produce_scenes.py production/time-crystals --stage images
    python tools/produce_scenes.py production/time-crystals --stage clips
"""

import argparse
import json
import math
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env.local", override=False)

import higgsfield_client  # noqa: E402

IMAGE_MODEL = "alibaba/qwen-image-3/edit"
VIDEO_MODEL = "kling-video/v3.0/std/image-to-video"
print_lock = threading.Lock()


def log(msg):
    with print_lock:
        print(msg, flush=True)


def upload(path):
    """Upload a local image and return its public URL. WebP is converted to PNG first."""
    path = Path(path)
    if path.suffix.lower() == ".webp":
        png = Path(tempfile.mkdtemp()) / (path.stem + ".png")
        subprocess.run(["convert", str(path), str(png)], check=True)
        path = png
    return higgsfield_client.upload_file(path)


def run(model, arguments, label):
    """Submit, wait, and return the completed result. Raises on any non-completed outcome."""
    controller = higgsfield_client.submit(model, arguments=arguments)
    log(f"[{label}] enqueued {controller.request_id}")
    result = controller.get()
    status = result.get("status")
    if status != "completed":
        raise RuntimeError(f"[{label}] final status {status!r}: {result.get('error') or 'no details'}")
    return result


def download(url, out):
    r = httpx.get(url, timeout=300, follow_redirects=True)
    r.raise_for_status()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(r.content)


def make_image(plan, scene, ref_urls, root):
    # A scene can also have an end_prompt: a second image Kling uses as the clip's last frame.
    targets = [(root / "scenes" / f"{scene['id']}.png", scene["prompt"])]
    if scene.get("end_prompt"):
        targets.append((root / "scenes" / f"{scene['id']}-end.png", scene["end_prompt"]))
    prefix = plan["atlas_prefix"] if scene.get("character") else plan["world_prefix"]
    done = []
    for out, prompt in targets:
        if out.exists():
            done.append(f"{out.name} exists, skipped")
            continue
        result = run(IMAGE_MODEL, {
            "prompt": f"{prefix}\n\nScene: {prompt}",
            "negative_prompt": plan["negative"],
            "image_urls": ref_urls,
            "aspect_ratio": "9:16",
            "resolution": "2k",
        }, out.stem)
        download(result["images"][0]["url"], out)
        done.append(f"{out.name} saved")
    return f"[{scene['id']}] " + "; ".join(done)


def make_clip(plan, scene, root):
    out = root / "clips" / f"{scene['id']}.mp4"
    if out.exists():
        return f"[{scene['id']}] clip exists, skipped"
    image = root / scene["image"] if scene.get("image") else root / "scenes" / f"{scene['id']}.png"
    seconds = (scene["end"] - scene["start"]) / plan["voice_speed"]
    duration = min(15, max(3, math.ceil(seconds)))
    arguments = {
        "image_url": upload(image),
        "prompt": f"{scene['motion']} Avoid: {plan['video_negative']}.",
        "duration": duration,
        "sound": "off",
    }
    end_image = root / "scenes" / f"{scene['id']}-end.png"
    if scene.get("end_prompt") and end_image.exists():
        arguments["last_image_url"] = upload(end_image)
    result = run(VIDEO_MODEL, arguments, scene["id"])
    url = (result.get("video") or {}).get("url")
    if not url:
        raise RuntimeError(f"[{scene['id']}] completed but no video URL; keys {sorted(result)}")
    download(url, out)
    return f"[{scene['id']}] clip saved ({duration}s)"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("folder", help="Production folder containing scenes.json")
    p.add_argument("--stage", choices=["images", "clips"], required=True)
    p.add_argument("--only", nargs="*", help="Scene ids to (re)make")
    p.add_argument("--workers", type=int, default=4)
    args = p.parse_args()

    root = Path(args.folder)
    plan = json.loads((root / "scenes.json").read_text(encoding="utf-8"))
    scenes = [s for s in plan["scenes"] if not args.only or s["id"] in args.only]

    if args.stage == "images":
        scenes = [s for s in scenes if not s.get("image")]
        ref_urls = [upload(root / r) for r in plan["style_refs"]]
        log(f"Uploaded {len(ref_urls)} style references")
        job = lambda s: make_image(plan, s, ref_urls, root)  # noqa: E731
    else:
        job = lambda s: make_clip(plan, s, root)  # noqa: E731

    failures = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(job, s): s["id"] for s in scenes}
        for f in as_completed(futures):
            try:
                log(f.result())
            except Exception as e:  # report every failure, keep going with the rest
                failures += 1
                log(f"FAILED [{futures[f]}]: {e}")
    if failures:
        sys.exit(f"{failures} scene(s) failed.")


if __name__ == "__main__":
    main()

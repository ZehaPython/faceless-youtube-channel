"""Generate an image with the Higgsfield API, optionally guided by reference images.

Default model is Qwen Image 3 Edit, which takes 1-3 reference images (e.g. the Atlas
reference) so the character stays consistent. Credentials come from HF_KEY in the
environment or .env.local; the value is never printed. This makes a billable request.

Usage:
    python tools/generate_image.py --prompt-file prompt.txt --ref channel/reference/atlas-reference.webp \
        --out production/<slug>/preview/first-frame-v2-art.png
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env.local", override=False)

import higgsfield_client  # noqa: E402
from higgsfield_client import CredentialsMissedError, HiggsfieldClientError  # noqa: E402


def upload_reference(path):
    """Upload a local image and return its public URL. WebP is converted to PNG first."""
    path = Path(path)
    if path.suffix.lower() == ".webp":
        png = Path(tempfile.mkdtemp()) / (path.stem + ".png")
        subprocess.run(["convert", str(path), str(png)], check=True)
        path = png
    return higgsfield_client.upload_file(path)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--prompt-file", required=True)
    p.add_argument("--negative-file", help="File with the negative prompt")
    p.add_argument("--ref", action="append", default=[], help="Reference image (repeat up to 3 times)")
    p.add_argument("--model", default="alibaba/qwen-image-3/edit")
    p.add_argument("--aspect-ratio", default="9:16")
    p.add_argument("--resolution", default="2k")
    p.add_argument("--out", required=True)
    args = p.parse_args()

    arguments = {
        "prompt": Path(args.prompt_file).read_text(encoding="utf-8").strip(),
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
    }
    if args.negative_file:
        arguments["negative_prompt"] = Path(args.negative_file).read_text(encoding="utf-8").strip()

    try:
        if args.ref:
            arguments["image_urls"] = [upload_reference(r) for r in args.ref]
            print(f"Uploaded {len(args.ref)} reference image(s)")
        last = []

        def on_update(status):
            # Print only when the status changes, not on every poll.
            name = type(status).__name__
            if last[-1:] != [name]:
                print(f"Status: {name}")
                last.append(name)

        result = higgsfield_client.subscribe(
            args.model,
            arguments=arguments,
            on_enqueue=lambda request_id: print(f"Request enqueued: {request_id}"),
            on_queue_update=on_update,
        )
    except CredentialsMissedError:
        sys.exit("FAILED: HF_KEY is not set.")
    except HiggsfieldClientError as e:
        sys.exit(f"FAILED: Higgsfield API error: {e}")
    except httpx.HTTPError as e:
        sys.exit(f"FAILED: network error ({type(e).__name__}: {e}).")

    status = result.get("status")
    if status != "completed":
        sys.exit(f"FAILED: final status {status!r}. Details: {result.get('error') or 'none given'}")
    images = result.get("images") or []
    if not images or not images[0].get("url"):
        sys.exit(f"FAILED: completed but no image URL. Response keys: {sorted(result)}")

    url = images[0]["url"]
    print(f"Image URL: {url}")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = httpx.get(url, timeout=120, follow_redirects=True)
        r.raise_for_status()
    except httpx.HTTPError as e:
        sys.exit(f"Generated, but download failed ({type(e).__name__}: {e}). Open the URL above instead.")
    out.write_bytes(r.content)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()

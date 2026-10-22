"""Render an SVG or HTML file to a PNG frame (default 1080x1920, YouTube Shorts).

Fallback for the preview frame when Higgsfield isn't available. Uses a headless
Chromium through Playwright, so fonts, gradients and filters render like a browser.

Usage:
    pip install playwright
    python tools/render_frame.py production/<slug>/preview/first-frame.svg
    python tools/render_frame.py frame.html -o frame.png --width 1080 --height 1920
"""

import argparse
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

# Cloud sessions ship Chromium here; on a PC Playwright uses its own install.
CLOUD_CHROMIUM = "/opt/pw-browsers/chromium"


def render(src, out, width, height):
    src = Path(src).resolve()
    with sync_playwright() as p:
        launch = {"executable_path": CLOUD_CHROMIUM} if os.path.isfile(CLOUD_CHROMIUM) else {}
        browser = p.chromium.launch(**launch)
        page = browser.new_page(viewport={"width": width, "height": height})
        # Open the file directly: a page built with set_content can't load file:// URLs.
        # SVGs should declare width/height matching the frame.
        page.goto(src.as_uri())
        page.wait_for_load_state("networkidle")
        page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": width, "height": height})
        browser.close()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("src", help="SVG or HTML file")
    p.add_argument("-o", "--out", help="PNG path (default: same name as src)")
    p.add_argument("--width", type=int, default=1080)
    p.add_argument("--height", type=int, default=1920)
    args = p.parse_args()
    out = args.out or str(Path(args.src).with_suffix(".png"))
    render(args.src, out, args.width, args.height)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

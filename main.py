"""Generate a test video with Seedance 2.5 through the Higgsfield API.

Credentials come from HF_KEY ("key-id:key-secret"), read from .env.local or the
environment. The value is never printed or logged.

Usage:
    pip install -r requirements.txt
    python main.py
"""

import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

# Load before importing the SDK. A real environment variable wins over the file.
load_dotenv(Path(__file__).with_name(".env.local"), override=False)

import higgsfield_client  # noqa: E402
from higgsfield_client import CredentialsMissedError, HiggsfieldClientError  # noqa: E402

MODEL = "bytedance/seedance-2.5/text-to-video"
ARGUMENTS = {
    "prompt": "A cinematic scene at sunset",
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "16:9",
}


def find_video_url(result):
    """Return the video URL from a completed result, or None.

    Per the Seedance 2.5 docs, a completed response carries {"video": {"url": ...}}.
    """
    video = result.get("video")
    return video.get("url") if isinstance(video, dict) else None


def main():
    def on_status(status):
        print(f"Status: {type(status).__name__}")

    try:
        result = higgsfield_client.subscribe(
            MODEL,
            arguments=ARGUMENTS,
            on_enqueue=lambda request_id: print(f"Request enqueued: {request_id}"),
            on_queue_update=on_status,
        )
    except CredentialsMissedError:
        sys.exit("FAILED: HF_KEY is not set. Add it to .env.local or the environment as key-id:key-secret.")
    except HiggsfieldClientError as e:
        sys.exit(f"FAILED: Higgsfield API error: {e}")
    except httpx.HTTPError as e:
        sys.exit(f"FAILED: could not reach the Higgsfield API ({type(e).__name__}: {e}). "
                 "Check that api.higgsfield.ai is allowed in the network settings.")

    # subscribe() returns the final status payload, whatever the outcome.
    status = result.get("status")
    if status == "nsfw":
        sys.exit("FAILED: the request was blocked by content moderation (nsfw). No video was produced.")
    if status == "failed":
        sys.exit(f"FAILED: generation failed. Details: {result.get('error') or 'none given'}")
    if status == "canceled":
        sys.exit("FAILED: the request was canceled. No video was produced.")
    if status != "completed":
        sys.exit(f"FAILED: unexpected final status {status!r}.")

    url = find_video_url(result)
    if not url:
        sys.exit(f"FAILED: request completed but no video URL was found. Response keys: {sorted(result)}")
    print(f"Video URL: {url}")


if __name__ == "__main__":
    main()

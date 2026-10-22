"""Analyze a YouTube channel's last N months of uploads.

Uses yt-dlp (kept up to date with YouTube's page changes) instead of a
hand-written HTML scraper. Writes a CSV of every video and a markdown report
with subscriber count, average views, title patterns vs baseline, and cadence.

Usage:
    pip install -U yt-dlp
    python tools/channel_analysis.py https://www.youtube.com/@kurzgesagt
    python tools/channel_analysis.py @kurzgesagt --months 12 --include-shorts
"""

import argparse
import csv
import re
import statistics
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import yt_dlp

# Title features checked against the channel's baseline (median views).
PATTERNS = {
    "Question (?)": lambda t: "?" in t,
    "Starts with What/Why/How": lambda t: re.match(r"(?i)^(what|why|how)\b", t) is not None,
    "'What if'": lambda t: re.search(r"(?i)\bwhat if\b", t) is not None,
    "Contains a number": lambda t: re.search(r"\d", t) is not None,
    "Addresses 'you/your'": lambda t: re.search(r"(?i)\byou(r|'re)?\b", t) is not None,
    "Superlative (biggest/most/worst...)": lambda t: re.search(
        r"(?i)\b(most|least|best|worst|biggest|largest|smallest|fastest|strongest|deadliest|oldest|greatest)\b", t) is not None,
    "Extreme words (end/destroy/kill/death...)": lambda t: re.search(
        r"(?i)\b(end|destroy\w*|kill\w*|death|dead|die|dying|danger\w*|terrif\w*|apocalyp\w*)\b", t) is not None,
    "Colon or dash (two-part title)": lambda t: re.search(r"[:–—-]", t) is not None,
    "Short title (<= 5 words)": lambda t: len(t.split()) <= 5,
    "Long title (>= 9 words)": lambda t: len(t.split()) >= 9,
    "ALL-CAPS word": lambda t: re.search(r"\b[A-Z]{3,}\b", t) is not None,
}
MIN_MATCHES = 3


def channel_url(arg, tab):
    base = arg if arg.startswith("http") else f"https://www.youtube.com/{arg if arg.startswith('@') else '@' + arg}"
    base = re.sub(r"/(videos|shorts|streams|featured)/?$", "", base.rstrip("/"))
    return f"{base}/{tab}"


def list_entries(url):
    opts = {"extract_flat": "in_playlist", "quiet": True, "skip_download": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info.get("entries") or []


def video_details(video_id):
    opts = {"quiet": True, "skip_download": True, "noplaylist": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)


def collect(channel, months, include_shorts):
    cutoff = datetime.now() - timedelta(days=round(months * 30.44))
    tabs = ["videos"] + (["shorts"] if include_shorts else [])
    videos, subscribers, channel_name = [], None, None
    for tab in tabs:
        # Tabs are newest-first, so stop at the first video older than the cutoff.
        for entry in list_entries(channel_url(channel, tab)):
            info = video_details(entry["id"])
            uploaded = datetime.strptime(info["upload_date"], "%Y%m%d")
            if uploaded < cutoff:
                break
            subscribers = subscribers or info.get("channel_follower_count")
            channel_name = channel_name or info.get("channel")
            videos.append({
                "title": info["title"],
                "views": info.get("view_count") or 0,
                "upload_date": uploaded.date().isoformat(),
                "duration_sec": info.get("duration") or 0,
                "format": "short" if tab == "shorts" else "long",
                "url": info.get("webpage_url"),
            })
            print(f"  {uploaded.date()}  {info.get('view_count', 0):>12,}  {info['title']}", file=sys.stderr)
    return channel_name, subscribers, sorted(videos, key=lambda v: v["upload_date"], reverse=True)


def fmt_duration(sec):
    return f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}" if sec >= 3600 else f"{sec // 60}:{sec % 60:02d}"


def title_patterns(videos):
    baseline = statistics.median(v["views"] for v in videos)
    rows = []
    for name, test in PATTERNS.items():
        hits = [v["views"] for v in videos if test(v["title"])]
        if len(hits) < MIN_MATCHES or len(hits) == len(videos):
            continue
        med = statistics.median(hits)
        rows.append((name, len(hits), med, med - baseline, med / baseline - 1))
    return baseline, sorted(rows, key=lambda r: r[3], reverse=True)


def cadence(videos):
    dates = sorted(datetime.fromisoformat(v["upload_date"]) for v in videos)
    gaps = [(b - a).days for a, b in zip(dates, dates[1:])]
    per_month = Counter(d.strftime("%Y-%m") for d in dates)
    weekdays = Counter(d.strftime("%A") for d in dates)
    return gaps, per_month, weekdays


def report(channel_name, subscribers, videos, months):
    lines = [f"# Channel analysis: {channel_name}", "",
             f"_Generated {datetime.now():%Y-%m-%d} with yt-dlp. Window: last {months} months._", ""]
    views = [v["views"] for v in videos]
    lines += ["## Summary", "",
              f"- **Subscribers:** {subscribers:,}" if subscribers else "- **Subscribers:** unavailable (hidden)",
              f"- **Videos in window:** {len(videos)}",
              f"- **Average views per video:** {statistics.mean(views):,.0f}",
              f"- **Median views per video:** {statistics.median(views):,.0f}",
              f"- **Total views (window):** {sum(views):,}", ""]

    baseline, patterns = title_patterns(videos)
    lines += ["## Title patterns vs baseline", "",
              f"Baseline = median views across all {len(videos)} videos = **{baseline:,.0f}**. "
              f"Patterns need at least {MIN_MATCHES} matching videos. With small samples, treat these as hints, not proof.", "",
              "| Pattern | Videos | Median views | Extra views vs baseline | Uplift |",
              "|---|---:|---:|---:|---:|"]
    lines += [f"| {n} | {c} | {m:,.0f} | {d:+,.0f} | {u:+.0%} |" for n, c, m, d, u in patterns]

    top = sorted(videos, key=lambda v: v["views"], reverse=True)[:max(5, len(videos) // 4)]
    lines += ["", f"### Top performers (top {len(top)})", "",
              "| Views | Title | Patterns matched |", "|---:|---|---|"]
    for v in top:
        matched = ", ".join(n for n, t in PATTERNS.items() if t(v["title"])) or "none"
        lines.append(f"| {v['views']:,} | {v['title']} | {matched} |")

    gaps, per_month, weekdays = cadence(videos)
    lines += ["", "## Upload cadence", ""]
    if gaps:
        lines += [f"- **Average gap between uploads:** {statistics.mean(gaps):.1f} days "
                  f"(median {statistics.median(gaps):.0f}, range {min(gaps)}–{max(gaps)})",
                  f"- **Uploads per month:** {len(videos) / months:.1f} on average"]
    lines += [f"- **Most common upload day:** {weekdays.most_common(1)[0][0]}", "",
              "| Month | Uploads |", "|---|---:|"]
    lines += [f"| {m} | {c} |" for m, c in sorted(per_month.items())]

    lines += ["", "## All videos", "", "| Date | Views | Duration | Title |", "|---|---:|---:|---|"]
    lines += [f"| {v['upload_date']} | {v['views']:,} | {fmt_duration(v['duration_sec'])} | {v['title']} |"
              for v in videos]
    return "\n".join(lines) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("channel", help="Channel URL or @handle")
    p.add_argument("--months", type=int, default=12)
    p.add_argument("--include-shorts", action="store_true")
    p.add_argument("--out", default="research/channels", help="Output directory")
    args = p.parse_args()

    print(f"Fetching {args.channel} ...", file=sys.stderr)
    channel_name, subscribers, videos = collect(args.channel, args.months, args.include_shorts)
    if not videos:
        sys.exit("No videos found in the window.")

    slug = re.sub(r"[^a-z0-9]+", "-", (channel_name or args.channel).lower()).strip("-")
    out = Path(args.out) / slug
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "videos.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(videos[0]))
        writer.writeheader()
        writer.writerows(videos)
    (out / "analysis.md").write_text(report(channel_name, subscribers, videos, args.months), encoding="utf-8")
    print(f"Wrote {out / 'videos.csv'} and {out / 'analysis.md'}", file=sys.stderr)


if __name__ == "__main__":
    main()

"""Shorten long pauses in a voiceover so a Short fits under 60 s without speeding up the voice much.

Every pause longer than --max-pause is cut down to --max-pause (centred, so breaths and word endings stay).
Speech itself is untouched.

Usage:
    python tools/tighten_pauses.py production/<slug>/audio/voiceover-v1.mp3 --max-pause 0.3
    -> writes production/<slug>/audio/voiceover-v1-tight.wav
"""

import argparse
import re
import subprocess
from pathlib import Path


def find_silences(path, noise_db, min_dur):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af",
                          f"silencedetect=noise={noise_db}dB:d={min_dur}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", out)]
    return list(zip(starts, ends))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("src")
    p.add_argument("--max-pause", type=float, default=0.3)
    p.add_argument("--noise-db", type=float, default=-35)
    p.add_argument("--out")
    args = p.parse_args()

    src = Path(args.src)
    out = Path(args.out) if args.out else src.with_name(src.stem + "-tight.wav")
    silences = [(a, b) for a, b in find_silences(src, args.noise_db, args.max_pause) if b - a > args.max_pause]

    # Keep [prev_end, silence_start + half] and [silence_end - half, ...]: each pause shrinks to max_pause.
    half = args.max_pause / 2
    keep, cursor = [], 0.0
    for a, b in silences:
        keep.append((cursor, a + half))
        cursor = b - half
    keep.append((cursor, None))

    parts = []
    for i, (a, b) in enumerate(keep):
        end = f":end={b:.4f}" if b is not None else ""
        parts.append(f"[0:a]atrim=start={a:.4f}{end},asetpts=PTS-STARTPTS[s{i}]")
    graph = ";".join(parts) + ";" + "".join(f"[s{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[out]"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-filter_complex", graph,
                    "-map", "[out]", "-c:a", "pcm_s16le", str(out)], check=True)
    removed = sum(b - a - args.max_pause for a, b in silences)
    print(f"Shortened {len(silences)} pauses, removed {removed:.2f} s -> {out}")


if __name__ == "__main__":
    main()

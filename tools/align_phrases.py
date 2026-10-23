"""Find when each phrase of the script is spoken in a voiceover (forced alignment, offline).

Uses pocketsphinx (its English model ships inside the PyPI package, no download needed) to align the script's
voiceover text to the audio word by word, then groups words into caption phrases split at punctuation.
Times are in the ORIGINAL audio (before any tempo change). Assumes the voice read the script word for word.

Usage:
    pip install pocketsphinx
    python tools/align_phrases.py scripts/dark-oxygen.md production/dark-oxygen/audio/voiceover-v1.mp3 \
        > production/dark-oxygen/phrases.json
"""

import json
import re
import subprocess
import sys

from pocketsphinx import Decoder

# Words missing from the default dictionary (ARPAbet).
EXTRA_PRONUNCIATIONS = {
    "polymetallic": "P AA L IY M AH T AE L IH K",
    "prochlorococcus": "P R OW K L AO R AH K AA K AH S",
}
NUMBER_WORDS = {"2024": "twenty twenty four", "2021": "twenty twenty one", "2012": "twenty twelve",
                "1979": "nineteen seventy nine"}


def script_lines(script_md):
    text = open(script_md, encoding="utf-8").read()
    block = text.split("## Voiceover-only text", 1)[1].split("\n## ", 1)[0]
    return [l[2:].strip() for l in block.splitlines() if l.startswith("> ")]


def spoken_tokens(word):
    """Script word -> the dictionary words it is pronounced as."""
    w = word.lower().replace("’", "'")
    w = re.sub(r"[^a-z0-9' -]", "", w)
    out = []
    for part in w.replace("-", " ").split():
        out += NUMBER_WORDS.get(part, part).split()
    return out


def main():
    script_md, audio = sys.argv[1], sys.argv[2]
    lines = script_lines(script_md)

    # Phrases split at punctuation; each phrase keeps its display text and its spoken tokens.
    phrases = []
    for line in lines:
        for p in re.findall(r"[^.?!:…]+(?:\.\.\.|[.?!:…])?", line):
            if p.strip():
                toks = [t for w in p.split() for t in spoken_tokens(w)]
                phrases.append({"text": p.strip(), "tokens": toks})

    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", audio, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    decoder = Decoder(samprate=16000, bestpath=False)
    for word, phones in EXTRA_PRONUNCIATIONS.items():
        if decoder.lookup_word(word) is None:
            decoder.add_word(word, phones, True)
    all_tokens = [t for p in phrases for t in p["tokens"]]
    missing = sorted({t for t in all_tokens if decoder.lookup_word(t) is None})
    if missing:
        sys.exit(f"Add pronunciations for: {missing}")

    decoder.set_align_text(" ".join(all_tokens))
    decoder.start_utt()
    decoder.process_raw(pcm, full_utt=True)
    decoder.end_utt()
    decoder.set_alignment()
    decoder.start_utt()
    decoder.process_raw(pcm, full_utt=True)
    decoder.end_utt()
    aligned = [(w.name, w.start / 100, (w.start + w.duration) / 100)
               for w in decoder.get_alignment() if w.name not in ("<s>", "</s>", "<sil>")]
    words = [a for a in aligned if not a[0].startswith("+")]
    if len(words) != len(all_tokens):
        sys.exit(f"Alignment produced {len(words)} words for {len(all_tokens)} tokens; check the script text.")

    out, i = [], 0
    for p in phrases:
        n = len(p["tokens"])
        seg = words[i:i + n]
        out.append({"start": round(seg[0][1], 2), "end": round(seg[-1][2], 2), "text": p["text"],
                    "words": [[w, round(a, 2), round(b, 2)] for w, a, b in seg]})
        i += n
    json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
    print(f"\nAligned {len(words)} words in {len(phrases)} phrases", file=sys.stderr)


if __name__ == "__main__":
    main()

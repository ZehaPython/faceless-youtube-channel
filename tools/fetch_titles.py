import yt_dlp, sys, json
out = {}
for h in sys.argv[1:]:
    t = []
    for tab in ("videos", "shorts"):
        try:
            with yt_dlp.YoutubeDL({"extract_flat": "in_playlist", "quiet": True, "no_warnings": True}) as y:
                i = y.extract_info(f"https://www.youtube.com/{h}/{tab}", download=False)
            t += [(e["title"], e.get("view_count")) for e in i.get("entries") or []]
        except Exception as ex:
            print(h, tab, ex, file=sys.stderr)
    out[h] = t
    print(h, len(t), file=sys.stderr)
json.dump(out, open("titles.json", "w"), ensure_ascii=False)

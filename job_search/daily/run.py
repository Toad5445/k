"""Daily sweep: fetch new postings, auto-sort them, and write the ones that need a final read to out/candidates.json.
Usage: python3 -I run.py [--window r86400|r604800] [--no-linkedin] [--no-sites]"""
import json, os, sys, time, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sources, classify

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "state", "seen.json")
OUT = os.path.join(HERE, "out")


def main():
    args = sys.argv[1:]
    window = args[args.index("--window") + 1] if "--window" in args else "r86400"
    seen = json.load(open(STATE)) if os.path.exists(STATE) else {}
    t0 = time.time()
    posts = []
    if "--no-sites" not in args:
        posts += sources.career_sites(seen)
    if "--no-linkedin" not in args:
        posts += sources.linkedin(seen, window)
    today = datetime.date.today().isoformat()
    tally, cands = {}, []
    for p in posts:
        dec, reasons, flags, group, quotes = classify.classify(p)
        tally[dec] = tally.get(dec, 0) + 1
        seen[p["id"]] = {"d": dec, "t": today, "c": p["company"][:40], "j": p["title"][:60], "r": "; ".join(reasons)[:120]}
        if dec in ("accept", "review"):
            cands.append({**{k: p.get(k) for k in ("id", "source", "company", "title", "loc", "url", "salary", "posted")},
                          "group": group, "auto": dec, "flags": flags, "quotes": quotes, "desc": p["desc"][:9000]})
    os.makedirs(OUT, exist_ok=True)
    json.dump(cands, open(os.path.join(OUT, "candidates.json"), "w"), indent=1)
    json.dump(seen, open(STATE, "w"))
    print(f"read {len(posts)} new postings in {int(time.time() - t0)}s -> {tally}; {len(cands)} need a final read (out/candidates.json)")


if __name__ == "__main__":
    main()

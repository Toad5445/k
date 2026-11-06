"""Daily sweep: fetch new postings, auto-sort them, and write the ones that need a final read to out/candidates.json.
Usage: python3 -I run.py [--window r86400|r604800] [--no-linkedin] [--no-sites]

Seen state = state/seen.json (baseline in git) + every board/seen/*.json and board/jobs/*.json file downloaded from
the job board's database (see RUNBOOK step 1). New ids from this run go to out/seen_doc.json for upload to the board."""
import glob, re
import json, os, sys, time, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sources, classify

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "state", "seen.json")
OUT = os.path.join(HERE, "out")
BOARD = os.path.join(HERE, "board")


class Seen(dict):
    """Also matches an id in the board's doc-id form (':' and other unsafe characters replaced by '-')."""
    def __contains__(self, k):
        return dict.__contains__(self, k) or dict.__contains__(self, re.sub(r"[^A-Za-z0-9_\-.~@+]", "-", k)[:180])


def board_seen():
    """Ids already recorded on the board: the seen/<date> docs and the job docs themselves."""
    ids = {}
    for f in glob.glob(os.path.join(BOARD, "seen", "*.json")):
        try:
            ids.update(json.load(open(f)).get("ids", {}))
        except Exception as e:
            print("skip", f, e)
    for f in glob.glob(os.path.join(BOARD, "jobs", "*.json")):
        name = os.path.basename(f)[:-5]
        ids[name] = "board"
    return ids


def main():
    args = sys.argv[1:]
    window = args[args.index("--window") + 1] if "--window" in args else "r129600"  # 36h; overlap is free (seen ids are skipped)
    seen = Seen(json.load(open(STATE)) if os.path.exists(STATE) else {})
    extra = board_seen()
    for k, v in extra.items():
        seen.setdefault(k, {"d": v})
    print(f"seen: {len(seen)} ids ({len(extra)} from the board)")
    t0 = time.time()
    posts = []
    if "--no-sites" not in args:
        posts += sources.career_sites(seen)
    if "--no-linkedin" not in args:
        posts += sources.linkedin(seen, window)
    today = datetime.date.today().isoformat()
    tally, cands, new_ids = {}, [], {}
    for p in posts:
        dec, reasons, flags, group, quotes = classify.classify(p)
        tally[dec] = tally.get(dec, 0) + 1
        new_ids[p["id"]] = dec
        seen[p["id"]] = {"d": dec, "t": today, "c": p["company"][:40], "j": p["title"][:60], "r": "; ".join(reasons)[:120]}
        if dec in ("accept", "review"):
            cands.append({**{k: p.get(k) for k in ("id", "source", "company", "title", "loc", "url", "salary", "posted")},
                          "group": group, "auto": dec, "flags": flags, "quotes": quotes, "desc": p["desc"][:9000]})
    os.makedirs(OUT, exist_ok=True)
    json.dump(cands, open(os.path.join(OUT, "candidates.json"), "w"), indent=1)
    # state/seen.json is a fixed baseline; new ids are saved on the board (out/seen_doc.json, RUNBOOK step 5)
    json.dump({"ids": new_ids, "date": today}, open(os.path.join(OUT, "seen_doc.json"), "w"))
    print(f"read {len(posts)} new postings in {int(time.time() - t0)}s -> {tally}; {len(cands)} need a final read (out/candidates.json)")


if __name__ == "__main__":
    main()

import json, re, sys

NUM = r"(?:\d+|zero|one|two|three|four|five|six|seven|eight|nine|ten)"
YRS = re.compile(r"[^.\n]{0,120}?\b(" + NUM + r")\s*(?:\+|plus)?\s*(?:(?:-|–|—|to)\s*(" + NUM + r")\s*\+?\s*)?(?:\(\d+\)\s*)?(?:full[- ]time\s+)?years?\b[^.\n]{0,140}", re.I)
WORD = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
EXPCTX = re.compile(r"experience|exp\b|work(ing)? in|background in|track record|tenure|professional", re.I)
NONEXP = re.compile(r"years? old|years? of age|year[- ]old|founded|years in business|years? ago|year[- ]round|per year|each year|every year|multi[- ]year|this year|\bsince \d{4}|in a row|anniversary|\bvesting\b|\b(two|2|three|3)[- ]year (program|analyst program|rotation)|over the (past|last) \d+|more than \d+ years (of|in) (business|operation|history)|\d+ years of (unbroken|history|operation\b|growth)|for (over|more than) \d+ years|\b\d+-year (history|track)|building on more than|over \d+ years,|has been .{0,20}for", re.I)
UPTO = re.compile(r"\bup to\b|no more than|less than|\bmaximum\b|or fewer|at most", re.I)
FLAGS = {
    "python": re.compile(r"\bpython\b", re.I), "sql": re.compile(r"\bsql\b", re.I), "cfa": re.compile(r"\bCFA\b"),
    "cpa": re.compile(r"\bCPA\b"), "masters": re.compile(r"master'?s|\bMBA\b", re.I),
    "lang": re.compile(r"(fluen|proficien|bilingual)[^.\n]{0,40}(mandarin|spanish|japanese|korean|french|german|chinese|cantonese|portuguese|italian|arabic|russian)", re.I),
    "license": re.compile(r"series \d+|\bSIE\b|licen[cs]e", re.I),
    "class": re.compile(r"class of 202\d|202[78]|graduat\w* (between|by|in) [^.\n]{0,40}", re.I),
    "enrolled": re.compile(r"currently (enrolled|pursuing)|rising senior", re.I),
    "contract": re.compile(r"\bcontract\b|temporary|\btemp\b|part[- ]time|hourly|\$\d+(\.\d+)?\s*(/|per)\s*h(ou)?r", re.I),
    "commission": re.compile(r"commission|uncapped|build your (own )?(book|agency|practice)", re.I),
    "hybrid": re.compile(r"hybrid|in[- ]office|on[- ]site|onsite|\d days? (a|per) week", re.I),
    "acct": re.compile(r"reconcil|journal entr|general ledger|accounts payable|accounts receivable|month[- ]end close|\bSOX\b|invoice|bookkeep", re.I),
}


def tonum(s):
    s = s.lower()
    return WORD[s] if s in WORD else int(s)


def analyze(desc):
    hits = []
    for m in YRS.finditer(desc or ""):
        ctx = m.group(0)
        if NONEXP.search(ctx):
            continue
        lo = tonum(m.group(1))
        if lo > 25:
            continue
        hits.append((lo, ctx.strip()))
    floors = [lo for lo, ctx in hits if not UPTO.search(ctx)]
    return hits, floors


def main():
    src = json.load(open(sys.argv[1]))
    items = src.items() if isinstance(src, dict) else enumerate(src)
    out = []
    for k, j in items:
        d = j.get("desc", "")
        if not d or j.get("closed"):
            continue
        hits, floors = analyze(d)
        verdict = "nofloor" if not hits else ("zero" if floors and min(floors) == 0 and max(floors) == 0 else ("upto" if not floors else "above0"))
        if any(f >= 1 for f in floors):
            verdict = "above0"
        fl = {n: bool(r.search(d)) for n, r in FLAGS.items()}
        out.append({"key": str(k), **{x: j.get(x) for x in ("title", "company", "board", "loc", "url", "apply", "salary", "crit", "posted", "commitment", "workplace")},
                    "verdict": verdict, "hits": [h[1] for h in hits][:4], "flags": [n for n, v in fl.items() if v]})
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    from collections import Counter
    print(Counter(o["verdict"] for o in out))


main()

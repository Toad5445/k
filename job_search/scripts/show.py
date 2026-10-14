import json, sys
d = json.load(open(sys.argv[1]))
items = d.values() if isinstance(d, dict) else d
for pat in sys.argv[2:]:
    b, t = pat.split("::")
    for j in items:
        if (b.lower() in (j.get("board") or j.get("company") or "").lower()) and t.lower() in j["title"].lower():
            print("=" * 100)
            print(j.get("board") or j.get("company"), "|", j["title"], "|", j.get("loc"), "|", j.get("url") or j.get("apply"), "|", j.get("salary"), "|", j.get("commitment"), j.get("workplace"), j.get("crit"), j.get("posted"))
            print(j["desc"][:int(sys.argv[0] and 9000)])
            break

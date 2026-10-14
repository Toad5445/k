import json, sys, re
d = json.load(open(sys.argv[1]))
KEY = re.compile(r"year|experience|required|must|degree|remote|hybrid|in[- ]office|on[- ]site|onsite|days|location|start date|202[5-8]|class of|program|licen|series|python|sql|\$\d|salary|graduat|intern|commission|contract|temporary|reconcil|journal|ledger|payable|receivable|invoice", re.I)
for k in sys.argv[2:]:
    j = d[k]
    print("=" * 80)
    print(k, "|", j.get("company"), "|", j["title"], "|", j.get("loc"), "|", j.get("salary"), "|", (j.get("crit") or {}).get("Employment type"), "|", j.get("posted"), "|closed" if j.get("closed") else "")
    lines = [l.strip() for l in j["desc"].split("\n") if l.strip()]
    print("  " + (lines[0][:200] if lines else ""))
    for l in lines[1:]:
        if KEY.search(l) and not re.search(r"equal (employment )?opportunity|without regard|accommodation|benefit|401", l, re.I):
            print("  -", l[:260])

import json, sys, re
d = json.load(open(sys.argv[1]))
n = int(sys.argv[2])
for k in sys.argv[3:]:
    j = d[k]
    print("=" * 90)
    print(k, "|", j["company"], "|", j["title"], "|", j["loc"], "|", j.get("salary"), "|", j.get("crit"), "|", j.get("posted"), "| closed" if j.get("closed") else "", "|", j.get("apply", "")[:150])
    desc = j["desc"]
    desc = re.sub(r"(?is)(equal (employment )?opportunity|we are an equal|eeo statement|reasonable accommodation).*", "[EEO trimmed]", desc)
    print(desc[:n])

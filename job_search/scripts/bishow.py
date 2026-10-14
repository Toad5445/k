import json, sys, re
d = json.load(open(sys.argv[1])); n = int(sys.argv[2])
for k in sys.argv[3:]:
    j = d[k]
    print("=" * 90)
    print(k, "|", j["company"], "|", j["title"], "|", j["url"], "|", j.get("apply", "")[:120], "|", j["emp"], "|", j["salary"][:150], "|", j["posted"][:10])
    desc = re.sub(r"(?is)(equal (employment )?opportunity employer|we are an equal|eeo statement|reasonable accommodation).*", "[EEO trimmed]", j["desc"])
    print(desc[:n])

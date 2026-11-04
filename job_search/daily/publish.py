"""Turn the jobs approved after the final read into Job Board documents.
Input: out/approved.json — a list of {"id", "exp", "caveat", optional overrides: "company", "title", "loc", "salary", "group"}
       out/rejected.json — a list of {"id", "reason"} for every candidate NOT approved (reason quotes the blocking line),
       and optional out/redflags.json — a list of {"id", "reason"}.
Every candidate in out/candidates.json must appear in exactly one of the three files, or nothing is published.
Output: one JSON file per document in out/publish/ and a printed `writes` array for ArtifactData batch (max 50 per call)."""
import json, os, re, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
cands = {c["id"]: c for c in json.load(open(os.path.join(OUT, "candidates.json")))}
approved = json.load(open(os.path.join(OUT, "approved.json")))
red = json.load(open(os.path.join(OUT, "redflags.json"))) if os.path.exists(os.path.join(OUT, "redflags.json")) else []
rej_path = os.path.join(OUT, "rejected.json")
rejected = json.load(open(rej_path)) if os.path.exists(rej_path) else []
decided = [a["id"] for a in approved] + [r["id"] for r in rejected] + [r["id"] for r in red]
missing = [i for i in cands if i not in decided]
unknown = [i for i in decided if i not in cands]
if missing or unknown:
    sys.exit(f"STOP: {len(missing)} candidates have no decision: {missing}\n{len(unknown)} decisions match no candidate: {unknown}\n"
             "Read each missing candidate's full desc and add it to approved.json or rejected.json, then rerun.")
bad = [r["id"] for r in rejected if len(r.get("reason", "")) < 15]
if bad:
    sys.exit(f"STOP: these rejections need a real reason quoting the blocking line: {bad}")
# keep the reasons with this run's seen record, so misses can be audited later
sd = os.path.join(OUT, "seen_doc.json")
if os.path.exists(sd):
    doc = json.load(open(sd)); doc["why"] = {r["id"]: r["reason"][:200] for r in rejected}
    json.dump(doc, open(sd, "w"))
pub = os.path.join(OUT, "publish"); os.makedirs(pub, exist_ok=True)
today = datetime.date.today().isoformat()
writes = []


def docid(i):
    return re.sub(r"[^A-Za-z0-9_\-.~:@+]", "-", i)[:180]


for a in approved:
    c = {**cands.get(a["id"], {}), **{k: v for k, v in a.items() if v not in (None, "")}}
    key = a["id"][3:] if a["id"].startswith("li:") else docid(a["id"])
    doc = dict(key=key, company=c.get("company", ""), title=c.get("title", ""), loc=c.get("loc", ""), salary=c.get("salary", ""),
               exp=a.get("exp", ""), caveat=a.get("caveat", ""), url=c.get("url", ""), posted=c.get("posted", ""),
               group=c.get("group") or "nyc", source=c.get("source", ""), added=today)
    f = os.path.join(pub, "job-" + docid(a["id"]).replace(":", "-") + ".json"); json.dump(doc, open(f, "w"))
    writes.append({"op": "set", "collection": "jobs", "doc_id": docid(a["id"]).replace(":", "-"), "file_path": f})
for r in red:
    c = cands.get(r["id"], {})
    f = os.path.join(pub, "red-" + docid(r["id"]).replace(":", "-") + ".json")
    json.dump(dict(company=r.get("company") or c.get("company", ""), title=r.get("title") or c.get("title", ""), reason=r["reason"], added=today), open(f, "w"))
    writes.append({"op": "set", "collection": "red", "doc_id": docid(r["id"]).replace(":", "-"), "file_path": f})
for i in range(0, len(writes), 50):
    print(json.dumps(writes[i:i + 50]))
print(f"# {len(approved)} jobs, {len(rejected)} rejected, {len(red)} red flags -> {len(writes)} writes", file=sys.stderr)

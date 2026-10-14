import json, re, sys, html, time, os
import requests

OUT = sys.argv[1]
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
LISTS = []
for base in ["https://builtin.com/jobs/remote/finance/entry-level", "https://builtin.com/jobs/new-york-city/finance/entry-level",
             "https://builtin.com/jobs/remote/finance/junior", "https://builtin.com/jobs/new-york-city/finance/junior"]:
    for p in range(1, 11):
        LISTS.append(base + ("" if p == 1 else f"?page={p}"))

TITLE_BAD = re.compile(r"senior|\bsr\.?\b|\bvp\b|director|principal|manager|head of|\blead\b|engineer|developer|intern\b|internship|accountant|accounting|\btax\b|audit|payroll|bookkeep|actuar|collector|receivable|payable|billing|\bii\b|\biii\b|loan processing|sales|account executive", re.I)


def clean(s):
    s = re.sub(r"<br\s*/?>|</p>|</li>|</div>|<li>", "\n", s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


det = json.load(open(OUT)) if os.path.exists(OUT) else {}
links = {}
for u in LISTS:
    try:
        r = requests.get(u, headers=H, timeout=30)
    except Exception:
        continue
    found = re.findall(r'href="(/job/[^"]+/(\d+))"[^>]*>\s*([^<]{3,200})<', r.text)
    if not found:
        found = [(a, b, "") for a, b in re.findall(r'href="(/job/[^"]+/(\d+))"', r.text)]
    n = 0
    for path, jid, title in found:
        if jid not in links:
            links[jid] = (path, html.unescape(title.strip())); n += 1
    print(u, n, flush=True)
    if n == 0:
        continue
    time.sleep(0.5)

for jid, (path, title) in links.items():
    if jid in det:
        continue
    slug = path.split("/")[2]
    if TITLE_BAD.search(slug.replace("-", " ")):
        continue
    try:
        r = requests.get("https://builtin.com" + path, headers=H, timeout=30)
    except Exception:
        continue
    t = r.text
    ld = re.search(r'<script type="application/ld(?:\+|&#x2B;)json">\s*(\{.*?"@type"\s*:\s*"JobPosting".*?\})\s*</script>', t, re.S)
    data = {}
    if ld:
        try:
            data = json.loads(ld.group(1))
        except Exception:
            data = {}
    if data.get("@type") != "JobPosting":
        data = {}
        for m in re.finditer(r'<script type="application/ld(?:\+|&#x2B;)json">(.*?)</script>', t, re.S):
            try:
                j = json.loads(m.group(1))
            except Exception:
                continue
            for g in (j.get("@graph", []) if isinstance(j, dict) else []) + ([j] if isinstance(j, dict) else []):
                if isinstance(g, dict) and g.get("@type") == "JobPosting":
                    data = g
    org = (data.get("hiringOrganization") or {}).get("name", "")
    loc = json.dumps(data.get("jobLocation", ""))[:300] + " " + str(data.get("jobLocationType", "")) + " " + json.dumps(data.get("applicantLocationRequirements", ""))[:300]
    apply = re.search(r'"howToApply"\s*:\s*"([^"]+)"', t) or re.search(r'href="(https?://[^"]+)"[^>]*>\s*Apply', t)
    det[jid] = {"title": data.get("title", title or slug), "company": org, "loc": loc, "url": "https://builtin.com" + path,
                "apply": apply.group(1) if apply else "", "posted": data.get("datePosted", ""), "valid": data.get("validThrough", ""),
                "emp": data.get("employmentType", ""), "salary": json.dumps(data.get("baseSalary", ""))[:200],
                "desc": clean(data.get("description", ""))}
    time.sleep(0.4)
json.dump(det, open(OUT, "w"))
print("details", len(det))

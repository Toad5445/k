import json, sys, re, html, time
import requests
from concurrent.futures import ThreadPoolExecutor

# (host, tenant, site, label)
SITES = [l.split("|") for l in sys.argv[2].split(";")]
QUERIES = sys.argv[3].split(";")
OUT = sys.argv[1]
H = {"Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"}
TITLE_BAD = re.compile(r"senior|\bsr\.?\b|\bvp\b|vice president|director|principal|manager|head of|\blead\b|engineer|developer|intern\b|internship|summer|2027|2028|accountant|accounting|\btax\b|audit|payroll|counsel|scientist|\bii\b|\biii\b|chief|controller|\bavp\b|officer", re.I)
LOC_OK = re.compile(r"new york|ny\b|remote|united states|white plains|stamford|greenwich|purchase|harrison|tarrytown|armonk|danbury|valhalla|elmsford|rye|norwalk|somers|yorktown|mount kisco|brewster|ridgefield|bronx|brooklyn|queens", re.I)


def clean(s):
    s = re.sub(r"<br\s*/?>|</p>|</li>|</div>|<li>", "\n", s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


def run(site):
    host, tenant, sitename, label = site
    base = f"https://{host}/wday/cxs/{tenant}/{sitename}"
    found = {}
    for q in QUERIES:
        for off in (0, 20, 40):
            try:
                r = requests.post(base + "/jobs", json={"appliedFacets": {}, "limit": 20, "offset": off, "searchText": q}, headers=H, timeout=30)
                if r.status_code != 200:
                    return label, {"error": r.status_code}
                js = r.json()
            except Exception as e:
                return label, {"error": str(e)}
            posts = js.get("jobPostings", [])
            for p in posts:
                t = p.get("title", "")
                loc = p.get("locationsText", "")
                if TITLE_BAD.search(t) or not (LOC_OK.search(loc) or "Locations" in loc):
                    continue
                found[p["externalPath"]] = {"title": t, "loc": loc, "posted": p.get("postedOn")}
            if len(posts) < 20:
                break
    out = []
    for path, m in found.items():
        try:
            r = requests.get(base + path, headers=H, timeout=30)
            jp = r.json().get("jobPostingInfo", {})
            out.append({"board": label, "title": jp.get("title", m["title"]), "loc": jp.get("location", m["loc"]) + " | " + " ".join(jp.get("additionalLocations", []) or []),
                        "commitment": jp.get("timeType"), "url": jp.get("externalUrl"), "posted": jp.get("postedOn"),
                        "desc": clean(jp.get("jobDescription", ""))})
        except Exception:
            pass
    return label, out


res = []
with ThreadPoolExecutor(8) as ex:
    for label, out in ex.map(run, SITES):
        if isinstance(out, dict):
            print(label, "ERR", out["error"])
        else:
            print(label, len(out))
            res += out
old = json.load(open(OUT)) if __import__("os").path.exists(OUT) else []
json.dump(old + res, open(OUT, "w"))

import json, re, sys, time, html, os
import requests
from urllib.parse import urlencode

OUT = sys.argv[1]
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

KEYWORDS = [
    "financial analyst", "FP&A analyst", "treasury analyst", "credit analyst", "investment analyst",
    "portfolio analyst", "risk analyst", "capital markets analyst", "investment banking analyst",
    "valuation analyst", "asset management analyst", "KYC analyst", "AML analyst", "finance analyst",
    "investment operations analyst", "corporate finance analyst", "junior analyst finance",
    "research analyst investment", "underwriting analyst", "fund operations analyst",
    "private equity analyst", "real estate finance analyst", "financial planning analyst",
    "budget analyst", "pricing analyst finance", "business analyst finance",
]
SEARCHES = [
    # (location, extra params)
    ("New York, New York, United States", {}),
    ("Westchester County, New York, United States", {}),
    ("Stamford, Connecticut, United States", {}),
    ("Danbury, Connecticut, United States", {}),
    ("United States", {"f_WT": "2"}),
]

seen = {}
if os.path.exists(OUT):
    seen = json.load(open(OUT))

for kw in KEYWORDS:
    for loc, extra in SEARCHES:
        for start in (0, 25, 50):
            p = {"keywords": kw, "location": loc, "f_E": "1,2", "f_JT": "F", "f_TPR": "r2592000", "start": start}
            if "Westchester" in loc or "Stamford" in loc or "Danbury" in loc:
                p["distance"] = "15"
            p.update(extra)
            url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?" + urlencode(p)
            for attempt in range(3):
                try:
                    r = requests.get(url, headers=H, timeout=30)
                    if r.status_code == 429:
                        time.sleep(5 * (attempt + 1)); continue
                    break
                except Exception as e:
                    time.sleep(3)
            else:
                continue
            if r.status_code != 200 or not r.text.strip():
                break
            cards = re.findall(r'data-entity-urn="urn:li:jobPosting:(\d+)".*?base-search-card__title">\s*(.*?)\s*</h3>.*?base-search-card__subtitle">.*?>\s*(.*?)\s*</a>.*?job-search-card__location">\s*(.*?)\s*</span>', r.text, re.S)
            if not cards:
                break
            for jid, title, comp, jloc in cards:
                if jid not in seen:
                    seen[jid] = {"title": html.unescape(title), "company": html.unescape(comp), "loc": html.unescape(jloc), "kw": kw, "search": loc + (" remote" if extra else "")}
            time.sleep(0.7)
    json.dump(seen, open(OUT, "w"), indent=0)
    print(kw, len(seen), flush=True)

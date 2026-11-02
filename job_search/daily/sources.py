"""Fetch postings from LinkedIn (guest API) and employer career sites. Each posting -> dict with
id, source, company, title, loc, url, posted, desc, salary."""
import re, html, time, json, threading
import requests
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor
import config as C

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def clean(s):
    s = re.sub(r"<br\s*/?>|</p>|</li>|</div>|<li>|</h\d>", "\n", s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


def get(url, tries=5, **kw):
    for a in range(tries):
        try:
            r = requests.get(url, headers=UA, timeout=30, **kw)
            if r.status_code == 429:
                time.sleep(4 * (a + 1)); continue
            return r
        except Exception:
            time.sleep(3)
    return None


def title_ok(t):
    return bool(C.TITLE_GOOD.search(t or "")) and not C.TITLE_BAD.search(t or "")


# ---------------- LinkedIn ----------------
def linkedin(seen, window="r86400", log=print):
    cards = {}
    for kw in C.LI_KEYWORDS:
        for where, lp in C.LI_LOCATIONS:
            for start in range(0, 250, 25):
                p = {"keywords": kw, "f_E": "2", "f_JT": "F", "f_TPR": window, "sortBy": "DD", "start": start, **lp}
                r = get("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?" + urlencode(p))
                if r is None or r.status_code != 200:
                    break
                found = re.findall(r'data-entity-urn="urn:li:jobPosting:(\d+)".*?base-search-card__title">\s*(.*?)\s*</h3>.*?'
                                   r'base-search-card__subtitle">.*?>\s*(.*?)\s*</a>.*?job-search-card__location">\s*(.*?)\s*</span>', r.text, re.S)
                if not found:
                    break
                for jid, t, c, l in found:
                    cards.setdefault("li:" + jid, dict(id="li:" + jid, source="LinkedIn", title=html.unescape(t),
                                                       company=html.unescape(c), loc=html.unescape(l), where=where,
                                                       url=f"https://www.linkedin.com/jobs/view/{jid}"))
                time.sleep(0.5)
    todo = [c for k, c in cards.items() if k not in seen and title_ok(c["title"]) and not C.BAD_LOC.search(c["loc"])]
    log(f"LinkedIn: {len(cards)} postings found, {len(todo)} new with a finance title to read")
    out, lock = [], threading.Lock()

    def one(c):
        r = get("https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/" + c["id"][3:], tries=6)
        if r is None or r.status_code != 200:
            return
        t = r.text
        m = re.search(r'show-more-less-html__markup[^>]*>(.*?)</div>', t, re.S)
        crit = dict((clean(a), clean(b)) for a, b in re.findall(r'description__job-criteria-subheader">(.*?)</h3>.*?description__job-criteria-text[^>]*>(.*?)</span>', t, re.S))
        sal = re.search(r'salary compensation__salary">\s*(.*?)\s*<', t, re.S)
        dt = re.search(r'posted-time-ago__text[^>]*>\s*(.*?)\s*<', t, re.S)
        with lock:
            out.append({**c, "desc": clean(m.group(1)) if m else "", "salary": clean(sal.group(1)) if sal else "",
                        "employment": crit.get("Employment type", ""), "posted": dt.group(1).strip() if dt else "",
                        "closed": "No longer accepting applications" in t})
        time.sleep(1.0)
    with ThreadPoolExecutor(3) as ex:
        list(ex.map(one, todo))
    return out


# ---------------- Employer career sites ----------------
def _loc_ok(loc):
    return (C.NYC.search(loc) or C.NEAR.search(loc) or C.REMOTE.search(loc) or "united states" in loc.lower()) and not C.BAD_LOC.search(loc)


def workday(site, seen):
    host, tenant, name, label = site
    base = f"https://{host}/wday/cxs/{tenant}/{name}"
    hdr = {**UA, "Content-Type": "application/json", "Accept": "application/json"}
    found = {}
    for q in C.WORKDAY_QUERIES:
        for off in range(0, 100, 20):
            try:
                r = requests.post(base + "/jobs", json={"appliedFacets": {}, "limit": 20, "offset": off, "searchText": q}, headers=hdr, timeout=30)
                posts = r.json().get("jobPostings", []) if r.status_code == 200 else []
            except Exception:
                posts = []
            for p in posts:
                key = f"wd:{tenant}:{p.get('externalPath')}"
                if key in seen or key in found or not title_ok(p.get("title")):
                    continue
                loc = p.get("locationsText", "")
                if not (_loc_ok(loc) or "Locations" in loc):
                    continue
                found[key] = p
            if len(posts) < 20:
                break
    out = []
    for key, p in found.items():
        try:
            jp = requests.get(base + p["externalPath"], headers=hdr, timeout=30).json().get("jobPostingInfo", {})
        except Exception:
            continue
        loc = (jp.get("location") or "") + " | " + " | ".join(jp.get("additionalLocations") or [])
        if not _loc_ok(loc):
            continue
        out.append(dict(id=key, source=label + " careers", company=label, title=jp.get("title", p["title"]), loc=loc,
                        url=jp.get("externalUrl") or f"https://{host}/en-US/{name}{p['externalPath']}", desc=clean(jp.get("jobDescription")),
                        salary="", employment=jp.get("timeType", ""), posted=jp.get("postedOn", ""), closed=False))
    return out


def greenhouse(tok, seen):
    r = get(f"https://boards-api.greenhouse.io/v1/boards/{tok}/jobs?content=true", tries=2)
    if r is None or r.status_code != 200:
        return []
    out = []
    for j in r.json().get("jobs", []):
        key = f"gh:{tok}:{j['id']}"
        loc = (j.get("location") or {}).get("name", "")
        if key in seen or not title_ok(j["title"]) or not _loc_ok(loc):
            continue
        out.append(dict(id=key, source="Greenhouse", company=(j.get("company_name") or tok), title=j["title"], loc=loc,
                        url=j.get("absolute_url"), desc=clean(html.unescape(j.get("content", ""))), salary="", employment="",
                        posted=(j.get("updated_at") or "")[:10], closed=False))
    return out


def lever(tok, seen):
    r = get(f"https://api.lever.co/v0/postings/{tok}?mode=json", tries=2)
    if r is None or r.status_code != 200:
        return []
    out = []
    for j in r.json():
        cat = j.get("categories") or {}
        loc = " | ".join([cat.get("location") or ""] + (cat.get("allLocations") or [])) + " | " + (j.get("workplaceType") or "")
        key = f"lv:{tok}:{j['id']}"
        if key in seen or not title_ok(j["text"]) or not _loc_ok(loc):
            continue
        desc = clean(j.get("description")) + "\n" + "\n".join(l.get("text", "") + "\n" + clean(l.get("content")) for l in j.get("lists", [])) + "\n" + clean(j.get("additional"))
        sr = j.get("salaryRange") or {}
        out.append(dict(id=key, source="Lever", company=tok, title=j["text"], loc=loc, url=j.get("hostedUrl"), desc=desc,
                        salary=f"${sr.get('min'):,}–${sr.get('max'):,}" if sr.get("min") else "", employment=cat.get("commitment") or "",
                        posted="", closed=False))
    return out


def ashby(tok, seen):
    r = get(f"https://api.ashbyhq.com/posting-api/job-board/{tok}?includeCompensation=true", tries=2)
    if r is None or r.status_code != 200:
        return []
    out = []
    for j in r.json().get("jobs", []):
        loc = (j.get("location") or "") + " | " + " | ".join(s.get("location", "") for s in j.get("secondaryLocations") or []) + (" | Remote" if j.get("isRemote") else "")
        key = f"ab:{tok}:{j['id']}"
        if key in seen or not title_ok(j["title"]) or not _loc_ok(loc):
            continue
        out.append(dict(id=key, source="Ashby", company=tok, title=j["title"], loc=loc, url=j.get("jobUrl"), desc=clean(j.get("descriptionHtml")),
                        salary=(j.get("compensation") or {}).get("compensationTierSummary", ""), employment=j.get("employmentType", ""),
                        posted=(j.get("publishedAt") or "")[:10], closed=False))
    return out


def career_sites(seen, log=print):
    out = []
    with ThreadPoolExecutor(10) as ex:
        for r in ex.map(lambda s: workday(s, seen), C.WORKDAY):
            out += r
        for r in ex.map(lambda t: greenhouse(t, seen), C.GREENHOUSE):
            out += r
        for r in ex.map(lambda t: lever(t, seen), C.LEVER):
            out += r
        for r in ex.map(lambda t: ashby(t, seen), C.ASHBY):
            out += r
    log(f"Career sites: {len(out)} new postings with a finance title in range")
    return out

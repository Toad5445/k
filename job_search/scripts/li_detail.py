import json, re, sys, time, html, os
import requests

IDS, OUT = sys.argv[1], sys.argv[2]
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

ids = json.load(open(IDS))
BAD = re.compile(r"senior|\bsr\.?\b|\bvp\b|vice president|director|principal|manager|head of|\blead\b|engineer|developer|intern\b|internship|summer|2027|2028|accountant|accounting|\btax\b|audit|payroll|bookkeep|counsel|attorney|recruiter|scientist|\bii\b|\biii\b|\biv\b|chief|controller|\bcfo\b|actuar|nurse|physician|billing|accounts (payable|receivable)|\bAP\b|\bAR\b|insurance agent|financial (representative|professional|advisor|consultant)", re.I)
ids = {k: v for k, v in ids.items() if not BAD.search(v["title"])}
print("to fetch", len(ids), flush=True)
det = json.load(open(OUT)) if os.path.exists(OUT) else {}


def text(s):
    s = re.sub(r"<br\s*/?>|</p>|</li>|</div>|<li>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


for jid, meta in ids.items():
    if jid in det:
        continue
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{jid}"
    r = None
    for attempt in range(4):
        try:
            r = requests.get(url, headers=H, timeout=30)
            if r.status_code == 429:
                time.sleep(6 * (attempt + 1)); continue
            break
        except Exception:
            time.sleep(3)
    if r is None or r.status_code != 200:
        det[jid] = {**meta, "error": getattr(r, "status_code", "x")}
        continue
    t = r.text
    m = re.search(r'show-more-less-html__markup[^>]*>(.*?)</div>', t, re.S)
    desc = text(m.group(1)) if m else ""
    crit = dict((text(a), text(b)) for a, b in re.findall(r'description__job-criteria-subheader">(.*?)</h3>.*?description__job-criteria-text[^>]*>(.*?)</span>', t, re.S))
    apply = re.search(r'id="applyUrl"[^>]*>\s*<!--"(.*?)"-->', t, re.S)
    posted = re.search(r'posted-time-ago__text[^>]*>\s*(.*?)\s*<', t, re.S)
    closed = "No longer accepting applications" in t
    sal = re.search(r'salary compensation__salary">\s*(.*?)\s*<', t, re.S)
    det[jid] = {**meta, "desc": desc, "crit": crit, "apply": html.unescape(apply.group(1)) if apply else "",
                "posted": posted.group(1) if posted else "", "closed": closed, "salary": text(sal.group(1)) if sal else ""}
    if len(det) % 25 == 0:
        json.dump(det, open(OUT, "w"))
        print(len(det), flush=True)
    time.sleep(0.6)
json.dump(det, open(OUT, "w"))
print("done", len(det))

import json, re, sys, html, os
import requests
from concurrent.futures import ThreadPoolExecutor

OUT = sys.argv[1]
GH = ["twosigma", "aqr", "janestreet", "wehrtyou", "pdtpartners", "schonfeld", "bamfunds", "pwpartners", "moelis",
      "guggenheimpartners", "addepar", "icapitalnetwork", "clearstreet", "arcesium", "betterment", "brex", "stash",
      "squarepointcapital", "virtu", "flowtraders", "generalatlantic", "stepstonegroup", "marketaxess", "tradeweb",
      "fundrise", "yieldstreet", "carta", "chime", "sofi", "affirm", "marqeta", "paxos", "galaxydigitalservices",
      "coinbase", "gemini", "anchorage", "point72", "vikingglobal", "lonepine", "tudor", "silverpoint", "hudsonbay",
      "millenniumadvisors", "dvtrading", "tower-research", "towerresearchcapital", "jumptrading", "imc", "optiver",
      "drw", "akunacapital", "sigconsult", "fiscalnote", "pimco", "oaktreecapital", "aresmanagement", "golubcapital",
      "blueowl", "sixthstreet", "hps", "hpsinvestmentpartners", "monroecapital", "churchillam", "antares", "maranon",
      "benefitstreetpartners", "kkr", "warburgpincus", "insightpartners", "tigerglobal", "coatue", "generalcatalyst",
      "bessemer", "lerer", "greycroft", "firstmark", "tpg", "carlyle", "blackstone", "apollo", "brookfield",
      "lazard", "pjtpartners", "centerview", "evercore", "houlihanlokey", "jefferies", "williamblair", "lincolninternational",
      "harriswilliams", "raine", "lionTree", "liontree", "gugg", "cantor", "btig", "oppenheimer", "cowen", "needham",
      "macquarie", "nomura", "mizuho", "natixis", "bnpparibas", "rbc", "bmo", "scotiabank", "cibc", "nationalbank",
      "sculptor", "davidsonkempner", "elliott", "baupost", "thirdpoint", "pershingsquare", "glenviewcapital",
      "eaglepointcredit", "stonepeak", "kkrcareers", "ardian", "hamiltonlane", "neubergerberman", "lordabbett",
      "voya", "nuveen", "pgim", "invesco", "franklintempleton", "alliancebernstein", "wellington", "fidelity",
      "mscicareers", "moodys", "kroll", "duffandphelps", "valuationresearch", "stout", "chathamfinancial",
      "trepp", "creditsights", "pitchbook", "preqin", "9fin", "octus", "reorg", "debtwire", "bloomberg",
      "ramp", "mercury", "pipe", "capchase", "arc", "rho", "tally", "public", "titan", "wealthfront", "robinhood",
      "acorns", "stripe", "plaid", "nerdwallet", "creditkarma", "lendingclub", "upstart", "bestegg", "figure",
      "better", "blend", "valon", "pagaya", "petal", "esusu", "kikoff", "self", "aspiration", "current", "dave",
      "varo", "greenlight", "step", "brightside", "payoneer", "flywire", "bilt", "bilt-rewards", "billtrust",
      "airbase", "navan", "spendesk", "tipalti", "modernTreasury", "moderntreasury", "column", "unit", "treasuryprime",
      "synctera", "alloy", "sardine", "persona", "socure", "hummingbird", "unit21", "chainalysis", "trmlabs",
      "ellevest", "farther", "range", "facet", "originfinancial", "domain", "cadre", "masterworks", "republic",
      "seedinvest", "forge", "equityzen", "augment", "nasdaqprivatemarket", "hiive", "caplight", "allocate",
      "moonfare", "juniper-square", "juniperssquare", "junipersquare", "altvia", "allvue", "dynamo", "chronograph",
      "canoeintelligence", "hightouch", "visible", "arch", "cobalt", "petra", "assetmark", "orion", "envestnet",
      "riskalyze", "nitrogen", "yieldx", "ycharts", "koyfin", "tegus", "alphasense", "aiera", "visiblealpha",
      "bitsight", "spglobal", "fitch", "dbrs", "morningstar", "kbra", "krollbondratings", "egan-jones",
      "maplecapital", "oxbow", "ironwood", "crescentcapital", "fortress", "cerberus", "angelogordon", "tpgangelogordon",
      "marathon", "kayne", "kayneanderson", "bain", "baincapital", "thl", "advent", "vista", "thomabravo", "silverlake",
      "generalatlanticcareers", "summit", "ta", "tacareers", "hgcapital", "permira", "cinven", "eqt", "cvc",
     ]
LEVER = ["arootah", "dadavidson", "flex", "scalemicrogridsolutions", "gynger", "bdg", "jobgether", "comply",
         "yieldstreet", "cadre", "masterworks", "republic", "titan", "public", "arcadia", "paxos", "kraken",
         "ramp", "mercury", "figure", "pipe", "capchase", "brex", "carta", "ondeck", "kabbage", "fundbox",
         "stashinvest", "acorns", "betterment", "wealthsimple", "personalcapital", "empower", "zest", "kensho",
         "chainalysis", "anchorage", "galaxy", "bitgo", "circle", "ripple", "consensys", "fireblocks", "talos",
         "clearco", "parafin", "settle", "wayflyer", "slope", "balance", "resolve", "melio", "routable",
         "trustly", "plaid", "dwolla", "unit", "synapse", "evolve", "lendio", "brightwheel", "tradeweb",
         "addepar", "ibkr", "drivewealth", "apex", "apexfintech", "alpaca", "atomic", "ewealth", "valuepenguin",
         "sixfold", "vouch", "newfront", "coalition", "at-bay", "kin", "lemonade", "hippo", "openly", "branch",
        ]
ASHBY = ["Convey", "fernstone", "whatnot", "ramp", "mercury", "brex", "plaid", "vanta", "deel", "rippling",
         "column", "moderntreasury", "unit", "increase", "lithic", "highnote", "rho", "meow", "slash", "puzzle",
         "pilot", "digits", "campfire", "rillet", "numeric", "tabs", "maxio", "chargeflow", "kalshi", "polymarket",
         "public", "titan", "range", "farther", "savvy", "frec", "composer", "atomic", "alpaca", "hiive",
         "augment", "caplight", "aumni", "carta", "pulley", "juniper-square", "allocate", "canoe", "chronograph",
         "9fin", "octus", "tegus", "aiera", "hebbia", "rogo", "fintool", "daloopa", "bluesky", "quartr",
         "clear-street", "clearstreet", "bilt", "imprint", "mesh", "sardine", "alloy", "persona", "middesk",
         "ondo", "securitize", "anchorage", "paxos", "galaxy", "bitgo", "fireblocks", "talos", "nydig",
        ]

LOC_OK = re.compile(r"new york|nyc|manhattan|brooklyn|remote|united states|\bus\b|usa|white plains|stamford|greenwich|westchester|harrison|purchase|tarrytown|elmsford|danbury|ridgefield|armonk|rye|mount kisco|brewster|norwalk|valhalla|yonkers|new rochelle|bronx|queens", re.I)
TITLE_OK = re.compile(r"analyst|associate|treasury|credit|investment|portfolio|risk|finance|financial|capital|valuation|kyc|aml|compliance|operations|fp&a|underwrit|research|trading|banking", re.I)
TITLE_BAD = re.compile(r"senior|sr\.?\b|\bvp\b|vice president|director|principal|manager|head of|lead\b|staff|engineer|developer|intern\b|internship|summer|2027|2028|accountant|accounting|tax|audit|payroll|bookkeep|counsel|attorney|recruit|designer|scientist|sales|account executive|\bii\b|\biii\b|\biv\b|chief|partner\b", re.I)


def clean(s):
    s = html.unescape(s or "")
    s = re.sub(r"<br\s*/?>|</p>|</li>|</div>|<li>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


def keep(title, loc):
    return TITLE_OK.search(title or "") and not TITLE_BAD.search(title or "") and LOC_OK.search(loc or "")


def gh(tok):
    out = []
    try:
        r = requests.get(f"https://boards-api.greenhouse.io/v1/boards/{tok}/jobs?content=true", timeout=30)
        if r.status_code != 200:
            return out
        for j in r.json().get("jobs", []):
            loc = (j.get("location") or {}).get("name", "")
            if keep(j["title"], loc):
                out.append({"src": "greenhouse", "board": tok, "title": j["title"], "loc": loc, "url": j.get("absolute_url"),
                            "updated": j.get("updated_at"), "desc": clean(j.get("content"))})
    except Exception as e:
        pass
    return out


def lever(tok):
    out = []
    try:
        r = requests.get(f"https://api.lever.co/v0/postings/{tok}?mode=json", timeout=30)
        if r.status_code != 200:
            return out
        for j in r.json():
            loc = (j.get("categories") or {}).get("location", "") or ""
            locs = " ".join((j.get("categories") or {}).get("allLocations", []) or [])
            if keep(j["text"], loc + " " + locs + " " + (j.get("workplaceType") or "")):
                desc = clean(j.get("description", "")) + "\n" + "\n".join(
                    l.get("text", "") + "\n" + clean(l.get("content", "")) for l in j.get("lists", [])) + "\n" + clean(j.get("additional", ""))
                out.append({"src": "lever", "board": tok, "title": j["text"], "loc": loc + " | " + locs + " | " + (j.get("workplaceType") or ""),
                            "commitment": (j.get("categories") or {}).get("commitment"), "url": j.get("hostedUrl"),
                            "salary": json.dumps(j.get("salaryRange")) if j.get("salaryRange") else "", "desc": desc})
    except Exception:
        pass
    return out


def ashby(tok):
    out = []
    try:
        r = requests.get(f"https://api.ashbyhq.com/posting-api/job-board/{tok}?includeCompensation=true", timeout=30)
        if r.status_code != 200:
            return out
        for j in r.json().get("jobs", []):
            loc = (j.get("location") or "") + " | " + " ".join(s.get("location", "") for s in j.get("secondaryLocations", []) or []) + (" | remote" if j.get("isRemote") else "")
            if keep(j["title"], loc):
                comp = (j.get("compensation") or {}).get("compensationTierSummary", "")
                out.append({"src": "ashby", "board": tok, "title": j["title"], "loc": loc, "commitment": j.get("employmentType"),
                            "workplace": j.get("workplaceType"), "url": j.get("jobUrl"), "salary": comp,
                            "desc": clean(j.get("descriptionHtml"))})
    except Exception:
        pass
    return out


res = []
with ThreadPoolExecutor(12) as ex:
    for r in ex.map(gh, GH): res += r
    for r in ex.map(lever, LEVER): res += r
    for r in ex.map(ashby, ASHBY): res += r
json.dump(res, open(OUT, "w"))
print(len(res))
from collections import Counter
print(Counter(x["board"] for x in res).most_common(60))

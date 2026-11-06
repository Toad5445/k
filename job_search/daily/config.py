"""Search configuration for the daily finance job sweep."""
import re

# LinkedIn guest search: Entry level (f_E=2), Full-time, sorted by date.
LI_KEYWORDS = [
    "financial analyst", "finance analyst", "investment analyst", "credit analyst", "treasury analyst",
    "risk analyst", "FP&A analyst", "capital markets analyst", "investment banking analyst",
    "equity research associate", "research associate finance", "portfolio analyst", "valuation analyst",
    "KYC analyst", "AML analyst", "compliance analyst", "operations analyst finance", "trading analyst",
    "finance associate", "investment associate", "credit associate", "private equity analyst",
    "real estate finance analyst", "underwriting analyst", "budget analyst", "client service analyst finance",
    "junior analyst", "entry level finance", "analyst", "associate finance", "underwriter", "corporate development associate",
    "client service associate", "operations associate", "loan operations", "middle office", "fund operations analyst",
    "transaction advisory associate", "business analyst finance", "strategy analyst", "pricing analyst", "investor relations analyst",
    "corporate banking analyst", "commercial banking analyst", "wealth management associate", "merchandise planning analyst",
]
# Seniority filter: None = no filter. Many real entry-level postings are tagged "Associate" or "Not Applicable",
# and LinkedIn has no filter value for "Not Applicable", so we search without one and let the title filter and
# experience screen do the work.
LI_LEVELS = [None]
LI_MAX_RESULTS = 1000  # per keyword and location
LI_LOCATIONS = [
    ("nyc", {"location": "New York, New York, United States"}),
    ("near", {"location": "Somers, New York, United States", "distance": "35"}),
]

# Employer career sites (no rate limit; full descriptions).
WORKDAY = [  # host, tenant, site, label
    ("spgi.wd5.myworkdayjobs.com", "spgi", "SPGI_Careers", "S&P Global"),
    ("mtb.wd5.myworkdayjobs.com", "mtb", "MTB", "M&T Bank"),
    ("td.wd3.myworkdayjobs.com", "td", "TD_Bank_Careers", "TD"),
    ("blackrock.wd1.myworkdayjobs.com", "blackrock", "BlackRock_Professional", "BlackRock"),
    ("ghr.wd1.myworkdayjobs.com", "ghr", "Lateral-US", "Bank of America"),
    ("nasdaq.wd1.myworkdayjobs.com", "nasdaq", "Global_External_Site", "Nasdaq"),
    ("mufgub.wd3.myworkdayjobs.com", "mufgub", "MUFG-Careers", "MUFG"),
    ("santander.wd3.myworkdayjobs.com", "santander", "SantanderCareers", "Santander"),
    ("capitalone.wd12.myworkdayjobs.com", "capitalone", "Capital_One", "Capital One"),
    ("aresmgmt.wd1.myworkdayjobs.com", "aresmgmt", "External", "Ares"),
    ("blackstone.wd1.myworkdayjobs.com", "blackstone", "Blackstone_Careers", "Blackstone"),
    ("tiaa.wd1.myworkdayjobs.com", "tiaa", "Search", "TIAA / Nuveen"),
    ("mmc.wd1.myworkdayjobs.com", "mmc", "MMC", "Marsh McLennan"),
    ("citi.wd5.myworkdayjobs.com", "citi", "2", "Citi"),
    ("statestreet.wd1.myworkdayjobs.com", "statestreet", "Global", "State Street"),
    ("pnc.wd5.myworkdayjobs.com", "pnc", "External", "PNC"),
    ("nb.wd1.myworkdayjobs.com", "nb", "NBCareers", "Neuberger Berman"),
    ("carlyle.wd1.myworkdayjobs.com", "carlyle", "Carlyle", "Carlyle"),
    ("synchronyfinancial.wd5.myworkdayjobs.com", "synchronyfinancial", "careers", "Synchrony"),
    ("mastercard.wd1.myworkdayjobs.com", "mastercard", "CorporateCareers", "Mastercard"),
    ("pru.wd5.myworkdayjobs.com", "pru", "Careers", "Prudential / PGIM"),
    ("pimco.wd1.myworkdayjobs.com", "pimco", "pimco-careers", "PIMCO"),
    ("mizuho.wd1.myworkdayjobs.com", "mizuho", "mizuhoamericas", "Mizuho"),
    ("abglobal.wd1.myworkdayjobs.com", "abglobal", "alliancebernsteincareers", "AllianceBernstein"),
    ("aig.wd1.myworkdayjobs.com", "aig", "aig", "AIG"),
    ("godirect.wd5.myworkdayjobs.com", "godirect", "voya_jobs", "Voya"),
    ("guggenheim.wd1.myworkdayjobs.com", "guggenheim", "Guggenheim_Partners", "Guggenheim"),
    ("athene.wd5.myworkdayjobs.com", "athene", "Apollo_Careers", "Apollo"),
    ("blueowl.wd1.myworkdayjobs.com", "blueowl", "blueowl", "Blue Owl"),
    ("travelers.wd5.myworkdayjobs.com", "travelers", "External", "Travelers"),
    ("moelis.wd1.myworkdayjobs.com", "moelis", "Experienced-Hires", "Moelis"),
    ("pjtpartners.wd1.myworkdayjobs.com", "pjtpartners", "Careers", "PJT Partners"),
    ("broadridge.wd5.myworkdayjobs.com", "broadridge", "Careers", "Broadridge"),
    ("ntrs.wd1.myworkdayjobs.com", "ntrs", "northerntrust", "Northern Trust"),
    ("hl.wd1.myworkdayjobs.com", "hl", "Campus", "Houlihan Lokey"),
    ("raymondjames.wd1.myworkdayjobs.com", "raymondjames", "RaymondJamesCareers", "Raymond James"),
]
WORKDAY_QUERIES = ["analyst", "associate", "finance", "credit", "investment"]
GREENHOUSE = ["point72", "icapitalnetwork", "chronograph", "pdtpartners", "clearstreet", "octus", "mercury", "robinhood",
              "williamblair", "liontree", "generalatlantic", "hpsinvestmentpartners", "trepp", "sofi", "gemini", "fiveringsllc",
              "schonfeld", "exoduspoint", "lincolninternational", "betterment", "carta", "equityzen", "brex", "ripple", "kalshi",
              "virtu", "flowtraders", "squarepointcapital", "alphasense", "stripe", "aqr"]
LEVER = ["dadavidson", "arootah", "yieldstreet", "addepar"]
ASHBY = ["ramp", "mercury", "column", "moderntreasury", "rho", "allocate", "range", "titan", "public", "9fin"]

# ---- Screening vocabulary ----
TITLE_GOOD = re.compile(r"financ|analyst|credit|treasury|invest|portfolio|risk|capital|bank|valuation|fp&a|kyc|aml|compliance|trad(e|ing)|fund|equity|wealth|asset|underwrit|research|m&a|deal|budget|pricing|strateg|"
                        r"associate|underwriter|loan|lending|coverage|transaction|corporate development|middle office|operations|"
                        r"client service|trust|performance|planner|planning|merchandis|investor relations|reporting|onboarding|settlement|"
                        r"derivatives|\bfx\b|securities|markets|mortgage|insurance|reinsurance|economic", re.I)
TITLE_BAD = re.compile(r"senior|\bsr\.?\b|\bvp\b|vice president|director|principal|manager|head of|\blead\b|\bchief\b|engineer|developer|scientist|"
                       r"intern\b|internship|summer|co-?op|2027|2028|accountant|accounting|\btax\b|audit|payroll|bookkeep|billing|"
                       r"receivable|payable|\bii\b|\biii\b|\biv\b|\b[2-5]\b(?!0)|counsel|attorney|paralegal|recruit|nurse|teller|relationship banker|personal banker|client associate|"
                       r"sales|account executive|business development rep|financial (advisor|representative|professional|consultant)|"
                       r"insurance agent|quant|talent (network|community|pool)|insight day|apprentice|fellowship|machine learning|software|data engineer|controller|\bcfo\b|actuar|avp|executive assistant|"
                       r"part[- ]time|seasonal|customer service|store|stock(ing)? (team )?associate|cashier|warehouse|fulfillment|fleet|task associate|"
                       r"guest service|front of house|backroom|pharmacy|production (associate|planner)|patient|clinical|behavior analyst|bcba|"
                       r"technical support|desktop support|help ?desk|media (planning|buying|analytics)|(?<!compliance )marketing|events?\b|veterinar|retail associate|sales associate", re.I)
NYC = re.compile(r"new york|\bnyc\b|manhattan|brooklyn|queens|bronx|staten island|jamaica, ny|flushing|long island city|astoria|"
                 r"forest hills|bayside|jackson heights|elmhurst|corona, ny|ridgewood, ny|woodside|sunnyside, ny|rego park|kew gardens", re.I)
NEAR = re.compile(r"white plains|purchase|harrison|\brye\b|rye brook|port chester|armonk|elmsford|tarrytown|sleepy hollow|valhalla|hawthorne|"
                  r"mount kisco|bedford|katonah|somers, ny|yorktown|brewster|carmel|mahopac|peekskill|ossining|chappaqua|pleasantville|"
                  r"scarsdale|yonkers|new rochelle|mount vernon|greenwich|stamford|norwalk|darien|new canaan|ridgefield|danbury|"
                  r"brookfield, ct|bethel|westport|wilton|fishkill|beacon|westchester|fairfield county|croton|cortlandt|montrose, ny|buchanan, ny|"
                  r"briarcliff|ardsley|dobbs ferry|irvington, ny|hastings-on-hudson|bronxville|eastchester|tuckahoe|mamaroneck|larchmont|"
                  r"pelham|nanuet|nyack|pearl river|suffern|orangeburg, ny|new city, ny|spring valley, ny|west nyack|rockland|"
                  r"cold spring|garrison|patterson, ny|pawling|hopewell junction|wappingers|poughkeepsie|newburgh|newtown, ct|"
                  r"new milford, ct|trumbull|shelton|monroe, ct|redding, ct|weston, ct|putnam county|dutchess", re.I)
BAD_LOC = re.compile(r", nj\b|new jersey|jersey city|hoboken|newark|jericho|melville|hauppauge|garden city|long island(?! city)|plainview|uniondale|"
                     r"mineola|hicksville|islandia|bethpage|lake success|westbury|huntington, ny|orangeburg, sc|edgewood|somers point|rio grande|cape may|atlantic city", re.I)
REMOTE = re.compile(r"\bremote\b|work from home|telecommut", re.I)
NOT_REMOTE = re.compile(r"hybrid|\d days? (a|per) week (in|on)|in[- ]office|on-?site (role|position|requirement)|must be located in", re.I)

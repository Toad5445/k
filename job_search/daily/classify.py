"""Rule-based first pass. Every posting gets accept / review / reject plus the reasons and the
experience lines quoted from the posting. Accept and review both get a final read before publishing."""
import re
import config as C

NUM = r"(?:\d+|zero|one|two|three|four|five|six|seven|eight|nine|ten)"
WORD = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
YRS = re.compile(r"\b(" + NUM + r")\s*(?:\+|plus)?\s*(?:(?:-|–|—|to)\s*(?:" + NUM + r")\s*\+?\s*)?(?:\(\d+\)\s*)?(?:full[- ]time\s+)?(?:years?|yrs?)\b", re.I)
MONTHS = re.compile(r"\b(\d+|six|twelve|eighteen)\s*\+?\s*months?\b[^.\n]{0,60}experience", re.I)
NONEXP = re.compile(r"years? old|of age|founded|in business|ago|year[- ]round|per year|each year|every year|multi[- ]year|this year|since \d{4}|"
                    r"in a row|anniversary|\bvesting\b|(year|month)s? (program|rotation)|[- ]year (program|rotation|analyst program)|over the (past|last)|"
                    r"\d+ years of (unbroken|history|operation\b|growth)|for (over|more than) \d+ years|track record|sabbatical|"
                    r"years? of (age|service)|tenure with|\d+-year", re.I)
UPTO = re.compile(r"\bup to\b|no more than|less than|\bmaximum\b|or fewer|at most|\bunder \d", re.I)
SOFT = re.compile(r"prefer|a plus|is a plus|nice to have|ideal|desired|desirable|bonus|advantage|beneficial|helpful|not required|"
                  r"optional|encouraged|welcome|considered|strongly consider|\bno [\w ]{0,15}required", re.I)
SOFT_HEAD = re.compile(r"^(preferred|nice to have|bonus|desired|pluses|plus|additional|preferred qualifications|preferred skills|"
                       r"preferred experience|what would be nice|nice-to-haves?|it would be great)", re.I)
HARD_HEAD = re.compile(r"^(required|requirements|minimum|basic|must|what you('ll)? (need|bring|have)|qualifications|you have|about you|"
                       r"who you are|education|experience|skills)", re.I)
POSITIVE = re.compile(r"\b0\s*(?:-|–|to)\s*\d|zero to|no (prior |previous )?(work )?experience (is )?(required|necessary|needed)|"
                      r"recent (college |university )?grad|new grad|entry[- ]level|early[- ]career|class of 2026|graduat\w+ (in|by) (may|spring|20)[^.\n]{0,15}2026", re.I)
REQ_NO_NUM = re.compile(r"(must have|required|requires|requirement|minimum)[^.\n]{0,50}\bexperience\b|\bexperience\b[^.\n]{0,70}\b(is )?required\b|"
                        r"(prior|previous|proven|demonstrated) (work )?experience (in|with|as)", re.I)
HARD_SKILL = {
    "Python": re.compile(r"\bpython\b", re.I), "SQL": re.compile(r"\bsql\b", re.I), "Master's degree": re.compile(r"master'?s degree|\bMBA\b (is )?required", re.I),
    "CFA": re.compile(r"\bCFA\b(?! (level|candidate|progress|program))", re.I), "CPA": re.compile(r"\bCPA\b", re.I),
    "a second language": re.compile(r"(fluen|proficien|bilingual)[^.\n]{0,40}(mandarin|spanish|japanese|korean|french|german|chinese|cantonese|portuguese|italian|arabic|russian|hebrew)", re.I),
    "an active license": re.compile(r"(active|current|must (hold|have))[^.\n]{0,25}(series (7|63|65|66|79|24)|license)", re.I),
}
REQ_WORD = re.compile(r"required|must|need to|essential|mandatory|minimum|proficien|strong (knowledge|experience|skills)|expert", re.I)
GRAD = re.compile(r"class of 2027|2027 (start|graduat|analyst|program|class)|start(s|ing)? (date|in)[^.\n]{0,25}2027|summer 2027|fall 2027|"
                  r"graduat\w+ (between|by|in)[^.\n]{0,40}2027|currently (enrolled|pursuing)|penultimate|rising senior|returning student", re.I)
TEMP = re.compile(r"(employment|job|position) type:?\s*(contract|temporary|part[- ]time)|\bcontract[- ]to[- ]hire\b|temp[- ]to[- ]perm|"
                  r"this is a (\d+[- ]month )?(temporary|contract)|\b\d+[- ]month contract\b|w2 contract|1099", re.I)
HOURLY = re.compile(r"\$\s?\d{2}(\.\d\d)?\s*(/|per|an)\s*h(ou)?r", re.I)
REDFLAG = re.compile(r"northwestern mutual|new york life|mass ?mutual|bankers life|globe life|primerica|transamerica agency|"
                     r"build your (own )?(book|agency|practice)|commission[- ]only|100% commission|uncapped commission|unlimited earning|"
                     r"ai (trainer|tutor|training)|train(ing)? (next-generation )?ai (models|systems)|evaluat\w+ ai (models|agents)|"
                     r"alignerr|mercor|dataannotation|afterquery|outlier\.ai|revature|pass-through fees|nm\.com", re.I)
ACCT = re.compile(r"reconcil|journal entr|general ledger|accounts payable|accounts receivable|month[- ]end close|\bSOX\b|invoice|bookkeep|accrual", re.I)


def _num(s):
    s = s.lower()
    return WORD[s] if s in WORD else int(s)


def experience_lines(desc):
    """Return (required_floor or None, quoted lines, soft_only flag)."""
    lines = [l.strip(" •·-*\t") for l in (desc or "").split("\n")]
    soft_section = False
    floor, quotes = None, []
    for l in lines:
        if not l:
            continue
        if len(l) < 70 and not YRS.search(l):
            if SOFT_HEAD.search(l):
                soft_section = True
            elif HARD_HEAD.search(l):
                soft_section = False
        hit = False
        for m in YRS.finditer(l):
            ctx = l[max(0, m.start() - 80): m.end() + 120]
            if NONEXP.search(ctx) or not re.search(r"experience|exp\b|background|work|role|industry|banking|finance|years? (in|of)", ctx, re.I):
                continue
            hit = True
            lo = _num(m.group(1))
            if lo == 0 or lo > 15 or UPTO.search(ctx) or SOFT.search(l) or soft_section:
                continue
            floor = lo if floor is None else min(floor, lo)
        mm = MONTHS.search(l)
        if mm and not SOFT.search(l) and not soft_section:
            hit = True
            floor = 1 if floor is None else floor
        if hit or (re.search(r"\bexperience\b", l, re.I) and (POSITIVE.search(l) or REQ_NO_NUM.search(l))):
            quotes.append(l[:300])
    return floor, quotes[:4]


def classify(p):
    d, title, loc = p.get("desc") or "", p.get("title") or "", p.get("loc") or ""
    text = d + "\n" + title
    reasons, flags = [], []
    if p.get("closed"):
        return "reject", ["no longer accepting applications"], [], None, []
    emp = (p.get("employment") or "").lower()
    if emp and not re.search(r"full", emp):
        reasons.append(f"not full-time ({p['employment']})")
    if REDFLAG.search(text + " " + (p.get("company") or "")):
        return "redflag", ["red flag: " + REDFLAG.search(text + " " + (p.get("company") or "")).group(0)], [], None, []
    # location
    if C.BAD_LOC.search(loc):
        reasons.append("NJ / Long Island")
    group = None
    if C.NYC.search(loc):
        group = "nyc"
    elif C.NEAR.search(loc) or p.get("where") == "near":
        group = "near"
    elif C.REMOTE.search(loc + " " + d[:3000]) and not C.NOT_REMOTE.search(d):
        group = "remote"
    else:
        reasons.append(f"outside your area ({loc[:60]})")
    if group == "remote" and re.search(r"(remote|eligible|hire)[^.\n]{0,80}(only|in the following states)[^.\n]{0,200}", d, re.I) and not re.search(r"new york|\bNY\b", d):
        flags.append("remote may be limited to certain states")
    # experience
    floor, quotes = experience_lines(d)
    if floor:
        reasons.append(f"requires {floor}+ years")
    for name, rx in HARD_SKILL.items():
        for l in d.split("\n"):
            if rx.search(l) and REQ_WORD.search(l) and not SOFT.search(l):
                reasons.append(f"requires {name}")
                break
    if GRAD.search(text):
        reasons.append("wrong graduation cycle / enrollment: " + GRAD.search(text).group(0))
    if TEMP.search(d):
        reasons.append("temporary / contract")
    if HOURLY.search(d):
        flags.append("paid hourly")
    if REQ_NO_NUM.search(d) and not floor:
        m = [l.strip() for l in d.split("\n") if REQ_NO_NUM.search(l) and not SOFT.search(l)]
        if m:
            flags.append("may require prior experience: " + m[0][:160])
    n_acct = len(ACCT.findall(d))
    if n_acct >= 4:
        flags.append(f"accounting-heavy duties ({n_acct} mentions)")
    elif n_acct >= 2:
        flags.append("some accounting-type duties")
    if reasons:
        return "reject", reasons, flags, group, quotes
    if POSITIVE.search(d) and not flags:
        return "accept", [], flags, group, quotes
    return "review", [], flags, group, quotes

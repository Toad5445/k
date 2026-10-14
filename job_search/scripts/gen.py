import csv, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from jobs_data import JOBS, BACKUPS

OUT = sys.argv[1]

SCREENED = [
    ("iCapital", "Structured Investments Distribution – Analyst (NYC)",
     "Cold-calling dressed up as an analyst job. The duties are to \"conduct calls to set appointments for licensed sales professionals\" and \"make 50+ outbound calls per day.\" It's also paid hourly as a non-exempt role."),
    ("Atomic (unnamed \"stealth\" AI holding company)", "Deal Origination Associate (Remote)",
     "Cold-outreach deal sourcing: \"Run heavy outbound. 100+ meaningful founder touches per week – cold email, LinkedIn, phone.\" It also requires 2–5 years of deal-sourcing experience."),
    ("ELITEBRAIN", "Financial Expert (Remote USA or LATAM)",
     "AI-training gig: a project-based role to \"help train next-generation AI systems\" by writing prompts and rubrics. Freelance work, not a job."),
    ("Xperteez Technology", "Bloomberg Specialist (Remote – Contract)",
     "AI-training contract (\"Role Type: Contractor\"), producing Bloomberg workflow data \"that supports the development of next-generation AI systems.\""),
    ("Leland", "Private Equity Mentor",
     "Freelance coaching gig (\"Coaches set their own hours and rates\"), not employment."),
    ("The SKG Team at Barnum Financial Group", "Investment Operations Associate (Elmsford, NY)",
     "A wealth-management team at an insurance-agency practice (the posting talks about \"proper protection planning\" for families). It's salaried at $65K, but it's the insurance-agency type of role you asked me to exclude."),
    ("EQT Corp.", "Compliance Specialist – Operations & Risk (Remote)",
     "Remote work excludes New York: \"excluding the following states: California, Connecticut, … New Jersey, New York, and Tennessee unless willing to relocate.\""),
    ("TalentHop", "AML Analyst (Remote, $54–60K)",
     "Staffing-agency posting for an unnamed employer, and it requires \"Experience with AML procedures and compliance requirements\"."),
    ("Jobgether", "200+ \"Financial Analyst\" postings on its job board",
     "A job-aggregator site that reposts other companies' listings. I skipped all of them."),
    ("Hedgeye Risk Management", "Analyst, Research (future opportunity) – Stamford, CT",
     "Not a real opening: \"Please note there is not an active opening at this time.\""),
    ("Robert Half", "Financial Analyst – Entry Level (various)",
     "Temporary or temp-to-hire hourly placements."),
]

OTHER = [
    "**Experience floor above 0:** Pace University Budget Analyst (Pace's own posting says \"1-2 years\"; the LinkedIn copy left that out), Flex Financial Crime Analyst (remote, \"1–2 years\"), Macquarie ECS Analyst (1–3), Ares PE Secondaries (1–3), SMBC Trust Project Finance Credit Analyst (2+), Morgan Stanley Strategic Investments (1–2+), CIBC EIT Analyst and Wells Fargo PCM Analyst (6+ months), BofA ER Gaming & Lodging (9–12+ months), TD CIB Credit FIG (3–5), Oxford Properties (2+), Hightower (3+), LionTree (2+), Octus (2–6), Pelham Berkeley Compliance (3–36 months).",
    "**Requires prior experience without a number:** Point72 Macro & Alternatives Trade Support (Stamford; \"Zero to two years,\" but also requires hands-on confirmation-platform and futures-commission experience), RBC Municipal Finance, BNP Paribas Sector IB, BMO Equity Research, American Century ABS, Augustus Financial Crimes, Mercury KYC, Vestwell AML, Klarna, Brookfield, Volta, Citadel, Atlas Search and SMBC FX Settlements, Morgan Stanley Restricted Securities (Purchase).",
    "**Wrong graduation cycle or requires current enrollment:** S&P Global CREDit Graduate Program (\"current undergraduate… penultimate year of study only\"), DESRI Investment & Acquisitions (\"start date in Summer/Fall 2027\"), Barings Real Estate Debt Analyst Program (\"anticipated completion in Spring 2027\"), Bridgewater Finance Associate and Portfolio Associate (Class of 2027), BlackRock and TD 2027 programs.",
    "**Python, SQL or a Master's required:** MetLife/PineBridge Multi Asset Analyst, Kalshi Surveillance Analyst, TransUnion Argus Consulting Analyst (White Plains), Point72 Technical Business Analyst, Morgan Stanley FID Municipal Markets, Greystone Planning & RE Analyst.",
    "**Accounting work under a finance title:** Tapestry Analyst, Credit (AR, collections, journal entries), Cantina Labs Financial Analyst (runs the accounts-payable process), Tanya Taylor Junior Financial Analyst (AP/AR), Hearst Magazines Financial Analyst (SOX, reconciliations), CBRE Finance Analyst (journal entries), Precision AQ Client Finance Analyst I (invoicing, accruals, GL reconciliations).",
    "**Other:** Healthpeak Investments Analyst (I couldn't confirm the location; Built In shows NYC but HQ is Denver and another listing says Albany), Tokio Marine HCC Associate Underwriter in Chappaqua (hourly, insurance underwriting, requires office work experience), NewtekOne Commercial Credit Analyst (remote, but both listings show \"This job has closed\"), VX Services Commercial Finance Analyst (posting removed).",
]

g_order = ["Remote", "NYC", "Near Somers"]
g_title = {"Remote": "Remote (open to New York residents)", "NYC": "New York City", "Near Somers": "Near Somers, NY (within ~45 min drive)"}

L = []
L.append("# Entry-Level Finance Jobs: Batch 1")
L.append("")
L.append("For Makar Kozlov (Somers, NY · Binghamton SOM, BS Business Administration, Finance concentration, May 2026 · GPA 3.81)")
L.append("")
L.append("Compiled and checked on **October 14, 2026**. **20 roles meet every hard requirement** (1 remote, 17 in NYC, 2 near Somers). Four backup candidates are listed separately and are not counted.")
L.append("")
L.append("**How each posting was checked:**")
L.append("- I read the full description from the employer's own job feed (Greenhouse, Lever or Workday) or from the full LinkedIn or Built In listing, not a search-result snippet.")
L.append("- The experience line below is quoted word for word.")
L.append("- I re-checked every posting on Oct 14, 2026 and found it still live: no \"No longer accepting applications\" banner on LinkedIn, and still listed on the employer's site or Built In.")
L.append("- I checked each one for an experience floor of 0, the right graduation cycle, no internship/temp/contract/commission arrangement, no accounting duties, no Python/SQL/Master's/CFA/CPA requirement, and location, and against your already-seen list.")
L.append("")
L.append("**Sources searched:** LinkedIn (about 1,700 entry-level, full-time postings across 26 finance title searches in NYC, Westchester, Stamford, Danbury and US-remote), Built In (remote and NYC entry-level finance), and the Greenhouse, Lever, Ashby and Workday job boards of a few hundred finance and fintech employers.")
L.append("")
L.append("**Remote roles are scarce.** Nearly every remote entry-level finance listing I opened was hybrid, excluded New York, required 1+ years, or was an AI-training gig. Only one remote role passed, and it carries a caveat.")
L.append("")
n = 0
for g in g_order:
    L.append(f"## {g_title[g]}")
    L.append("")
    for j in [x for x in JOBS if x["group"] == g]:
        n += 1
        L.append(f"### {n}. {j['company']}: {j['title']}")
        L.append("")
        loc = j["location"] + (f" · **Drive from Somers:** {j['drive']}" if j["drive"] else "")
        L.append(f"- **Location / work mode:** {loc} · {j['mode']}")
        L.append(f"- **Salary:** {j['salary']}")
        L.append(f"- **Link:** {j['link']}")
        L.append(f"- **Source:** {j['source']}")
        L.append(f"- **Experience requirement (quoted):** \"{j['exp']}\"" if not j['exp'].startswith("No years") else f"- **Experience requirement:** {j['exp']}")
        L.append(f"- **Role:** {j['summary']}")
        if j["caveat"]:
            L.append(f"- **⚠ Caveat:** {j['caveat']}")
        L.append("")
L.append("## Backup candidates (not counted in the 20)")
L.append("")
L.append("These technically meet the rules but carry more doubt than the 20 above. Worth a look if you want more volume.")
L.append("")
for b in BACKUPS:
    L.append(f"- **{b['company']}: {b['title']}** ({b['location']}; {b['salary']}). {b['link']}  ")
    L.append(f"  Experience: \"{b['exp']}\"  ")
    L.append(f"  Why it's a backup: {b['why']}")
L.append("")
L.append("## Screened out")
L.append("")
L.append("### Red flags")
L.append("")
for c, t, r in SCREENED:
    L.append(f"- **{c}: {t}.** {r}")
L.append("")
L.append("### Other exclusions (failed a hard requirement)")
L.append("")
for o in OTHER:
    L.append(f"- {o}")
L.append("")
L.append("**Already seen:** I checked every result against your applied/previously-sent list. Deckers (Financial Analyst – Retail), Citrini Research and OTC Markets (Trading Compliance) came up again and were dropped.")
L.append("")
open(os.path.join(OUT, "finance_jobs.md"), "w").write("\n".join(L))

with open(os.path.join(OUT, "finance_jobs.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["#", "Group", "Company", "Title", "Location", "Work mode", "Drive from Somers", "Salary", "Link", "Source", "Experience requirement (quoted)", "Summary", "Caveat"])
    for i, j in enumerate([x for g in g_order for x in JOBS if x["group"] == g], 1):
        w.writerow([i, g_title[j["group"]], j["company"], j["title"], j["location"], j["mode"], j["drive"], j["salary"], j["link"], j["source"], j["exp"], j["summary"], j["caveat"]])
print("jobs", len(JOBS))

# Finance job search toolkit

Scripts and records behind `finance_jobs.md` / `finance_jobs.csv`, kept so the next batch starts from working tools instead of from scratch. Nothing here runs on its own; it's only used when a new batch is requested.

## Screening rules (as of Oct 14, 2026)

A job must meet every one:

1. Full-time, permanent, salaried. No internships, part-time, temp, contract, contract-to-hire or freelance.
2. **Experience floor of 0.**
   - Ranges that start at 0 are fine ("0-2 years", "recent grads welcome").
   - **"Up to N years" is fine, even when followed by "is required"**: zero falls inside "up to".
   - Exclude any minimum above 0 ("1+ years", "1-3 years", "minimum 6 months"), even when it's only "preferred".
   - **Exclude postings that require prior experience without a number**, including "entry-level experience … required".
3. Graduation cycle fits May 2026. No Class of 2027 programs, 2027 start dates, or current-enrollment requirements.
4. Finance first, general business second.
5. No accounting roles. Judge by the actual duties, not the title.
6. Location, in priority order: remote open to New York residents, then NYC, then within about 45 minutes' drive of Somers, NY. No New Jersey or Long Island.
7. No Python, SQL, Master's, CFA/CPA, non-English language or active license required (licenses sponsored after hire are fine).

Clarifications:

- **Insurance companies are fine** for finance roles: FP&A, investments, treasury, risk and similar. Exclude insurance *sales* roles (Financial Representative, agency-building, commission pay).
- **Staffing-agency postings are fine.** Flag that the employer is unnamed so it can be confirmed.

Red flags (exclude and list separately):

- Commission or cold-calling roles with analyst titles.
- AI-training gigs.
- Aggregator reposts (Jobgether, Joveo/SecondWind).
- Remote roles whose state list leaves out New York.

## Files

- `data/already_seen.csv` lists every posting already sent (batch 1 and its backups) plus the applied/previously-sent list. Check new results against it.
- `data/screening_log.txt` records the include/exclude decision and reason for each posting reviewed in batch 1.
- `data/reviewed_linkedin_ids.json` holds LinkedIn job IDs already read, so they can be skipped.

## Pipeline (`scripts/`)

| Script | What it does |
|---|---|
| `li_search.py OUT.json` | LinkedIn guest search: entry-level, full-time, past 30 days, across 26 finance titles × NYC / Westchester / Stamford / Danbury / US-remote. |
| `li_detail.py IDS.json OUT.json` | Downloads full LinkedIn descriptions, skipping senior and accounting titles. LinkedIn throttles to about 25 postings a minute. |
| `ats_pull.py OUT.json` | Pulls Greenhouse, Lever and Ashby boards for a list of finance and fintech employers. |
| `wd.py OUT.json "host\|tenant\|site\|label;..." "query;..."` | Searches Workday career sites (banks and asset managers). |
| `builtin.py OUT.json` | Built In remote and NYC entry-level finance listings. |
| `screen.py IN.json OUT.json` | First-pass filter. Classifies the experience floor and flags Python, SQL, CFA, Master's, contract, commission and accounting terms. It's only a pre-filter; every shortlisted posting still gets read in full. |
| `req.py`, `lishow.py`, `bishow.py`, `show.py` | Print a posting's requirement lines or full text for manual review. |
| `jobs_data.py` + `gen.py OUTDIR` | The final job list, and the generator for `finance_jobs.md` / `.csv`. |

Run Python with `-I`, and keep downloaded data in a scratch folder outside the repo.

Lessons from batch 1:

- LinkedIn's copy sometimes cuts off the requirements section (Pace University's posting hid "1-2 years"). If no requirement is visible, check the employer's own posting.
- LinkedIn's remote filter is unreliable, and real remote entry-level finance roles are rare.

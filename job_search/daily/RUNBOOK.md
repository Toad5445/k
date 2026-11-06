# Daily job sweep runbook

Run this from a fresh cloud session every morning. Goal: put today's new entry-level finance matches for Makar Kozlov on
**Makar's Job Board** (https://claude.ai/artifact/RwZix5jhKfvpzfY4qGEcvY) before he wakes up. Work quietly; there is no one
watching. Don't send progress updates.

## 1. Get the code and the board's memory
`git clone https://github.com/Toad5445/k /home/user/k` (the repo is public; no add_repo or push access is needed —
this run never pushes to git).

Then download what the board already knows, so nothing is read twice. Load the ArtifactData tool (ToolSearch
`select:ArtifactData`) and, with `url: https://claude.ai/artifact/RwZix5jhKfvpzfY4qGEcvY`, run `action: "list"` with
`out_dir: /home/user/k/job_search/daily/board` and `query: {"limit": 1000}` for each of these collections:
- `seen` (one doc per earlier run, listing every posting id it read)
- `jobs` (every job already on the board)

Follow `next_cursor` if a result has one. The files land in `board/seen/` and `board/jobs/`, where run.py picks them up.

## 2. Fetch and auto-sort (about 45–75 minutes, unattended — this is normal)
```
cd /home/user/k/job_search/daily && python3 -m pip install -q requests 2>/dev/null; python3 -I run.py
```
Run it in the background and wait for it to finish. It reads only postings it has never seen before (`state/seen.json` plus the `board/` files from step 1), from:
- LinkedIn, last 36 hours, all seniority levels (many real entry-level jobs are tagged "Not Applicable"), Full-time,
  NYC and within ~35 miles of Somers, NY, every result page (not just the first few)
- about 70 employers' own career sites (Workday, Greenhouse, Lever, Ashby)

It writes `out/candidates.json`: the postings the rules marked `accept` or `review`. Everything else was rejected
automatically. It also writes `out/seen_doc.json`: every id this run read, for step 5.

## 3. Final read (the only part that needs judgment — take your time)
Open every candidate in `out/candidates.json` and read its WHOLE `desc` (not just the first few hundred characters:
requirements are usually near the end). Budget about a minute per candidate; 100+ candidates can take over an hour,
and that is expected. Do not skim to save time. Work in batches of ~10 and write decisions as you go.

Default to APPROVE. Reject only when you can quote a specific line that breaks one of these rules:
- Full-time, salaried, permanent. No internships, temp, contract, part-time, hourly-only, or commission pay.
- Experience: "0–N years", "recent grads", "up to N years", "N years including internships/coursework", or any years
  listed as preferred / ideal / a plus are FINE. Reject only if a minimum above 0 is REQUIRED (e.g. "2+ years required",
  "minimum 1 year", or a plain "2+ years of experience in X" under Requirements), or prior work experience is explicitly
  required without a number. Company history ("40 years of expertise") is not an experience requirement.
- Fits a May 2026 graduate: no Class of 2027 programs, 2027 start dates, or "currently enrolled".
- Finance or finance-adjacent business role (banking, investing, credit, risk, compliance, ops at financial firms,
  insurance underwriting, FP&A, corporate finance, strategy, real estate finance, merchandise/financial planning).
  Not pure accounting (AP/AR, staff accountant, tax, audit, bookkeeping, reconciliation-only). Not IT/engineering/data
  engineering. Mixed roles are fine with a caveat.
- Location: NYC (all five boroughs), within ~50 minutes' drive of Somers, NY (Westchester, Putnam, Rockland, southern
  Dutchess, Fairfield County CT), or remote open to New York residents. No New Jersey or Long Island.
- No required Python, SQL, Master's, CFA/CPA, second language, or active license (preferred / sponsored after hire is fine).
- Insurance companies are fine for finance roles; insurance or commission SALES roles are not. Staffing-agency posts are
  fine (caveat: confirm the employer).
- Not already on the board (`board/jobs/`) — same company AND same title counts as a duplicate even with a different id.
- Not one of these already-seen roles: Paul Weiss; Societe Generale IB/M&A roles; Credit Agricole CIB; Goldman (QIS,
  Capital Solutions); Stifel; MUFG Rates Trading Assistant; Leargas; NYC OMB; Piper Sandler; Evercore; Somnia; CRP; Deeter;
  Deckers; 747 Capital; UOB; Secretariat; Port Authority; Capgemini; M2O; Axiom; Citrini; JPMorgan ECM and WM Solutions;
  Stagwell; LevelUP; Iron Road; Man Group; OTC Markets; CAIS; Welltower; Janebridge; 32BJ; Freepoint; ACX; DLC; (qp);
  Interactive Brokers; and batch 1's roles in `finance_jobs.md` at the repo root.

Red flags go on the board's red-flag list, not the job list: insurance-agency "financial representative" roles, commission or
cold-calling "analyst" roles, AI-training gigs, fake-remote relocation programs (e.g. Revature), and suspicious templated posts.

Write three files. Every candidate id must be in exactly one of them — publish.py refuses to run otherwise:
- `out/approved.json`: `[{"id": "<candidate id>", "exp": "<exact experience line quoted, or 'No years stated; ...'>", "caveat": "<short caveat or ''>"}]`
  Optional overrides per job: `company`, `title`, `loc` (add drive time for near-Somers jobs, e.g. "Stamford, CT, ~40 min drive"),
  `salary`, `group` (remote / nyc / near).
- `out/rejected.json`: `[{"id": "...", "reason": "<rule broken + the quoted line>"}]`
- `out/redflags.json`: `[{"id": "...", "reason": "..."}]` (may be `[]`)

## 4. Publish to the board
```
python3 -I publish.py
```
It prints one JSON `writes` array per 50 documents. Send each with the ArtifactData tool:
`action: "batch"`, `url: https://claude.ai/artifact/RwZix5jhKfvpzfY4qGEcvY`, `writes: <that array>`.
Then read `meta/run` (`action: "get"`) and `update` it (with `if_version`) to
`{"note": "Last updated <Mon D, YYYY>: <N> new matches from <M> new postings.", "updated": "<YYYY-MM-DD>"}`.

## 5. Save what was read (do this even if there were 0 matches)
ArtifactData `action: "set"`, same `url`, `collection: "seen"`, `doc_id: "<YYYY-MM-DD>"` (add `-2`, `-3`… if that id
already exists in `board/seen/`), `file_path: /home/user/k/job_search/daily/out/seen_doc.json`.
Do NOT commit or push anything to git.

## 6. Finish
Reply with one line: how many postings were read, how many matches were added, and the board link.

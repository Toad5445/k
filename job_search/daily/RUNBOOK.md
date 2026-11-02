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

## 2. Fetch and auto-sort (about 10–20 minutes, unattended)
```
cd /home/user/k/job_search/daily && python3 -m pip install -q requests 2>/dev/null; python3 -I run.py
```
Run it in the background and wait for it to finish. It reads only postings it has never seen before (`state/seen.json` plus the `board/` files from step 1), from:
- LinkedIn, last 24 hours, Entry level + Full-time, NYC and within ~35 miles of Somers, NY
- about 70 employers' own career sites (Workday, Greenhouse, Lever, Ashby)

It writes `out/candidates.json`: the postings the rules marked `accept` or `review`. Everything else was rejected
automatically. It also writes `out/seen_doc.json`: every id this run read, for step 5.

## 3. Final read (the only part that needs judgment)
Read each candidate's `desc`, `quotes` and `flags`. Approve it only if ALL of these hold:
- Full-time, salaried, permanent. No internships, temp, contract, hourly-only, or commission pay.
- Experience: "0–N years", "recent grads", "up to N years", or any years listed as preferred / ideal / a plus are FINE.
  Reject only if a minimum above 0 is REQUIRED, or prior experience is required without a number.
- Fits a May 2026 graduate: no Class of 2027 programs, 2027 start dates, or "currently enrolled".
- Finance or finance-adjacent business role. Not pure accounting (AP/AR, staff accountant, tax, audit, bookkeeping,
  reconciliation-only). Mixed roles are fine with a caveat.
- Location: NYC, within ~50 minutes' drive of Somers, NY, or remote open to New York residents. No New Jersey or Long Island.
- No required Python, SQL, Master's, CFA/CPA, second language, or active license (licenses sponsored after hire are fine).
- Insurance companies are fine for finance roles; insurance or commission SALES roles are not. Staffing-agency posts are fine
  (caveat: confirm the employer).
- Not already on the board (the board's `jobs` collection) and not one of these already-seen roles: Paul Weiss; Societe Generale
  IB/M&A roles; Credit Agricole CIB; Goldman (QIS, Capital Solutions); Stifel; MUFG Rates Trading Assistant; Leargas; NYC OMB;
  Piper Sandler; Evercore; Somnia; CRP; Deeter; Deckers; 747 Capital; UOB; Secretariat; Port Authority; Capgemini; M2O;
  Axiom; Citrini; JPMorgan ECM and WM Solutions; Stagwell; LevelUP; Iron Road; Man Group; OTC Markets; CAIS; Welltower;
  Janebridge; 32BJ; Freepoint; ACX; DLC; (qp); Interactive Brokers; and batch 1's roles in `finance_jobs.md` at the repo root.

Red flags go on the board's red-flag list, not the job list: insurance-agency "financial representative" roles, commission or
cold-calling "analyst" roles, AI-training gigs, fake-remote relocation programs (e.g. Revature), and suspicious templated posts.

Write `out/approved.json`:
```
[{"id": "<candidate id>", "exp": "<exact experience line quoted, or 'No years stated; ...'>", "caveat": "<short caveat or ''>"}]
```
Optional overrides per job: `company`, `title`, `loc` (add drive time for near-Somers jobs, e.g. "Stamford, CT, ~40 min drive"),
`salary`, `group` (remote / nyc / near). Write `out/redflags.json` as `[{"id": "...", "reason": "..."}]` if there are any.

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

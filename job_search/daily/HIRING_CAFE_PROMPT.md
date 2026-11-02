Paste everything below the line into a Claude desktop session that runs on your computer (not the cloud), with the built-in browser or Claude in Chrome turned on.

---

Use the browser to search Hiring Cafe for entry-level finance jobs for me (Makar Kozlov), read each promising posting in full, and add the ones that qualify to my job board. If a Cloudflare "verify you are human" check appears, stop and ask me to click through it myself; never try to get around it.

SEARCH
Open this saved search (within 50 miles of Somers, NY; bachelor's required; "No Prior Experience Required"; last 61 days):
https://hiringcafe.com/classic?searchState=%7B%22locations%22%3A%5B%7B%22id%22%3A%22us-zip-10589%22%2C%22postal_code%22%3A%2210589%22%2C%22types%22%3A%5B%22postal_code%22%5D%2C%22formatted_address%22%3A%22Somers%2C+NY%2C+US%22%2C%22address_components%22%3A%5B%7B%22long_name%22%3A%2210589%22%2C%22short_name%22%3A%2210589%22%2C%22types%22%3A%5B%22postal_code%22%5D%7D%2C%7B%22long_name%22%3A%22Somers%22%2C%22short_name%22%3A%22Somers%22%2C%22types%22%3A%5B%22locality%22%5D%7D%2C%7B%22long_name%22%3A%22New+York%22%2C%22short_name%22%3A%22NY%22%2C%22types%22%3A%5B%22administrative_area_level_1%22%5D%7D%2C%7B%22long_name%22%3A%22United+States%22%2C%22short_name%22%3A%22US%22%2C%22types%22%3A%5B%22country%22%5D%7D%5D%2C%22geometry%22%3A%7B%22location%22%3A%7B%22lat%22%3A41.3346%2C%22lon%22%3A-73.6951%7D%7D%2C%22postal_code_source%22%3A%22geonames%22%2C%22workplace_types%22%3A%5B%5D%2C%22options%22%3A%7B%22radius%22%3A50%2C%22radius_unit%22%3A%22miles%22%2C%22ignore_radius%22%3Afalse%7D%7D%5D%2C%22searchQuery%22%3A%22junior+analyst%22%2C%22dateFetchedPastNDays%22%3A61%2C%22bachelorsDegreeRequirements%22%3A%5B%22Required%22%5D%2C%22seniorityLevel%22%3A%5B%22No+Prior+Experience+Required%22%5D%7D
Then change only the search text and repeat for: financial analyst, analyst, credit analyst, investment analyst, treasury analyst, finance associate, equity research, risk analyst, FP&A. Also run "financial analyst" once with Remote selected and no location. If a search returns 0 results, remove the most recently added filter. Load every result. Change the "last 61 days" setting to 7 days after the first full pass, so later weekly runs only look at new postings.

ABOUT ME
Binghamton BS Business Administration (Finance), May 2026, GPA 3.81. Excel/PowerPoint/Word; no Python or SQL. Somers, NY. Available now; no sponsorship needed.

RULES (include only if all are true)
- Full-time, salaried, permanent. No internships, temp, contract, or commission pay.
- Experience: "0-N years", "recent grads", "up to N years", or any experience marked preferred / ideal / a plus are fine. Exclude only if a minimum above 0 is REQUIRED, or prior experience is required without a number.
- Fits a May 2026 grad: no Class of 2027 programs, 2027 start dates, or "currently enrolled".
- Finance or finance-adjacent business roles. No pure accounting (AP/AR, staff accountant, tax, audit, bookkeeping).
- NYC, within ~50 minutes' drive of Somers, or remote open to New York residents. No New Jersey or Long Island.
- No required Python, SQL, Master's, CFA/CPA, second language, or active license.
- Insurance companies are fine for finance roles, but not insurance or commission sales. Staffing-agency posts are fine (note that the employer should be confirmed).
- Skip anything already on my board: https://claude.ai/artifact/RwZix5jhKfvpzfY4qGEcvY

OUTPUT
If you have the ArtifactData tool, add each qualifying job to that board's `jobs` collection (doc id "hc-" plus a short slug) with these fields: key (same as the doc id), company, title, loc (add the drive time for jobs near Somers), salary, exp (the exact experience line, quoted), caveat, url (the employer's posting if Hiring Cafe links to it), posted, group ("remote", "nyc" or "near"), source ("Hiring Cafe"), added (today's date as YYYY-MM-DD). Put red flags in the `red` collection with company, title, reason and added.
If you don't have that tool, show me the list in chat with the same details, grouped Remote / NYC / Near Somers, and I'll forward it.
Finish by telling me how many postings you looked at and how many you added.

# Working papers and the pre-flight check

Your figures live in one file, outside any git checkout, and a script checks
them before IRIS is ever opened.

```bash
mkdir -p ~/.pk-iris
cp scripts/working-papers.example.json ~/.pk-iris/working-papers.json
python3 scripts/check.py
```

## Why check locally at all

IRIS reports **one validation failure per submission attempt**. Each round trip
costs a page load, sometimes a session, and sessions expire mid-action. Finding
four problems takes four attempts and can take an evening.

Worse, the most expensive error is not reported by IRIS at all. A non-zero
Unreconciled Amount `703000` will submit. FBR raises it months later, as a
notice, and by then the return is filed.

`check.py` runs the arithmetic locally, in a second, as many times as you like.
It checks **internal consistency of figures you supply**. It never computes a
tax liability, and it is not tax advice.

## What it checks

| Check | Catches |
|---|---|
| `reconciliation` | closing net assets that opening + inflows − outflows cannot explain — `703000 ≠ 0` before IRIS ever sees it |
| `property-floor` | a property declared below last year's value, which IRIS rejects at submission |
| `property-detail` | a property missing land area, unit, province, district, city, plot no. or sector |
| `business-capital` | Capital `3352` set without moving the matching account across — the `3352 → 7003` trap that inflates net worth |
| `admitted-tax` | admitted tax that is not chargeable less withholding, and a withholding credit larger than the certificates support |
| `withholding-evidence` | a credit claimed on a certificate with no income tax line — the MVT slip and the domestic electricity bill |
| `foreign-assets` | a foreign balance declared as an ordinary asset, so counted twice; and whether the 116A threshold is reached |
| `types` | strings where rupees belong, and negative amounts |
| `expenses` | personal expenses recorded as derived rather than measured |

Exit code is 0 when clean and 1 when anything failed, so it fits in a loop or a
commit hook if you want one.

## The file

One file does three jobs, and that is deliberate — three files would drift.

**Intake.** The figures you gather before filing. Every amount is **at cost**,
never market value, for the reason in `wealth-statement.md`.

**Carry-forward.** `prior_year` holds last year's net assets and every
property's declared value. These are the two things the reconciliation and the
floor rule cannot be computed without. Next year, this year's closing position
becomes `prior_year` and the rest is cleared. That is the whole mechanism.

**Post-filing record.** `filed` holds the date, the admitted tax, the CPR, the
codes actually used, and what the form did this year. Fill it in while you still
remember — it is what makes next September cheap.

### Fields worth explaining

- `assets.accounts[].in_business_balance_sheet` — set this on an account you
  moved onto the business balance sheet. It is then excluded from personal
  assets, because `balance_sheet.capital` already represents it through
  Business Capital `7003`. The check enforces that the two agree.
- `withholding[].certificate_shows_income_tax` — set it to `false` when the
  certificate shows only MVT, GST or duty. Those carry no claimable credit and
  claiming them invites a disallowance.
- `foreign_assets[]` — a platform balance is declared **here and nowhere else**.
  Putting it in `assets.accounts` as well counts it twice and breaks the
  reconciliation by exactly its value.
- `usd_pkr` — optional. Set it and the 116A threshold test runs; leave it and
  the script tells you the test was skipped.
- `expenses.personal_basis` — `measured` or `derived`. An honest record of how
  the figure was arrived at, because a number chosen to close the
  reconciliation is exactly what a query asks about.

## Privacy

**The real file never goes in a git checkout.** Not "in the repo but
gitignored" — a gitignore is one `git add -f` away from failing. It lives at
`~/.pk-iris/working-papers.json`, outside any repository, and the repo carries
only `scripts/working-papers.example.json` with invented figures.

`check.py` is standard library only and reads nothing but the path you give it.
It writes no log, emits no report file, and makes no network call. That is the
privacy argument, and it is checkable in one sitting.

One thing that is **not** controlled: this conversation contains your figures.
That is inherent in using an assistant for a tax return, and worth knowing
rather than being reassured about.

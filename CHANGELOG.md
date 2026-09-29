# Changelog

All notable changes to this plugin are recorded here.

Users only receive a change if `version` in `.claude-plugin/plugin.json` is
bumped, so every entry below corresponds to a version bump.

## [0.4.0] — 2026-09-29

Tooling. The plugin was prose; this adds the two artifacts that prevent errors
prose cannot, and nothing else. Eight other ideas were considered and rejected —
recorded IRIS selectors, an MCP server, a tax calculator, a YAML intake format,
encryption at rest, a screenshot archive, a per-error regression suite, and
per-tax-year version pinning.

### Added

- **`scripts/check.py`** — pre-flight validator. Standard library only, no
  network, no log file, no config. Nine checks, each one an error someone has
  actually paid for: the reconciliation closing to zero, the property-value
  floor, mandatory property address fields, the `3352 → 7003` business capital
  trap, admitted tax against chargeable less withholding, withholding credits
  claimed on certificates that show no income tax line, foreign balances
  declared twice, type and sign sanity, and the basis of personal expenses.

  Why it earns its place: IRIS reports **one validation failure per submission
  attempt**, and each round trip risks a session. The reconciliation error is
  worse — IRIS does not report it at all, FBR does, months later, as a notice.

  It checks internal consistency of figures you supply. It never computes a tax
  liability. `python3 scripts/check.py --selftest` is its entire test suite.
- **`scripts/working-papers.example.json`** — one file doing three jobs:
  intake, year-over-year carry-forward (`prior_year` holds last year's net
  assets and every property's declared value — the two things the
  reconciliation and the floor rule cannot be computed without), and the
  post-filing record.
- **`references/working-papers.md`** — the schema, what each check catches, and
  the privacy rules.
- **CI** — the self-test, the example file, a guard against a real
  working-papers file ever being committed, and a manifest parse.

### Changed

- **Order of work step 1** is now "gather source data, then check it" — the
  figures go in the file and through `check.py` before the portal is opened,
  and again before the return is handed over for Submit.
- **`.gitignore`** refuses `working-papers*.json` and `profile.md`. Belt and
  braces only: the real files belong in `~/.pk-iris/`, outside any checkout,
  because a gitignore is one `git add -f` away from failing.

## [0.3.1] — 2026-09-29

Corrections found by re-reading FBR's own consolidation of the Ordinance rather
than commentary, plus a fix for a bug that destroys user data on update.

### Fixed

- **Non-ATL rates do not double on export proceeds.** Tenth Schedule
  **Rule 10(ca)**, inserted by the Finance Act 2022, excludes tax collected or
  deducted under s.154A from the Schedule entirely, so 0.25% and 1% apply
  regardless of ATL status. The plugin previously repeated FBR's 2025-26
  Withholding Income Tax Rate Card, which published doubled 0.5% / 2% figures;
  the card was wrong against FBR's own statute, and the 2026-27 card corrects
  itself and cites R.10(ca). A reader off the ATL would have concluded a 0.5%
  bank deduction was correct when it should have been disputed. The claim was
  in `field-map.md`, `payment-and-submit.md` and `scope-and-limits.md`.
- **A dividend code pointed at the wrong line.** `64330050` is the *dividend
  received from debt securities / mutual funds* line, not the 25% rate for a
  company whose own income is exempt — that is `64030090`. Codes for the 7.5%,
  0% and 35% cases added, all read from the notified form and flagged for
  on-screen confirmation.
- **Your filing profile was destroyed by `claude plugin update`.**
  `references/your-profile.md` sat inside the plugin directory and the README
  told users to fill it in there. It is now `profile.example.md`, a template
  only; the filled-in copy belongs at `~/.pk-iris/profile.md`, outside any
  checkout. **If you filled in the old file, copy it to the new location before
  your next update.**
- **The ATL and extension passage in `payment-and-submit.md`** replaced with
  what s.182A actually says: four consequences of late filing, and re-entry to
  the list on a surcharge of Rs 1,000 for an individual. The two extension
  routes are now distinguished — the Board's blanket extension under s.214A and
  the Commissioner's personal extension under s.119.
- **SRO 1495(I)/2026 is dated 2 September 2026**, not the 4th. Its draft was
  SRO 835(I)/2026 of 7 May 2026, which explains why the form and the s.7E
  judgment share a date.

### Changed

- **The section 7E passage** now records that the notified TY2026 forms contain
  no 7E schedule, field or deemed-income line anywhere in their 111 pages; that
  the Finance Act 2026 removes 7E from TY2027 while the judgment is what removes
  it for TY2026; and that an FBR letter of 23 September 2026 directs field
  offices to process 7E-based revisions and refunds. The appellate map has been
  cut — sources contradict each other on it and it changes no filing decision.
- **Section 236C(2A) added as a live trap.** It was never repealed, and still
  bars registration of a property transfer until the seller discharges "tax
  liability under section 7E" — a section that no longer exists. Named, with
  instructions to send the user to a practitioner rather than improvise.
- **The property-value floor rule is labelled an observed portal validation.**
  No provision of the Ordinance, the Rules, an SRO or an FBR circular stating it
  could be located. It still has to be satisfied; it is no longer presented as
  law.
- **`s.154A(3)` has two triggers**, not one: failing a condition knocks receipts
  out of final tax whether or not anyone intended it. What follows from that is
  not spelled out in the section — the minimum-tax proviso people remember was
  s.154(5), omitted by the Finance Act 2024 — so it is flagged rather than
  answered.
- **The 0.25% sunset is stated.** Division IVA carries "for tax years 2024 up to
  tax year 2026", added by the Finance Act 2023. The reported Finance Act 2026
  extension to tax year 2029 now carries an instruction to confirm it against
  the current consolidation before relying on it.

### Added

- **The profile is now built by interview.** Claude asks the questions and
  writes `~/.pk-iris/profile.md` itself, reading last year's return off the
  portal rather than asking the taxpayer to retype it. Includes the three
  no-prior-year cases, and the warning that a first filer's declared property
  values become permanent floors.
- **`PREPARE PSID`** named in the never-click rules, in both the skill and the
  agent. The notified TY2026 form places it next to `CALCULATE` on the
  Computations page.

### Still open

- Whether provincial sales tax registration is required under provincial law in
  its own right — replacing the s.154A(2)(c) question, which is now closed from
  FBR's own PDF.

## [0.3.0] — 2026-09-28

Accuracy audit against FBR sources and Big Four commentary before announcing.
Three material corrections — anyone on 0.1.x or 0.2.x should update.

### Fixed

- **Section 154A rates were described wrongly.** The 1% line is not a
  "non-PSEB IT exporter" rate; it is the residual "any other case" under
  s.154A(1). Since the Finance Act 2022, clause (1)(a) is itself confined to
  PSEB-registered and certified exporters.
- **Section 154A(2)(c) was recorded as unresolved when it is not.** The Finance
  Act 2023 inserted a proviso disapplying the sales-tax-return condition for
  PSEB-registered IT/ITeS exporters. Previously the guide told Claude to flag
  provincial sales tax registration as a possible threat to the 0.25% regime;
  for a PSEB-registered exporter it is not one.
- **Dividend rates had no basis for choosing between them.** 15% and 25% were
  listed without saying which dividend attracts which, risking the wrong code.

### Added

- Non-ATL rates are double (0.5% / 2% on s.154A), with the unresolved conflict
  over whether the Tenth Schedule applies to s.154A noted
- The Finance Act 2026 extension of the 0.25% concession to tax year 2029
- Section 154A(3) opt-out of final taxation
- Full dividend rate table — IPP pass-through, REIT and SPV cases — and the
  Finance Act 2025 debt/equity split for mutual fund dividends
- **Section 7E**: struck down as void ab initio by the Federal Constitutional
  Court on 7 May 2026 and omitted by the Finance Act 2026, so no 7E liability
  arises on a TY2026 return — with the caveat that the form may still show the
  field and no FBR circular giving effect to the judgment could be found
- Section 102's actual condition — foreign tax withheld by the employer in the
  country where the employment was *exercised* — which is why it will not
  rescue a contractor/employee mischaracterisation for someone working from
  Pakistan
- Deadline extensions are discretionary and do not postpone the liability to pay

## [0.2.0] — 2026-09-28

Repository and documentation work. No change to the filing knowledge itself.

### Added

- Install instructions in the README — marketplace and one-line forms, plus the
  update command
- `CONTRIBUTING.md`, with the rule that contributions describe what was
  observed rather than what was expected
- `CHANGELOG.md`
- GitHub issue templates for the two highest-value reports: a validation error
  not yet in the playbook, and a field or code that has moved
- `LICENSE` (MIT) — the README claimed MIT but no licence file existed

### Changed

- `PUBLISHING.md` now covers maintaining a published marketplace rather than
  creating one
- Tax year the content was verified against is stated up front in the README

## [0.1.0] — 2026-09-28

First release. Built while filing a tax year 2026 return on IRIS 2.0.

### Added

- **`pk-iris-agent`** — drives the portal through browser automation, verifies
  after every change, and stops before Submit, before any payment, and before
  deleting or reducing a declared row
- **`pk-iris-filing`** skill — workflow, portal mechanics, and references:
  - `field-map.md` — where fields actually live, and the codes. Including that
    Final Tax fields under Tax Chargeable/Payments are `disabled` for every code
  - `wealth-statement.md` — cost basis, the reconciliation, the Capital `3352` →
    Business Capital `7003` → Net Assets chain, the Property Information modal,
    and the property-value floor rule
  - `payment-and-submit.md` — admitted tax, PSID, claiming, submitting
  - `scope-and-limits.md` — what was verified, what was not, and how to correct
    an already-submitted return
  - `your-profile.md` — blank template for standing circumstances
- **`pk-iris-errors`** skill — four IRIS validation messages with causes and
  fixes, plus silent write failures and a non-zero reconciliation checklist
- Marketplace manifest, so the repository is installable as its own marketplace

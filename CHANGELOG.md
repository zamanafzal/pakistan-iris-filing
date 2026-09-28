# Changelog

All notable changes to this plugin are recorded here.

Users only receive a change if `version` in `.claude-plugin/plugin.json` is
bumped, so every entry below corresponds to a version bump.

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

# Changelog

All notable changes to this plugin are recorded here.

Users only receive a change if `version` in `.claude-plugin/plugin.json` is
bumped, so every entry below corresponds to a version bump.

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

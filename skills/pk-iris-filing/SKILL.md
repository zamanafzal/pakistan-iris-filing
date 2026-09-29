---
name: pk-iris-filing
description: >
  This skill should be used when someone is preparing, reviewing, or filing a
  Pakistan income tax return on FBR's IRIS 2.0 portal — phrases like "file my
  tax return", "IRIS return", "FBR return", "114(1)", "wealth statement",
  "116 reconciliation", "section 154A export income", "PSEB 0.25%", "admitted
  income tax", "claim my PSID payment", or when they are working inside
  iris.fbr.gov.pk. Scoped to individuals filing a 114(1) with a wealth
  statement, particularly freelancers and IT/ITeS exporters. Covers portal
  mechanics, field and code locations, export final tax under s.154A, the 116
  wealth statement and reconciliation, the business balance sheet, property
  declarations, and the payment-then-submit sequence.
metadata:
  version: "0.1.0"
---

# Filing an income tax return on FBR IRIS 2.0

Drive the IRIS portal through browser automation, prepare the return, verify
every figure against source data, and hand the irreversible steps back to the
taxpayer.

**Read `references/scope-and-limits.md` first.** It states what in this skill
was verified on the live portal and what was never exercised. Where a request
falls outside that boundary — a salary return, rental income, capital gains,
slab-rate computation, a province other than Punjab — say so plainly instead of
improvising. Confident guesses about a tax return are worse than an admission.

This is not tax advice. The taxpayer is responsible for what they declare, and
anything contentious needs a Pakistani tax practitioner.

## Hard rules

These are not preferences. Apply them without exception.

1. **Never type into a credential field.** Not the CNIC/NTN box, not the
   password box, not any login form. When the session expires — and it will,
   repeatedly — say plainly that IRIS logged the user out and wait for them to
   log back in.
2. **Never click Submit.** Prepare everything, verify it, present the figures,
   and let the taxpayer press Submit. Submission is irreversible, and undoing it
   means a revised return.
3. **Never generate a PSID or make a payment.** Compute what is owed, state it,
   and let the taxpayer do the payment. The notified TY2026 form places a
   **`PREPARE PSID`** button next to `CALCULATE` on the Computations page — do
   not click it.
4. **Never delete or reduce an existing declared row without asking.** Removing
   a property or asset row, or lowering a declared value, changes net worth and
   can trip FBR's own rules. Explain the change and get a yes first.
5. **Never invent a figure.** If a value is unknown — a land area, an
   acquisition date, a cost basis — ask. A wealth statement is a legal
   declaration, and a plausible-looking guess is a false declaration.
6. **Avoid clicking Print** while driving the browser; a print dialog blocks the
   extension and the session has to be recovered manually.

## Order of work

1. **Gather source data first.** Working papers, bank statements, proceeds
   certificates, withholding certificates. Do not open the portal to "see what's
   there" before knowing what the numbers should be.
2. **Read `~/.pk-iris/profile.md`** — the taxpayer's standing circumstances, if
   they have one. Do not ask what it already answers. If that file does not
   exist, check the old in-plugin location
   `references/your-profile.md` (removed in 0.3.1, still present in installs
   that have not updated) and offer to move it to `~/.pk-iris/profile.md`.
   If neither exists, build one by asking — see *Building the profile* below.
3. **Check last year's return.** Dashboard → Completed Tasks → Declaration →
   eye icon opens the prior year read-only. It settles questions about
   precedent — which codes were used, whether a nil balance sheet was filed,
   what each property was declared at. Cheapest tie-breaker available.
4. **Enter income**, then the final-tax lines. See `references/field-map.md` —
   the editable locations are not where the form suggests.
5. **Enter the wealth statement** (116) at **cost**, never market value. See
   `references/wealth-statement.md`.
6. **Reconcile.** Unreconciled Amount `703000` must read exactly 0 before
   anything else matters.
7. **Balance sheet**, if business income is declared. Usually nil — and the
   reason capital must stay blank is in `references/wealth-statement.md`.
8. **Compute the admitted tax** `9203`, state the exact figure, let the taxpayer
   pay, then claim the payment. See `references/payment-and-submit.md`.
9. **Final walkthrough**, then hand over for Submit.

## Portal mechanics that will otherwise waste hours

**Sessions expire constantly.** Save after every meaningful change. A save costs
one click; losing twenty minutes of form-filling costs the user's patience. If a
click lands on a login page, say so and stop.

**Workflow URLs are single-use.** The `?t=` token in an IRIS workflow URL dies
with the session. To reopen a draft: Dashboard → Draft tab → IT Declaration →
pencil icon. Never reuse a URL from earlier in the conversation.

**Verify every write through the DOM.** The page reflows between a click and a
keystroke, so typed text lands in the wrong field more often than expected.
After typing, read the field back and confirm the value is where it belongs.
Screenshots are not proof — read the input's `value`.

**Modal re-renders discard uncommitted edits.** Add a row first and save it,
then edit its values. Editing and then opening another modal loses the edit
silently.

**Sidebar buttons sometimes render with no visible label.** Click them by
matching button text in the DOM rather than by coordinate.

**Dropdowns are Angular Material.** Options exist in the DOM only while the
dropdown is open, and sub-options depend on the parent selection — read them
after opening, not before.

## The diagnostic technique

When it is unclear whether field A feeds field B, find out instead of assuming:
enter a small distinctive test value in A, press CALCULATE, read B, then delete
the test value, press CALCULATE again, and confirm B returned to its original
state.

This is how the Business Capital → Net Assets link was established. It is safe,
fast, and beats reasoning about an undocumented form. Always tell the taxpayer
what the test value is for, and confirm in writing when it has been removed — a
stray test figure in a tax return is alarming to see.

## Verify after every change

| Code | Meaning | Expectation |
|---|---|---|
| `703000` | Unreconciled Amount | exactly 0 |
| `703001` | Net Assets Current Year | ties to the working papers |
| `7019` | Total Assets | ties to the working papers |
| `9200` | Tax Chargeable | matches the computation |
| `9201` | Withholding Income Tax | matches certificates held |
| `9203` | Admitted Income Tax | matches the PSID and the claimed CPR |

If `703000` is not zero, stop and find out why before doing anything else. A
non-zero reconciliation is FBR's flag for unexplained wealth.

## Reference material

- `references/scope-and-limits.md` — what is verified, what is not, and the
  rules for correcting an already-submitted return
- `references/field-map.md` — where each field actually lives, and the codes
- `references/wealth-statement.md` — assets, reconciliation, properties, the
  balance sheet, and the property-value floor rule
- `references/payment-and-submit.md` — admitted tax, PSID, claiming, submitting
- `references/profile.example.md` — the blank profile template. The taxpayer's
  filled-in copy lives at `~/.pk-iris/profile.md`, outside the plugin, because
  `claude plugin update` replaces everything inside it

## Building the profile

Do not hand the taxpayer a blank file and ask them to fill it in — they will do
it in September, under deadline, badly. Ask the questions and write the file
yourself, to `~/.pk-iris/profile.md`, saving each answer as it arrives so an
expired session costs nothing.

**Establish whether a prior year exists before asking anything else.** The
answer changes which questions are worth asking:

1. **Read last year's return from the portal** — Dashboard → Completed Tasks →
   Declaration → eye icon. Read-only, and it settles prior net assets, every
   property's declared value, which codes were used and whether a nil balance
   sheet was filed. Transcription is where errors enter, so never ask the
   taxpayer to retype what is on screen.
2. If the portal copy will not open, ask for **the PDF**.
3. If an accountant filed it and there is no access, ask for **four things
   specifically** — prior net assets, each property's declared value and
   description, the codes used, and declared personal expenses. Not "last
   year's return".

**If there is no prior year at all**, say which of three situations applies,
because they differ:

- **First-time filer.** There is no `703002` to inherit, so the opening position
  has to be established and declared. Pre-existing wealth belongs in the
  *opening* figure — the reconciliation only has to explain the change during
  the year. A first-timer who does not understand this will try to invent income
  to force `703000` to zero.
- **Filed before, but never a wealth statement.** Same opening problem; code
  precedent still exists and is worth reading.
- **Records genuinely gone.** Reconstruct from what is documentable — bank
  balances at 30 June, deeds, registration books — and tell them plainly that
  the figure is a reconstruction.

**Tell a first filer this explicitly:** nothing constrains what they declare
this year, and everything they declare becomes a permanent floor. Every property
value entered now is the minimum that can ever be declared for it again. A
casual number in year one is a constraint for life.

Ask standing facts once — PSEB registration, how proceeds arrive, which assets
exist, the valuation basis. Ask amounts every year. They run on different clocks
and mixing them is part of why blank templates do not get filled.

## Tone

The taxpayer is filing their own return, usually against a deadline, often at
the end of a long day. Be concise. Report what was verified, not what was
clicked. When something genuinely matters — an overpayment, a broken
reconciliation, a rule that blocks what they asked for — say it plainly and
early, with the number, before offering options.

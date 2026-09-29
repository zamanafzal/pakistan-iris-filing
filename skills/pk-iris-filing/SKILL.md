---
name: pk-iris-filing
description: >
  This skill should be used when someone is preparing, reviewing, or filing a
  Pakistan income tax return on FBR's IRIS 2.0 portal — phrases like "file my
  tax return", "IRIS return", "FBR return", "114(1)", "wealth statement",
  "116 reconciliation", "section 154A export income", "PSEB 0.25%", "admitted
  income tax", "claim my PSID payment", or when they are working inside
  iris.fbr.gov.pk. Scoped to individuals filing a 114(1) with a wealth
  statement, particularly contractors/freelancers and IT/ITeS exporters. Covers
  portal
  mechanics, field and code locations, export final tax under s.154A, the 116
  wealth statement and reconciliation, the business balance sheet, property
  declarations, and the payment-then-submit sequence.
metadata:
  version: "0.1.0"
---

# Filing an income tax return on FBR IRIS 2.0

Work through the return field by field, verify every figure against source data,
and hand the irreversible steps back to the taxpayer.

## Two ways to work — establish which before starting

**Guided (the default).** The taxpayer has IRIS open and does the clicking. You
say exactly where to go, what to enter, and what to read back; they report what
they see. This needs no extension, survives IRIS reflowing under you, and works
for anyone. Assume this unless told otherwise.

**Driven.** You operate the portal yourself through browser automation, with the
Claude in Chrome extension connected. Faster when it works, and it can read
fields back through the DOM rather than asking. It is also the fragile path:
pages reflow between a click and a keystroke, tokens expire, and a print dialog
can block the extension entirely.

Ask once, early: *"Do you want to drive, or shall I?"* Do not assume the
extension is connected, and do not fail over silently — if automation stops
working mid-filing, say so and continue in guided mode rather than retrying.

**Everything in this skill applies to both modes.** What changes is only who
performs the click and how a value is read back:

| | Guided | Driven |
|---|---|---|
| Navigation | you name the path, they click | you click |
| Entering a value | you give the exact figure and field | you type it |
| Verifying a write | ask them to read the field back to you | read the input's `value` from the DOM |
| A dropdown's options | ask them to read the list | read the open dropdown from the DOM |
| Session expiry | they will see the login page and tell you | a click lands on the login page |

In guided mode the verification step matters **more**, not less: you cannot see
the screen, so nothing is confirmed until the taxpayer reads it back. Never
record a figure as entered because you told someone to enter it.

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
2. **Never click Submit, and never tell the taxpayer to.** Prepare everything,
   verify it, present the figures, and let them decide to submit. Submission is
   irreversible, and undoing it means a revised return. In guided mode this rule
   is about your *instructions*: walk them to the point of submitting, state
   what you verified, and stop there.
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
6. **Avoid Print while driving.** A print dialog blocks the extension and the
   session has to be recovered manually. In guided mode this does not apply —
   the taxpayer can print freely.

## Order of work

1. **Gather source data first, then check it.** Working papers, bank
   statements, proceeds certificates, withholding certificates. Do not open the
   portal to "see what's there" before knowing what the numbers should be.

   Put the figures in `~/.pk-iris/working-papers.json` and run
   `python3 scripts/check.py`. It closes the reconciliation, tests every
   property against last year's floor, and catches the `3352 → 7003` capital
   trap — locally, in a second, instead of one IRIS submission at a time. See
   `references/working-papers.md`.
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
10. **Write down what the form did.** See *Closing the loop* below. This is the
    step that makes next year cheap and the plugin true for more than one
    person, and it is the step everyone skips.

## Portal mechanics that will otherwise waste hours

**Sessions expire constantly.** Save after every meaningful change. A save costs
one click; losing twenty minutes of form-filling costs the user's patience. If a
click lands on a login page, say so and stop.

**Workflow URLs are single-use.** The `?t=` token in an IRIS workflow URL dies
with the session. To reopen a draft: Dashboard → Draft tab → IT Declaration →
pencil icon. Never reuse a URL from earlier in the conversation.

**Verify every write.** The page reflows between a click and a keystroke, so
text lands in the wrong field more often than expected. After any value is
entered, confirm it is where it belongs — in driven mode by reading the input's
`value` from the DOM (screenshots are not proof), in guided mode by asking the
taxpayer to read the field back to you. A value you have not had confirmed is
not entered.

**Modal re-renders discard uncommitted edits.** Add a row first and save it,
then edit its values. Editing and then opening another modal loses the edit
silently.

**Sidebar buttons sometimes render with no visible label.** When driving, click
them by matching button text in the DOM rather than by coordinate. When guiding,
describe the button by its position in the sidebar and ask what it says — an
unlabelled button is confusing for the taxpayer too, and worth naming.

**Dropdowns are Angular Material.** Options exist only while the dropdown is
open, and sub-options depend on the parent selection — read them after opening,
not before. Never tell the taxpayer which option to pick from a list you have
not had read back to you; FBR's lists are incomplete in ways that surprise
people, tehsils especially.

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

Run `python3 scripts/check.py` once more before handing the return over for
Submit. What it reports locally is cheaper to fix than what IRIS reports one
error at a time, and far cheaper than what FBR reports months later.

## Reference material

- `references/scope-and-limits.md` — what is verified, what is not, and the
  rules for correcting an already-submitted return
- `references/field-map.md` — where each field actually lives, and the codes
- `references/wealth-statement.md` — assets, reconciliation, properties, the
  balance sheet, and the property-value floor rule
- `references/payment-and-submit.md` — admitted tax, PSID, claiming, submitting
- `references/working-papers.md` — the figures file, the pre-flight check, privacy
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

## Closing the loop

Everything in this plugin was observed on **one** filing — one taxpayer, one
income type, one province. Whatever this taxpayer just saw is evidence nobody
else has.

Once the return is submitted, or while it is still fresh:

1. **Write the post-filing record** into `~/.pk-iris/working-papers.json` under
   `filed` — the date, the admitted tax, the CPR, the codes actually used, and
   anything the form did that surprised you. Next September this is worth more
   than memory.
2. **Check `OBSERVATIONS.md`** in the plugin repo. It lists what nobody has
   looked at yet. If this filing happened to answer one — a province outside
   Punjab, a page the plugin has never opened, a validation error not in
   `pk-iris-errors` — offer to write it up as an issue or a pull request, and
   produce the text for them to paste.
3. **Correct what was wrong.** If a code had moved, a field was not where the
   field map said, or something here turned out to be untrue, say so plainly and
   offer the diff. Silently working around a stale fact is how the plugin rots.

Offer this; do not insist. Someone who has just filed at 11pm on the 30th wants
to close the laptop. Ask once, and if they say no, at least write the
post-filing record.

**Never put their figures in an issue, a pull request or a commit.** What is
useful is label text, field codes, behaviour and the tax year. None of it needs
a rupee of their data, and a screenshot almost always carries their name.

## Tone

The taxpayer is filing their own return, usually against a deadline, often at
the end of a long day. Be concise. Report what was verified, not what was
clicked. When something genuinely matters — an overpayment, a broken
reconciliation, a rule that blocks what they asked for — say it plainly and
early, with the number, before offering options.

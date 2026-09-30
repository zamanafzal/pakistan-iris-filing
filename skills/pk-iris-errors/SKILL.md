---
name: pk-iris-errors
description: >
  This skill should be used when IRIS 2.0 rejects a return at submission or
  refuses to save, and the user pastes or describes the message — for example
  "Total Assets and Total Equity / Liabilities against Codes 3349 and 3399 must
  be entered", "Please provide complete address of all the Immovable
  Properties", "The declared property value must not be lower than the previous
  year's declared value", "Session is Expired", "Measurement Unit is required",
  or any other FBR IRIS validation or error message. Also covers symptoms rather
  than messages — export or s.154A income missing from the final computation,
  income taxed under the wrong regime, or a figure that will not save. Maps each
  to its real cause and the fix that does not break the wealth statement
  reconciliation.
metadata:
  version: "0.1.0"
---

# IRIS validation errors: cause and fix

Work through these one at a time. Expect several rounds — IRIS reports one
problem per attempt, so fixing one reveals the next. Nothing is damaged by a
failed submission; the return stays a draft.

**After every fix**, re-verify before handing back for another Submit:

- Unreconciled `703000` is still 0
- Net Assets `703001` is unchanged (unless the fix was meant to change it)
- The claimed payment still matches Admitted Income Tax `9203`
- The save toast said "Changes saved successfully"

---

## "Total Assets and Total Equity / Liabilities against Codes 3349 and 3399 must be entered"

**Cause.** The business balance sheet is empty. `3349` and `3399` are computed
totals — they cannot be typed into, and they stay blank while every line item
underneath them is blank.

**Fix.** Enter `0` in **Other Assets `3348`** and `0` in **Other Liabilities
`3398`**, then press CALCULATE. Both totals compute to `0` and the validation
passes.

**Do not** put a figure in Capital `3352` to make the totals non-zero. Capital
feeds `7003` Business Capital in the wealth statement, which feeds Total Assets
and Net Assets — it will inflate net worth and break the reconciliation. See
`pk-iris-filing/references/wealth-statement.md`.

Check the prior year first: if a nil balance sheet was filed and accepted
before, matching it is both correct and consistent.

---

## "Please provide complete address of all the Immovable Properties in Wealth Statement or Balance sheet"

**Cause.** One or more property rows lack the structured address fields. On the
Personal Assets page these rows are highlighted amber.

**Fix.** Open each property's pencil icon and complete every starred field:
Property type, Property sub-type, Land area unit, Province, District, City,
Property/Plot/House/Shop No., Sector/Mohalla/Block.

**Watch for two traps.**

*The land-area trap.* Land area carries no asterisk, so it looks optional — but
selecting a unit makes it mandatory ("Kanal is required"). There is no way to
save a property without stating its size. If the size is unknown, the user needs
the deed, a fard malkiat from the Arazi Record Centre, or the provincial
land-records portal. Do not invent a figure.

*Nothing to import.* These structured fields are new from TY2026. Earlier
returns stored only a free-text description and an amount, so the prior year
cannot supply them. Say so rather than promising to look them up.

If a tehsil is missing from FBR's list, select the parent tehsil and put the
town name in Sector/Mohalla/Block.

---

## "The declared property value must not be lower than the previous year's declared value"

**Cause.** A property record is declared below what the same record carried last
year. Most often this happens after splitting one declared property into two
rows — the original record keeps the prior-year value as its floor, so any split
that preserves the total leaves it short.

This floor is an **observed portal validation**; no provision of the Ordinance,
the Rules, an SRO or an FBR circular stating it could be located. That changes
nothing about having to satisfy it, but say so if a user asks where the rule
comes from.

**Fix.** Restore the record to at least its prior-year value.

If the user wanted two rows, explain the bind honestly: raising the total to
clear the floor adds to net worth and breaks the reconciliation, which is worse
than a combined row. Declare the holding as **one row** at the prior value, name
both parcels in the description, and put the combined area in the land-area
field. Nothing is concealed. A genuine split can only be made in a year where
each resulting record stands at or above its own prior figure.

---

## "Measurement Unit is required" / "Kanal is required"

**Cause.** Land area unit is mandatory; once chosen, the numeric land area
becomes mandatory too.

**Fix.** Supply both. There is no configuration in which a property can be saved
with neither.

---

## "Session is Expired"

**Cause.** IRIS times out aggressively, and it happens mid-action — including
on the click that would have saved the work.

**Fix.** Tell the user plainly that IRIS logged them out and ask them to log in.
**Never type into the CNIC/NTN or password fields.** Then reopen the draft via
Dashboard → Draft → IT Declaration → pencil icon. Do not reuse the previous
workflow URL; its `?t=` token is dead.

Then re-check what actually saved. Work lost to a session drop is common;
assume nothing persisted after the last confirmed "Changes saved successfully".

**Prevention:** save after every meaningful change.

---

## Export income is missing from the computation, or taxed at the wrong rate

Reported as "my IT export isn't showing up on the final computation", "the
154A income has gone", or "it's being taxed at slab rates".

**Four different causes produce this, and the fixes are unrelated.** Establish
which before changing anything — ask what the Computations page actually shows
at `920100` Fixed / Final Tax and at `9000` Total Income.

**1. It was entered on the page that cannot accept it.** The most common by a
distance. Under Tax Chargeable / Payments → Withholding Tax → Final Tax, every
Taxable Amount and Tax Deducted input carries `disabled: true`. Typing there
fails silently, and after a save-and-reload an empty row disappears entirely —
which reads as the entry being deleted.

*Fix.* Enter it at **Business → Tax Deduction → Final Tax**, gross amount, then
CALCULATE. The consolidated Withholding Tax page mirrors; it does not accept
input.

**2. The ⇄ icon has been clicked on the row.** The notified form offers
*"You may offer this receipt under Normal Tax regime by clicking ⇄ icon"* — the
s.154A(3) opt-out, as a control sitting on the 154A row. Toggled, the receipt
leaves final tax and is charged at slab rates. A stray click does this silently
and the computation changes completely.

*Fix.* Check the state of the icon on the row before concluding anything else
is wrong. Moving back is the taxpayer's decision, not a correction to make on
their behalf without saying so.

**3. IRIS has applied s.154A(2) and knocked the receipts out.** Sub-section (3)
removes final-tax treatment from a person "who does not fulfil the specified
conditions" — the return filed, withholding statements filed if required, sales
tax returns filed if required.

*The trap:* the Finance Act 2023 added a proviso disapplying the sales-tax
condition **for exporters under clause (1)(a)** — that is, PSEB-registered and
certified exporters. A PSEB exporter should never be knocked out by that
condition. If one appears to have been, that is worth establishing carefully:
either a condition genuinely is unmet, or the portal is not implementing the
proviso. Do not tell the user which without evidence, and do not work around it
by re-entering the figure somewhere else.

**4. The form changed underneath the draft.** FBR amended the TY2026 return by
SRO 1495(I)/2026 on **2 September 2026**, four weeks before the due date.
Whether IRIS migrated drafts started before that date is unknown. If a draft
predates it and figures are behaving inexplicably, check whether a fresh draft
behaves the same way before spending an hour on the old one.

**In every case, verify what the computation shows rather than what was
entered.** `920100` Fixed / Final Tax carrying the expected figure is the test
that the income landed in the right regime; `9000` Total Income carrying it
instead means it did not.

---

## Typed values silently not saving

**Cause, most often:** the field is `disabled`. Final Tax fields under Tax
Chargeable / Payments → Withholding Tax are disabled for every code; the
editable locations are Business → Tax Deduction → Final Tax and Other Sources →
Tax Deductions → Final Tax.

**Cause, second most often:** the page reflowed between the click and the
keystroke, so the text landed in a neighbouring field — or nowhere.

**Fix.** Have the value confirmed after typing, every time — read the input's
`value` from the DOM when driving, or ask the taxpayer to read the field back
when guiding.
If it is empty, check `disabled` before retrying. If it landed in the wrong
field, fix both fields and re-verify.

---

## Unreconciled Amount is not zero

Not a submission error, but stop everything until it is resolved. A non-zero
`703000` is FBR's flag for unexplained wealth.

**Work through in this order:**

1. Did an asset get revalued to market instead of cost? Revaluation raises
   closing net assets with no matching inflow.
2. Did a balance sheet Capital figure leak into `7003` Business Capital?
3. Is an inflow missing — a gift, an inheritance, a loan received, a disposal?
4. Is an outflow missing — personal expenses understated?
5. Did a property or asset row change value as a side effect of an edit?

Never close the gap by adjusting personal expenses to whatever number makes it
balance. Find the real cause, and if the user must choose between imperfect
options, show them the options.

---

## Return submits but a tab looks empty

An empty **Business Details** tab ("No businesses available") did not block
submission on the TY2026 form even with substantial business income declared.
Worth mentioning to the user as a completeness gap, but do not treat it as a
blocker unless IRIS actually says so.

# Wealth statement, reconciliation, properties, balance sheet

## The arithmetic that governs everything

```
Closing Net Assets = Opening Net Assets + Income + Other Inflows − Expenses
```

IRIS computes the gap as `703000` Unreconciled Amount. **It must be exactly 0.**
A non-zero figure is the single most effective way to attract an FBR notice: it
says wealth appeared that declared income does not explain.

Every consequence below follows from this one equation.

## Declare assets at cost, never market value

Assets go in at what was paid for them, in the year they were acquired — not
what they are worth now.

This is not a stylistic choice. Revaluing an asset upward raises closing net
assets with no matching inflow, so the reconciliation breaks by exactly the
revaluation, and the only way to close it is to declare income that was never
earned. A property bought years ago at 20,000,000 stays at 20,000,000 however
much it has appreciated. The same applies to gold, vehicles, and everything
else.

If the user proposes using current values, explain this before agreeing.

## The Business Capital trap

**Balance sheet `3352` Capital feeds wealth statement `7003` Business Capital,
which is a locked computed field, which feeds `7019` Total Assets, which feeds
`703001` Net Assets.**

Verified empirically: entering Capital of 1,000 moved Net Assets up by exactly
1,000. Removing it moved them back. The link is direct and unfiltered.

So any capital declared on the business balance sheet **adds to net worth** and
breaks the reconciliation, unless the same amount is simultaneously removed from
personal assets. It is not possible to "put some numbers in to pass the
validation".

Two coherent options exist:

**Nil balance sheet.** Enter `0` in Other Assets `3348` and `0` in Other
Liabilities `3398`, press CALCULATE, and both totals compute to 0. `7003` stays
blank, net assets are untouched. This is what satisfies the "Codes 3349 and
3399 must be entered" validation, and it is what most freelance service
providers with no separate books have always filed — check the prior year to
confirm.

**Move assets across.** Declare the business bank account under `3320`, set
`3352` Capital to the same figure, and remove that account from personal `7006`
using the ⇄ move icon. Net worth is unchanged because the asset moved rather
than duplicated. More faithful to reality for a business with real working
capital; more work, and more ways to get it wrong under deadline.

Note that `3349` and `3399` are computed and cannot be typed into directly —
only their children are editable.

## Property declarations

### The Property Information modal

Opened by the pencil icon on any immovable property row. Mandatory fields are
starred:

- Property type\* — Agricultural, Commercial, Industrial, Residential
- Property sub-type\* — Constructed Property, Farm House, Flat, Open Plot
  (the same four for every property type)
- Date of Acquisition — optional
- Land area unit\* — Acre, Kanal, Marla, Square Foot, Square Meter
- Land area — **optional until a unit is chosen, then mandatory**
- Acquisition cost/value
- Country — fixed at Pakistan
- Province / Territory\*, District\*, City\* (Tehsil)
- Property/Plot/House/Shop No.\*
- Sector / Mohalla / Block\*

The land-area trap catches people: the field carries no asterisk, so it looks
skippable, but selecting a unit turns it mandatory ("Kanal is required"). There
is no way to record a property without stating its size. If the user does not
know, they need the gift/transfer deed, a fard malkiat from the Arazi Record
Centre, or the provincial land-records portal.

Rows with incomplete detail are highlighted amber on the Personal Assets page —
a quick visual check for what still needs attention.

### Structured address fields are new

Up to TY2025 the form stored only a free-text description plus an amount. The
structured address fields arrived with TY2026, so **there is nothing to import
from the prior year** and every property will need them filled by hand. Do not
promise the user that last year's return can supply this; it cannot.

### Tehsil lists are incomplete

FBR's tehsil dropdowns lag administrative reality — a district's list may carry
only three or four tehsils and omit one that was notified more recently, even
though it exists. Check the list rather than assuming. When the town
is missing, select the parent tehsil and put the town name in the Sector /
Mohalla / Block field, so the full address is still on record. Tell the user
this was done.

Where a city offers both administrative towns and a plain city entry (Lahore
lists Iqbal Town, Nishter Town, Wapda Town … and also "Lahore"), prefer the
plain city entry over guessing a town. The precise address is in the free-text
fields anyway.

### The property-value floor rule

**A property's declared value must not be lower than its previous year's
declared value.** IRIS enforces this per property record at submission:

> The declared property value must not be lower than the previous year's
> declared value. Please correct the value of the relevant property before
> proceeding.

The important consequence: **a single declared property cannot be split into two
rows in a later year** while keeping the total constant. The original record
inherits the prior-year value as its floor, so any split leaves it short. Raising
the total to satisfy the floor adds to net worth and breaks the reconciliation —
which is a far worse problem than a combined row.

If a holding really is two parcels, declare it as one row and name both parcels
in the description and the combined area in the land-area field. Nothing is
concealed. A genuine split can only be made in a year where each resulting
record can stand at or above its own prior figure.

## Vehicles and bank accounts

`7008` Motor Vehicles and `7006` Investments are parent rows fed by sub-grids —
the parent shows `disabled: true` and sums its children. Add each vehicle or
account through the `+` button. Vehicle rows want registration number, maker and
model; a model field may strip spaces, so read it back after typing.

## Cross-checks worth running before filing

- **Unreconciled `703000` = 0.** Non-negotiable.
- **Dividends** reconciled against `SUMMARY OF ECONOMIC TRANSACTIONS`, both
  gross and tax deducted.
- **Withholding credits** claimed only where a certificate actually shows income
  tax. A provincial motor vehicle tax slip showing only MVT, penalty and arrears
  carries no s.234 income tax. A domestic-tariff electricity bill showing only
  GST and duty carries no s.235 income tax. Claiming these invites a
  disallowance.
- **Loans given** — a receivable declared in the wealth statement needs to be
  fundable from declared income or existing assets, and ideally documented.
- **Large cash balances** draw attention; make sure the figure is defensible.
- **Personal expenses** that exactly match the prior year are an obvious pattern;
  if derived rather than measured, say so to the user so they can decide.

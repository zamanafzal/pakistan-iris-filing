# IRIS 2.0 field map

Where fields actually live, and the codes behind them. Verified live on the
TY2026 114(1) form. FBR changes the form between tax years — treat this as a
strong prior, confirm on screen, and update this file when something moves.

## Form layout

The return opens with tabs across the top: **Data · Amortization ·
Depreciation · Business Details · Payment · Attachment**. Almost everything
happens under **Data**, whose left sidebar holds the sections:

```
Business            Manufacturing/Trading Items · Other Revenues ·
                    Admin, Selling & Financial Expenses ·
                    Inadmissible/Admissible Deductions · Adjustments ·
                    7F Tax Builders and Developers ·
                    Income from Social Media Content ·
                    Tax Deduction · Balance Sheet
Other Sources       Receipts/Deductions · Tax Deductions
Foreign Sources     Foreign Sources
Tax Chargeable /    Allowances, Reductions and Credits ·
  Payments          Withholding Tax · Computations
116 - Wealth        116A - Foreign Assets/Liabilities ·
  Statement         Personal Assets / Liabilities ·
                    Reconciliation of Net Assets
```

Buttons on every Data page: `ADD INCOME SOURCES`, `SUMMARY OF ECONOMIC
TRANSACTIONS`, `IMPORT PREVIOUS RETURN`, `CALCULATE`.

`SUMMARY OF ECONOMIC TRANSACTIONS` is FBR's own third-party data on the
taxpayer — bank profit, dividends, withholding. Use it to reconcile declared
figures against what FBR already knows. Mismatches here are what generate
notices.

Do not press `IMPORT PREVIOUS RETURN` casually. It overwrites current data.

## Final tax — the fields that look editable but are not

Under **Tax Chargeable / Payments → Withholding Tax → Final Tax**, the Taxable
Amount and Tax Deducted inputs render normally but carry `disabled: true` for
**every** code. Typing into them fails silently. Re-adding the row, pressing
CALCULATE, switching tabs, saving and reloading — none of it helps, and after a
save-and-reload an empty row disappears entirely.

The editable locations are:

| Income type | Editable at |
|---|---|
| Export of IT/ITeS services (s.154A) | **Business → Tax Deduction → Final Tax** |
| Dividends (s.150) | **Other Sources → Tax Deductions → Final Tax** |

Enter the gross amount, press `CALCULATE`, and let IRIS compute the tax. Do not
type the tax figure — if IRIS's computed value differs from expectation, that
difference is worth understanding before overriding anything.

### The ⇄ icon moves receipts out of final tax

The notified TY2026 form carries this instruction on the final tax grid:

> *"You may offer this receipt under Normal Tax regime by clicking ⇄ icon"*
> — SRO 1495(I)/2026, p.14. **Read from the notified form, not observed live —
> confirm on screen.**

That icon is the physical implementation of the **s.154A(3) opt-out**. Clicking
it moves the receipt from final tax to the normal regime, where it is taxed at
slab rates instead of 0.25% or 1%. For an exporter that is a difference of
whole multiples, not percentages.

Two consequences:

- **A stray click is expensive and quiet.** If export income appears on the
  computation under normal tax rather than at `920100 Fixed / Final Tax`, check
  whether this icon has been toggled on the row before assuming a portal bug.
- **Do not click it to "see what it does".** This is the one control on the
  154A row that changes the tax treatment rather than the data. If a taxpayer
  genuinely wants to opt out, s.154A(3) requires the option to be exercised
  every year at the time of filing, and the consequences are not spelled out in
  the section — see below. That is a decision for the taxpayer with advice, not
  a field to experiment with.

## Codes worth knowing

### Section 154A export of IT/ITeS services

| Code | Rate | Applies to |
|---|---|---|
| `64060290` | 0.25% | computer software / IT / ITeS exported by an exporter **registered with and certified by PSEB** — s.154A(1)(a) |
| `64060285` | 1% | **any other case** under s.154A(1) |

The 1% line is a residual, not a "non-PSEB IT exporter" rate. Since the Finance
Act 2022, s.154A(1)(a) is itself confined to PSEB-registered and certified
exporters, so an IT exporter without certification is not taxed under clause (a)
at all — they fall into another clause of s.154A(1) and pick up the 1% residual,
alongside services rendered outside Pakistan, royalties and fees from foreign
enterprises, foreign construction contracts, indenting commission and notified
services.

**ATL status does not change these rates.** The Tenth Schedule — which doubles
withholding for persons not on the Active Taxpayer List — does not apply to
s.154A at all:

> **10.** The provisions of this Schedule shall not apply on tax collectible or
> deductible in case of the following sections:— … **(ca) tax collected or
> deducted under section 154A;**

with the footnote *"New sub-rule (ca) inserted by the Finance Act, 2022."* So
0.25% and 1% apply whether or not the exporter is on the ATL.

FBR's **2025-26** Withholding Income Tax Rate Card published doubled 0.5% / 2%
figures for s.154A; the 2026-27 card does not, and cites R.10(ca). Where the
card and the statute conflict, the statute governs — the card says so on its own
face. This one is worth remembering as a method, not just a fact: the rate card
is a facilitation document, and it was wrong against FBR's own Ordinance for a
year.

**The 0.25% rate has a sunset.** Division IVA carries the qualifier *"for tax
years 2024 up to tax year 2026"*, added by the Finance Act 2023. The Finance
Act 2026 is reported to have extended it to **tax year 2029** — confirm that
against the current consolidation before relying on it for TY2027 onwards; the
extension is not in the consolidation to 31 July 2025.

s.154A(1) has the authorised dealer collect at the time FX proceeds are
realised. **s.154A(2)** makes the final-tax treatment conditional on:

- **(a)** the return has been filed;
- **(b)** withholding tax statements for the year have been filed *if required
  under the Ordinance*;
- **(c)** sales tax returns under Federal or Provincial law have been filed *if
  required under the law*.

No credit for foreign taxes paid is allowed against this income.

**Condition (c) carries a proviso that matters.** The Finance Act 2023 inserted:

> *Provided that this condition shall not apply in case of an exporter mentioned
> in clause (a) of sub-section (1) of this section.*

This is read from FBR's own consolidation of the Ordinance, not from a
commentary.

So for a **PSEB-registered** exporter, provincial sales tax registration (PRA,
SRB, KPRA, BRA) is **not** a condition of the 0.25% regime. Whether registration
is required under the provincial law in its own right is a separate question
with its own exposure — do not conflate the two.

**s.154A(3)** has **two** triggers, and the first is the one with exposure:
sub-s (2) does not apply to a person "who does not fulfil the specified
conditions **or** who opts not to be subject to final taxation". Failing a
condition knocks the receipts out of final tax whether or not anyone intended
it. The opt-out proper is exercised every year, at the time of filing the s.114
return.

Note that s.154A says nothing about what happens next. The minimum-tax proviso
people remember was s.154(5), omitted by the Finance Act 2024 — so the
consequence of falling out of final taxation under s.154A is not spelled out in
the section. Flag this; do not assert an answer.

### Dividends

| Code | Rate | Applies to |
|---|---|---|
| `64030055` | 15% | the residual — an ordinary dividend from a Pakistani company, and dividends from a REIT |
| `64030090` | 25% | a dividend from a company whose **own income is exempt** from tax u/s 5 |
| `64330050` | 25% / 15% | dividend received from **debt securities / mutual funds** — this is where the split below lands |
| `64030052` | 7.5% | IPP pass-through dividend |
| `64330066` | 0% | a REIT scheme receiving from an SPV |
| `64030064` | 35% | any other person receiving from a REIT SPV — the line carrying an explicit ATL / non-ATL label |
| `64330067` | 35% | dividend u/s 150 @ 35% |

Only the first two rows were used in the filing this came from. The rest are
read from the notified form (SRO 1495(I)/2026) — **confirm on screen before
relying on one**, and in particular confirm the equity-portion code, which was
recovered by OCR from a scanned page.

**Mutual funds are split.** From the Finance Act 2025, the portion of a mutual
fund dividend derived from **debt securities** is taxed at 25% and the portion
from **equities** at 15%, apportioned on average annual investments. This
replaced an older rule taxing the whole dividend at 25% where the fund drew 50%
or more of its income from profit on debt. FBR's rate card still lists both
rules without year labels; Circular No. 1 of 2025-26 is what makes the split the
current position.

**Non-ATL rates are double throughout for dividends.** Every s.150 row on FBR's
rate card is referenced to R.1 of the Tenth Schedule and shows the doubled
figure. This is the opposite of s.154A above, which R.10(ca) excludes from the
Schedule entirely — do not carry one rule across to the other.

Reconcile both the gross and the tax deducted against `SUMMARY OF ECONOMIC
TRANSACTIONS` before filing — FBR's own third-party data has proved more
accurate than working papers.

### Computations (Tax Chargeable / Payments → Computations)

| Code | Line |
|---|---|
| `9000` | Total Income |
| `9013` | Share in Income from AOP |
| `920100` | Fixed / Final Tax |
| `9200` | Tax Chargeable |
| `923198` | Adjustment of Minimum Tax Paid u/s 113 in earlier years |
| `92101` | Refund Adjustment of Other Year(s) against Demand of this Year |
| `9201` | Withholding Income Tax |
| `9203` | **Admitted Income Tax** — the figure to pay |

### Business balance sheet (Business → Balance Sheet)

Assets, totalling to `3349`:

| Code | Line | Notes |
|---|---|---|
| `3349` | Total Assets | computed, not typeable |
| `3301` | Land (Business) | sub-grid via `+ Property` |
| `3302` | Building (Business) | sub-grid via `+ Property` |
| `3320` | Bank Account | sub-grid via `+` |
| `3303` | Plant / Machinery / Equipment / Furniture | editable |
| `3315` | Stocks in trade / Stores / Spares | editable |
| `3304` | Motor Vehicle(s) | sub-grid via `+` |
| `3312` | Advances / Deposits / Prepayments | editable |
| `3319` | Cash in hand | editable |
| `3321` | Bonds/Securities | editable |
| `3348` | Other Assets | editable |

Equity and liabilities, totalling to `3399`:

| Code | Line |
|---|---|
| `3399` | Total Equity / Liabilities — computed |
| `3352` | Capital |
| `3371` | Long Term Borrowings / Debt / Loan |
| `3384` | Trade Creditors / Payables |
| `3398` | Other Liabilities |

### Wealth statement (116 → Personal Assets / Liabilities)

| Code | Line |
|---|---|
| `7001` | Agricultural Property |
| `7002` | Commercial/Industrial/Residential Property — the combined code used up to TY2025 |
| `7109` | Residential/Commercial Property — the TY2026-onwards code |
| `7003` | Business Capital — **computed, fed by balance sheet `3352`** |
| `700302` | Business Capital in AOPs/Companies |
| `7004` | Equipment (Non-Business) |
| `7006` | Investments / Stocks / Bonds / Accounts — sub-grid, one row per account |
| `7008` | Motor Vehicle(s) — sub-grid, one row per vehicle |
| `7009` | Precious Possession |
| `7010` | Household Effects |
| `7011` | Personal Items |
| `7012` | Cash in hand |
| `7013` | Any Other Asset(s) — receivables, loans given |
| `7014` | Assets held on others' name |
| `7020` | Assets held outside Pakistan — also drives the 116A page |
| `7019` | Total Assets — computed |
| `7021` | Payables (Borrowing / Loan / Credits) |
| `7029` | Total Liabilities — computed |
| `703001` | Net Assets Current Year — computed |

Property rows change code when edited on the TY2026 form: a row imported as
`7002` becomes `7001` or `7109` depending on the property type chosen. This is
expected.

### Reconciliation (116 → Reconciliation of Net Assets)

| Code | Line |
|---|---|
| `703001` | Net Assets Current Year |
| `703002` | Net Assets Previous Year |
| `703003` | Increase / Decrease in Assets |
| `7049` | Inflows |
| `7031` | Income Declared as per Return subject to Normal Tax |
| `7089` / `7087` | Personal Expenses |
| `703000` | **Unreconciled Amount — must be 0** |

Personal Expenses live on the Reconciliation page in the TY2026 form, not on a
separate Personal Expenses page as in earlier years. If the sidebar has no
Personal Expenses entry, this is why.

## Foreign assets

Code `7020` (Assets held outside Pakistan) surfaces the **116A - Foreign
Assets/Liabilities** page. Enabling "Income from Foreign Sources and Assets"
under `ADD INCOME SOURCES` is what makes the 116A sidebar entry appear.

Money earned abroad but never remitted — a platform wallet balance, for example
— is an asset held outside Pakistan even though no proceeds certificate exists
for it. Declare it; the absence of a PRC is not a reason to omit it.

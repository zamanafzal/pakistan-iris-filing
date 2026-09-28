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

## Codes worth knowing

### Section 154A export of IT/ITeS services

| Code | Rate | Applies to |
|---|---|---|
| `64060290` | 0.25% | PSEB-registered exporter |
| `64060285` | 1% | not PSEB-registered |

s.154A(1) has the authorised dealer collect at the time FX proceeds are
realised. **s.154A(2)** makes the reduced regime conditional on: the return
being filed; withholding statements filed *if required*; and sales tax returns
under Federal **or Provincial** law filed *if required*. The provincial limb
(PRA in Punjab, SRB in Sindh, KPRA, BRA) is the one people miss. Whether a given
IT exporter is actually *required* to register is unresolved — flag it, do not
resolve it, and point the taxpayer at a practitioner.

### Dividends

| Code | Rate |
|---|---|
| `64030055` | 15% |
| `64330050` | 25% |

Reconcile both the gross and the tax deducted against `SUMMARY OF ECONOMIC
TRANSACTIONS` before filing.

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

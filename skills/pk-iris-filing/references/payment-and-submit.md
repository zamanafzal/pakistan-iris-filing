# Paying the tax, claiming the payment, and submitting

## The sequence, in order

1. Compute and verify **Admitted Income Tax `9203`** on the Computations page.
2. Tell the user that exact figure.
3. **The user** generates the PSID for that amount and pays it.
4. The payment posts and appears under the **Payment** tab → *Unclaimed
   Payments*.
5. **Claim it** against the return — click CLAIM, then Save.
6. Verify *Claimed Payments (1)* and the Head-wise Summary show head `9203` and
   the exact amount.
7. **The user** presses Submit.

Steps 3 and 7 belong to the user. Step 5 is a return-data action and can be done
for them, once the posted amount has been read on screen and confirmed to match.

## Why claiming matters

Submitting before claiming means FBR raises a demand for the admitted tax even
though the money has already left the account. Recovering from that is
paperwork. Always claim, save, and confirm before the user submits.

## Verify the amount before the user pays

Check `9203` on screen immediately before telling the user what to pay. Tax
Chargeable `9200` is *not* the amount to pay — withholding `9201` comes off it:

```
9203 Admitted Income Tax = 9200 Tax Chargeable − 9201 Withholding Income Tax
```

Reading the wrong line here means the user overpays by the whole withholding
amount, and getting an overpayment back from FBR is far harder than paying the
right figure once.

## The Payment tab

Three panels: **Unclaimed Payments**, **Claimed Payments**, **Head-wise
Summary**. Each payment card shows the CPR number, the Code (the amount head)
and the Amount.

Before clicking CLAIM, confirm:

- the **Code** is `9203`
- the **Amount** equals the admitted tax exactly
- the **CPR** corresponds to the PSID the user paid

After claiming: Unclaimed shows "Not Available", Claimed shows (1), and the
Head-wise Summary lists head `9203` with the amount. Save, and check the toast
reads "Changes saved successfully".

A claimed payment can be un-claimed via DELETE on the claimed card. That removes
the claim, not the payment — but do not do it without the user asking.

## Before handing over for Submit

Present a short table of what was verified, not a narrative of what was clicked:

| | |
|---|---|
| Total Income `9000` | |
| Tax Chargeable `9200` | |
| Withholding `9201` | |
| Admitted Income Tax `9203` | |
| Claimed payment | CPR, head, amount |
| Unclaimed payments | none |
| Net Assets `703001` | |
| Net Assets Previous Year `703002` | |
| Unreconciled `703000` | 0 |

Then say explicitly that Submit is theirs to press.

## If Submit returns a validation error

Expect several rounds. Ask the user to paste the message, then work through it
using the `iris-validation-errors` skill. Fix, save, re-verify the reconciliation
and the claimed payment, and hand back for another attempt. Validation errors do
not damage anything — the return stays a draft.

## Deadline

The statutory due date for individuals is **30 September** following the tax
year end (30 June). Filing late costs Active Taxpayer List status and attracts
penalties, so when time is short, prioritise a correct, submittable return over
an elegant one.

Two different extensions exist and they are not interchangeable. The **Board**
may extend the date for everyone under **s.214A**; the **Commissioner** may
extend one taxpayer's date on their own application under **s.119**. FBR has
granted a blanket extension in each of the recent years, and the tax bars
usually petition for one, but **an extension is discretionary, year-specific,
and often announced at the last moment**. Never plan around one, and never tell
a taxpayer an extension is coming.

An extension postpones only the filing, not the liability to pay — default
surcharge still runs on tax paid late.

## What filing late actually costs

Missing the due date puts the taxpayer outside the Active Taxpayer List, and
s.182A sets out four consequences:

- **not included in the ATL** for the year the return was late;
- **no loss carry-forward** for that tax year;
- **no refund issued** while off the list;
- **no additional payment for delayed refund** under s.171, and time spent off
  the list does not count toward it.

Re-entry is possible: the proviso to s.182A(1)(a) lets a late filer back onto
the list on payment of a surcharge of **Rs 1,000 for an individual** (Rs 10,000
for an AOP, Rs 20,000 for a company).

**Being off the ATL does not double withholding on export proceeds.** The Tenth
Schedule does not apply to s.154A at all — see the Tenth Schedule R.10(ca) note
in `field-map.md`. It does double withholding on most other things, dividends
included, so the ATL still matters; it just does not bite where a s.154A
exporter would first expect it to.

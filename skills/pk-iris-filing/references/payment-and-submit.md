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
year end (30 June). Filing late costs the Active Taxpayer List status and
attracts penalties, so when time is short, prioritise a correct, submittable
return over an elegant one.

# What this plugin still needs to see

Everything here was learned from **one filing**: a tax year 2026 return for a
PSEB-registered IT/ITeS exporter, filing as a sole proprietor, taxed entirely
under section 154A, with property in Punjab.

That is the plugin's strength and its ceiling. Every field location and portal
behaviour in it was observed rather than guessed — but observed **once**, by one
person, on one kind of return. Until someone else files with it, there is no way
to tell what is true about IRIS from what was merely true about that return.

**If you are filing, you are standing in front of the answer.** Most of the list
below takes seconds to settle — open a tab, read a label, and say what you saw.
You do not need to be a tax expert; you need to be in the portal, which the
maintainer is not, eleven months of the year.

## How to report what you see

Easiest first:

- **Open an issue.** Three templates:
  *Validation error* (IRIS rejected something), *Field moved* (a code or field
  is not where the plugin says), *Portal surface observed* (you looked at a page
  on this list).
- **Open a pull request** against the relevant reference file. Tag what you add
  `[live]` and add your tax year.
- **Or tell Claude at the end of your filing.** Ask it to write up what it
  learned; it will produce the diff for you to paste.

**Never include your own figures, NTN, CNIC, CPR or address.** What is useful is
the *label text*, the *field code*, the *behaviour* and the *tax year*. Nothing
here needs a single rupee of your data. A screenshot almost always carries your
name in the header — quote the text instead.

---

## Highest value first

Ordered by how many filers each unlocks, against how little work it takes to
answer. Tick a box, cite the tax year you saw it in.

### Anyone can answer these in a minute

- [ ] **Province dropdowns outside Punjab.** Open the Property Information
      modal, pick Sindh / KP / Balochistan / ICT / AJK / Gilgit-Baltistan in
      turn, and say what the third level is called — tehsil, taluka, something
      else — and whether any list is empty. Punjab is the only one mapped, and
      probably half of all users are elsewhere.
- [ ] **The `ADD INCOME SOURCES` dialog.** The complete list of toggles,
      verbatim, and which sidebar section each one reveals.
- [ ] **`SUMMARY OF ECONOMIC TRANSACTIONS`.** What the panel actually shows —
      tabs or one list, what the columns are, whether rows name the withholding
      agent, whether it can be read before any data entry.
- [ ] **The Attachment tab.** Is anything mandatory for a 114(1)? What file
      types and size limit?
- [ ] **Business Details.** What does the add flow ask for, and is it populated
      from your registration profile rather than typed?
- [ ] **Is there a Form 181 gate?** Does IRIS make you refresh your profile
      before the return form opens?

### Worth a few minutes if you have business income or assets

- [ ] **Depreciation and Amortization tabs.** Column structure, and whether the
      depreciation charge flows into business income automatically or has to be
      re-entered as an expense.
- [ ] **`IMPORT PREVIOUS RETURN`.** Currently documented only as "do not press
      casually". If you press it on an **empty** draft at the very start of a
      filing: does it prompt for a year, does it merge or replace, does it bring
      wealth statement rows across with their prior declared values, and is
      there a confirm dialog? *If a dialog appears, read its exact wording and
      cancel — that text is often the whole answer, at zero risk.*
- [ ] **116A Foreign Assets/Liabilities.** The plugin's biggest hole and its
      core audience: anyone with a Payoneer, Wise, PayPal, Upwork or exchange
      balance. What are the rows and fields? **Does it want PKR at cost or the
      foreign currency at closing?** Must `7020` and the 116A rows agree, and
      which is computed from which?

### If you file a kind of return this plugin refuses

The plugin currently declines these outright. Each one opened up would serve far
more people than the niche it was built for.

- [ ] **A salary return.** The single biggest gap. Read back the Employment
      codes (`1000`, `1009`, `1010`, `1049`, `1008`, `1059`, `1089`, `1099`),
      say whether `1049 Allowances` is one input or a sub-grid, and capture the
      `+ ADD EMPLOYER DETAILS` modal.
- [ ] **Rental income.** Does IRIS compute the 1/5 repairs allowance itself, and
      what does it do to the Unreconciled Amount `703000`?
- [ ] **Capital gains.** Does IRIS compute tax from holding period and
      acquisition date, or does it expect you to pick a rate code?
- [ ] **Anything with tax at slab rates**, rather than final tax.

### Worth confirming every year, by everyone

- [ ] **The Reconciliation page codes**, in particular `7032` (Exempt) and
      `7033` (Final/Fixed Tax), which are not yet in the field map and matter
      for every income type the plugin does not cover.
- [ ] **The Personal Expenses sub-grid** under `7089` — every line it offers,
      and whether one of them is income tax paid.
- [ ] **Whether the Computations page still carries `PREPARE PSID`**, and where.
- [ ] **Any validation error not in `pk-iris-errors`** — the verbatim message,
      what caused it, and what fixed it. These are the most useful single
      contribution anyone can make, because they cannot be researched, only
      encountered.

---

## Things that cannot be answered by looking

Separate list, because these need a practitioner or a published source rather
than a portal session. Do not guess at them.

- Whether the Tenth Schedule's non-application to s.154A survives the next
  Finance Act.
- Whether provincial sales tax registration is required under provincial law in
  its own right, for a PSEB-registered exporter.
- Whether overseas platform income is contracting or employment.
- Where the property-value floor rule comes from. It is enforced by IRIS at
  submission, and no provision of the Ordinance, the Rules, an SRO or a circular
  stating it has been found. **If you can cite an authority for it, that would
  settle a question the plugin currently has to describe as unexplained.**

---

## The rule this list exists to protect

Content in this plugin is tagged by where it came from: observed on the live
portal, read from statute or a notified form, or reasoned but unconfirmed. That
tagging is the whole product — it is what lets Claude say "I do not know" at the
moment it matters, on a document where a confident wrong answer costs real
money.

So contributions are welcome in any state, **as long as they are labelled
honestly**. "I saw this on the TY2027 form" is worth more than a polished
paragraph that might be right.

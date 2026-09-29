# Pakistan IRIS Filing

File your own income tax return on FBR's **IRIS 2.0** portal, with Claude
reading the form over your shoulder — the 114(1) return, the 116 wealth
statement and its reconciliation, section 154A export final tax, property
declarations, paying and claiming the admitted tax, and getting past IRIS's
validation errors.

Built while actually filing a **tax year 2026** return, so what's in it is what
the portal **does**, not what the form appears to do. Those turned out to be
different things surprisingly often.

---

## What it saves you

Four things that cost the author hours, in a form you can read in thirty
seconds:

- The Final Tax fields under Tax Chargeable/Payments are `disabled` for **every**
  code. Typing into them fails silently — no error, no warning, the value simply
  isn't there when you come back. The editable locations are somewhere else
  entirely.
- Balance sheet **Capital `3352`** feeds wealth statement **Business Capital
  `7003`**, which feeds Net Assets. Putting a number there to satisfy a
  validation inflates your net worth and breaks your reconciliation — and a
  broken reconciliation is FBR's flag for unexplained wealth.
- A property's **Land area** field carries no asterisk, but becomes mandatory
  the moment you pick a unit. There is no way to save a property without
  stating its size.
- A property's declared value **cannot go below last year's**, which makes
  splitting one declared property into two rows impossible without breaking the
  reconciliation.

Each of those is the kind of thing you find out at 11pm on 30 September.

---

## Install

In a Claude session:

```
/plugin install pakistan-iris-filing --marketplace zamanafzal/pakistan-iris-filing
```

Or from the terminal:

```bash
claude plugin marketplace add zamanafzal/pakistan-iris-filing
claude plugin install pakistan-iris-filing@pakistan-tax-tools
```

The plugin is `pakistan-iris-filing`; the marketplace it lives in is
`pakistan-tax-tools`. Update later with `claude plugin update
pakistan-iris-filing@pakistan-tax-tools`.

---

## Using it

Say what you want in plain language:

- "Let's file my FBR return for this year"
- "IRIS says the declared property value must not be lower than last year's"
- "Review my return before I submit"
- "Help me claim my PSID payment"

Paste an IRIS error message and the error skill fires on its own.

### You drive, or Claude drives

**By default you do the clicking.** Claude tells you exactly where to go, what
to enter, and what to read back to it. This needs no browser extension, works on
any setup, and is the more robust of the two — IRIS reflows under automation
more than you'd like.

**If you'd rather Claude drove**, connect the Claude in Chrome extension and say
so. It's faster when it works, and it can read fields back itself instead of
asking you. If automation breaks mid-filing, Claude says so and carries on
guiding rather than silently retrying.

Either way **you** log in, **you** pay, and **you** press Submit.

### Before you open the portal

Put your figures in one file and check them locally:

```bash
mkdir -p ~/.pk-iris
cp scripts/working-papers.example.json ~/.pk-iris/working-papers.json
python3 scripts/check.py
```

IRIS reports **one validation failure per submission attempt**, and each round
trip risks a session expiry. The most expensive error it doesn't report at all —
a wealth statement that doesn't reconcile will submit happily, and FBR raises it
months later as a notice.

`check.py` runs that arithmetic in a second, as many times as you like: the
reconciliation, every property against last year's floor, the `3352 → 7003`
capital trap, admitted tax against chargeable less withholding, withholding
credits claimed on certificates that show no income tax line, and foreign
balances accidentally declared twice. Standard library only, no network, no log
file. It checks your figures against each other — it never computes your tax.

Your working papers stay in `~/.pk-iris/`, outside any checkout, because they're
a complete picture of your finances and this repo is public.

### You don't fill in a profile — Claude builds one

Say you're filing and it works through your standing circumstances (PSEB
registration, how your income arrives, which assets exist, your valuation
basis), reads last year's return off the portal rather than making you retype
it, and writes `~/.pk-iris/profile.md` as it goes. Next September it doesn't ask
again.

> **Upgrading from 0.3.0 or earlier?** If you filled in
> `skills/pk-iris-filing/references/your-profile.md`, copy it to
> `~/.pk-iris/profile.md` now. Anything left inside the plugin directory is
> overwritten by the next update.

---

## Who it's for

Individuals filing a **114(1) with a wealth statement** — especially freelancers
and IT/ITeS exporters taxed under section 154A.

**It is deliberately not a general-purpose IRIS plugin.** Salary returns, rental
income, capital gains, agriculture, AOP and company returns, tax slab
computation, minimum tax, deductible allowances and tax credits, and provinces
other than Punjab were never exercised. The plugin says so, and tells Claude to
say so rather than guess. See
[`scope-and-limits.md`](skills/pk-iris-filing/references/scope-and-limits.md).

---

## What's inside

| Component | Purpose |
|---|---|
| **pk-iris-agent** | Guides or drives the portal, verifies after every change, hands the irreversible steps back to you |
| **pk-iris-filing** | Workflow, portal mechanics, field/code map, wealth statement rules, payment sequence, working papers |
| **pk-iris-errors** | Paste an IRIS error → what actually caused it → the fix that doesn't break your reconciliation |
| **scripts/check.py** | Pre-flight validator. Nine checks, standard library only |

---

## What it will not do

By design, it always stops and asks before:

- **Submitting the return** — it prepares and verifies; you press Submit
- **Generating a PSID or paying** — it tells you the amount; you pay it
- **Deleting or reducing a declared row** — it explains the consequence first
- **Inventing a figure** — a land area, an acquisition date, a cost basis. A
  plausible guess in a wealth statement is a false declaration

And it never touches login fields. IRIS expires sessions aggressively; when that
happens it tells you and waits.

To change any of this, edit "What you never do without asking" in
[`agents/pk-iris-agent.md`](agents/pk-iris-agent.md).

---

## Help make it true for more than one person

**Everything here was learned from one filing.** One taxpayer, one income type,
one province, one tax year. That's the plugin's strength — nothing in it is
guessed — and its ceiling: there's no way to tell what's true about IRIS from
what was merely true about that return.

If you're filing, you're standing in front of the answer. Most of what's
missing takes seconds to settle: open a tab, read a label, say what you saw.

**[`OBSERVATIONS.md`](OBSERVATIONS.md) is the list**, ordered by how much each
one unlocks. Some highlights:

- What the province dropdowns look like **outside Punjab** — probably half of
  all users, and ten minutes of read-only work
- The **116A foreign assets** schedule — the biggest hole for exactly this
  plugin's audience, anyone holding a Payoneer, Wise, Upwork or exchange balance
- Any **validation error** not already in the errors skill. These can't be
  researched, only encountered, so they're the single most valuable thing anyone
  can contribute

Three issue templates make it quick, and Claude will write up the report for you
at the end of your filing if you ask.

**Send no personal data** — no NTN, CNIC, CPR, account numbers, addresses or
amounts. What's useful is label text, field codes, behaviour and the tax year,
and none of that needs a rupee of your figures. Screenshots almost always carry
your name in the header; quote the text instead.

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before a pull request.

---

## Keeping it current

**FBR revises the form every year.** TY2026 differed from TY2025 in ways that
mattered — property addresses became structured and mandatory, property codes
changed, Personal Expenses moved onto the Reconciliation page. Treat every code
and field location as a strong prior to confirm on screen, and update
[`field-map.md`](skills/pk-iris-filing/references/field-map.md) when something
moves.

Rates and statutory claims are re-verified against FBR's own consolidation of
the Ordinance, not commentary. That process has already caught FBR's published
rate card contradicting FBR's own statute — see the 0.3.1 entry in
[`CHANGELOG.md`](CHANGELOG.md).

---

## This is not tax advice

It describes how the portal behaves and how one filing was approached. You are
responsible for what you declare. Anything contentious — how income should be
characterised, whether a registration was required, how to treat an unusual
asset — needs a Pakistani tax practitioner, not a plugin.

Two questions in particular are flagged as **unresolved** rather than answered:
whether provincial sales tax registration is required under provincial law in
its own right, and how to characterise overseas platform income as contracting
versus employment. Both have real money attached and neither is settled here.

One more worth knowing: your conversation with Claude contains your figures.
That's inherent in using an assistant for a tax return, and worth knowing rather
than being reassured about.

---

## Credits

Built by **Zaman Afzal** — [github.com/zamanafzal](https://github.com/zamanafzal)
— while filing a tax year 2026 return.

Issues and pull requests:
[github.com/zamanafzal/pakistan-iris-filing](https://github.com/zamanafzal/pakistan-iris-filing)

## License

MIT. Use it, fork it, improve it. If you extend it to salary returns or another
province, that's the most useful thing you could contribute.

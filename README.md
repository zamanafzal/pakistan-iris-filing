# Pakistan IRIS Filing

Helps you file your own income tax return on FBR's **IRIS 2.0** portal — the
114(1) return, the 116 wealth statement and its reconciliation, section 154A
export final tax, property declarations, paying and claiming the admitted tax,
and getting past IRIS's validation errors.

Built while actually filing a **tax year 2026** return, so the contents are what
the portal **does**, not what the form appears to do. Those turned out to be
different things surprisingly often.

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
`pakistan-tax-tools`. Once the marketplace is added, the plugin also appears in
the desktop app's plugin browser under **Add plugin**.

Update later with:

```bash
claude plugin update pakistan-iris-filing@pakistan-tax-tools
```

## Who it's for

Individuals filing a **114(1) with a wealth statement** — especially freelancers
and IT/ITeS exporters taxed under section 154A.

**It is deliberately not a general-purpose IRIS plugin.** Salary returns, rental
income, capital gains, agriculture, AOP and company returns, tax slab
computation, minimum tax, deductible allowances and tax credits, and provinces
other than Punjab were never exercised. The plugin says so and tells Claude to
say so rather than guess. See `skills/pk-iris-filing/references/scope-and-limits.md`.

## What's inside

| Component | Purpose |
|---|---|
| **pk-iris-agent** | Drives the portal, verifies after every change, hands the irreversible steps back to you |
| **pk-iris-filing** | Workflow, portal mechanics, field/code map, wealth statement rules, payment sequence, your profile |
| **pk-iris-errors** | Paste an IRIS error → what actually caused it → the fix that doesn't break your reconciliation |

Some of what it will save you:

- The Final Tax fields under Tax Chargeable/Payments are `disabled` for **every**
  code — typing into them fails silently. The editable locations are elsewhere.
- Balance sheet **Capital `3352`** feeds wealth statement **Business Capital
  `7003`**, which feeds Net Assets. Putting a number there to satisfy a
  validation will inflate your net worth and break your reconciliation.
- A property's **Land area** field carries no asterisk, but becomes mandatory the
  moment you pick a unit.
- A property's declared value **cannot go below last year's**, which makes
  splitting one declared property into two rows impossible without breaking the
  reconciliation.

## Before you open the portal

Put your figures in one file and check them locally:

```bash
mkdir -p ~/.pk-iris
cp scripts/working-papers.example.json ~/.pk-iris/working-papers.json
python3 scripts/check.py
```

IRIS reports **one validation failure per submission attempt**, and the most
expensive error — a wealth statement that doesn't reconcile — it doesn't report
at all; FBR does, months later, as a notice. `check.py` runs the arithmetic in a
second, as many times as you like. Standard library only, no network, no log
file. It checks your figures against each other; it never computes your tax.

Your working papers live in `~/.pk-iris/`, outside any checkout, because they're
a complete picture of your finances and this repo is public.

## Setup

No configuration, no API keys. Claude needs browser automation — the **Claude in
Chrome** extension connected — and **you** log into IRIS yourself.

## Using it

Say what you want in plain language:

- "Let's file my FBR return for this year"
- "IRIS says the declared property value must not be lower than last year's"
- "Review my return before I submit"
- "Help me claim my PSID payment"

The error skill also fires when you simply paste an IRIS message.

**You don't fill in a profile — Claude builds one by asking.** Say you're
filing and it works through your standing circumstances (PSEB registration, how
your income arrives, which assets exist, your valuation basis), reads last
year's return off the portal rather than making you retype it, and writes
`~/.pk-iris/profile.md` as it goes. Next September it doesn't ask again.

That file lives in your home directory, **not** in the plugin — `claude plugin
update` replaces everything inside the plugin, so anything kept there is lost on
the next update. `skills/pk-iris-filing/references/profile.example.md` is the
blank template if you'd rather start it by hand. Keep amounts and identifiers
out of it; those belong in your working papers.

> **Upgrading from 0.3.0 or earlier?** If you filled in
> `skills/pk-iris-filing/references/your-profile.md`, copy it to
> `~/.pk-iris/profile.md` now. The next plugin update will overwrite it where it
> is.

## What it will not do

By design, it always stops and asks before:

- **Submitting the return** — it prepares and verifies; you press Submit
- **Generating a PSID or paying** — it tells you the amount; you pay it
- **Deleting or reducing a declared row** — it explains the consequence first

And it never touches login fields. IRIS expires sessions aggressively; when that
happens it tells you and waits.

To change any of this, edit "What you never do without asking" in
`agents/pk-iris-agent.md`.

## Keeping it current

**FBR revises the form every year.** TY2026 differed from TY2025 in ways that
mattered — property addresses became structured and mandatory, property codes
changed, Personal Expenses moved onto the Reconciliation page. Treat every code
and field location as a strong prior to confirm on screen, and update
`references/field-map.md` when something moves.

At the end of each filing, add what you learned. That's the whole point — next
September you will not remember which field was disabled.

## This is not tax advice

It describes how the portal behaves and how one filing was approached. You are
responsible for what you declare. Anything contentious — how income should be
characterised, whether a registration was required, how to treat an unusual
asset — needs a Pakistani tax practitioner, not a plugin.

Two questions in particular are flagged as **unresolved** rather than answered:
whether provincial sales tax registration is required under provincial law in
its own right, and how to characterise overseas platform income as contracting
versus employment. Both have real money attached and neither is settled here.

(A third — whether s.154A(2)(c)'s sales tax condition bites for a PSEB-registered
exporter — is now closed: the Finance Act 2023 proviso disapplies it, read from
FBR's own consolidation of the Ordinance.)

## Credits

Built by **Zaman Afzal** — [github.com/zamanafzal](https://github.com/zamanafzal) —
while filing a tax year 2026 return, with Claude driving the portal.

Issues and pull requests:
[github.com/zamanafzal/pakistan-iris-filing](https://github.com/zamanafzal/pakistan-iris-filing)

## License

MIT. Use it, fork it, improve it. If you extend it to salary returns or another
province, that's the most useful thing you could contribute.

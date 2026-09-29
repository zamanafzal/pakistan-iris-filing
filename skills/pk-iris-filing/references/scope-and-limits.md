# What this plugin knows, and what it does not

Read this before relying on anything else here. The value of this plugin is that
its contents were **observed on the live IRIS 2.0 portal**, not inferred from
what the form appears to do — and repeatedly, the form's appearance was wrong.
That value only holds if the boundary is respected.

## Verified first-hand

Observed directly while preparing and submitting a **tax year 2026 114(1)**
return for a **PSEB-registered IT/ITeS exporter filing as a sole proprietor**:

- Portal navigation, session behaviour, how drafts and prior-year returns open
- Which final-tax fields are `disabled` and where the editable ones live
- Field codes across business income, balance sheet, wealth statement,
  reconciliation and computations
- That balance sheet Capital propagates into wealth statement net assets
  (established by a controlled test, not by reasoning)
- The Property Information modal: every mandatory field, all type and sub-type
  options, land area units, and the order in which fields become required
- Four submission validation messages, verbatim, each with a cause and a fix
  that worked
- The payment → claim → submit sequence

## Not covered — say so rather than guess

None of the following was exercised. Claude must **tell the user plainly that
this plugin does not cover it** rather than improvising:

- **Salary returns.** A return whose income is employment income uses form
  sections this plugin never touched.
- **Foreign salary**, and the interaction with s.102 exemption / s.103 foreign
  tax credit.
- **Property (rental) income**, **capital gains**, **agriculture income** —
  declared under heads that were left empty here.
- **Normal-regime computation.** This return was entirely final tax. Tax slab
  rates, minimum tax u/s 113, deductible allowances (Zakat, education), and tax
  credits (donations, pension) were never computed.
- **AOP and company returns.** Individuals only.
- **Provinces other than Punjab.** District and tehsil dropdown behaviour was
  only observed for Punjab.
- **Any validation error not listed** in the errors skill.
- **116A foreign assets detail.** The page was surfaced but not filled in depth.

## Section 7E was struck down

On **7 May 2026** the Federal Constitutional Court held section 7E — deemed
income on immovable property — **ultra vires the Constitution and void ab
initio**, and set aside all actions, proceedings and notices taken under it
(short order 7 May 2026; detailed judgment June 2026; lead case reported as
C.P.L.A. 1442-K/2022, taken from KPMG's note rather than from the judgment
itself, which could not be retrieved from the Court's own site).

The **Finance Act 2026** separately omitted section 7E from the statute with
effect from 1 July 2026, making no provision for refund of tax already paid.
Note which instrument does what: the Act removes 7E from **TY2027 onwards**;
what removes it for **TY2026** is the judgment.

So **no 7E liability arises on a tax year 2026 return**, and the notified TY2026
return forms carry **no 7E schedule, field or deemed-income line** — checked
across all 111 pages of SRO 1495(I)/2026. If a 7E field appears on screen, it is
a portal artefact, not a notified requirement.

Two things that are still live:

- **Refunds.** An FBR **letter** to Chief Commissioners dated 23 September 2026
  directs field offices not to reject 7E-based revision requests and to process
  the resulting refunds. This is reported secondhand and appears to be an
  internal instruction rather than a published circular; it expressly does not
  extend to Super Tax u/s 4C. Anyone who paid 7E in an earlier year should take
  advice rather than assume a refund follows automatically.
- **s.236C(2A) was never repealed.** It still bars registration or attestation
  of a property transfer until the seller has discharged "tax liability under
  section 7E" — a section that no longer exists. Say that this exists and send
  the user to a practitioner. Do not improvise a way through it.

## The form changes every year

FBR revises the return between tax years, and the TY2026 form differed from
TY2025 in ways that mattered — property address fields became structured and
mandatory, property codes changed from a single combined code to type-specific
ones, and Personal Expenses moved onto the Reconciliation page.

Treat every code and field location here as a **strong prior to confirm on
screen**, not as fact. When something has moved, update `field-map.md` rather
than working around it silently.

## This is not tax advice

The material here describes how the portal behaves and how a particular filing
was approached. It is not advice, and the person filing is responsible for what
they declare. Anything contentious — characterisation of income, whether a
registration was required, how to treat an unusual asset — needs a Pakistani tax
practitioner, not this plugin.

Two points in particular were **unresolved** in the filing this came from and
should not be presented to a user as settled:

- **Contractor versus employee** characterisation of overseas platform income.
  Export of services under s.154A and foreign salary are taxed completely
  differently — a final tax of a fraction of a percent against normal slab
  rates. The distinction turns on the actual contract terms, and getting it
  wrong is expensive in either direction. Note also that s.102 exempts foreign
  source salary only where foreign income tax was **withheld by the employer and
  paid** to the revenue authority of the country in which the employment was
  *exercised* — someone working from Pakistan for a foreign employer generally
  has neither, so s.102 will not rescue a mischaracterisation.
- **Whether provincial sales tax registration is required in its own right.**
  The s.154A(2)(c) condition no longer bites for a PSEB-registered exporter —
  that question is closed. Whether PRA, SRB, KPRA or BRA registration is
  required under the provincial law itself is a separate question with its own
  exposure, and this plugin does not answer it.

## If the return has already been submitted

Corrections are possible, but the rules are specific and worth confirming
against the current Ordinance text rather than taking from here:

- **Revised return — s.114(6).** Written reasons must accompany it. The
  Commissioner's written approval is required, **except** where the revision is
  filed within **60 days** of the original. Separately, approval is treated as
  granted where the revision declares *more* taxable income than the original.
  Note that FBR's taxpayer guidance also refers to a five-year limit that does
  not appear in the section itself.
- **Revised wealth statement — s.116(3).** No Commissioner approval; filed under
  intimation, with revised reconciliation and reasons, at any time before a
  notice under s.122(9). Subject to a five-year limit measured from the return's
  **due date**, and the Commissioner may declare a revision void if not
  satisfied it corrects a bona fide error.
- **s.114(6A)** reduces or eliminates penalties where tax short-paid is deposited
  voluntarily before an audit notice.

These were researched from secondary statute hosts and FBR guidance, not read
from the official Ordinance PDF. Tell the user to confirm the current text
before acting, and never state a deadline as certain without checking.

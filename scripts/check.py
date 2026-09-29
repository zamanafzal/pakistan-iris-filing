#!/usr/bin/env python3
"""Pre-flight checks for a Pakistan IRIS 2.0 return, before the portal is opened.

Reads a working-papers JSON file and reports what IRIS would reject at
submission, and what FBR would query months later.

    python3 scripts/check.py [path]     default: ~/.pk-iris/working-papers.json
    python3 scripts/check.py --selftest

Exit 0 when clean, 1 when anything failed. Standard library only, on purpose:
this file reads a complete picture of someone's finances, and it should be
reviewable in one sitting.

It checks internal consistency of figures you supply. It never computes a tax
liability, and it is not tax advice.
"""

import json
import os
import sys

# The fields IRIS makes mandatory on the Property Information modal. Land area
# carries no asterisk on screen but becomes mandatory the moment a unit is
# picked, which is why it is here.
PROPERTY_REQUIRED = [
    ("land_area", "land area"),
    ("land_area_unit", "land area unit"),
    ("province", "province"),
    ("district", "district"),
    ("city", "city / tehsil"),
    ("plot_no", "property / plot / house / shop no."),
    ("sector", "sector / mohalla / block"),
]

# s.116A: a resident individual files the foreign assets schedule where foreign
# income reaches USD 10,000 or foreign assets reach USD 100,000.
FOREIGN_ASSETS_USD = 100_000
FOREIGN_INCOME_USD = 10_000

MONEY_KEYS = {
    "value", "amount", "pkr_at_cost", "declared_value", "net_assets",
    "net_assets_current", "cash", "capital", "other_assets", "other_liabilities",
    "chargeable", "withholding_credit", "admitted", "personal", "tax_paid",
}


def rupees(n):
    return f"{n:,.0f}"


class Report:
    def __init__(self):
        self.failures = []
        self.notices = []

    def fail(self, check, message):
        self.failures.append(f"{check}: {message}")

    def note(self, check, message):
        self.notices.append(f"{check}: {message}")

    @property
    def ok(self):
        return not self.failures


def number(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def amounts(items, key="value"):
    return sum(number(item.get(key)) for item in items if isinstance(item, dict))


def asset_rows(papers):
    """Every personal asset row, flattened, with the category it came from."""
    assets = papers.get("assets") or {}
    rows = []
    for category in ("properties", "vehicles", "accounts", "other"):
        for row in assets.get(category) or []:
            rows.append((category, row))
    return rows


def total_assets(papers):
    """Total personal assets, following the rules that trip people up.

    Accounts moved onto the business balance sheet are excluded, because they
    are already represented by Capital 3352 feeding Business Capital 7003.
    Foreign assets are counted once, from their own block.
    """
    assets = papers.get("assets") or {}
    total = amounts(assets.get("properties") or [])
    total += amounts(assets.get("vehicles") or [])
    total += amounts([a for a in assets.get("accounts") or []
                      if not a.get("in_business_balance_sheet")])
    total += amounts(assets.get("other") or [])
    total += number(assets.get("cash"))
    total += amounts(papers.get("foreign_assets") or [], key="pkr_at_cost")
    # Business Capital 7003 is a wealth statement asset, fed by balance sheet 3352.
    total += number((papers.get("balance_sheet") or {}).get("capital"))
    return total


def total_liabilities(papers):
    return amounts(papers.get("liabilities") or [], key="amount")


def total_income(papers):
    return sum(number(v) for v in (papers.get("income") or {}).values())


def total_outflows(papers):
    expenses = papers.get("expenses") or {}
    return sum(number(v) for k, v in expenses.items() if not k.endswith("_basis"))


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------


def check_types(papers, report):
    """Amounts must be numbers, and not negative."""
    def walk(node, path):
        if isinstance(node, dict):
            for key, value in node.items():
                walk(value, f"{path}.{key}" if path else key)
        elif isinstance(node, list):
            for i, value in enumerate(node):
                walk(value, f"{path}[{i}]")
        else:
            leaf = path.split(".")[-1].split("[")[0]
            if leaf in MONEY_KEYS:
                if isinstance(node, str):
                    report.fail("types", f"{path} is a string ({node!r}), not a number")
                elif isinstance(node, bool):
                    report.fail("types", f"{path} is a boolean, not a number")
                elif isinstance(node, (int, float)) and node < 0:
                    report.fail("types", f"{path} is negative ({node})")

    walk(papers, "")


def check_reconciliation(papers, report):
    """Unreconciled Amount 703000 must be exactly zero.

    closing net assets = opening + income + other inflows - outflows
    """
    prior = papers.get("prior_year") or {}
    if prior.get("net_assets") is None:
        report.note(
            "reconciliation",
            "no prior_year.net_assets — a first wealth statement declares an opening "
            "position rather than inheriting one, and the reconciliation cannot be "
            "checked until that figure is stated",
        )
        return

    opening = number(prior.get("net_assets"))
    closing = total_assets(papers) - total_liabilities(papers)
    inflows = total_income(papers) + amounts(papers.get("other_inflows") or [], key="amount")
    outflows = total_outflows(papers)

    gap = closing - (opening + inflows - outflows)
    if abs(gap) >= 1:
        direction = "more" if gap > 0 else "less"
        report.fail(
            "reconciliation",
            f"unreconciled by {rupees(abs(gap))} — closing net assets are "
            f"{rupees(abs(gap))} {direction} than opening plus inflows less outflows "
            f"explains. 703000 must be 0",
        )

    declared = papers.get("net_assets_current")
    if declared is not None and abs(number(declared) - closing) >= 1:
        report.fail(
            "reconciliation",
            f"net_assets_current says {rupees(number(declared))} but assets less "
            f"liabilities come to {rupees(closing)}",
        )


def check_property_floor(papers, report):
    """A property's declared value must not fall below last year's."""
    prior = {p.get("id"): p
             for p in (papers.get("prior_year") or {}).get("properties") or []
             if p.get("id")}
    for row in (papers.get("assets") or {}).get("properties") or []:
        pid = row.get("id")
        if pid not in prior:
            continue
        floor = number(prior[pid].get("declared_value"))
        value = number(row.get("value"))
        if value < floor:
            report.fail(
                "property-floor",
                f"{pid} declared at {rupees(value)}, below last year's {rupees(floor)} "
                f"— IRIS rejects this at submission",
            )


def check_property_detail(papers, report):
    """Every immovable property needs the full structured address."""
    for row in (papers.get("assets") or {}).get("properties") or []:
        pid = row.get("id") or row.get("description") or "unnamed property"
        missing = [label for field, label in PROPERTY_REQUIRED if not row.get(field)]
        if missing:
            report.fail("property-detail", f"{pid} is missing {', '.join(missing)}")


def check_foreign_assets(papers, report):
    """Foreign assets are declared once, in their own block, and may need 116A."""
    for category, row in asset_rows(papers):
        if row.get("foreign"):
            name = row.get("id") or row.get("description") or "a row"
            report.fail(
                "foreign-assets",
                f"{name} in assets.{category} is flagged foreign — declare it in "
                f"foreign_assets instead, or it is counted twice",
            )

    foreign = [f for f in papers.get("foreign_assets") or []
               if number(f.get("pkr_at_cost")) > 0]
    if not foreign:
        return

    total_pkr = amounts(foreign, key="pkr_at_cost")
    foreign_income = number((papers.get("income") or {}).get("foreign"))
    rate = number(papers.get("usd_pkr"))

    if not rate:
        report.note(
            "foreign-assets",
            f"{rupees(total_pkr)} of foreign assets declared. The 116A schedule is "
            f"required at USD {FOREIGN_ASSETS_USD:,} of assets or USD "
            f"{FOREIGN_INCOME_USD:,} of foreign income — set usd_pkr to have that tested",
        )
        return

    assets_usd = total_pkr / rate
    income_usd = foreign_income / rate
    if assets_usd >= FOREIGN_ASSETS_USD or income_usd >= FOREIGN_INCOME_USD:
        report.note(
            "foreign-assets",
            f"116A schedule required — foreign assets around USD {assets_usd:,.0f}, "
            f"foreign income around USD {income_usd:,.0f}",
        )


def check_business_capital(papers, report):
    """Capital 3352 feeds Business Capital 7003, which feeds net assets."""
    capital = number((papers.get("balance_sheet") or {}).get("capital"))
    moved = [a for a in (papers.get("assets") or {}).get("accounts") or []
             if a.get("in_business_balance_sheet")]
    moved_total = amounts(moved)

    if capital and not moved:
        report.fail(
            "business-capital",
            f"Capital 3352 is {rupees(capital)} but no account is marked "
            f"in_business_balance_sheet — Capital feeds 7003 and raises net worth "
            f"with nothing moved across to offset it",
        )
    elif capital and abs(capital - moved_total) >= 1:
        report.fail(
            "business-capital",
            f"Capital 3352 is {rupees(capital)} but accounts moved onto the balance "
            f"sheet come to {rupees(moved_total)}",
        )
    elif moved and not capital:
        report.fail(
            "business-capital",
            f"{rupees(moved_total)} of accounts are marked in_business_balance_sheet "
            f"but Capital 3352 is 0 — those assets are declared nowhere",
        )


def check_admitted_tax(papers, report):
    """9203 Admitted = 9200 Chargeable less 9201 Withholding."""
    tax = papers.get("tax") or {}
    if not tax:
        return
    chargeable = number(tax.get("chargeable"))
    credit = number(tax.get("withholding_credit"))
    admitted = tax.get("admitted")

    if admitted is not None and abs((chargeable - credit) - number(admitted)) >= 1:
        report.fail(
            "admitted-tax",
            f"admitted tax is {rupees(number(admitted))} but chargeable "
            f"{rupees(chargeable)} less withholding {rupees(credit)} is "
            f"{rupees(chargeable - credit)}",
        )

    if chargeable - credit < 0:
        report.note(
            "admitted-tax",
            f"withholding exceeds tax chargeable by {rupees(credit - chargeable)} — "
            f"a refund position, which this plugin does not cover",
        )

    claimable = sum(number(w.get("amount")) for w in papers.get("withholding") or []
                    if w.get("certificate_shows_income_tax"))
    if papers.get("withholding") and abs(claimable - credit) >= 1:
        report.fail(
            "admitted-tax",
            f"withholding credit claimed is {rupees(credit)} but certificates that "
            f"actually show income tax come to {rupees(claimable)}",
        )


def check_withholding_evidence(papers, report):
    """A credit is claimable only where the certificate shows an income tax line."""
    for row in papers.get("withholding") or []:
        if number(row.get("amount")) > 0 and not row.get("certificate_shows_income_tax"):
            source = row.get("source") or "an entry"
            report.fail(
                "withholding-evidence",
                f"{source}: certificate shows no income tax line — a motor vehicle "
                f"slip showing only MVT, or a bill showing only GST, carries no "
                f"claimable credit",
            )


def check_expense_basis(papers, report):
    """Personal expenses that were derived rather than measured are worth flagging."""
    if (papers.get("expenses") or {}).get("personal_basis") == "derived":
        report.note(
            "expenses",
            "personal expenses are derived rather than measured — say so to the "
            "taxpayer, since a figure chosen to close the reconciliation is exactly "
            "what an FBR query asks about",
        )


CHECKS = [
    check_types,
    check_reconciliation,
    check_property_floor,
    check_property_detail,
    check_foreign_assets,
    check_business_capital,
    check_admitted_tax,
    check_withholding_evidence,
    check_expense_basis,
]


def run(papers):
    report = Report()
    for check in CHECKS:
        check(papers, report)
    return report


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------


def _clean():
    """A minimal set of papers that reconciles exactly."""
    return {
        "tax_year": 2027,
        "prior_year": {
            "tax_year": 2026,
            "net_assets": 1_000_000,
            "properties": [{"id": "plot-1", "declared_value": 800_000}],
        },
        "income": {"export_154a_gross": 500_000},
        "other_inflows": [],
        "expenses": {"personal": 300_000, "personal_basis": "measured"},
        "withholding": [
            {"source": "bank", "amount": 1_250, "certificate_shows_income_tax": True}
        ],
        "assets": {
            "properties": [{
                "id": "plot-1", "value": 800_000,
                "land_area": 5, "land_area_unit": "Marla",
                "province": "Punjab", "district": "Lahore", "city": "Lahore",
                "plot_no": "12", "sector": "Block C",
            }],
            "vehicles": [],
            "accounts": [{"description": "current account", "value": 400_000}],
            "cash": 0,
            "other": [],
        },
        "foreign_assets": [],
        "liabilities": [],
        "balance_sheet": {"capital": 0, "other_assets": 0, "other_liabilities": 0},
        "tax": {"chargeable": 1_250, "withholding_credit": 1_250, "admitted": 0},
    }


def selftest():
    report = run(_clean())
    assert report.ok, report.failures

    def broken_with(mutate):
        papers = _clean()
        mutate(papers)
        return run(papers).failures

    def mutate_recon(p):
        p["assets"]["accounts"][0]["value"] = 900_000
    failures = broken_with(mutate_recon)
    assert any("unreconciled" in f for f in failures), failures

    def mutate_floor(p):
        p["assets"]["properties"][0]["value"] = 700_000
        p["assets"]["accounts"][0]["value"] = 500_000  # keep the reconciliation clean
    failures = broken_with(mutate_floor)
    assert any("property-floor" in f for f in failures), failures

    def mutate_detail(p):
        del p["assets"]["properties"][0]["land_area"]
    failures = broken_with(mutate_detail)
    assert any("land area" in f for f in failures), failures

    def mutate_capital(p):
        p["balance_sheet"]["capital"] = 100_000
    failures = broken_with(mutate_capital)
    assert any("business-capital" in f for f in failures), failures

    def mutate_cert(p):
        p["withholding"][0]["certificate_shows_income_tax"] = False
    failures = broken_with(mutate_cert)
    assert any("withholding-evidence" in f for f in failures), failures

    def mutate_admitted(p):
        p["tax"]["admitted"] = 5_000
    failures = broken_with(mutate_admitted)
    assert any("admitted-tax" in f for f in failures), failures

    def mutate_foreign(p):
        p["assets"]["accounts"].append(
            {"description": "Payoneer", "value": 0, "foreign": True})
    failures = broken_with(mutate_foreign)
    assert any("foreign-assets" in f for f in failures), failures

    def mutate_type(p):
        p["assets"]["cash"] = "50000"
    failures = broken_with(mutate_type)
    assert any("types" in f for f in failures), failures

    print("selftest: all checks pass")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()

    args = [a for a in argv[1:] if not a.startswith("-")]
    path = args[0] if args else os.path.expanduser("~/.pk-iris/working-papers.json")

    try:
        with open(path) as handle:
            papers = json.load(handle)
    except FileNotFoundError:
        print(f"no working papers at {path}")
        print("copy scripts/working-papers.example.json there, or pass a path")
        return 1
    except json.JSONDecodeError as error:
        print(f"{path} is not valid JSON: {error}")
        return 1

    report = run(papers)
    for line in report.failures:
        print(line)
    for line in report.notices:
        print(f"note — {line}")

    if report.ok:
        print("OK, with notices above" if report.notices else "OK")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

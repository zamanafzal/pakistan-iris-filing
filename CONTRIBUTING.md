# Contributing

The value of this plugin is accumulated, verified knowledge of how IRIS actually
behaves. That only stays true if corrections come from people who watched the
portal do something, rather than from people who read the form and inferred.

So there is one rule: **contribute what you observed, not what you expect.**

## The most useful contributions

In rough order of value:

1. **A validation error not yet in the playbook.** The exact message text, what
   actually caused it, and the fix that worked. These are the hardest thing to
   discover alone and the easiest to share.
2. **A field or code that moved.** FBR revises the form every tax year. If
   `field-map.md` sends someone to the wrong place, that is a bug.
3. **Coverage we don't have.** Salary returns, rental income, capital gains,
   AOP and company returns, slab-rate computation, provinces other than Punjab.
   `scope-and-limits.md` lists these as explicitly out of scope; moving one of
   them in — from having done it — is the biggest possible improvement.
4. **A tehsil or district missing from FBR's dropdowns**, and what you selected
   instead.

## How to contribute

Open an issue using one of the templates, or send a pull request.

If you are changing behaviour rather than fixing a typo, say in the PR:

- **which tax year** you observed it in
- **what you saw on screen** — not what you concluded
- whether you confirmed it by testing (entering a value, pressing CALCULATE,
  reading the result, then removing it) or by reading the form

## What does not belong here

- **Tax advice.** This documents portal mechanics and the reasoning behind one
  filing. It is not advice and must not start reading like it. Where a question
  is genuinely one of advice — how income should be characterised, whether a
  registration was required — the right change is to flag it as unresolved, not
  to answer it.
- **Anyone's personal data.** No NTNs, CNICs, account numbers, addresses or
  declared amounts, including your own. `your-profile.md` is a blank template
  and stays blank in the repo.
- **Confident guesses.** If you are not sure, say so in the text. "This was not
  verified" is useful. A wrong certainty costs someone money.

## Keeping scope honest

`skills/pk-iris-filing/references/scope-and-limits.md` is the contract with
users: it states what was verified and what was not. If you add coverage, move
the item out of the "not covered" list in the same change. If you add something
you did not verify, add it to the unverified list in the same change.

That file is the reason the plugin can be trusted where it does speak. Please
keep it accurate.

## Releasing

Maintainers: bump `version` in `.claude-plugin/plugin.json` on every release and
add a `CHANGELOG.md` entry. Pushing without a version bump means existing users
keep their cached copy and never receive the change.

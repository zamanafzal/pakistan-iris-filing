# Maintaining this plugin

This repo is both the plugin **and** its own marketplace, so one push ships a
release.

Published at <https://github.com/zamanafzal/pakistan-iris-filing>.

## Layout

```
pakistan-iris-filing/
├── .claude-plugin/
│   ├── plugin.json         the plugin manifest
│   └── marketplace.json    the marketplace manifest, source "./"
├── .github/ISSUE_TEMPLATE/ templates for error and field-map reports
├── agents/
├── skills/
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── PUBLISHING.md
```

## How people install it

```
/plugin install pakistan-iris-filing --marketplace zamanafzal/pakistan-iris-filing
```

Or from the terminal:

```bash
claude plugin marketplace add zamanafzal/pakistan-iris-filing
claude plugin install pakistan-iris-filing@pakistan-tax-tools
```

## Shipping a release

1. Make the changes.
2. **Bump `version` in `.claude-plugin/plugin.json`.** Push without bumping it
   and existing users keep their cached copy — the change never reaches them.
   This is the single easiest mistake to make here.
3. Add a `CHANGELOG.md` entry.
4. Validate:

   ```bash
   claude plugin validate --strict .
   ```

5. Commit and push.

Users update with:

```bash
claude plugin update pakistan-iris-filing@pakistan-tax-tools
```

Auto-update is off by default for third-party marketplaces; users can turn it
on per-marketplace in `/plugin` → Marketplaces.

Optionally tag the release:

```bash
claude plugin tag --push    # creates {name}--v{version}
```

## Getting listed publicly

To appear in Anthropic's **community marketplace**, so people find it without
knowing this repo exists:

- <https://platform.claude.com/plugins/submit> — individual authors
- <https://claude.ai/admin-settings/directory/submissions/plugins/new> — Team/Enterprise orgs

Listings pin to a specific commit, so submit after a release rather than
mid-change, and resubmit or update the listing when you ship something
significant. There is a delay between submission and appearing. The **official**
marketplace is partners-only and takes no public submissions.

## Things not to change casually

- **`"name": "pakistan-tax-tools"`** in `marketplace.json` is the marketplace's
  permanent identifier and part of every install command. Changing it breaks the
  update path for everyone who has already installed.
- **`"name": "pakistan-iris-filing"`** in `plugin.json` must keep matching the
  entry in `marketplace.json`, or the install fails.
- The skill and agent names (`pk-iris-filing`, `pk-iris-errors`,
  `pk-iris-agent`) appear in users' sessions; renaming them is a breaking
  change.

## Adding more plugins later

The marketplace can hold several. Add entries to the `plugins` array — a
relative `source` for something in this repo, or
`{"source": "github", "repo": "owner/name"}` for a separate one.

## Trust

There is no security review for third-party marketplaces; validation is
structural only. The trust model is yours, which is why the README and the
skills are explicit that this is not tax advice and why `scope-and-limits.md`
states plainly what was never verified. Keep that discipline — it is the whole
basis on which someone should be willing to let this near their tax return.

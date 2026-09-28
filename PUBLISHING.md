# Publishing this plugin

This repo is both the plugin **and** its own marketplace, so one push makes it
installable.

## Layout

```
pakistan-iris-filing/
├── .claude-plugin/
│   ├── plugin.json         the plugin manifest
│   └── marketplace.json    the marketplace manifest, source "./"
├── agents/
├── skills/
├── README.md
└── PUBLISHING.md
```

## Publish

```bash
git init
git add .
git commit -m "Pakistan IRIS filing plugin"
git branch -M main
git remote add origin https://github.com/zamanafzal/pakistan-iris-filing.git
git push -u origin main
```

Make the repo **public** so people can install without credentials.

Validate first if you have the CLI:

```bash
claude plugin validate --strict .
```

## How people install it

Add the marketplace once, then install:

```bash
claude plugin marketplace add zamanafzal/pakistan-iris-filing
claude plugin install pakistan-iris-filing@pakistan-tax-tools
```

Or, in a Claude session, both steps at once:

```
/plugin install pakistan-iris-filing --marketplace zamanafzal/pakistan-iris-filing
```

Once a marketplace is added, its plugins also show up in the desktop app's
plugin browser under **Add plugin**.

## Shipping updates

1. Edit the files.
2. **Bump `version` in `.claude-plugin/plugin.json`.** If you push without
   bumping it, users keep the cached copy and never see the change.
3. Commit and push.

Users update with:

```bash
claude plugin update pakistan-iris-filing@pakistan-tax-tools
```

Auto-update is off by default for third-party marketplaces; users can enable it
per-marketplace in `/plugin` → Marketplaces.

## Getting listed publicly

To appear in Anthropic's **community marketplace**, so people can find it
without knowing your repo, submit at:

- <https://platform.claude.com/plugins/submit> — individual authors
- <https://claude.ai/admin-settings/directory/submissions/plugins/new> — Team/Enterprise orgs

Listings are pinned to a specific commit, and there's a delay between
submission and appearing. The **official** marketplace is partners-only and
takes no public submissions.

## Notes

- `"name": "pakistan-tax-tools"` in `marketplace.json` is the marketplace's
  permanent identifier — it's part of every install command. Change it now if
  you want something else; changing it after people have installed will break
  their update path.
- The marketplace can hold more plugins later: add entries to the `plugins`
  array, either with a relative `source` for plugins in this repo or a
  `{"source": "github", "repo": "..."}` entry for separate repos.
- There is no security review for third-party marketplaces. Validation is
  structural only, and the trust model is yours — which is another reason the
  README is explicit that this is not tax advice.

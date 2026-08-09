# GitHub profile — what's applied, what's left

Applied on 2026-08-08 with the `gh` CLI (already installed at
`C:\Program Files\GitHub CLI\gh.exe`, authenticated as `Danny-397`):

- Topics on all six project repos + `Danny-397.github.io`
- Description and homepage on `Danny-397.github.io`
- Rewrote the `Tradeski` description (it used non-breaking hyphens, which
  render oddly and break search)
- Disabled the empty wikis on five repos
- Created `Danny-397/Danny-397` with the profile README

## Still to do — needs two scopes the current token lacks

The active token has `gist, read:org, repo, workflow`. These two need more:

```bash
gh auth refresh -h github.com -s user,delete_repo
```

That opens a browser to approve the added scopes. Then:

### 1. Profile bio and website link (needs `user`)

Right now the profile has no bio and no link to the portfolio — the two things
a visitor reads first.

```bash
gh api -X PATCH /user \
  -f bio="High-school CS researcher in NY. Six deployed systems; three report negative results." \
  -f blog="https://danny-397.github.io" \
  -f location="New York"
```

### 2. Delete the Gymnasium fork (needs `delete_repo`)

`Danny-397/Gymnasium` is a 386 MB fork of `Farama-Foundation/Gymnasium` with no
commits of your own. It is one of your public repos and carries someone else's
description, so it dilutes a profile that is otherwise all original work.

```bash
gh repo delete Danny-397/Gymnasium --yes
```

Forking again later is one click, and deleting the fork does not touch any local
clone or any dependency — nothing here imports from your fork.

# GitHub profile — what's applied, what's left

Applied on 2026-08-08 with the `gh` CLI (already installed at
`C:\Program Files\GitHub CLI\gh.exe`, authenticated as `Danny-397`):

- Topics on all six project repos + `Danny-397.github.io`
- Description and homepage on `Danny-397.github.io`
- Rewrote the `Tradeski` description (it used non-breaking hyphens, which
  render oddly and break search)
- Disabled the empty wikis on five repos
- Created `Danny-397/Danny-397` with the profile README

Reviewed again on 2026-09-13:

- Corrected the `RL-Chess-Engine` description, which claimed "millions of
  self-play games". The run was 1,000 games; the README and the technical
  report were already honest about that, so only the public description was
  overselling.
- **Reversed the advice to delete the Gymnasium fork — see below.** It is not
  a bare fork.

## Still to do

### 1. Pin the six projects (browser only — no API for this)

Nothing is pinned right now, so <https://github.com/Danny-397> lists repos in
GitHub's default order with the Gymnasium fork mixed in. Pinning is the single
highest-value change left: it is what a visitor sees before anything else.

There is no `gh` command and no GraphQL mutation for profile pins — GitHub has
never exposed one. Do it at <https://github.com/Danny-397> → **Customize your
pins**, in this order (strongest first, matching the portfolio):

1. `RL-for-Crypto-and-stocks-`
2. `Quantum-Safe-Scan`
3. `Alphaglyph`
4. `RL-Chess-Engine`
5. `Tradeski`
6. `neural-canvas`

### 2. Profile bio and website link (needs the `user` scope)

The profile still has **no bio and no website link** — the two things a visitor
reads first, and the only route from the profile to the portfolio.

The active token has `gist, read:org, repo, workflow`, so this needs:

```bash
gh auth refresh -h github.com -s user
```

That opens a browser to approve the added scope. Then:

```bash
gh api -X PATCH user \
  -f bio="High-school CS researcher in NY. Six deployed systems; three report negative results." \
  -f blog="https://danny-397.github.io" \
  -f location="New York"
```

(Note: `gh api user`, not `/user` — a leading slash gets rewritten to a
filesystem path by Git Bash on Windows and the call fails.)

Both fields can also be set by hand at
<https://github.com/settings/profile>, which needs no scope change at all.

## Do **not** delete the Gymnasium fork

An earlier version of this file recommended
`gh repo delete Danny-397/Gymnasium --yes` on the grounds that the fork has no
commits of your own and dilutes an otherwise all-original profile. **That is
wrong, and running it would destroy evidence.**

`Danny-397/Gymnasium` holds the branch `fix/async-autoreset-reward-dtype`, which
is the head of:

> **[Farama-Foundation/Gymnasium#1657](https://github.com/Farama-Foundation/Gymnasium/pull/1657)**
> — *Fix AsyncVectorEnv crash on autoreset with non-scalar rewards*
> (+85 / −3 across 2 files, opened 2026-08-02, closed 2026-08-04)

Deleting the fork would:

- delete the branch holding that work, and
- break every code link, diff and file view inside the public PR — the PR page
  survives, but the substance behind it does not render.

The PR was closed unmerged: a maintainer judged it
*"a bug with the environment and not with the AsyncVectorEnv implementation."*
That does not make it worthless — it is a real root-cause diagnosis against a
widely used library, and the collaboration essay in `College-Essays` is anchored
to it. An honest account of a contribution that a maintainer declined is
stronger evidence than no contribution at all.

The "no commits of your own" check that produced the original advice queried the
fork's **default branch**, where there genuinely are none. The work lives on a
side branch. Keep the fork.

If the fork's prominence is the worry, pinning the six projects (step 1) solves
it — pinned repositories display above the rest, and forks are labelled and sort
below.

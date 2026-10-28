# ACE3P documentation: where things stand and what is next

Written 2026-10-26 for Lixin Ge. Keep this file current; delete items as they are done.

## Current state

| Item | State |
|---|---|
| Site | https://slaclab.github.io/ace3p-docs/ , public, no login |
| Versions | `v2026.10` (alias `latest`, what the root shows) and `dev` (follows `main`) |
| Docs repo | `slaclab/ace3p-docs`, Public, license CC BY 4.0, `main` at 18c4d00 |
| Source repo | `slaclab/ace3p` master at 6e9858032 (fork `lge0303/ace3p` master identical), tag `v2026.10` |
| Content | 7 module guides with tutorials, Cubit chapter (own nav entry), Getting Started centred on Perlmutter + ThinLinc with S3DF as a SLAC-only note, tools page (Cubit, ParaView), command syntax for every module and acdtool, 13 source-generated keyword tables, Interfaces, Corrections log |
| Automation | Pushing a `v*` tag to the ACE3P repo regenerates keyword tables, copies `docs/user/` pages, opens a pull request here, requests auto-merge, and tags this repo after the merge |
| Secret | `ACE3P_DOCS_TOKEN` in the ACE3P repo is a classic token; a fine-grained token for slaclab is pending approval |

## Merged 2026-10-27

- ace3p-docs PR #2 (Getting started restructure) and PR #3 (Perlmutter tool paths: Cubit 16.16, ParaView 5.11.0 under `$CFS/ace3p/tools/`).
- ace3p PR #240 (Gun3P grid-region export) and PR #241 (`docs/user/` tree + release workflow). `lge0303/ace3p` master reset to upstream (6e9858032).

## Still open

- `grid-region-test-portable` (Gun3P test on Perlmutter) stays on the fork, not merged: its default data path is Lixin's local copy, unusable by others. Keep as a personal test. Decision 2026-10-27.
- Fork branches already merged and safe to delete on GitHub: `gun3p-grid-output-region`, `docs-user-tree`, `track3p-cpu-localization`, `openmp-files-io`.

Fork note: `lge0303/ace3p` master diverged from `slaclab/ace3p` master by one commit (ed977c672, now carried by `docs-user-tree`). After that PR merges, reset the fork's master to upstream: `git checkout master && git reset --hard upstream/master && git push --force-with-lease origin master`.

## To do in the GitHub web UI (only you can)

1. ~~Allow auto-merge, delete head branches~~ and 2. ~~`main` ruleset with `build` check~~: done (PRs #2 and #3 went through the ruleset).
3. **Dry run**: https://github.com/lge0303/ace3p/actions/workflows/docs-keywords.yml , *Run workflow*, leave `tag_docs` unticked. Expect a pull request "Release docs for ACE3P dev" in ace3p-docs, or "Nothing changed". If auto-merge is set up it merges by itself when the build is green.
4. **Close** the stale pull request "Keyword reference for ACE3P master" in ace3p-docs if still open; its branch is already deleted.
5. **About box** on the ace3p-docs repo page: gear icon, tick *Use your GitHub Pages website*.
6. **Token swap**, when slaclab approves the fine-grained token: paste it into `ACE3P_DOCS_TOKEN` and delete the classic token at https://github.com/settings/tokens .
7. **ace3p.slac.stanford.edu**: Mo was asked to point the Documentation link at the new address. Check it works.

## To ask colleagues

- **Module owners**: read their module pages and the matching entries on the Corrections page. Two items need a physics decision: the Track3P pillbox 2016-vs-2026 rerun difference, and the sign of the RF gun frequency shift (+47.4 kHz).
- **Developers**: document features in `docs/user/<module>/` of the ACE3P repo in the same pull request as the code, and add a line to `docs/user/CHANGES/next.md`. Rules are in `docs/user/README.md` there.

## How to make the next release

1. In the ACE3P repo, make sure `docs/user/CHANGES/next.md` lists the user-visible changes.
2. Tag and push: `git tag -a v2026.11 -m "ACE3P release 2026.11" && git push origin v2026.11`.
3. The workflow opens the pull request in ace3p-docs. Review it if you like; it merges on its own when the build passes, or merge it by hand.
4. The workflow tags ace3p-docs `v2026.11` within 30 minutes of the merge. If it did not, tag by hand: `git tag v2026.11 && git push origin v2026.11` in the ace3p-docs checkout.
5. The deploy publishes `v2026.11` and moves `latest` to it. Check the version dropdown on the site.
6. In the ACE3P repo, empty `docs/user/CHANGES/next.md` for the next cycle.

Binaries built from the tag print `ACE3P Release: v2026.11` in their start-up banner.

## Content still to convert (ask Claude when ready)

Sources are in `/sdf/group/rfar/ace3p/cw23/`.

- A3PI user guide (`a3pi/`, 22 pages) into `docs/interfaces/`.
- 2025 release notes (`news/ace3p-updates-032525.pdf`) as a proper Releases entry; the current v2026.10 notes are three lines.
- ParaView mechanical-mode animation scripts (`mmode/`).
- `presentations/ACE3P-Introduction.pptx` overview material for the home or Modules index.
- ACE3P GUI page in Interfaces when the colleagues' tool (v1.4.15) is stable.
- Point the workflow project's AI input generator at the command syntax pages and keyword tables instead of the PDFs.

## Local working copies on S3DF

| Path | What |
|---|---|
| `/sdf/group/rfar/lge/sdf/ace3p-docs` | docs repo, branch `main`, git identity set to Lixin Ge |
| `/sdf/group/rfar/lge/sdf/ace3p` | ACE3P, on branch `Track3p-GPU`, ahead of master |
| `/sdf/group/rfar/lge/ace3p-master-wt` | ACE3P upstream master (a641a8ea8, PR #240 merged); has a `build/` with the converters built |
| `/sdf/group/rfar/lge/ace3p-docs-user-wt` | ACE3P branch `docs-user-tree` (docs/user tree + workflow, for PR) |
| `/sdf/group/rfar/lge/ace3p-capabilities-cw23` | seminar branch: capability list, feature trees, decks under md/seminar |
| conda env `workflow-s3df` | has mkdocs, mike, pymupdf, python-pptx |

Build and preview locally:

```bash
source /sdf/group/rfar/software/conda/etc/profile.d/conda.sh && conda activate workflow-s3df
cd /sdf/group/rfar/lge/sdf/ace3p-docs
mkdocs build --strict          # what CI runs
mkdocs serve                   # http://127.0.0.1:8000
```

Regenerate the tables and developer pages by hand, from a checkout of the tagged ACE3P:

```bash
python tools/extract_keywords.py /path/to/ace3p --out docs/reference
python tools/assemble_source_docs.py /path/to/ace3p v2026.11 --site .
```

Note: `gh` on S3DF is broken; use plain `git`. Repository settings, secrets, and workflow runs are done in the browser.

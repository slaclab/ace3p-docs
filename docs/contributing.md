# Contributing

This documentation is maintained in the public `slaclab/ace3p-docs` repository and published at <https://slaclab.github.io/ace3p-docs/>. Anyone can read it and file issues; changes go through pull requests and are merged by the ACE3P team.

## Report a problem

Use the **Edit this page** icon at the top of any page to open the source on GitHub, or open an issue at <https://github.com/slaclab/ace3p-docs/issues>. Include the page URL and, for technical errors, the ACE3P version you observed the behavior with.

## Build locally

```bash
git clone git@github.com:slaclab/ace3p-docs.git
cd ace3p-docs
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Open <http://127.0.0.1:8000>. The site rebuilds on every save. Run `mkdocs build --strict` before pushing; it fails on broken links and missing pages, which is also what continuous integration checks.

## Structure

```
docs/
  index.md              home page
  getting-started/      system setup: S3DF, Perlmutter, local tools
  workflow/             the common pipeline: input format, mesh, batch jobs
  modules/              one guide per solver; omega3p/ has tutorials
  reference/            GENERATED keyword tables, do not edit by hand
  interfaces/           GUI, dashboard, workflow assistant
  assets/               images, grouped by module
tools/
  extract_keywords.py   generates docs/reference/*.md from ACE3P source
mkdocs.yml              navigation and theme
```

Add a new page by creating the Markdown file and adding it to `nav` in `mkdocs.yml`.

## Writing guidelines

- Write prose, not slide bullets. Each tutorial step says what to do, what to expect, and why.
- Show real input files from the examples directory, complete and runnable. Annotate with comments rather than paraphrasing.
- Use system-neutral commands in module guides. Put S3DF and Perlmutter specifics in Getting Started.
- Images go in `docs/assets/<module>/` and are referenced with relative paths.
- Do not commit credentials, personal home-directory paths, or unpublished results.

## Regenerating the reference pages

The reference tables come from the ACE3P source tree:

```bash
python tools/extract_keywords.py /path/to/ace3p --out docs/reference
```

The script scans for `Get(kvc, "Keyword", InitOrFallback<T>(default) ...)`, the `find`, `findSwitch`, and `findContainer` calls, and the string-compare parser of the rf post-processor. Point it at a checkout of the tagged ACE3P release so that the revision recorded in each page matches the tag.

## Documentation written with the code

ACE3P developers can document a feature in the same pull request that implements it, in `docs/user/` of the ACE3P source repository (see its `README.md`). Two kinds of page are picked up:

- `docs/user/<module>/<topic>.md` appears here under *Modules > (module) > Notes from the source tree*, carrying a banner that names its origin.
- `docs/user/CHANGES/<tag>.md` or `CHANGES/next.md` becomes the release-notes page under *Releases*.

`tools/assemble_source_docs.py` does the copying and rewrites the generated part of the navigation. Pages copied this way are owned by the ACE3P repository: edit them there, not here, or the next release overwrites the change.

## What happens at an ACE3P release

The ACE3P source repository has a workflow, `.github/workflows/docs-keywords.yml`, that runs when a release tag `v*` is pushed:

1. Regenerates the keyword tables and copies the developer pages.
2. Builds the site strictly, so a broken link in a developer page fails before anything is published.
3. Opens a pull request here on branch `release-docs/<tag>` and requests auto-merge.
4. When the pull request has merged, tags this repository `<tag>`. The deploy workflow then publishes that version and points `latest` at it.

For this to run unattended, the ACE3P repository needs the secret `ACE3P_DOCS_TOKEN` (a token with contents and pull-request write access here), and this repository needs *Allow auto-merge* enabled in Settings and a branch ruleset on `main` requiring the `build` check. Without auto-merge the pull request waits for a maintainer; the workflow still tags once it is merged within 30 minutes, and otherwise the tag is made by hand as below.

Hand-written guides and tutorials are never changed by this workflow. Only `docs/reference/*.md`, `docs/modules/*/from-source/`, `docs/releases/`, and the generated block of `mkdocs.yml` are.

## Versioning

Documentation versions are published with [mike](https://github.com/jimporter/mike). Pushing to `main` updates the `dev` version. Pushing a tag `vX.Y` publishes that version and points the `latest` alias at it:

```bash
git tag v2026.10
git push origin v2026.10
```

Tag the documentation with the same version string as the ACE3P release it describes. The ACE3P binaries print that string in their start-up banner as `ACE3P Release: v2026.10`, so a user can match a run to its documentation version.

# Contributing

This documentation is maintained in the `slaclab/ace3p-docs` repository. Readers can file issues; changes go through pull requests.

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
python tools/extract_keywords.py /path/to/ace3p --out docs/reference --modules omega3p emfem solver
```

The script scans for `Get(kvc, "Keyword", InitOrFallback<T>(default) ...)` and `find("Keyword")` calls. When the ACE3P source repository tags a release, a continuous-integration job there will run this script and open a pull request here with the updated pages. Until that job exists, run the script by hand before tagging a documentation version.

## Versioning

Documentation versions are published with [mike](https://github.com/jimporter/mike). Pushing to `main` updates the `dev` version. Pushing a tag `vX.Y` publishes that version and points the `latest` alias at it:

```bash
git tag v2026.10
git push origin v2026.10
```

Tag the documentation with the same version string as the ACE3P release it describes.

# ACE3P Documentation

User documentation for **ACE3P**, SLAC's parallel finite-element electromagnetic simulation suite: getting started on S3DF and NERSC Perlmutter, the simulation workflow, per-module user guides and tutorials, and input-keyword reference tables generated from the ACE3P source.

**Published site:** https://slaclab.github.io/ace3p-docs/

Built with [MkDocs](https://www.mkdocs.org/) and the [Material](https://squidfunk.github.io/mkdocs-material/) theme. Versioned with [mike](https://github.com/jimporter/mike) so each ACE3P release has matching documentation.

## Build locally

```bash
pip install -r requirements.txt
mkdocs serve            # live preview at http://127.0.0.1:8000
mkdocs build --strict   # what CI runs
```

## Regenerate the keyword reference

```bash
python tools/extract_keywords.py /path/to/ace3p --out docs/reference
```

## Contributing

See [docs/contributing.md](docs/contributing.md). Issues and pull requests are welcome. The `main` branch is protected; changes land through pull requests.

## Origin

This site supersedes the CW23 workshop slide decks previously distributed as PDFs on SLAC Confluence.

Copyright SLAC National Accelerator Laboratory. The documentation text and images are licensed under [CC BY 4.0](LICENSE). ACE3P itself is not part of this repository and is distributed under its own terms.

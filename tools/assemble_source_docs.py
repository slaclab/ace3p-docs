#!/usr/bin/env python3
"""Bring developer-written documentation from the ACE3P source tree into this site.

ACE3P developers document features next to the code, in ``docs/user/`` of the
ACE3P repository::

    docs/user/README.md                 how to write these pages (not copied)
    docs/user/CHANGES/v2026.11.md       release notes for a tag, or
    docs/user/CHANGES/next.md           notes for the upcoming release
    docs/user/<module>/<topic>.md       one page per feature, <module> is one of
                                        omega3p s3p t3p pic3p track3p tem3p gun3p acdtool cubit
    docs/user/<module>/img/*.png        images referenced by those pages

This script copies them into the documentation site::

    docs/modules/<module>/from-source/<topic>.md    plus an index.md listing them
    docs/releases/<tag>.md                           plus an index.md listing all releases

and rewrites the block of ``mkdocs.yml`` between ``# BEGIN generated nav`` and
``# END generated nav`` so every copied page is reachable from the navigation.
Files whose name starts with an underscore are templates and are skipped.

Usage:
    python tools/assemble_source_docs.py /path/to/ace3p vX.Y [--site .]
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from datetime import date

MODULES = ["omega3p", "s3p", "t3p", "pic3p", "track3p", "tem3p", "gun3p", "acdtool", "cubit"]
MODULE_TITLES = {"omega3p": "Omega3P", "s3p": "S3P", "t3p": "T3P", "pic3p": "Pic3P",
                 "track3p": "Track3P", "tem3p": "TEM3P", "gun3p": "Gun3P",
                 "acdtool": "acdtool", "cubit": "Cubit"}
BEGIN = "      # BEGIN generated nav"
END = "      # END generated nav"


def title_of(path: str, fallback: str) -> str:
    with open(path, errors="ignore") as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    return fallback.replace("-", " ").replace("_", " ").capitalize()


def banner(src_rel: str, tag: str) -> str:
    return (f'!!! info "From the ACE3P source tree"\n'
            f'    Written by the ACE3P developers in `{src_rel}` and copied here for release `{tag}` '
            f'on {date.today().isoformat()}. Propose changes in the ACE3P repository, not on this page.\n\n')


def copy_page(src: str, dst: str, src_rel: str, tag: str) -> None:
    text = open(src, errors="ignore").read()
    # Insert the banner after the first heading so the page title stays first.
    m = re.match(r"(# [^\n]*\n)", text)
    if m:
        text = text[: m.end()] + "\n" + banner(src_rel, tag) + text[m.end():].lstrip("\n")
    else:
        text = banner(src_rel, tag) + text
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "w").write(text)


def assemble_modules(ace3p: str, site: str, tag: str) -> dict[str, list[tuple[str, str]]]:
    """Copy module fragments. Returns {module: [(title, relpath), ...]}."""
    found: dict[str, list[tuple[str, str]]] = {}
    for mod in MODULES:
        src_dir = os.path.join(ace3p, "docs", "user", mod)
        dst_dir = os.path.join(site, "docs", "modules", mod, "from-source")
        if os.path.isdir(dst_dir):
            shutil.rmtree(dst_dir)
        if not os.path.isdir(src_dir):
            continue
        pages = sorted(f for f in os.listdir(src_dir)
                       if f.endswith(".md") and not f.startswith("_") and f != "index.md")
        if not pages:
            continue
        os.makedirs(dst_dir, exist_ok=True)
        entries = []
        for fn in pages:
            src_rel = f"docs/user/{mod}/{fn}"
            copy_page(os.path.join(src_dir, fn), os.path.join(dst_dir, fn), src_rel, tag)
            entries.append((title_of(os.path.join(src_dir, fn), fn[:-3]), f"modules/{mod}/from-source/{fn}"))
        img = os.path.join(src_dir, "img")
        if os.path.isdir(img):
            shutil.copytree(img, os.path.join(dst_dir, "img"))
        index = [f"# {MODULE_TITLES[mod]}: notes from the source tree", "",
                 f"Pages written by the ACE3P developers alongside the code, copied from `docs/user/{mod}/` "
                 f"in the ACE3P repository at release `{tag}`. They describe features as implemented and "
                 f"complement the [{MODULE_TITLES[mod]} guide](../index.md).", ""]
        index += [f"- [{t}]({os.path.basename(p)})" for t, p in entries]
        open(os.path.join(dst_dir, "index.md"), "w").write("\n".join(index) + "\n")
        found[mod] = entries
    return found


def assemble_releases(ace3p: str, site: str, tag: str) -> list[str]:
    """Copy release notes for this tag. Returns all release tags present, newest first."""
    rel_dir = os.path.join(site, "docs", "releases")
    os.makedirs(rel_dir, exist_ok=True)
    changes = os.path.join(ace3p, "docs", "user", "CHANGES")
    src = None
    for cand in (f"{tag}.md", "next.md"):
        if os.path.isfile(os.path.join(changes, cand)):
            src = os.path.join(changes, cand)
            break
    if src and re.match(r"v[\w.-]+$", tag):
        dst = os.path.join(rel_dir, f"{tag}.md")
        text = open(src, errors="ignore").read()
        if not text.lstrip().startswith("# "):
            text = f"# ACE3P {tag}\n\n" + text
        text = re.sub(r"^(# [^\n]*\n)", lambda m: m.group(1) + "\n" + banner(
            os.path.relpath(src, ace3p), tag), text, count=1)
        open(dst, "w").write(text)
    tags = sorted((f[:-3] for f in os.listdir(rel_dir) if f.endswith(".md") and f != "index.md"),
                  key=version_key, reverse=True)
    index = ["# Releases", "",
             "Release notes written by the ACE3P developers, one page per tagged release. "
             "The keyword tables and command syntax pages of each documentation version describe the same release; "
             "use the version selector in the header to switch.", ""]
    index += [f"- [ACE3P {t}]({t}.md)" for t in tags]
    open(os.path.join(rel_dir, "index.md"), "w").write("\n".join(index) + "\n")
    return tags


def version_key(v: str):
    return [int(x) if x.isdigit() else x for x in re.split(r"[.\-]", v.lstrip("v"))]


def rewrite_nav(site: str, modules: dict, releases: list[str]) -> None:
    """Rewrite the generated block of mkdocs.yml.

    The block lives at the end of the top-level nav, indented like a top-level entry.
    It holds the Releases section. Module from-source indexes are attached under each
    module in the hand-written nav by a one-line marker, see insert_module_entries().
    """
    path = os.path.join(site, "mkdocs.yml")
    text = open(path).read()
    block = ["  # BEGIN generated nav (tools/assemble_source_docs.py; do not edit by hand)",
             "  - Releases:",
             "      - releases/index.md"]
    block += [f"      - ACE3P {t}: releases/{t}.md" for t in releases]
    block.append("  # END generated nav")
    new = "\n".join(block)
    if "# BEGIN generated nav" in text:
        text = re.sub(r"  # BEGIN generated nav.*?  # END generated nav", new, text, flags=re.S)
    else:
        # Place before the Contributing entry.
        text = text.replace("  - Contributing: contributing.md", new + "\n  - Contributing: contributing.md", 1)
    text = insert_module_entries(text, modules)
    open(path, "w").write(text)


def insert_module_entries(text: str, modules: dict) -> str:
    """Add or remove 'Notes from the source tree' under each module in the nav."""
    for mod in MODULES:
        marker = f"          - Notes from the source tree: modules/{mod}/from-source/index.md\n"
        text = text.replace(marker, "")
        if mod in modules:
            # Insert right after the module's index line.
            anchor = f"          - modules/{mod}/index.md\n"
            if anchor in text:
                text = text.replace(anchor, anchor + marker, 1)
            else:
                print(f"warning: no nav anchor for {mod}; add '{marker.strip()}' by hand", file=sys.stderr)
    return text


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ace3p", help="path to the ACE3P source checkout")
    ap.add_argument("tag", help="release tag being documented, e.g. v2026.11, or 'dev'")
    ap.add_argument("--site", default=".", help="path to the ace3p-docs checkout")
    a = ap.parse_args()
    modules = assemble_modules(a.ace3p, a.site, a.tag)
    releases = assemble_releases(a.ace3p, a.site, a.tag)
    rewrite_nav(a.site, modules, releases)
    for mod, entries in modules.items():
        print(f"{mod}: {len(entries)} page(s) from source")
    print(f"releases: {', '.join(releases) or 'none'}")


if __name__ == "__main__":
    main()

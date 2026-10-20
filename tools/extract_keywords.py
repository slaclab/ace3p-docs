#!/usr/bin/env python3
"""Generate input-keyword reference pages from the ACE3P C++ source tree.

ACE3P solvers read input-file keywords through a small family of calls on a
key-value container (``LuaKeyValueContainer``)::

    Get(kvc, "NumEigenvalues", InitOrFallback<int>(1) or quiet);   // typed, with default
    if (!kvc.find("MaxImpacts", m_maxImpacts)) { m_maxImpacts = 50; } // default assigned after
    if (!kvc.find("JobName", name)) { kvcError(); }                  // required
    kvc.find("StartPoint", 0, x);                                    // indexed (list) value
    kvc.findSwitch("Toggle");                                        // on/off switch
    kvc.findContainer("Boundary", bdKvc);                            // a block

This script scans the source for those calls and emits one Markdown page per
module with keyword, type, default, presence, and the source location that
reads it.  Names and defaults always come from the code so they cannot drift;
descriptions live in the hand-written module guides.

Usage:
    python tools/extract_keywords.py /path/to/ace3p [--out docs/reference] [--modules ...]
"""
from __future__ import annotations

import argparse
import collections
import os
import re
import subprocess
from datetime import date

MODULES = {
    "omega3p": "Omega3P",
    "omega3p/postprocess": "acdtool postprocess rf (omega3p/postprocess)",
    "s3p": "S3P",
    "tfe3p": "T3P and Pic3P (tfe3p)",
    "multipacting": "Track3P (multipacting)",
    "tem3p": "TEM3P",
    "gun3p": "Gun3P",
    "tools": "acdtool (tools)",
    "emfem": "Shared electromagnetic FEM (emfem)",
    "solver": "Eigensolver and linear-solver options (solver)",
    "excitation": "Excitation pulses (excitation)",
    "waveguide": "Waveguide ports (waveguide)",
    "slacsupport": "Bunch shapes and shared utilities (slacsupport)",
    "kly3p": "Kly3P",
}
DEFAULT_MODULES = ["omega3p", "s3p", "tfe3p", "multipacting", "tem3p", "gun3p", "tools",
                   "omega3p/postprocess", "emfem", "solver", "excitation", "waveguide", "slacsupport"]

# Directories inside a module that hold tests, inputs, or unrelated codes.
SKIP_DIRS = re.compile(r"^(regression.*|test.*|testsuites.*|posinst|docs?|mp-postprocess|MPPostprocess|scripts|poisson2d)$")

KEY = r'"([^"\\]+)"'
VAR = r'[\w.\[\]>-]+'
OBJ = r'([\w]+(?:\.\w+|->\w+)*)'  # kvc, m_kvc, domainkvc, this->m_input ...

PAT_GET = re.compile(
    rf'Get\(\s*{OBJ}\s*,\s*{KEY}(?:\s*,\s*{KEY})?\s*,\s*([^;]*?)\)\s*;', re.S)
PAT_DEFAULT = re.compile(
    r'InitOrFallback(?:<\s*([A-Za-z:_<> ]+?)\s*>)?\s*\(\s*([^()]*?(?:\([^()]*\))?[^()]*?)\s*\)')
PAT_SEV = re.compile(r'\bor\s+(quiet|warn|die)\b')
SEVERITY = {"quiet": "optional", "warn": "optional (warns)", "die": "required"}

# if (!kvc.find("Key", var)) { var = default; }   or   ... ) var = default;
PAT_FIND_DEFAULT = re.compile(
    rf'if\s*\(\s*!\s*{OBJ}(?:\.|->)find\(\s*{KEY}\s*,\s*({VAR})\s*\)\s*\)\s*\{{?\s*\3\s*=\s*([^;]+);', re.S)
# if (!kvc.find("Key", var)) { kvcError(); }   or   ... ) kvcError(...)
PAT_FIND_REQUIRED = re.compile(
    rf'if\s*\(\s*!\s*{OBJ}(?:\.|->)find\(\s*{KEY}\s*,[^;{{]*\)\s*\)\s*\{{?\s*(?:kvcError|throw|SLAC_Error|abort|exit)', re.S)
PAT_FIND_INDEXED = re.compile(rf'{OBJ}(?:\.|->)find\(\s*{KEY}\s*,\s*\d+\s*,')
PAT_FIND = re.compile(rf'{OBJ}(?:\.|->)find\(\s*{KEY}')
PAT_SWITCH = re.compile(rf'{OBJ}(?:\.|->)findSwitch(?:Off)?\(\s*{KEY}')
PAT_CONTAINER = re.compile(rf'{OBJ}(?:\.|->)findContainer\(\s*{KEY}')
# Block-variable binding: findContainer("Domain", domainkvc) -> domainkvc reads keys of block Domain
PAT_BIND = re.compile(rf'findContainer\(\s*{KEY}\s*,\s*(?:\d+\s*,\s*)?&?\s*({VAR})\s*\)')
PAT_BIND_GET = re.compile(rf'\b({VAR})\s*=\s*Get\(\s*{OBJ}\s*,\s*{KEY}\s*\)')
# rf post-processor input parser: strncmp(token, "RoverQ", 6) == 0
PAT_STRNCMP = re.compile(rf'strn?cmp\(\s*{VAR}\s*,\s*{KEY}(?:\s*,\s*\d+)?\s*\)\s*==\s*0')


def infer_type(explicit: str | None, default: str) -> str:
    if explicit:
        return explicit.replace("std::", "")
    if not default:
        return ""
    if re.fullmatch(r"-?\d+", default):
        return "int"
    if re.fullmatch(r"-?[\d.]+(e[-+]?\d+)?", default):
        return "double"
    if default.startswith('"') or "string(" in default:
        return "string"
    if default in ("true", "false"):
        return "bool"
    return ""


def container_hint(obj: str, bindings: dict | None = None) -> str:
    """Turn the container variable name into a block name.

    Uses the findContainer("Block", var) bindings seen in the same file first, then
    falls back to a heuristic on the variable name: domainkvc -> Domain."""
    name = obj.split("->")[-1].split(".")[-1]
    base = re.sub(r"^m_", "", name)
    if bindings:
        for cand in (name, base, "m_" + base):
            if cand in bindings:
                return bindings[cand]
    name = base
    name = re.sub(r"(kvc|Kvc|KVC)$", "", name)
    name = re.sub(r"^(kvc|Kvc|KVC)_?", "", name)
    KNOWN = {"bd": "Boundary", "vm": "VolumeMaterial", "ts": "TimeStepping", "mon": "Monitor",
             "pic": "Loading.Particles", "picbunch": "Loading.Particles.Distribution",
             "picmon": "Loading.Particles.Monitors", "port": "Port", "time": "TimeStepping",
             "em": "RFHeating", "ward": "Ward", "domain": "Domain", "emitter": "Emitter",
             "material": "Material", "mode": "Mode", "load": "Loading", "loadinfo": "LoadingInfo"}
    if name.lower() in KNOWN:
        return KNOWN[name.lower()]
    # Short or generic variable names carry no block information.
    if len(name) <= 2 or re.fullmatch(r"(input|problem|child|temp|tmp|the|pp_?|p|l|e|dr|es|te|ns|qb|t|"
                                      r"templine|tempstring|_|m|global|state|tau3p_startup)", name, flags=re.I):
        return ""
    return name[0].upper() + name[1:]


def clean_default(d: str) -> str:
    d = " ".join(d.split())
    d = re.sub(r"^std::string\((.*)\)$", r"\1", d)
    d = re.sub(r"^string\((.*)\)$", r"\1", d)
    return d


def scan(root: str, module: str):
    rows: dict[str, dict] = {}

    bindings_holder: list[dict] = [{}]

    def add(key, *, obj="", alias="", typ="", default="", presence="", loc="", container=None):
        if key.startswith(".") or not key.strip():
            return
        row = dict(key=key, alias=alias, type=typ, default=default, presence=presence,
                   loc=loc, container=container if container is not None else container_hint(obj, bindings_holder[0]))
        old = rows.get(key)
        if old is None:
            rows[key] = row
            return
        # Prefer the row that carries a default or a presence verdict.
        score = lambda r: (bool(r["default"]), bool(r["presence"]), bool(r["type"]))
        if score(row) > score(old):
            row["container"] = row["container"] or old["container"]
            rows[key] = row
        elif not old["container"]:
            old["container"] = row["container"]

    for dp, dirs, files in os.walk(os.path.join(root, module)):
        # Sorted traversal keeps the output identical across filesystems, so a
        # regeneration on another machine does not churn the "Read in" column.
        dirs[:] = sorted(d for d in dirs if not SKIP_DIRS.match(d))
        if module == "omega3p":
            dirs[:] = [d for d in dirs if d != "postprocess"]
        for fn in sorted(files):
            if not fn.endswith((".C", ".cc", ".cpp", ".h")):
                continue
            path = os.path.join(dp, fn)
            try:
                src = open(path, errors="ignore").read()
            except OSError:
                continue
            rel = os.path.relpath(path, root)
            lineno = lambda m: f"{rel}:{src[: m.start()].count(chr(10)) + 1}"

            bindings = bindings_holder[0] = {}
            for m in PAT_BIND.finditer(src):
                block, var = m.groups()
                bindings.setdefault(var.split("->")[-1].split(".")[-1], block.rsplit(".", 1)[-1])
            for m in PAT_BIND_GET.finditer(src):
                var, _, block = m.groups()
                bindings.setdefault(var.split("->")[-1].split(".")[-1], block.rsplit(".", 1)[-1])
            for m in PAT_STRNCMP.finditer(src):
                add(m.group(1), loc=lineno(m), container=os.path.splitext(fn)[0])

            for m in PAT_GET.finditer(src):
                obj, key, alias, spec = m.groups()
                d = PAT_DEFAULT.search(spec)
                s = PAT_SEV.search(spec)
                default = clean_default(d.group(2)) if d else ""
                add(key, obj=obj, alias=alias or "", typ=infer_type(d.group(1) if d else None, default),
                    default=default, presence=SEVERITY.get(s.group(1), "") if s else "", loc=lineno(m))
            for m in PAT_FIND_DEFAULT.finditer(src):
                obj, key, _, default = m.groups()
                default = clean_default(default)
                add(key, obj=obj, typ=infer_type(None, default), default=default,
                    presence="optional", loc=lineno(m))
            for m in PAT_FIND_REQUIRED.finditer(src):
                obj, key = m.groups()
                add(key, obj=obj, presence="required", loc=lineno(m))
            for m in PAT_FIND_INDEXED.finditer(src):
                obj, key = m.groups()
                add(key, obj=obj, typ="list", loc=lineno(m))
            for m in PAT_SWITCH.finditer(src):
                obj, key = m.groups()
                add(key, obj=obj, typ="switch (on/off)", loc=lineno(m))
            for m in PAT_CONTAINER.finditer(src):
                obj, key = m.groups()
                add(key, obj=obj, typ="block", loc=lineno(m))
            for m in PAT_FIND.finditer(src):
                obj, key = m.groups()
                add(key, obj=obj, loc=lineno(m))
    return sorted(rows.values(), key=lambda r: (r["container"].lower(), r["key"].lower()))


def git_describe(root: str) -> str:
    for cmd in (["describe", "--tags", "--exact-match"], ["describe", "--tags", "--always"]):
        try:
            tag = subprocess.run(["git", "-C", root, *cmd], capture_output=True, text=True,
                                 check=True).stdout.strip()
            d = subprocess.run(["git", "-C", root, "log", "-1", "--format=%ad", "--date=short"],
                               capture_output=True, text=True, check=True).stdout.strip()
            return f"{tag} {d}"
        except Exception:
            continue
    return "unknown"


def render(module: str, title: str, rows, source_rev: str) -> str:
    groups = collections.defaultdict(list)
    for r in rows:
        if "." in r["key"]:
            section = r["key"].rsplit(".", 1)[0]
        else:
            section = r["container"] or "(top level or unspecified block)"
        groups[section].append(r)
    out = [
        f"# {title} keyword reference",
        "",
        "!!! info \"Auto-generated\"",
        f"    This page was generated from the ACE3P source tree by `tools/extract_keywords.py` "
        f"on {date.today().isoformat()} (source revision `{source_rev}`). "
        "Keyword names, types, and defaults are taken directly from the code. "
        "Descriptions live in the module user guides and the command syntax pages. Do not edit this file by hand.",
        "",
        f"**{len(rows)} keywords found.** Sections are the block named in a dotted key "
        "(`EigenSolver.Tolerance`) or, for bare keys, the name of the container variable the code reads "
        "them from (`domainkvc` becomes *Domain*). A blank *Default* means the code reads the keyword "
        "with `find()` and the fallback is not a literal, or the keyword is a block or switch. "
        "*Presence* `required` means the code aborts when the key is absent.",
        "",
    ]
    for section in sorted(groups, key=lambda s: (s.startswith("("), s.lower())):
        out += [f"## {section}", "", "| Keyword | Type | Default | Presence | Read in |",
                "|---|---|---|---|---|"]
        for r in groups[section]:
            name = r["key"].rsplit(".", 1)[-1] if "." in r["key"] else r["key"]
            alias = f" (alias `{r['alias']}`)" if r["alias"] else ""
            default = f"`{r['default']}`" if r["default"] else ""
            typ = f"`{r['type']}`" if r["type"] else ""
            out.append(f"| `{name}`{alias} | {typ} | {default} | {r['presence']} | `{r['loc']}` |")
        out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="path to ACE3P source checkout")
    ap.add_argument("--out", default="docs/reference")
    ap.add_argument("--modules", nargs="*", default=DEFAULT_MODULES)
    args = ap.parse_args()
    rev = git_describe(args.source)
    os.makedirs(args.out, exist_ok=True)
    for mod in args.modules:
        rows = scan(args.source, mod)
        page = render(mod, MODULES.get(mod, mod), rows, rev)
        dest = os.path.join(args.out, f"{mod.replace('/', '-')}.md")
        open(dest, "w").write(page)
        print(f"{dest}: {len(rows)} keywords")


if __name__ == "__main__":
    main()

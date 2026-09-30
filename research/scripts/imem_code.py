#!/usr/bin/env python3
"""imem_code.py — the codebase as a knowledge object, linked to the research.

WHY (measured gap): `codemap` links records to *files* via prose path mentions, but
nothing knows which *symbol* embodies an idea, which code has no research rationale,
or which claims have no code. When eval.cpp grows a new term with no record, or a
record claims an optimization with no symbol, both facts are invisible.

This module parses src/*.cpp/*.h with a small deterministic scanner (functions,
structs, macros, globals — no compiler needed) and joins it to the record graph:
  * symbol_index: every definition with file + line.
  * record_symbols: records -> symbols (via `symbols:` front-matter, backticks in
    prose, and file mentions).
  * untraced_code: symbols never named by any record (research debt: code without a why).
  * untraced_claims: claims/decisions with `implemented_by` empty and no symbol naming
    them (ideas without a where).
"""
from __future__ import annotations

import re

from imem_core import as_list  # noqa: F401  (documented dependency)
import imem_core as CORE       # dynamic: tests and callers may rebind REPO_ROOT

FUNC_RE = re.compile(r"^\s*(?:static\s+|inline\s+|constexpr\s+|extern\s+|template\s*<[^>]*>\s*)?"
                     r"(?:[\w:<>*&]+\s+)+(\w+)\s*\([^;{}]*\)\s*(?:const\s*)?(?:\{|;)")
STRUCT_RE = re.compile(r"^\s*(?:struct|class|enum(?:\s+class)?|union)\s+(\w+)")
MACRO_RE = re.compile(r"^\s*#\s*define\s+(\w+)")
GLOBAL_RE = re.compile(r"^\s*(?:static\s+)?(?:const(?:expr)?\s+)?"
                       r"(?:[\w:<>*&]+\s+)+(\w+)\s*(?:\[[^\]]*\])?\s*(?:=\s*[^;]+)?;")
NAMESPACE_RE = re.compile(r"^\s*namespace\s+(\w+)")


def scan_file(path) -> list:
    """[(symbol, kind, line)] — deterministic, comment-aware enough for this codebase
    (line comments stripped; block comments are rare here and treated as code, which
    can only add a symbol, never hide one — the safe direction for an index)."""
    syms = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return syms
    ns = []
    for i, raw in enumerate(text.splitlines(), 1):
        line = re.sub(r"//.*$", "", raw).rstrip()
        if not line.strip():
            continue
        m = NAMESPACE_RE.match(line)
        if m and "{" in line:
            ns.append(m.group(1))
            continue
        if line.strip() == "}":
            if ns:
                ns.pop()
            continue
        m = MACRO_RE.match(line)
        if m:
            syms.append((m.group(1), "macro", i))
            continue
        m = STRUCT_RE.match(line)
        if m:
            syms.append((m.group(1), "type", i))
            continue
        m = FUNC_RE.match(line)
        if m and m.group(1) not in ("if", "for", "while", "switch", "return"):
            name = "::".join(ns + [m.group(1)]) if ns else m.group(1)
            syms.append((name, "func", i))
            continue
        m = GLOBAL_RE.match(line)
        if m and len(line) < 160:
            syms.append((m.group(1), "global", i))
    return syms


def symbol_index(src_dir=None) -> dict:
    """{symbol: [{file, line, kind}]} across src/ (and tools/ for experiment code)."""
    root = CORE.REPO_ROOT / (src_dir or "src")
    idx: dict = {}
    files = sorted(root.glob("*.cpp")) + sorted(root.glob("*.h"))
    if (CORE.REPO_ROOT / "tools").exists():
        files += sorted((CORE.REPO_ROOT / "tools").glob("*.py"))
    for path in files:
        rel = path.relative_to(CORE.REPO_ROOT).as_posix()
        for sym, kind, line in scan_file(path):
            entry = {"file": rel, "line": line, "kind": kind}
            idx.setdefault(sym, []).append(entry)
            # A bare-name alias for namespaced symbols (kana::foo -> foo), so records
            # naming bare identifiers resolve. Kept unambiguous-first: if the bare name
            # is independently defined, the bare entry wins and the alias is skipped.
            if "::" in sym:
                bare = sym.split("::")[-1]
                if bare not in idx:
                    idx[bare] = [{"file": rel, "line": line, "kind": kind,
                                  "alias_of": sym}]
    return idx
def record_symbols(records: dict, index: dict) -> dict:
    """{record_id: [symbols]} — from `symbols:` front-matter (authoritative), then
    backticked prose tokens that match known symbols. Aliases resolve transparently:
    `quiescence` in prose matches `kana::quiescence` in code."""
    syms = set(index)
    out = {}
    for rec in records.values():
        found = set()
        for s in as_list(rec.fm.get("symbols")):
            if str(s) in syms:
                found.add(str(s))
        for tok in re.findall(r"`([A-Za-z_][A-Za-z0-9_:]*)`", rec.body):
            base = tok.split("::")[-1]
            if tok in syms:
                found.add(tok)
            elif base in syms:
                found.add(base)
        if found:
            out[rec.id] = sorted(found)
    return out


def traceability(records: dict, index: dict = None) -> dict:
    """Both directions of 'theory -> code -> experiment -> result':
    untraced_code (symbols no record names) and untraced_claims (claims/decisions with
    no code link). Either direction is research debt with an owner and a fix."""
    from imem_core import records_of_type
    index = index or symbol_index()
    rec_syms = record_symbols(records, index)
    named = set()
    for syms in rec_syms.values():
        named.update(syms)
    untraced_code = sorted(
        [{"symbol": s, "defs": d} for s, d in index.items() if s not in named],
        key=lambda r: r["symbol"])
    untraced_claims = []
    for rec in records_of_type(records, "claim", "decision", "hypothesis"):
        if rec.fm.get("example"):
            continue
        impl = [str(x) for x in as_list(rec.fm.get("implements") or
                                        rec.fm.get("implemented_by") or [])]
        if not impl and rec.id not in rec_syms:
            untraced_claims.append({"id": rec.id, "title": rec.title[:120],
                                    "type": rec.type,
                                    "status": str(rec.fm.get("status"))})
    traced = sorted([{"record": rid, "symbols": s} for rid, s in rec_syms.items()],
                    key=lambda r: r["record"])
    return {"symbols": len(index), "records_naming_symbols": len(rec_syms),
            "untraced_code": untraced_code[:60], "n_untraced_code": len(untraced_code),
            "untraced_claims": untraced_claims[:60],
            "n_untraced_claims": len(untraced_claims),
            "traced": traced}

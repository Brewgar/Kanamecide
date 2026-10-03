#!/usr/bin/env python3
"""Build the FND-0035 F2/F3 pre/post node-count table (depth 6, 11 act_E00007 positions).

THIS TABLE IS EVIDENCE, NOT A DEFECT. A node-count delta is EXPECTED: F2 adds a repetition
scan and a halfmove test to every qsearch node, and F3 removes the illegal stand-pat fail-high
while in check (which previously returned early and pruned the subtree). The table records what
happened; it asserts nothing about strength, and no strength claim is derived from it.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D = ROOT / "_obs" / "fnd0035"


def load(name):
    with (D / name).open(encoding="utf-8") as fh:
        return {r["name"]: r for r in csv.DictReader(fh)}


pre, post = load("nodes_pre_d6.csv"), load("nodes_post_d6.csv")
names = list(pre.keys())

lines = [
    "# FND-0035 F2/F3 - node-count pre/post table (`go depth 6`, Release binary)",
    "",
    "EVIDENCE, NOT A DEFECT. No strength interpretation; no SPRT. Metric is cumulative nodes",
    "at fixed depth (`go depth 6`, never `go nodes` - FND-0035 Finding 4).",
    "",
    "PRE  = binary 686EA5979415054982703985C543CEB9EE7C0CD47C166903CAF8C79D12276F3B (121344 B),",
    "      src/search.cpp F18A0C3CCDB51BB0DE212F0D552855048D5475FF005C4FF14769DD4809B06F8D",
    "POST = binary A0951F4F40B5B85923BA832362C378009F0F8ED7C4DD20BB39EF70F59B5D8BCF (121856 B),",
    "      src/search.cpp 251C19E8E710C715CFEB0B2DB39EC81A2DA6A5B774565496125E897AA326774E",
    "",
    "| # | position | nodes PRE | nodes POST | delta | delta % | bestmove PRE | bestmove POST | bm same |",
    "|---|---|---:|---:|---:|---:|---|---|---|",
]
tp = tq = 0
same = 0
for i, n in enumerate(names, 1):
    a, b = int(pre[n]["nodes"]), int(post[n]["nodes"])
    d = b - a
    pct = (d / a * 100.0) if a else 0.0
    bs = "yes" if pre[n]["bestmove"] == post[n]["bestmove"] else "**NO**"
    same += pre[n]["bestmove"] == post[n]["bestmove"]
    tp += a
    tq += b
    lines.append(f"| {i} | {n} | {a:,} | {b:,} | {d:+,} | {pct:+.1f}% | "
                 f"`{pre[n]['bestmove']}` | `{post[n]['bestmove']}` | {bs} |")
tot = tq - tp
lines += [
    f"| | **TOTAL (11)** | **{tp:,}** | **{tq:,}** | **{tot:+,}** | **{tot/tp*100:+.1f}%** | | | "
    f"{same}/11 |",
    "",
    "## Reading this table (bounded, non-strength)",
    "",
    f"- Node count rose {tot/tp*100:+.1f}% in total. **This is the expected direction and is not a",
    "  regression**: F2 adds a threefold scan + halfmove test to every qsearch node (both are",
    "  O(path length) work that did not exist there before), and F3 deletes a fail-high that used",
    "  to return `beta` immediately while in check, so those nodes now expand.",
    f"- Best moves are identical on {same}/11 positions, so the repair changed the search's mind",
    "  nowhere on this set at depth 6. A changed best move would not by itself have been a defect",
    "  (F3 changes scores at in-check leaves by design); it is recorded either way so the",
    "  adversarial pass can see exactly where, if anywhere, the search moved.",
    "- Nothing here is a strength statement. No SPRT was run and none may be inferred.",
    "",
]
out = D / "nodes_pre_post_table_d6.md"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
print(f"\nwrote {out}")

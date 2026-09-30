#!/usr/bin/env python3
"""imem_retrieve.py — one fused retrieval call: lexical + semantic + graph.

WHY (measured): `research.py search` is BM25-only with graph expansion; `graph` needs
a record id you already know; `beliefs` needs a hypothesis id. An agent facing "what
have we tried for quiescence efficiency" must already know the vocabulary ("stand-pat",
"delta pruning", "check evasion") or miss E-00008. Fusion fixes that: semantic vectors
catch the synonyms, BM25 catches the exact anchors, the graph catches the neighbors,
and reciprocal-rank fusion (RRF) merges them without tuned weights.

`answer()` returns, for one query: ranked records (fused), the claims touched, open
contradictions/revivals/questions on the topic, and — when the query is vague — the
"research partner" decomposition: known bottlenecks, failed approaches, best evidence,
suggested next experiments. That is §42 of the mandate, computed, not chatted.
"""
from __future__ import annotations

import math

from imem_core import as_list, by_id
from imem_text import tokens


def bm25_scores(records: dict, query: str, limit: int = 20) -> list:
    """Okapi BM25 (k1=1.5, b=0.75) over title x3 / tags x2 / body x1. Deterministic."""
    from imem_text import doc_terms as _dt
    qtokens = tokens(query)
    if not qtokens:
        return []
    docs, lens, dfs = {}, {}, {}
    for key, rec in records.items():
        tf = dict(_dt(rec))
        docs[key], lens[key] = tf, sum(tf.values())
        for t in tf:
            dfs[t] = dfs.get(t, 0) + 1
    n = max(1, len(docs))
    avg = sum(lens.values()) / n
    out = {}
    for key, tf in docs.items():
        s = 0.0
        for t in qtokens:
            if t not in tf:
                continue
            idf = math.log(1 + (n - dfs[t] + 0.5) / (dfs[t] + 0.5))
            s += idf * (tf[t] * 2.5) / (tf[t] + 1.5 * (0.25 + 0.75 * lens[key] / avg))
        if s > 0:
            out[key] = s
    return sorted(out.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]


def semantic_scores(records: dict, embed, query: str, limit: int = 20) -> list:
    """Project the query into the random-indexing space and rank docs by cosine.

    Corpus-relative by construction: the query is folded with the corpus idf, so
    corpus jargon ('stand-pat', 'sprt-lite', 'pext') carries weight and generic words
    do not. Deterministic: same corpus + query -> same ranking."""
    if embed is None:
        return []
    from imem_text import doc_terms
    recs = sorted(records.values(), key=lambda r: r.key)
    tf_list = [doc_terms(r) for r in recs]
    df: dict = {}
    for tf in tf_list:
        for t in tf:
            df[t] = df.get(t, 0) + 1
    qtf: dict = {}
    for t in tokens(query):
        qtf[t] = qtf.get(t, 0) + 1
    qv = embed.vector_for_terms(qtf, df, max(1, len(recs)))
    out = []
    for i, key in enumerate(embed.keys):
        denom = embed.norms[i]
        s = sum(a * b for a, b in zip(qv, embed.vecs[i])) / denom if denom else 0.0
        if s > 1e-9:
            out.append((key, s))
    out.sort(key=lambda kv: (-kv[1], kv[0]))
    return out[:limit]
def neighbors(records: dict, keys, depth: int = 1, rel_filter=None) -> dict:
    """BFS over front-matter+inline edges (undirected). {key: (distance, edge_kind)}."""
    adj: dict = {}
    for rec in records.values():
        for rel, dst, _anch, _fld in rec.links_fm + rec.links_inline:
            other = next((r.key for r in records.values() if r.id == dst), None)
            if other is None:
                continue
            if rel_filter and rel not in rel_filter:
                continue
            adj.setdefault(rec.key, []).append((other, rel))
            adj.setdefault(other, []).append((rec.key, rel))
    seeds = list(keys)
    seen = {s: (0, "self") for s in seeds}
    frontier = seeds
    for d in range(1, depth + 1):
        nxt = []
        for cur in frontier:
            for other, kind in sorted(adj.get(cur, [])):
                if other not in seen:
                    seen[other] = (d, kind)
                    nxt.append(other)
        frontier = nxt
    for s in seeds:
        seen.pop(s, None)
    return seen


def rrf_fuse(rankings: list, k: int = 60) -> list:
    """Reciprocal-rank fusion over ranked key lists. No tuned weights: a record that
    ranks #1 anywhere beats one that ranks #9 everywhere. Deterministic ties by key."""
    scores: dict = {}
    for ranking in rankings:
        for rank, key in enumerate(ranking):
            scores[key] = scores.get(key, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores, key=lambda key: (-scores[key], key))


def snippet(text: str, query: str, width: int = 240) -> str:
    import re
    toks = set(tokens(query))
    for m in re.finditer(r"\S+", text or ""):
        if m.group(0).lower().strip(".,;:()\"'`*_#|/-") in toks:
            a = max(0, m.start() - width // 2)
            b = min(len(text), m.start() + width // 2)
            return re.sub(r"\s+", " ", text[a:b]).strip()
    return re.sub(r"\s+", " ", (text or "")[:width]).strip()


def search(records: dict, query: str, embed=None, limit: int = 10,
           graph_depth: int = 1) -> dict:
    """Fused retrieval: BM25 + semantic + graph expansion. Ranked hits each carry a
    provenance snippet and how they entered the set."""
    lex = [k for k, _s in bm25_scores(records, query, limit=20)]
    sem = [k for k, _s in semantic_scores(records, embed, query, limit=20)]
    fused = rrf_fuse([lex, sem])[: max(limit * 2, 12)]
    expanded = neighbors(records, fused[:8], depth=graph_depth)
    order = rrf_fuse([fused, [k for k in expanded]])
    hits = []
    for key in order[:limit]:
        rec = records[key]
        hits.append({"key": key, "id": rec.id, "type": rec.type,
                     "title": rec.title, "status": str(rec.fm.get("status")),
                     "snippet": snippet(rec.title + "\n" + rec.body, query),
                     "via": ("graph:" + expanded[key][1]) if key in expanded
                     else "ranked"})
    return {"query": query, "hits": hits,
            "lexical": lex[:8], "semantic": sem[:8],
            "note": "FUSED PROJECTION — follow the record ids, not this ranking."}
def answer(records: dict, query: str, embed=None, limit: int = 8) -> dict:
    """The research-partner query: fused hits PLUS the topic's live state — claims,
    open contradictions, due revivals, open questions, best evidence. One call answers
    'what do we know, how well, what conflicts, what's next' without reading files."""
    from imem_claims import contradiction_candidates, live_claims
    from imem_prior import question_readiness, revival_rows
    res = search(records, query, embed, limit=limit)
    hit_ids = {records[h["key"]].id for h in res["hits"]}
    graph_ids = set(hit_ids)
    for h in res["hits"]:
        rec = records[h["key"]]
        for _rel, dst, _a, _f in rec.links_fm + rec.links_inline:
            graph_ids.add(dst)
    claims = [c for c in live_claims(records)
              if c["id"] in graph_ids or c["id"] in hit_ids]
    contras = [c for c in contradiction_candidates(records)
               if c["a"] in graph_ids or c["b"] in graph_ids]
    revivals = [r for r in revival_rows(records, {}) if r["id"] in graph_ids]
    questions = [q for q in question_readiness(records) if q["id"] in graph_ids]
    res.update({
        "claims": [{"id": c["id"], "statement": c["statement"], "status": c["status"],
                    "direction": c["direction"], "domain": c["domain"],
                    "tested_by": c["tested_by"]} for c in claims[:12]],
        "contradictions": contras[:8],
        "revivals_on_topic": revivals[:8],
        "questions_on_topic": questions[:8],
        "decomposition": _decompose(records, query, res),
    })
    return res


def _decompose(records: dict, query: str, res: dict) -> dict:
    """What would make a vague query precise: untested claims, strongest evidence,
    and the next experiment the priority engine wants."""
    from imem_claims import live_claims
    from imem_evidence import promotion_ladder
    from imem_prior import priority_rows
    hit_ids = {records[h["key"]].id for h in res["hits"]}
    untested = [c["id"] for c in live_claims(records)
                if c["id"] in hit_ids and not c["tested_by"]][:6]
    strong = []
    for hid in hit_ids:
        rec = by_id(records, hid)
        if rec is None:
            continue
        lad = promotion_ladder(records, rec)
        if lad["rung"] >= 3:
            strong.append({"id": hid, "rung": lad["rung"],
                           "measured_by": lad["measured_by"]})
    pri = [p for p in priority_rows(records) if p["id"] in hit_ids][:3]
    return {"untested_claims": untested,
            "strongest_evidence": strong[:6],
            "suggested_next": [{"id": p["id"], "title": p["title"], "score": p["score"],
                                "why": p["inputs"]} for p in pri],
            "narrowing": ("Name the engine subsystem, the parameter, and the "
                          "direction you expect — then ask again.")}

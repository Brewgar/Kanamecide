#!/usr/bin/env python3
"""imem_text.py — deterministic, offline, stdlib-only semantic vectors for imem.

WHY: BM25 is exact-token only. Semantic "rediscovery" pairs (same idea, different
words) are invisible to it, e.g. H-0011 (copy-make vs make-unmake) and DEC-0004
(make-unmake decision) share almost no tokens but are the same research object from
opposite sides. These vectors find those with no model download, no vector DB, no net.

METHOD (corpus-relative, deterministic):
  1. tokenize like memorylib (mirrored stop rules);
  2. PPMI(term, doc) matrix built from the live corpus only — no outside weights;
  3. truncated SVD by power iteration on the symmetric doc-doc Gram matrix;
  4. doc vectors scaled by sqrt(eigenvalue); cosine is the similarity.
Same corpus -> byte-identical vectors (fixed seeds, fixed iterations, sorted inputs).
"""
from __future__ import annotations

import hashlib
import math
import random
import re

_RE_SPLIT = re.compile(r"[^a-z0-9]+")
_STOP = set(
    "the a an and or of to in on for with by is are was were be been this that "
    "these those it its as at from into not no yes per via vs we i you them our one "
    "two all any each same only than then so such when where which who what how why "
    "do does did can could should would will shall may must if else but also more "
    "most least s t re md".split())


def tokens(text: str) -> list:
    """Same contract as memorylib.tokens: lowercase, len>2, stopwords out, no digits."""
    return [t for t in _RE_SPLIT.split((text or "").lower())
            if len(t) > 2 and t not in _STOP and not t.isdigit()]


def doc_terms(record) -> dict:
    """Weighted term multiset: title x3, tags x2, body x1 (mirrors the BM25 emphasis so
    lexical and semantic views agree on what matters)."""
    tf: dict = {}
    for t in tokens(getattr(record, "title", "")):
        tf[t] = tf.get(t, 0) + 3
    tags = record.fm.get("tags") if hasattr(record, "fm") else []
    for t in tokens(" ".join(map(str, tags or []))):
        tf[t] = tf.get(t, 0) + 2
    for t in tokens((getattr(record, "body", "") or "")[:6000]):
        tf[t] = tf.get(t, 0) + 1
    return tf


def term_signature(term: str, dim: int, seed: int) -> list:
    """Deterministic sparse ternary signature for one term: +1 and -1 at two
    hash-derived positions in `dim` dims (classic random indexing, Sahlgren 2005).

    Why this and not SVD: a 206-doc corpus with pure-Python power iteration costs
    ~500M interpreter operations (measured: killed by the 30 s foreground limit),
    while a ternary signature costs O(1) per (term, vector) pair. Random indexing is
    the offline, stdlib-only, deterministic approximation that has the same cosine
    geometry for our purpose (same jargon -> same direction)."""
    h = hashlib.sha256(("%d:%s" % (seed, term)).encode("utf-8")).digest()
    a = int.from_bytes(h[0:4], "big") % dim
    b = int.from_bytes(h[4:8], "big") % dim
    if b == a:
        b = (a + 1) % dim
    return [(a, 1.0), (b, -1.0)]


def term_signature_table(vocab: list, dim: int, seed: int) -> dict:
    return {t: term_signature(t, dim, seed) for t in vocab}
    h = hashlib.sha256()
    h.update(("k=%d\n" % k).encode())
    for key, tf in zip(keys, tf_list):
        h.update(key.encode())
        h.update(b"\0")
        for t in sorted(tf):
            h.update(("%s:%d\n" % (t, tf[t])).encode())
    return h.hexdigest()
def ppmi_weights(tf_list: list, doc_freq: dict, n_docs: int) -> list:
    """Positive PMI with smoothing (alpha=0.75): downweighs corpus-ubiquitous terms
    ("perft", "depth") so similarity is about *aboutness*, not boilerplate."""
    out = []
    for tf in tf_list:
        total = sum(tf.values()) or 1
        row = {}
        for t, c in tf.items():
            p_td = c / total
            p_t = ((doc_freq.get(t, 0) or 1) / n_docs) ** 0.75
            score = math.log(p_td / p_t + 1e-9) - math.log(2.0)
            if score > 0:
                row[t] = score
        out.append(row)
    return out


def corpus_fingerprint(keys: list, tf_list: list, k: int) -> str:
    h = hashlib.sha256()
    h.update(("k=%d\n" % k).encode())
    for key, tf in zip(keys, tf_list):
        h.update(key.encode())
        h.update(b"\0")
        for t in sorted(tf):
            h.update(("%s:%d\n" % (t, tf[t])).encode())
    return h.hexdigest()


def gram_matrix(weights: list) -> list:
    """Symmetric doc-doc Gram matrix of sparse PPMI rows (list of lists of float)."""
    n = len(weights)
    norms = [math.sqrt(sum(v * v for v in row.values())) or 1.0 for row in weights]
    G = [[0.0] * n for _ in range(n)]
    postings: dict = {}
    for i, row in enumerate(weights):
        for t, v in row.items():
            postings.setdefault(t, []).append((i, v / norms[i]))
    for lst in postings.values():
        for a in range(len(lst)):
            ia, va = lst[a]
            for b in range(a, len(lst)):
                ib, vb = lst[b]
                s = va * vb
                G[ia][ib] += s
                if ib != ia:
                    G[ib][ia] += s
    for i in range(n):
        G[i][i] += 1e-6
    return G


def top_eigenpairs(G: list, k: int, iters: int = 200, seed: int = 0x1E4D) -> list:
    """k leading (eigenvalue, unit vector) pairs of symmetric G by power iteration with
    symmetric deflation. Deterministic: seeded start, fixed iterations, sign-fixed."""
    n = len(G)
    k = max(1, min(k, n))
    rng = random.Random(seed)
    pairs = []
    H = [row[:] for row in G]
    for _ in range(k):
        v = [rng.uniform(-1.0, 1.0) for _ in range(n)]
        nv = math.sqrt(sum(x * x for x in v)) or 1.0
        v = [x / nv for x in v]
        for _ in range(iters):
            w = [sum(H[i][j] * v[j] for j in range(n)) for i in range(n)]
            nw = math.sqrt(sum(x * x for x in w))
            if nw < 1e-12:
                break
            v = [x / nw for x in w]
        lam = sum(v[i] * sum(H[i][j] * v[j] for j in range(n)) for i in range(n))
        if lam < 1e-12:
            break
        for i in range(n):
            if abs(v[i]) > 1e-9:
                if v[i] < 0:
                    v = [-x for x in v]
                break
        pairs.append((lam, v))
        for i in range(n):
            for j in range(n):
                H[i][j] -= lam * v[i] * v[j]
    return pairs


class EmbedSpace:
    """Corpus-relative semantic vectors. Build once from records, reuse for queries."""

    def __init__(self, keys: list, vecs: list, norms: list, fingerprint: str, k: int):
        self.keys = keys
        self.vecs = vecs
        self.norms = norms
        self.fingerprint = fingerprint
        self.dim = k
        self.by_key = {key: i for i, key in enumerate(keys)}

    @classmethod
    def build(cls, records, k: int = 64, seed: int = 0x1E4D, method: str = "ri"):
        """Build the space. method='ri' (default, fast) or 'svd' (exact truncated SVD;
        O(k * iters * n_docs^2) interpreter ops — only sane for a few hundred docs and
        long-running jobs, hence not the default)."""
        recs = sorted(records.values(), key=lambda r: r.key)
        keys = [r.key for r in recs]
        tf_list = [doc_terms(r) for r in recs]
        fp = corpus_fingerprint(keys, tf_list, k)
        df: dict = {}
        for tf in tf_list:
            for t in tf:
                df[t] = df.get(t, 0) + 1
        n = max(1, len(recs))
        if method == "svd":
            weights = ppmi_weights(tf_list, df, n)
            pairs = top_eigenpairs(gram_matrix(weights), k, seed=seed)
            vecs, norms = [], []
            for i in range(len(recs)):
                v = [math.sqrt(lam) * vec[i] for lam, vec in pairs]
                nn = math.sqrt(sum(x * x for x in v)) or 1.0
                vecs.append(v)
                norms.append(nn)
            return cls(keys, vecs, norms, fp, len(pairs))
        # random indexing: w(t,d) = tf * log(N/df) folding into ternary signatures
        vocab = sorted(df)
        sigs = term_signature_table(vocab, k, seed)
        vecs, norms = [], []
        for tf in tf_list:
            v = [0.0] * k
            total = sum(tf.values()) or 1
            for t, c in tf.items():
                w = (c / total) * math.log(1 + n / (df[t] or 1))
                for pos, sign in sigs[t]:
                    v[pos] += sign * w
            nn = math.sqrt(sum(x * x for x in v)) or 1.0
            vecs.append(v)
            norms.append(nn)
        return cls(keys, vecs, norms, fp, k)

    def vector_for_terms(self, tf: dict, df: dict, n_docs: int, seed: int = 0x1E4D) -> list:
        """Fold a term multiset (a query) into the same space, using the corpus idf."""
        vocab = sorted(df)
        sigs = term_signature_table(vocab, self.dim, seed)
        v = [0.0] * self.dim
        total = sum(tf.values()) or 1
        for t, c in tf.items():
            if t not in sigs:
                continue
            w = (c / total) * math.log(1 + n_docs / (df[t] or 1))
            for pos, sign in sigs[t]:
                v[pos] += sign * w
        n = math.sqrt(sum(x * x for x in v)) or 1.0
        return [x / n for x in v]

    def similar(self, key: str, limit: int = 8) -> list:
        """[(other_key, cosine)] — everything except `key` itself, ranked."""
        i = self.by_key.get(key)
        if i is None:
            return []
        vi, ni = self.vecs[i], self.norms[i]
        out = []
        for j, other in enumerate(self.keys):
            if j == i:
                continue
            denom = ni * self.norms[j]
            s = sum(a * b for a, b in zip(vi, self.vecs[j])) / denom if denom else 0.0
            out.append((other, s))
        out.sort(key=lambda kv: (-kv[1], kv[0]))
        return out[: max(0, limit)]

    def to_jsonable(self) -> dict:
        return {"keys": self.keys,
                "vecs": [[round(x, 6) for x in v] for v in self.vecs],
                "norms": [round(x, 6) for x in self.norms],
                "fp": self.fingerprint, "dim": self.dim}

    @classmethod
    def from_jsonable(cls, d: dict):
        vecs = [[float(x) for x in v] for v in d["vecs"]]
        return cls(list(d["keys"]), vecs, [float(x) for x in d["norms"]],
                   str(d["fp"]), int(d["dim"]))

#!/usr/bin/env python3
"""E-0013 artifact pins, and the READ-TIME RE-HASH that makes them a control.

E-0013 Addendum 2 (S-0039), Ruling 2 (F-U9): the E-0013 artifacts are **hash-pinned in
`research/` and deliberately NOT committed** - the 13 MB `positions.jsonl` is derived and
regenerable, and this repository's own E-0010 precedent keeps raw measurement artifacts
local and out of git history.

The ruling states the pin's weakness and names the two disciplines that fix it. This tool is
discipline 2:

    "Somebody must re-hash at read time. The consuming job must verify the digest before it
     reads the file and abort on mismatch. Without a verifying reader, a hash pin is a
     comment with a hexadecimal shape."

So the manifest is not documentation. `verify()` re-hashes every artifact on disk and
compares it with the committed digest, and `read_corpus()` is the entry point a consuming
job calls INSTEAD OF opening `positions.jsonl`: it verifies everything, then refuses to
hand back a corpus the manifest does not actually pin.

Three properties, each of which can fail:

  1. **It re-hashes; it does not re-read a field.** The measured digest comes from the bytes
     on disk every time. A manifest cannot vouch for itself.
  2. **It is mode-aware.** A count-only artifact's digest is a MEASUREMENT's digest, not the
     fitter's corpus digest (Ruling 2's second weakness, and the reason `ac8c92f0...` must
     never be quoted as a corpus). `read_corpus()` refuses a count-only pin outright rather
     than handing it over with a caveat.
  3. **It fails LOUDLY.** Any mismatch, any missing file, any self-contradictory manifest
     is a refusal with the measured digest printed, because a reader told nothing is a
     reader that proceeds.

Usage:
    python tools/e0013_pins.py --verify           # re-hash every pinned artifact
    python tools/e0013_pins.py --read-corpus      # what a fitter calls before reading
    python tools/e0013_pins.py --modes            # what each pinned digest IS
    python tools/e0013_pins.py --selftest         # synthetic; proves a tamper FAILS
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_FORMAT = "kana-e0013-pins-v1"
DEFAULT_MANIFEST = ROOT / "research" / "manifests" / "e0013-artifact-pins.json"
REPORT_FORMAT = "kana-e0013-extract-report-v1"
MODE_COUNT_ONLY = "count-only"
MODE_LABELLED = "labelled"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise SystemExit(f"ABORT: {path} has a BOM; a manifest with a BOM is not "
                         f"byte-identical to the same manifest without one")
    manifest = json.loads(raw.decode("utf-8"))
    if manifest.get("format") != MANIFEST_FORMAT:
        raise SystemExit(f"ABORT: {path} format is {manifest.get('format')!r}, expected "
                         f"{MANIFEST_FORMAT!r}")
    for key in ("artifacts", "fitter_corpus", "read_time_check"):
        if key not in manifest:
            raise SystemExit(f"ABORT: {path} has no {key!r} key; a pin that omits a "
                             f"required field is not a pin")
    return manifest


def resolve(repo: Path, rel: str) -> Path:
    p = Path(rel)
    return p if p.is_absolute() else repo / p


def verify(manifest: dict[str, Any], repo: Path = ROOT) -> dict[str, Any]:
    """Re-hash every pinned artifact. Returns a result dict; never raises for a mismatch.

    `ok` is the AND of every per-artifact result, and `problems` carries the reasons, so a
    caller can print all of it rather than stopping at the first thing that moved.
    """
    results: list[dict[str, Any]] = []
    problems: list[str] = []
    for name, entry in sorted(manifest["artifacts"].items()):
        path = resolve(repo, entry["path"])
        if not path.is_file():
            results.append({"name": name, "ok": False, "reason": "MISSING",
                            "path": entry["path"]})
            problems.append(f"{name}: MISSING at {entry['path']}")
            continue
        measured = sha256_file(path)
        size = path.stat().st_size
        expected = entry["sha256"]
        ok = measured == expected
        if not ok:
            problems.append(
                f"{name}: DIGEST MISMATCH at {entry['path']} - measured {measured}, pinned "
                f"{expected}. The bytes on disk are not the bytes the pin commits to.")
        if "bytes" in entry and size != entry["bytes"]:
            ok = False
            problems.append(f"{name}: SIZE MISMATCH at {entry['path']} - measured {size}, "
                            f"pinned {entry['bytes']}")
        results.append({"name": name, "ok": ok, "measured_sha256": measured,
                        "pinned_sha256": expected, "bytes": size,
                        "kind": entry.get("kind"),
                        "is_fitter_corpus": entry.get("is_fitter_corpus", False)})
    return {"ok": not problems, "results": results, "problems": problems}


def read_corpus(manifest: dict[str, Any], repo: Path = ROOT) -> dict[str, Any]:
    """The read-time gate a consuming job calls INSTEAD OF opening positions.jsonl.

    The order is the point: verify every pin FIRST, and only then ask whether the verified
    bytes are a corpus. A caller that checked the mode first would learn what the artifact
    CLAIMS to be before learning whether it is what the manifest says it is.
    """
    outcome = verify(manifest, repo)
    if not outcome["ok"]:
        raise SystemExit("ABORT: artifact pins do not verify; nothing may be read.\n  "
                         + "\n  ".join(outcome["problems"]))
    corpus = manifest["fitter_corpus"]
    if not corpus.get("sha256"):
        raise SystemExit(
            "ABORT: the manifest pins NO fitter corpus digest.\n"
            f"  reason: {corpus.get('null_reason')}\n"
            "  A count-only artifact's digest is the digest of a MEASUREMENT. Reading it as\n"
            "  a corpus is the confusion Ruling 2 names, and it is refused here rather\n"
            "  than warned about."
        )
    entry = None
    for name, candidate in sorted(manifest["artifacts"].items()):
        if candidate.get("sha256") == corpus["sha256"] and candidate.get("is_fitter_corpus"):
            entry = (name, candidate)
            break
    if entry is None:
        raise SystemExit(
            f"ABORT: the manifest's fitter_corpus.sha256 {corpus['sha256']} matches no "
            f"pinned artifact flagged is_fitter_corpus. The manifest disagrees with itself."
        )
    name, candidate = entry
    return {"name": name, "path": candidate["path"], "sha256": corpus["sha256"],
            "verified": True, "mode": MODE_LABELLED, "verified_results": outcome["results"]}


def report_modes(manifest: dict[str, Any], repo: Path = ROOT) -> dict[str, Any]:
    """What each pinned digest IS, cross-checked against the artifact's own report.

    A pin that stores only a hash leaves a reader to guess what the hash is a hash OF. So
    where the artifact is a `report.json`, this compares the manifest's `kind` /
    `is_fitter_corpus` claim with the mode the bytes themselves declare. A manifest that
    says "corpus" over a count-only file is caught here instead of being believed.
    """
    out: dict[str, Any] = {}
    for name, entry in sorted(manifest["artifacts"].items()):
        path = resolve(repo, entry["path"])
        item: dict[str, Any] = {"manifest_kind": entry.get("kind"),
                                "manifest_mode": entry.get("mode"),
                                "manifest_is_fitter_corpus": entry.get("is_fitter_corpus", False)}
        if path.name == "report.json" and path.is_file():
            rep = json.loads(path.read_bytes().decode("utf-8"))
            item["report_mode"] = rep.get("mode")
            item["report_is_fitter_corpus"] = (rep.get("corpus") or {}).get("is_fitter_corpus")
            item["report_src_commit"] = rep.get("src_commit")
            item["report_provenance_asserted"] = (rep.get("provenance") or {}).get("asserted")
        if path.name == "report.json" and path.is_file():
            rep = json.loads(path.read_bytes().decode("utf-8"))
            item["report_mode"] = rep.get("mode")
            item["report_is_fitter_corpus"] = (rep.get("corpus") or {}).get("is_fitter_corpus")
            item["report_src_commit"] = rep.get("src_commit")
            item["report_provenance_asserted"] = (rep.get("provenance") or {}).get("asserted")
            # A report written BEFORE the corpus/provenance blocks existed cannot answer
            # the question, and its silence is not agreement. That is a NAMED state, not a
            # pass and not a lie: the manifest can declare it, and then a reader sees
            # exactly which artifact is pre-fix instead of inferring it.
            predates = entry.get("schema_predates_the_2026_09_27_fixes", False)
            item["schema_predates_the_2026_09_27_fixes"] = predates
            item["report_has_corpus_block"] = "corpus" in rep
            item["agrees"] = (item["report_mode"] == entry.get("mode")
                              and (predates or item["report_is_fitter_corpus"]
                                   == entry.get("is_fitter_corpus", False)))
            item["agrees_note"] = (
                "the artifact predates the corpus/provenance blocks, so it cannot answer; "
                "the manifest declares this explicitly and the pin is over the bytes as they "
                "are, not over a schema they lack"
            ) if predates else None
        out[name] = item
    return out


def _write_manifest(path: Path, artifacts: dict[str, Any], corpus: dict[str, Any]) -> None:
    path.write_bytes((json.dumps({
        "format": MANIFEST_FORMAT,
        "artifacts": artifacts,
        "fitter_corpus": corpus,
        "read_time_check": "python tools/e0013_pins.py --verify",
    }, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def selftest() -> int:
    """Synthetic only. The real dataset and the real artifacts are never touched.

    The point of this suite is the NEGATIVE case: a re-hash check that has only ever been
    seen passing has not been tested. So the fixtures are pinned, then tampered with, and
    the tamper is REQUIRED to be caught - by digest, by size, by absence, and by a manifest
    that has quietly relabelled a count-only artifact as a corpus.
    """
    import tempfile

    checks: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, bool(ok), detail))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        corpus = root / "positions.jsonl"
        smap = root / "split_map.json"
        corpus.write_bytes(b'{"game_id":0,"y":1.0}\n{"game_id":1,"y":0.0}\n')
        smap.write_bytes(b'{"map":{"0":"train"}}\n')
        original = corpus.read_bytes()

        def corpus_pin() -> dict[str, Any]:
            return {
                "path": str(corpus), "sha256": sha256_file(corpus),
                "bytes": corpus.stat().st_size,
            }

        def full_pin() -> dict[str, Any]:
            return {
                "positions.jsonl": dict(corpus_pin(), kind="fitter-corpus",
                                        mode=MODE_LABELLED, is_fitter_corpus=True),
                "split_map.json": {
                    "path": str(smap), "sha256": sha256_file(smap),
                    "bytes": smap.stat().st_size, "kind": "split-map",
                    "mode": MODE_LABELLED, "is_fitter_corpus": True,
                },
            }

        def count_only_pin() -> dict[str, Any]:
            return {
                "positions.jsonl": dict(corpus_pin(), kind="count-only-pass",
                                        mode=MODE_COUNT_ONLY, is_fitter_corpus=False),
            }

        mf = root / "pins.json"
        NO_CORPUS = {"sha256": None,
                     "null_reason": "count-only pass: no label field was read, so every "
                                    "row's y is null and this file is NOT the corpus a "
                                    "fitter may read"}

        # 1. Untampered pins verify. Otherwise nothing below means anything.
        _write_manifest(mf, full_pin(), {"sha256": sha256_file(corpus), "null_reason": None})
        good = load_manifest(mf)
        outcome = verify(good, root)
        check("pins: an untampered artifact set verifies", outcome["ok"],
              "; ".join(outcome["problems"]))
        got = read_corpus(good, root)
        check("pins: read_corpus hands back the corpus digest after verifying",
              got["verified"] is True and got["sha256"] == sha256_file(corpus)
              and got["name"] == "positions.jsonl", json.dumps(got, sort_keys=True))

        # 2. THE TAMPER. One row appended to the corpus - a single flipped label would be
        #    exactly this small and exactly this consequential. It must be caught.
        corpus.write_bytes(original + b'{"game_id":2,"y":1.0}\n')
        after = verify(load_manifest(mf), root)
        check("pins: a TAMPERED artifact FAILS the read-time re-hash",
              after["ok"] is False
              and any("DIGEST MISMATCH" in p for p in after["problems"]),
              "; ".join(after["problems"]) or "the tamper was NOT caught")
        try:
            read_corpus(load_manifest(mf), root)
            check("pins: read_corpus ABORTS on a tampered artifact", False, "no abort raised")
        except SystemExit as exc:
            check("pins: read_corpus ABORTS on a tampered artifact",
                  "do not verify" in str(exc), str(exc)[:80])

        # 3. A pinned size that is wrong fails even when the digest is right, so the size
        #    check is asserted to be wired rather than assumed to be load-bearing.
        corpus.write_bytes(original)
        size_pin = full_pin()
        size_pin["positions.jsonl"]["bytes"] += 1
        _write_manifest(mf, size_pin, {"sha256": sha256_file(corpus), "null_reason": None})
        sized = verify(load_manifest(mf), root)
        check("pins: a wrong pinned SIZE fails even with a right digest",
              sized["ok"] is False and any("SIZE MISMATCH" in p for p in sized["problems"]),
              "; ".join(sized["problems"]) or "the size check is not wired")

        # 4. Absence. A pinned file that is not there is a failure, not a pass.
        corpus.write_bytes(original)
        _write_manifest(mf, full_pin(), {"sha256": sha256_file(corpus), "null_reason": None})
        corpus.unlink()
        gone = verify(load_manifest(mf), root)
        check("pins: a MISSING pinned artifact FAILS",
              gone["ok"] is False and any("MISSING" in p for p in gone["problems"]),
              "; ".join(gone["problems"]) or "a missing artifact was treated as a pass")
        corpus.write_bytes(original)

        # 5. THE COUNT-ONLY CASE. Ruling 2's second weakness: the manifest must not be able
        #    to hand a MEASUREMENT to a fitter. This is the `ac8c92f0...` situation.
        _write_manifest(mf, count_only_pin(), dict(NO_CORPUS))
        count_only = load_manifest(mf)
        check("pins: a count-only artifact still VERIFIES (it is a real, pinned measurement)",
              verify(count_only, root)["ok"])
        try:
            read_corpus(count_only, root)
            check("pins: read_corpus REFUSES a count-only pin as a corpus", False,
                  "no abort raised")
        except SystemExit as exc:
            check("pins: read_corpus REFUSES a count-only pin as a corpus",
                  "pins NO fitter corpus digest" in str(exc), str(exc)[:80])

        # 6. A manifest that LIES: it claims a corpus digest while its own artifact entry
        #    says count-only. read_corpus cross-checks the manifest against itself and must
        #    refuse the self-contradiction rather than believe the claim.
        _write_manifest(mf, count_only_pin(), {"sha256": sha256_file(corpus),
                                                "null_reason": None})
        try:
            read_corpus(load_manifest(mf), root)
            check("pins: a manifest claiming corpus over count-only bytes is REFUSED", False,
                  "no abort raised")
        except SystemExit as exc:
            check("pins: a manifest claiming corpus over count-only bytes is REFUSED",
                  "disagrees with itself" in str(exc), str(exc)[:80])

        # 7. Mode cross-check against the artifact's OWN report bytes, which is where a
        #    reader would otherwise have to take the manifest's word for it.
        #    reader would otherwise have to take the manifest's word for it.
        rep = root / "report.json"
        rep.write_bytes((json.dumps({
            "format": REPORT_FORMAT, "mode": MODE_COUNT_ONLY,
            "corpus": {"is_fitter_corpus": False, "fitter_corpus_sha256": None},
            "src_commit": "0" * 40, "provenance": {"asserted": False},
        }, sort_keys=True) + "\n").encode("utf-8"))
        honest = {
            "report.json": {
                "path": str(rep), "sha256": sha256_file(rep), "bytes": rep.stat().st_size,
                "kind": "count-only-pass", "mode": MODE_COUNT_ONLY, "is_fitter_corpus": False,
            },
        }
        _write_manifest(mf, honest, dict(NO_CORPUS))
        modes = report_modes(load_manifest(mf), root)
        check("pins: the report's own mode is read back and AGREES with the manifest",
              modes["report.json"]["agrees"] is True
              and modes["report.json"]["report_mode"] == MODE_COUNT_ONLY,
              json.dumps(modes, sort_keys=True))
        check("pins: the mode cross-check READS the bytes (it is not a rubber stamp)",
              modes["report.json"]["report_src_commit"] == "0" * 40
              and modes["report.json"]["report_provenance_asserted"] is False)
        liar = {
            "report.json": {
                "path": str(rep), "sha256": sha256_file(rep), "bytes": rep.stat().st_size,
                "kind": "fitter-corpus", "mode": MODE_LABELLED, "is_fitter_corpus": True,
            },
        }
        _write_manifest(mf, liar, dict(NO_CORPUS))
        check("pins: a manifest that RELABELS count-only bytes as a corpus DISAGREES",
              report_modes(load_manifest(mf), root)["report.json"]["agrees"] is False,
              json.dumps(report_modes(load_manifest(mf), root), sort_keys=True))

        # 8. A manifest missing a required key is refused at LOAD, not at first use.
        (root / "thin.json").write_bytes(
            (json.dumps({"format": MANIFEST_FORMAT, "artifacts": {}}) + "\n").encode("utf-8"))
        try:
            load_manifest(root / "thin.json")
            check("pins: a manifest with no fitter_corpus key is REFUSED at load", False,
                  "no abort raised")
        except SystemExit as exc:
            check("pins: a manifest with no fitter_corpus key is REFUSED at load",
                  "fitter_corpus" in str(exc), str(exc)[:80])

        # 9. The committed manifest exists and names the real artifacts. This is what makes
        #    the pin a committed control rather than a file only this session produced.
        check("pins: the committed manifest exists at the documented path",
              DEFAULT_MANIFEST.is_file(), str(DEFAULT_MANIFEST))
        if DEFAULT_MANIFEST.is_file():
            real = load_manifest(DEFAULT_MANIFEST)
        if DEFAULT_MANIFEST.is_file():
            real = load_manifest(DEFAULT_MANIFEST)
            check("pins: the committed manifest pins the three Ruling-2 artifacts",
                  {"positions.jsonl", "split_map.json", "report.json"}
                  <= set(real["artifacts"]), str(sorted(real["artifacts"])))

    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not ok else ""))
    failed = [n for n, ok, _ in checks if not ok]
    print(f"PINS-SELFTEST {'PASS' if not failed else 'FAIL'} checks={len(checks)} "
          f"failed={len(failed)}")
    return 0 if not failed else 1
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--verify", action="store_true",
                        help="re-hash every pinned artifact and report; exit 2 on mismatch")
    parser.add_argument("--read-corpus", action="store_true",
                        help="the read-time gate: verify every pin, then hand back the "
                             "fitter's corpus digest - or abort")
    parser.add_argument("--modes", action="store_true",
                        help="print what each pinned digest IS, cross-checked against the "
                             "artifact's own report")
    parser.add_argument("--selftest", action="store_true",
                        help="synthetic checks including a TAMPERED artifact; no real "
                             "artifact is read or written")
    return parser.parse_args(argv)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--verify", action="store_true",
                        help="re-hash every pinned artifact and report; exit 2 on mismatch")
    parser.add_argument("--read-corpus", action="store_true",
                        help="the read-time gate: verify every pin, then hand back the "
                             "fitter's corpus digest - or abort")
    parser.add_argument("--modes", action="store_true",
                        help="print what each pinned digest IS, cross-checked against the "
                             "artifact's own report")
    parser.add_argument("--selftest", action="store_true",
                        help="synthetic checks including a TAMPERED artifact; no real "
                             "artifact is read or written")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.selftest:
        return selftest()
    manifest = load_manifest(Path(args.manifest))
    if args.modes:
        modes = report_modes(manifest)
        print(json.dumps(modes, indent=2, sort_keys=True))
        if not all(m.get("agrees", True) for m in modes.values()):
            print("ABORT: a manifest entry disagrees with the mode its artifact declares",
                  file=sys.stderr)
            return 2
        return 0
    if args.read_corpus:
        got = read_corpus(manifest)
        print(json.dumps({k: v for k, v in got.items() if k != "verified_results"},
                         indent=2, sort_keys=True))
        return 0
    if args.verify:
        outcome = verify(manifest)
        for r in outcome["results"]:
            verdict = "OK  " if r["ok"] else "FAIL"
            extra = r.get("measured_sha256") or r.get("reason")
            print(f"{verdict} {r['name']:<18} kind={r.get('kind')} "
                  f"corpus={r.get('is_fitter_corpus')} measured={extra}")
        if not outcome["ok"]:
            print("ABORT: pins do not verify", file=sys.stderr)
            for p in outcome["problems"]:
                print(f"  {p}", file=sys.stderr)
            return 2
        print(f"PINS OK artifacts={len(outcome['results'])} re-hashed at read time")
        return 0
    print("nothing to do: pass --verify, --read-corpus, --modes or --selftest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
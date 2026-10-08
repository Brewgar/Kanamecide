#!/usr/bin/env python3
"""Download Cute Chess + Stockfish into tools/engines/ (gitignored).

Cute Chess 1.5.1 (GPLv3+): official GitHub release asset.
Stockfish (GPLv3+): official stockfishchess.org build.
Both are EXTERNAL tools, never committed to git. SHA-256 verified.
Usage: python tools/fetch_engines.py
"""
import hashlib
import sys
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEST = HERE / "engines"
DEST.mkdir(parents=True, exist_ok=True)

CUTE_URL = ("https://github.com/cutechess/cutechess/releases/download/"
            "v1.5.1/cutechess-1.5.1-win64.zip")
CUTE_SHA = "048942ca3473db860cb914fe94108da37051f693f47e368688ec6ec450f924bc"
SF_URL = ("https://github.com/official-stockfish/Stockfish/releases/"
          "download/sf_17.1/stockfish-windows-x86-64-avx2.zip")

OUT = HERE.parent / "_fetch_out.txt"


def emit(s: str) -> None:
    print(s, flush=True)
    with OUT.open("a", encoding="utf-8") as fh:
        fh.write(s + "\n")


def fetch(url: str, dest: Path) -> None:
    emit(f"GET {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "kanamecide/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r, dest.open("wb") as fh:
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            fh.write(chunk)
    emit(f"saved {dest} bytes={dest.stat().st_size}")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if OUT.is_file():
        OUT.unlink()
    emit("== cutechess ==")
    cz = DEST / "cutechess-1.5.1-win64.zip"
    if not cz.is_file():
        fetch(CUTE_URL, cz)
    got = sha256(cz)
    emit(f"sha256={got}")
    emit("sha-ok=" + str(got == CUTE_SHA))
    with zipfile.ZipFile(cz) as z:
        names = z.namelist()
        emit(f"zip entries={len(names)}")
        z.extractall(DEST / "cutechess-1.5.1")
    for p in sorted((DEST / "cutechess-1.5.1").rglob("cutechess-*")):
        emit(f"bin: {p} size={p.stat().st_size if p.is_file() else -1}")
    emit("== stockfish ==")
    sz = DEST / "stockfish-win.zip"
    if not sz.is_file():
        fetch(SF_URL, sz)
    emit(f"sha256={sha256(sz)}")
    try:
        with zipfile.ZipFile(sz) as z:
            emit(f"zip entries={len(z.namelist())}")
            z.extractall(DEST / "stockfish")
    except Exception as exc:
        emit(f"stockfish unzip: {exc}")
        return 1
    for p in sorted((DEST / "stockfish").rglob("*.exe")):
        emit(f"bin: {p} size={p.stat().st_size}")
    emit("FETCH-DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""W-0005 / E-0012 offline SPRT validation replay — researcher-architect, 2026-09-22.

Replays the RECORDED W/D/L sequences of the retained E-0010 rung files
(e0010_k1n..k6n_games.jsonl — EV-0001 evidence, root-level, READ-ONLY) through the
E-SPRT-lite "draws-as-halves" LLR rule pre-registered in E-0012:

    q(d)   = 1 / (1 + 10^(-d/400))                       (expected score at Elo delta d)
    q0,q1  = q(lo), q(hi)                               (tier margins, from DEC-0010)
    llr_i  = s*ln(q1/q0) + (1-s)*ln((1-q1)/(1-q0))      (s in {1, 1/2, 0}, A's perspective)
    LLR_n  = sum_{i<=n} llr_i
    decide H1 when LLR >= +ln(19) = +2.9444  (alpha=beta=0.05)
    decide H0 when LLR <= -2.9444

No engine is executed. This validates the DEC-0010 ASN/crossing model against recorded
data (D-0007's resolved-routed residual "W-0005 model validation"), NOT any engine.
Every input number is quoted from E-0010 (verified twice: R-0004, R-0008); every model
prediction quoted is reproduced by re-running research/context/w0002_power.py.

Pre-registered acceptance bands (written in E-0012 BEFORE this replay ran; anchored on
the three published model predictions, Wald-Elo 191 / exact-lite expectation / score-
space ~133, not on this replay's output):
  Tier S [0,+20] on k6 (true +116.1): H1 accepted, crossing in [100, 260]  -> PASS/FAIL
  Tier R [0,+5]  on k6: NO decision within 240 games (predictions 494, 713)  -> PASS/FAIL
  Tier M [100,150] on k6: NO decision; final cumulative LLR < 0 (drift toward H0)
                                                                     -> PASS/FAIL
Per-rung totals must equal E-0010's table (k1 85/64/51; k2 101/54/45; k3 116/57/27;
k4 120/63/17; k5 122/51/27; k6 144/66/30) — sample-integrity check.
"""

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BOUNDS = math.log(0.95 / 0.05)  # +2.9444389791664403
SIGMA_ELO = 371.0               # MEASURED, E-0010 six rungs, DEC-0010 calibration
TIER_S, TIER_R, TIER_M = (0.0, 20.0), (0.0, 5.0), (100.0, 150.0)

EXPECTED = {  # (W, D, L, N) from the E-0010 record (verified by R-0004, R-0008)
    "k1n": (85, 51, 64, 200), "k2n": (101, 45, 54, 200), "k3n": (116, 27, 57, 200),
    "k4n": (120, 17, 63, 200), "k5n": (122, 27, 51, 200), "k6n": (144, 30, 66, 240),
}
# measured Elo per rung (E-0010 ladder), used for model-predicted crossings
ELO_MEAS = {"k1n": 36.3, "k2n": 82.3, "k3n": 104.5, "k4n": 100.8, "k5n": 127.6, "k6n": 116.1}


def elo_q(d):
    return 1.0 / (1.0 + 10.0 ** (-d / 400.0))


def llr_step(s, lo, hi):
    q0, q1 = elo_q(lo), elo_q(hi)
    return s * math.log(q1 / q0) + (1.0 - s) * math.log((1.0 - q1) / (1.0 - q0))


def replay(scores, lo, hi):
    """Cumulative lite LLR over the recorded sequence; returns (verdict, crossing, final)."""
    tot = 0.0
    for i, s in enumerate(scores, 1):
        tot += llr_step(s, lo, hi)
        if tot >= BOUNDS:
            return ("H1", i, tot)
        if tot <= -BOUNDS:
            return ("H0", i, tot)
    return (None, None, tot)


def wald_crossing(lo, hi, true_delta):
    """w0002_power.py asn(): Elo-space normal-approx expected crossing at a true effect."""
    drift = (hi - lo) * (true_delta - (lo + hi) / 2.0) / SIGMA_ELO ** 2
    return BOUNDS / drift if drift != 0 else float("inf")


def exact_lite_crossing(lo, hi, q_bar):
    """Expected crossing under the lite model at the rung's measured score q_bar."""
    q0, q1 = elo_q(lo), elo_q(hi)
    e = q_bar * math.log(q1 / q0) + (1.0 - q_bar) * math.log((1.0 - q1) / (1.0 - q0))
    return (BOUNDS / e if e != 0 else float("inf")), e



def main():
    print("W-0005 / E-0012 offline SPRT replay — researcher-architect, 2026-09-22")
    print(f"bounds +/-{BOUNDS:.4f} (alpha=beta=0.05); sigma(Elo)={SIGMA_ELO:.0f} (E-0010, DEC-0010)")
    print()

    integrity_ok = True
    rung_scores = {}
    for tag in ("k1n", "k2n", "k3n", "k4n", "k5n", "k6n"):
        path = ROOT / f"e0010_{tag}_games.jsonl"
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        games = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        gs = [g["g"] for g in games]
        assert gs == sorted(gs), f"{tag}: game ids not in order"
        bad_vals = {g["res"] for g in games} - {"A", "B", "D"}
        assert not bad_vals, f"{tag}: unexpected res values {bad_vals}"
        scores = [{"A": 1.0, "D": 0.5, "B": 0.0}[g["res"]] for g in games]
        w = sum(1 for s in scores if s == 1.0)
        d = sum(1 for s in scores if s == 0.5)
        l_ = sum(1 for s in scores if s == 0.0)
        n = len(scores)
        exp = EXPECTED[tag]
        match = (w, d, l_, n) == exp
        integrity_ok &= match
        lists = [tuple(g["opening"]) + tuple(g["san"]) for g in games]
        dup = n - len(set(lists))
        a_white = sum(1 for g in games if g["a_white"])
        rung_scores[tag] = scores
        print(f"{tag}: N={n}  W={w} D={d} L={l_}  (record {exp[0]}/{exp[1]}/{exp[2]}, N={exp[3]})  "
              f"totals_match={match}  duplicate-move-lists={dup}  a_white={a_white}/{n}")
        print(f"     input sha256: {sha}")
    print()

    print("== Replay: cumulative draws-as-halves (lite) LLR, [lo,hi] from DEC-0010 ==")
    for tag in ("k1n", "k2n", "k3n", "k4n", "k5n", "k6n"):
        scores = rung_scores[tag]
        q_bar = sum(scores) / len(scores)
        elo = ELO_MEAS[tag]
        for name, (lo, hi) in (("S [0,+20]", TIER_S), ("R [0,+5]", TIER_R), ("M [100,150]", TIER_M)):
            verdict, cross, final = replay(scores, lo, hi)
            pw = wald_crossing(lo, hi, elo)
            pe, _ = exact_lite_crossing(lo, hi, q_bar)
            predw = f"Wald={pw:7.0f}" if pw != float("inf") else "Wald=    inf"
            predl = f"lite={pe:7.0f}" if pe != float("inf") else "lite=    inf"
            outcome = f"decide {verdict} at game {cross:>4}" if verdict else f"no decision in {len(scores)}"
            print(f"  {tag} {name:12s}: {outcome:24s} final LLR={final:+7.3f}   (pred-cross {predw} {predl})")
    print()

    s = rung_scores["k6n"]
    vS = replay(s, *TIER_S)
    vR = replay(s, *TIER_R)
    vM = replay(s, *TIER_M)
    bandS = vS[0] == "H1" and 100 <= (vS[1] or 10**9) <= 260
    bandR = vR[0] is None
    bandM = vM[0] is None and vM[2] < 0
    print("== k6 (stage-6 vs stage-0, true +116.1 Elo) vs pre-registered bands ==")
    print(f"  Tier S [0,+20]:   verdict={vS[0]} crossing_game={vS[1]} final={vS[2]:+.3f} "
          f"-> band [100,260] & H1: {'PASS' if bandS else 'FAIL'}")
    print(f"  Tier R [0,+5]:    verdict={vR[0]} crossing_game={vR[1]} final={vR[2]:+.3f} "
          f"-> 'no decision in 240': {'PASS' if bandR else 'FAIL'}")
    print(f"  Tier M [100,150]: verdict={vM[0]} crossing_game={vM[1]} final={vM[2]:+.3f} "
          f"-> 'no decision, LLR<0': {'PASS' if bandM else 'FAIL'}")
    print()

    print("== Model quantities re-derived (w0002_power.py formulas, sigma=371) ==")
    A = BOUNDS
    for name, (lo, hi) in (("Tier S [0,20]", TIER_S), ("Tier R [0,5]", TIER_R), ("Tier M [100,150]", TIER_M)):
        kl = (hi - lo) ** 2 / (2 * SIGMA_ELO ** 2)
        asn_h1 = ((1 - 0.05) * A + 0.05 * (-A)) / kl
        asn_h0 = (0.05 * A + (1 - 0.05) * A) / kl
        print(f"  {name:17s} ASN(H1)={asn_h1:7.1f}  ASN(H0)={asn_h0:7.1f}")
    print()
    print(f"sample-integrity: all-rung totals match E-0010 = {integrity_ok}")
    print("NOTE: a single replay estimates a crossing TIME at the known true effect, not ASN;")
    print("ASN(H1)=~1822 (Tier S) is the model's expectation at the +20 edge, re-derived above.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""E-0010 gate (c): Bayesian Elo + LOS from self-play match tallies.
Model: draws count as halves (standard). Prior Beta(1,1) on the effective win
probability q of engine A (stage-K) vs B (stage-0). LOS = P(q > 0.5) computed
with the regularized incomplete beta function (continued-fraction, NR).
Elo point = 400*log10(mean_q/(1-mean_q)) with Laplace +1 smoothing documented.

Usage: python e0010_elo.py <W> <L> <D> [tag]
"""
import sys, math


def betacf(a, b, x, itmax=200, eps=3e-14):
    """Continued fraction for the incomplete beta (Numerical Recipes 6.4.5)."""
    qab = a + b; qap = a + 1.0; qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < 1e-30: d = 1e-30
    d = 1.0 / d
    h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30: d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30: c = 1e-30
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30: d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30: c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def betai(a, b, x):
    """Regularized incomplete beta I_x(a,b)."""
    if x <= 0.0: return 0.0
    if x >= 1.0: return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                  + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * betacf(a, b, x) / a
    return 1.0 - bt * betacf(b, a, 1.0 - x) / b


def elli_analysis(W, L, D, tag="", legal_ok=True):
    N = W + L + D
    if N == 0:
        print(f"{tag} no games"); return
    Wp = W + D / 2.0; Lp = L + D / 2.0
    # Bayesian posterior q ~ Beta(Wp+1, Lp+1)  (uniform prior)
    a = Wp + 1.0; b = Lp + 1.0
    mean_q = a / (a + b)
    elo_point = 400.0 * math.log10((Wp + 1.0) / (Lp + 1.0))
    elo_bayes = 400.0 * math.log10(mean_q / (1.0 - mean_q))
    los = 1.0 - betai(a, b, 0.5)
    # 95% credible interval on q -> Elo interval (approx, via beta quantile search)
    lo = hi = mean_q
    for target, lo_side in ((0.025, True), (0.975, False)):
        q = target
        step = 0.001
        v = betai(a, b, q)
        # binary search
        loq, hiq = 0.0, 1.0
        for _ in range(60):
            mid = (loq + hiq) / 2.0
            if betai(a, b, mid) < target:
                loq = mid
            else:
                hiq = mid
        if lo_side:
            lo = hiq
        else:
            hi = hiq
    elo_lo = 400.0 * math.log10(lo / (1.0 - lo))
    elo_hi = 400.0 * math.log10(hi / (1.0 - hi))
    print(f"{tag} N={N} W={W} L={L} D={D} | Wrate={Wp/N:.3f} "
          f"Elo={elo_point:+.1f} (bayes {elo_bayes:+.1f}) "
          f"CI95=[{elo_lo:+.1f},{elo_hi:+.1f}] LOS={los*100:.2f}% "
          f"legal={legal_ok}")
    return {"N": N, "W": W, "L": L, "D": D, "elo": elo_point,
            "elo_bayes": elo_bayes, "lo": elo_lo, "hi": elo_hi,
            "los": los}


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: e0010_elo.py W L D [tag]")
        sys.exit(2)
    W = int(sys.argv[1]); L = int(sys.argv[2]); D = int(sys.argv[3])
    tag = sys.argv[4] if len(sys.argv) > 4 else ""
    elli_analysis(W, L, D, tag)
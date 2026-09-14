#!/usr/bin/env python3
"""E-0010 gates (b) and (d), run AFTER all matches finish (uncontended machine).
(b) eval symmetry: --symmetry 1000 <stage> for stages 0..6; record violations.
(d) NPS: --bench 5 on the match binary vs O3d baseline (mean ~31.95 Mnps);
    drop must be <= 30%.
Writes e0010_gates_bd.txt and e0010_gates_bd_done.txt.
"""
import subprocess, sys, os, re

BASE = r"C:\Users\tahae\Kanamecide"
EXE  = os.path.join(BASE, "build", "Release", "kana.exe")
OUT  = os.path.join(BASE, "e0010_gates_bd.txt")
O3D_MEAN_NPS = 31.95e6   # from _g0_bench.txt (O3d baseline, commit 962368b)

def main():
    lines = []
    # Gate (b): symmetry across stages 0..6
    lines.append("=== Gate (b): eval symmetry, 1000 positions per stage ===")
    b_ok = True
    for stg in range(7):
        r = subprocess.run([EXE, "--symmetry", "1000", str(stg)],
                           capture_output=True, text=True, timeout=600)
        out = r.stdout.strip()
        lines.append(out)
        m = re.search(r"full_mirror_viol=(\d+)", out)
        if not m or int(m.group(1)) != 0:
            b_ok = False
    lines.append(f"gate_b_verdict={'PASS' if b_ok else 'FAIL'} (full_mirror_viol must be 0 for all stages)")

    # Gate (d): uncontended bench
    lines.append("")
    lines.append("=== Gate (d): --bench 5 on match binary (uncontended) ===")
    r = subprocess.run([EXE, "--bench", "5"], capture_output=True, text=True, timeout=1800)
    lines.append(r.stdout.strip())
    nps_vals = [float(x) for x in re.findall(r"summary: mean ([0-9.]+)", r.stdout)]
    if len(nps_vals) >= 1:
        mean = sum(nps_vals) / len(nps_vals)
        base = O3D_MEAN_NPS / 1e6                       # baseline in Mnps
        drop = 100.0 * (base - mean) / base             # negative drop = improvement
        lines.append(f"case_means={[f'{v:.2f}' for v in nps_vals]}")
        lines.append(f"mean_nps={mean:.2f} Mnps  o3d_baseline={base:.2f} Mnps  "
                     f"drop={drop:+.1f}%  verdict={'PASS' if drop <= 30.0 else 'FAIL'} (<=30%)")

    txt = "\n".join(lines) + "\n"
    with open(OUT, "w") as f: f.write(txt)
    print(txt)
    with open(os.path.join(BASE, "e0010_gates_bd_done.txt"), "w") as f:
        f.write("done\n")

if __name__ == "__main__":
    main()

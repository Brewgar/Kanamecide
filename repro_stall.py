#!/usr/bin/env python3
"""E-0010 Phase-1 repro/acceptance: bestmove-stall discriminator.

Usage: python -u repro_stall.py [ntrials] [nengines] [tag]
- Boots nengines kana.exe UCI processes (setoption EvalStage verified live).
- Each wave sends position+go to EVERY engine simultaneously (contention
  equivalent to the match harness); go flavors rotate: incremental formula,
  movetime 100, movetime 250.
- bestmove timeout 3.0s. On a miss: records hang vs EOF vs dead-poll, plus
  timestamped last lines relative to the go send (stdout) and the engine
  stderr [GO]/[SR]/[BM] trace file for that engine.
- Single engine, ntrials>=50 => Phase-1 acceptance gate (bestmove every time).
Writes _repro_stall_<tag>.txt. Exit 0 iff every go produced a legal bestmove.
"""
import subprocess, sys, time, threading, queue, os, random, chess

BASE = r"C:\Users\tahae\Kanamecide"
EXE  = os.path.join(BASE, "build", "Release", "kana.exe")
NT   = int(sys.argv[1]) if len(sys.argv) > 1 else 60
NENG = int(sys.argv[2]) if len(sys.argv) > 2 else 1
TAG  = sys.argv[3] if len(sys.argv) > 3 else "s1"
OUT  = os.path.join(BASE, "_repro_stall_" + TAG + ".txt")

def say(s):
    print(s, flush=True)

class Eng:
    def __init__(self, idx, stage):
        self.idx = idx
        self.stage = stage
        errname = os.path.join(BASE, "_repro_err_%s_%d.txt" % (TAG, idx))
        self.errf = open(errname, "w", encoding="utf-8", errors="replace")
        self.errname = errname
        self.p = subprocess.Popen([EXE, "uci"], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=self.errf,
                                  text=True, bufsize=1, encoding="utf-8",
                                  errors="replace")
        self.q = queue.Queue()
        threading.Thread(target=self._pump, daemon=True).start()

    def _pump(self):
        try:
            for line in self.p.stdout:
                self.q.put((time.time(), line.rstrip()))
        except Exception:
            pass
        self.q.put((time.time(), None))

    def send(self, cmd):
        try:
            self.p.stdin.write(cmd + "\n")
            self.p.stdin.flush()
            return True
        except Exception:
            return False

    def wait_for(self, prefix, timeout):
        end = time.time() + timeout
        lines = []
        while time.time() < end:
            try:
                t, l = self.q.get(timeout=max(0.01, end - time.time()))
            except queue.Empty:
                continue
            if l is None:
                return None, lines, "EOF"
            lines.append((t, l))
            if l.startswith(prefix):
                return l, lines, "ok"
        return None, lines, "TIMEOUT"

def go_for(flavor):
    if flavor == "inc":
        return "go wtime 1500 btime 1500 winc 100 binc 100"
    if flavor == "mt100":
        return "go movetime 100"
    return "go movetime 250"

def rnd_position(rng, plies):
    b = chess.Board()
    for _ in range(plies):
        legal = list(b.legal_moves)
        if not legal:
            break
        b.push(rng.choice(legal))
    return [m.uci() for m in b.move_stack]

def main():
    rng = random.Random(20260913)
    engs = [Eng(i, 6 - (i % 7)) for i in range(NENG)]
    ok_boot = True
    for e in engs:
        e.send("isready")
        ok_boot = ok_boot and e.wait_for("readyok", 5.0)[0] is not None
        e.send("ucinewgame")
        e.send("setoption EvalStage " + str(e.stage))
        e.send("isready")
        ok_boot = ok_boot and e.wait_for("readyok", 5.0)[0] is not None
    say("boot ok=%s neng=%d trials=%d tag=%s" % (ok_boot, NENG, NT, TAG))
    total = fails = 0
    for w in range(NT):
        pend = []
        for e in engs:
            flavor = ("inc", "mt100", "mt250")[w % 3]
            pos = rnd_position(rng, rng.randint(0, 120))
            moves = " ".join(pos)
            pcmd = "position startpos" + ((" moves " + moves) if moves else "")
            sf = None
            tgo = time.time()
            if not e.send(pcmd):
                sf = "SENDFAIL(position)"
            elif not e.send(go_for(flavor)):
                sf = "SENDFAIL(go)"
            pend.append((e, flavor, pos, sf, tgo))
        for e, flavor, pos, sf, tgo in pend:
            total += 1
            if sf:
                fails += 1
                say("wave %d eng %d: %s (poll=%s)" % (w, e.idx, sf, e.p.poll()))
                continue
            line, lines, st = e.wait_for("bestmove", 3.0)
            if st == "ok":
                bm = line.split()[1] if len(line.split()) > 1 else ""
                legal_ok = False
                try:
                    b = chess.Board()
                    for mv in pos:
                        b.push_uci(mv)
                    m = chess.Move.from_uci(bm)
                    legal_ok = (m in b.legal_moves)
                except Exception:
                    legal_ok = False
                if not legal_ok:
                    fails += 1
                    say("wave %d eng %d %s: bestmove ILLEGAL: %s" % (w, e.idx, flavor, bm))
                continue
            fails += 1
            alive = e.p.poll() is None
            say("wave %d eng %d %s: %s alive=%s stderr=%s" % (w, e.idx, flavor, st, alive, e.errname))
            for t, l in lines[-8:]:
                say("    stdout +%.0fms %s" % ((t - tgo) * 1000.0, l))
        if (w + 1) % 10 == 0:
            say("progress wave %d/%d total=%d fails=%d" % (w + 1, NT, total, fails))
    say("TOTAL %d GO, MISS %d -> %s" % (total, fails,
        "CLEAN (acceptance MET)" if fails == 0 else "STALL/FAILURE REPRODUCED"))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("neng=%d trials=%d total_go=%d fails=%d verdict=%s\n" %
                (NENG, NT, total, fails, "CLEAN" if fails == 0 else "REPRODUCED"))
    for e in engs:
        e.send("quit")
        try:
            e.p.wait(timeout=3)
        except Exception:
            e.p.kill()
        try:
            e.errf.close()
        except Exception:
            pass
    sys.exit(0 if fails == 0 else 1)

if __name__ == "__main__":
    main()

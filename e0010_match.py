#!/usr/bin/env python3
"""E-0010 gate (c): stage-K vs stage-0 self-play match driver.
Two pipe-based engine processes, alternating colors, ~100ms+100ms inc via the
O3d time formula (go wtime 1500 btime 1500 winc 100 binc 100 -> ~100ms/move).
Every engine move validated by python-chess.
Usage: python e0010_match.py EXE stageK games tag [outdir]
"""
import subprocess, sys, time, threading, queue, chess, os

BASE = r"C:\Users\tahae\Kanamecide"
EXE  = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "build", "Release", "kana.exe")
STK  = int(sys.argv[2]) if len(sys.argv) > 2 else 6
GAMES= int(sys.argv[3]) if len(sys.argv) > 3 else 200
TAG  = sys.argv[4] if len(sys.argv) > 4 else "k6"
ODIR = sys.argv[5] if len(sys.argv) > 5 else BASE
MAXPLIES = 300

class Engine:
    def __init__(self, exe, stage):
        self.stage = stage
        self.p = subprocess.Popen([exe, "uci"], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                  text=True, bufsize=1, encoding="utf-8", errors="replace")
        self.q = queue.Queue()
        self.reader = threading.Thread(target=self._pump, daemon=True)
        self.reader.start()
        self.send("uci")

    def _pump(self):
        try:
            for line in self.p.stdout:
                self.q.put(line)
        except Exception:
            pass
        self.q.put(None)

    def send(self, cmd):
        try:
            self.p.stdin.write(cmd + "\n"); self.p.stdin.flush(); return True
        except Exception:
            return False

    def wait_for(self, prefix, timeout):
        end = time.time() + timeout; lines = []
        while time.time() < end:
            if self.p.poll() is not None: return None, lines
            try: l = self.q.get(timeout=max(0.01, end - time.time()))
            except queue.Empty: continue
            if l is None: return None, lines
            lines.append(l.rstrip())
            if l.startswith(prefix): return l, lines
        return None, lines

    def boot(self):
        self.send("isready")
        if self.wait_for("readyok", 5.0)[0] is None: return False
        self.send("ucinewgame")
        self.send(f"setoption EvalStage {self.stage}")
        self.send("isready")
        return self.wait_for("readyok", 5.0)[0] is not None

def one_move(eng, board, g=None, ply=None):
    parts = ["position", "startpos"]
    if board.move_stack:
        parts.append("moves"); parts.extend(m.uci() for m in board.move_stack)
    if not eng.send(" ".join(parts)): return None, "ENGINE-DIED", []
    if not eng.send("go wtime 1500 btime 1500 winc 100 binc 100"): return None, "ENGINE-DIED", []
    line, lines = eng.wait_for("bestmove", 5.0)
    if line is None:
        preview = " | ".join(lines[-12:])
        print(f"  [DBG g{g} ply{ply}] no bestmove; last lines: {preview}", flush=True)
        return None, "TIMEOUT", lines
    tok = line.split()
    return (tok[1].strip() if len(tok) > 1 else ""), "ok", lines

def play_game(engA, engB, a_white, g):
    board = chess.Board(); san = []
    if not engA.boot() or not engB.boot(): return 0, [], "BOOT-FAIL"
    t0 = time.time()
    while not board.is_game_over() and len(san) < MAXPLIES:
        eng = engA if (board.turn == chess.WHITE) == a_white else engB
        best, st, _ = one_move(eng, board, g, len(san))
        if st != "ok": return len(san), san, st
        if best in ("(none)", "0000", ""): break
        try:
            mv = chess.Move.from_uci(best)
            san.append(board.san(mv)); board.push(mv)
        except Exception:
            return len(san), san, "ILLEGAL:" + best
    dt = time.time() - t0
    if board.is_checkmate(): end = "mate"
    elif board.is_stalemate(): end = "stalemate"
    elif board.is_repetition(3) or board.can_claim_fifty_moves(): end = "draw-claim"
    elif board.is_insufficient_material(): end = "draw-material"
    elif len(san) >= MAXPLIES: end = "plycap"
    else: end = "gameover"
    return len(san), san, end + f"({dt:.0f}s)"

def main():
    engA, engB = Engine(EXE, STK), Engine(EXE, 0)
    print(f"[{TAG}] boot A(stage{STK})={engA.boot()} B(stage0)={engB.boot()}", flush=True)
    res = []
    for g in range(GAMES):
        a_white = (g % 2 == 0)
        ply, san, end = play_game(engA, engB, a_white, g)
        if end.startswith(("ILLEGAL", "TIMEOUT", "ENGINE-DIED", "BOOT")):
            res.append("BAD"); print(f"[{TAG}] g{g}: BAD {end}", flush=True); continue
        b = chess.Board()
        for m in san: b.push_san(m)
        r = b.result()
        if r == "1-0": big = "A" if a_white else "B"      # white won
        elif r == "0-1": big = "B" if a_white else "A"    # black won
        else: big = "D"
        res.append(big)
        print(f"[{TAG}] g{g}: A={'W' if big=='A' else 'L' if big=='B' else 'D'} ply={ply} {end}", flush=True)
    wA = res.count("A"); wB = res.count("B"); d = res.count("D"); bad = res.count("BAD")
    print(f"[{TAG}] games={GAMES} A={wA} B={wB} D={d} bad={bad}", flush=True)
    with open(f"e0010_{TAG}_result.txt", "w") as f:
        f.write(f"total={GAMES} A={wA} B={wB} draw={d} bad={bad}\n")
        f.write(f"results={' '.join(res)}\n")
    for eng in (engA, engB):
        eng.send("quit")
        try: eng.p.wait(timeout=3)
        except Exception: eng.p.kill()

if __name__ == "__main__":
    main()
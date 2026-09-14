#!/usr/bin/env python3
"""E-0010 gate (c) v2: stage-K vs stage-0 self-play match driver WITH opening
randomization so every game is an independent sample.

Randomization scheme (recorded in experiment file):
  - Per game g: rng = random.Random((SEED0, g))  (SEED0 fixed per match, default 20260914)
  - Play N_OPEN=10 random legal plies from startpos using python-chess with that rng.
  - The resulting full move list is sent to BOTH engines as:
        position startpos moves <uci...>
  - Colors balanced by alternating which engine takes White (a_white = g%2==0).
  - Deterministic given EXE + seeds -> fully reproducible.

Incremental per-game flush (m1 writer pattern): one JSON line per finished game
appended to e0010_{TAG}_games.jsonl and fsync'd. On exit writes
e0010_{TAG}_result.txt summary and e0010_{TAG}_done.txt sentinel.

Usage: python e0010_match2.py EXE stageK games tag [outdir] [seed0]
"""
import subprocess, sys, time, threading, queue, chess, os, json, random

BASE = r"C:\Users\tahae\Kanamecide"
EXE  = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "build", "Release", "kana.exe")
STK  = int(sys.argv[2]) if len(sys.argv) > 2 else 6
GAMES= int(sys.argv[3]) if len(sys.argv) > 3 else 200
TAG  = sys.argv[4] if len(sys.argv) > 4 else "k6v2"
ODIR = sys.argv[5] if len(sys.argv) > 5 else BASE
SEED0= int(sys.argv[6]) if len(sys.argv) > 6 else 20260914
N_OPEN = 10          # random opening plies
MAXPLIES = 300

GAMESF = os.path.join(ODIR, f"e0010_{TAG}_games.jsonl")
RESULTF= os.path.join(ODIR, f"e0010_{TAG}_result.txt")
DONEF  = os.path.join(ODIR, f"e0010_{TAG}_done.txt")

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
        self.send(f"setoption name EvalStage value {self.stage}")
        self.send("isready")
        return self.wait_for("readyok", 5.0)[0] is not None

def one_move(eng, board):
    parts = ["position", "startpos"]
    if board.move_stack:
        parts.append("moves"); parts.extend(m.uci() for m in board.move_stack)
    if not eng.send(" ".join(parts)): return None, "ENGINE-DIED"
    if not eng.send("go wtime 1500 btime 1500 winc 100 binc 100"): return None, "ENGINE-DIED"
    line, _ = eng.wait_for("bestmove", 5.0)
    if line is None: return None, "TIMEOUT"
    tok = line.split()
    return (tok[1].strip() if len(tok) > 1 else ""), "ok"

def opening_position(g):
    """Random opening: N_OPEN legal plies from startpos, rng seeded by (SEED0, g)."""
    rng = random.Random(SEED0 * 1000003 + g)
    b = chess.Board()
    for _ in range(N_OPEN):
        moves = list(b.legal_moves)
        b.push(rng.choice(moves))
        if b.is_game_over():  # essentially impossible in 10 plies; shift seed if it happens
            return opening_position(g + 1_000_003)
    return b

def play_game(engA, engB, a_white, g):
    board = opening_position(g)
    opening_uci = [m.uci() for m in board.move_stack]
    san = []
    if not engA.boot() or not engB.boot():
        return len(opening_uci), opening_uci, [], "BOOT-FAIL"
    t0 = time.time()
    while not board.is_game_over() and len(san) + len(opening_uci) < MAXPLIES:
        eng = engA if (board.turn == chess.WHITE) == a_white else engB
        best, st = one_move(eng, board)
        if st != "ok": return len(opening_uci), opening_uci, san, st
        if best in ("(none)", "0000", ""): break
        try:
            mv = chess.Move.from_uci(best)
            san.append(board.san(mv)); board.push(mv)
        except Exception:
            return len(opening_uci), opening_uci, san, "ILLEGAL:" + best
    dt = time.time() - t0
    if board.is_checkmate(): end = "mate"
    elif board.is_stalemate(): end = "stalemate"
    elif board.is_repetition(3) or board.can_claim_fifty_moves(): end = "draw-claim"
    elif board.is_insufficient_material(): end = "draw-material"
    elif len(san) + len(opening_uci) >= MAXPLIES: end = "plycap"
    else: end = "gameover"
    return len(opening_uci), opening_uci, san, end + f"({dt:.0f}s)"

def flush(rec):
    with open(GAMESF, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n"); f.flush(); os.fsync(f.fileno())

def main():
    engA, engB = Engine(EXE, STK), Engine(EXE, 0)
    okA, okB = engA.boot(), engB.boot()
    print(f"[{TAG}] boot A(stage{STK})={okA} B(stage0)={okB} seed0={SEED0} nopen={N_OPEN}", flush=True)
    res = []
    for g in range(GAMES):
        a_white = (g % 2 == 0)
        nopen, opening_uci, san, end = play_game(engA, engB, a_white, g)
        if end.startswith(("ILLEGAL", "TIMEOUT", "ENGINE-DIED", "BOOT")):
            res.append("BAD")
            print(f"[{TAG}] g{g}: BAD {end}", flush=True)
            flush({"g": g, "a_white": a_white, "opening": opening_uci, "res": "BAD",
                   "end": end, "plies": nopen, "san": san})
            continue
        b = chess.Board()
        for u in opening_uci: b.push_uci(u)
        for m in san: b.push_san(m)
        r = b.result()
        if r == "1-0": big = "A" if a_white else "B"
        elif r == "0-1": big = "B" if a_white else "A"
        else: big = "D"
        res.append(big)
        print(f"[{TAG}] g{g}: A={'W' if big=='A' else 'L' if big=='B' else 'D'} ply={len(san)+nopen} {end}", flush=True)
        flush({"g": g, "a_white": a_white, "opening": opening_uci, "res": big,
               "end": end, "plies": len(san) + nopen, "san": san})
    wA = res.count("A"); wB = res.count("B"); d = res.count("D"); bad = res.count("BAD")
    print(f"[{TAG}] games={GAMES} A={wA} B={wB} D={d} bad={bad}", flush=True)
    with open(RESULTF, "w") as f:
        f.write(f"total={GAMES} A={wA} B={wB} draw={d} bad={bad} seed0={SEED0} nopen={N_OPEN} stageK={STK}\n")
        f.write(f"results={' '.join(res)}\n")
    for eng in (engA, engB):
        eng.send("quit")
        try: eng.p.wait(timeout=3)
        except Exception: eng.p.kill()
    with open(DONEF, "w") as f:
        f.write(f"A={wA} B={wB} D={d} BAD={bad}\n")

if __name__ == "__main__":
    main()


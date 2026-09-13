#!/usr/bin/env python3
"""E-0010 Phase-1: contended self-play repro of the match bestmove stall.

Usage: python -u e0010_repro_match.py [pairs] [maxgames] [stagetop] [tag]
Mirrors e0010_match.py exactly (per-move 5s timeout, go wtime 1500 btime 1500
winc 100 binc 100, position startpos moves <full history>, boot per game) and
adds: per-engine stderr capture ([GO]/[SR]/[BM] engine trace), per-game
incrementally flushed result lines, terminal/null-move detection, and on the
FIRST failure a full evidence dump (stdout offsets, stderr trace tail, poll
state) before killing everything. Exit 2 on failure, 0 if all games finish.
"""
import subprocess, sys, time, threading, queue, os, chess

BASE = r"C:\Users\tahae\Kanamecide"
EXE  = os.path.join(BASE, "build", "Release", "kana.exe")
PAIRS = int(sys.argv[1]) if len(sys.argv) > 1 else 6
MAXG  = int(sys.argv[2]) if len(sys.argv) > 2 else 40
STG   = int(sys.argv[3]) if len(sys.argv) > 3 else 6
TAG   = sys.argv[4] if len(sys.argv) > 4 else "m1"
OUT   = os.path.join(BASE, "_repro_match_%s_result.txt" % TAG)
MAXPLIES = 300
ABORT = threading.Event()

def say(s):
    print(s, flush=True)

class Eng:
    def __init__(self, idx, stage):
        self.idx = idx
        self.stage = stage
        self.errname = os.path.join(BASE, "_repro_err_%s_e%d.txt" % (TAG, idx))
        self.errf = open(self.errname, "w", encoding="utf-8", errors="replace")
        self.p = subprocess.Popen([EXE, "uci"], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=self.errf,
                                  text=True, bufsize=1, encoding="utf-8",
                                  errors="replace")
        self.q = queue.Queue()
        self.t0 = time.time()
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

    def boot(self):
        self.send("isready")
        if self.wait_for("readyok", 5.0)[0] is None: return False
        self.send("ucinewgame")
        self.send("setoption EvalStage " + str(self.stage))
        self.send("isready")
        return self.wait_for("readyok", 5.0)[0] is not None

def one_move(eng, board, g, ply):
    parts = ["position", "startpos"]
    if board.move_stack:
        parts.append("moves")
        parts.extend(m.uci() for m in board.move_stack)
    tgo = time.time()
    if not eng.send(" ".join(parts)):
        return None, "SENDFAIL(pos)", tgo, []
    if not eng.send("go wtime 1500 btime 1500 winc 100 binc 100"):
        return None, "SENDFAIL(go)", tgo, []
    line, lines, st = eng.wait_for("bestmove", 5.0)
    if line is None:
        return None, st, tgo, lines
    bm = line.split()[1] if len(line.split()) > 1 else ""
    return bm, "ok", tgo, lines

def dump_evidence(tag, engA, engB):
    for e in (engA, engB):
        say("=== evidence %s eng%d stage=%d poll=%s ===" % (tag, e.idx, e.stage, e.p.poll()))
        end = time.time() + 0.2
        tail = []
        while time.time() < end:
            try:
                t, l = e.q.get(timeout=0.05)
            except queue.Empty:
                continue
            if l is not None:
                tail.append((t, l))
        for t, l in tail[-8:]:
            say("    stdout +%.0fms %s" % ((t - e.t0) * 1000.0, l))

def kill_all(allpairs):
    for pa, pb in allpairs:
        for e in (pa, pb):
            try:
                e.p.kill()
            except Exception:
                pass
            try:
                e.errf.flush()
                e.errf.close()
            except Exception:
                pass

def pair_worker(pi, pa, pb, results, rl):
    for g in range(MAXG):
        if ABORT.is_set():
            return
        a_white = (g % 2 == 0)
        if not pa.boot() or not pb.boot():
            say("[p%d] g%d BOOT-FAIL" % (pi, g))
            with rl: results.append("p%d g%d BAD BOOT-FAIL" % (pi, g))
            ABORT.set()
            return
        board = chess.Board()
        san = []
        t0 = time.time()
        while not board.is_game_over() and len(san) < MAXPLIES and not ABORT.is_set():
            eng = pa if (board.turn == chess.WHITE) == a_white else pb
            bm, st, tgo, lines = one_move(eng, board, g, len(san))
            if st != "ok":
                say("[p%d] g%d ply%d: %s (pollA=%s pollB=%s)" %
                    (pi, g, len(san), st, pa.p.poll(), pb.p.poll()))
                for t, l in lines[-8:]:
                    say("    stdout +%.0fms %s" % ((t - tgo) * 1000.0, l))
                dump_evidence("p%d g%d ply%d %s" % (pi, g, len(san), st), pa, pb)
                with rl: results.append("p%d g%d BAD %s ply%d" % (pi, g, st, len(san)))
                ABORT.set()
                return
            if bm in ("0000", "(none)", ""):
                say("[p%d] g%d ply%d: ENGINE NULLMOVE" % (pi, g, len(san)))
                dump_evidence("p%d g%d ply%d nullmove" % (pi, g, len(san)), pa, pb)
                with rl: results.append("p%d g%d BAD NULLMOVE ply%d" % (pi, g, len(san)))
                ABORT.set()
                return
            try:
                mv = chess.Move.from_uci(bm)
                if mv not in board.legal_moves:
                    raise ValueError("not legal")
                san.append(board.san(mv))
                board.push(mv)
            except Exception:
                say("[p%d] g%d ply%d: ILLEGAL %s" % (pi, g, len(san), bm))
                dump_evidence("p%d g%d ply%d illegal %s" % (pi, g, len(san), bm), pa, pb)
                with rl: results.append("p%d g%d BAD ILLEGAL:%s ply%d" % (pi, g, bm, len(san)))
                ABORT.set()
                return
        dt = time.time() - t0
        if board.is_checkmate():
            r = "1-0" if board.turn == chess.BLACK else "0-1"
            end = "mate"
        elif len(san) >= MAXPLIES:
            r, end = "*", "plycap"
        elif board.is_stalemate():
            r, end = "*", "stalemate"
        elif board.is_insufficient_material():
            r, end = "*", "draw-material"
        elif board.can_claim_fifty_moves() or board.is_repetition(3):
            r, end = "*", "draw-claim"
        else:
            r, end = "*", "gameover"
        big = "D" if r == "*" else ("A" if (r == "1-0") == a_white else "B")
        with rl: results.append("p%d g%d %s ply%d %s(%.0fs)" % (pi, g, big, len(san), end, dt))
        say("[p%d] g%d: %s ply%d %s(%.0fs)" % (pi, g, big, len(san), end, dt))

def main():
    say("repro_match pairs=%d maxgames=%d stage=%d vs 0 tag=%s" % (PAIRS, MAXG, STG, TAG))
    allpairs = [(Eng(2 * pi, STG), Eng(2 * pi + 1, 0)) for pi in range(PAIRS)]
    results = []
    rl = threading.Lock()
    def writer():
        seen = 0
        with open(OUT, "w", encoding="utf-8") as f:
            f.write("pairs=%d maxgames=%d tag=%s started\n" % (PAIRS, MAXG, TAG))
            f.flush()
            while not ABORT.is_set() or seen < len(results):
                with rl:
                    while seen < len(results):
                        f.write(results[seen] + "\n")
                        seen += 1
                f.flush()
                time.sleep(1.0)
            f.write("END lines=%d\n" % len(results))
    wt = threading.Thread(target=writer, daemon=True)
    wt.start()
    threads = [threading.Thread(target=pair_worker, args=(pi, allpairs[pi][0], allpairs[pi][1], results, rl)) for pi in range(PAIRS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    time.sleep(2.0)
    verdict = "FAILED" if any("BAD" in r for r in results) else "ALL-CLEAN"
    say("VERDICT %s games=%d" % (verdict, len(results)))
    kill_all(allpairs)
    with open(OUT, "a", encoding="utf-8") as f:
        f.write("VERDICT=%s games=%d\n" % (verdict, len(results)))
    sys.exit(2 if verdict == "FAILED" else 0)

if __name__ == "__main__":
    main()

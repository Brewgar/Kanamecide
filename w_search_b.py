import io
C = r'''
struct ScoredMove { Move m; int s; };

static int qsearch(Board& b, int alpha, int beta, uint64_t& nodes) {
    nodes++;
    int best = -INF;
    int sp = evaluate(b);
    if (stopped(nodes)) return sp;
    if (sp >= beta) return beta;
    best = sp;
    if (sp > alpha) alpha = sp;

    Move pseudo[256]; int np = generate_moves(b, pseudo);
    Move moves[256]; int n = 0;
    bool in_chk = in_check(b, b.side);
    for (int i = 0; i < np; i++) {
        Move m = pseudo[i];
        if (in_chk || move_flag(m) == PROMOTION || move_flag(m) == EN_PASSANT || b.mailbox[move_to(m)] != 0)
            moves[n++] = m;
    }
    std::stable_sort(moves, moves + n,
        [&b](Move a, Move c) { return capture_value(b, a) > capture_value(b, c); });

    int legal = 0;
    for (int i = 0; i < n; i++) {
        Move m = moves[i]; Undo u; make_move(b, m, u);
        if (attacked_by(b, b.king_sq[~b.side], b.side)) { unmake_move(b, m, u); continue; }
        legal++;
        int sc = -qsearch(b, -beta, -alpha, nodes);
        unmake_move(b, m, u);
        if (sc > best) best = sc;
        if (best > alpha) alpha = best;
        if (alpha >= beta) break;
    }
    if (in_chk && legal == 0) return -MATE;     // checkmated
    return best;
}

'''
with io.open(r"c:\Users\tahae\Kanamecide\src\search.cpp", "a", encoding="utf-8", newline="\n") as f:
    f.write(C.replace("\r\n", "\n"))
print("partB appended:", len(C), "chars")

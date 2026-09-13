import io
C = r'''int negamax(Board& b, int depth, int alpha, int beta, int ply, uint64_t& nodes) {
    nodes++;
    if (stop_flag.load(std::memory_order_relaxed)) return 0;
    if (count_reps(b.key) >= 2) return 0;        // threefold repetition
    if (b.halfmove >= 100) return 0;             // 50-move rule
    if (stopped(nodes)) return 0;
    if (depth <= 0) return QSEARCH ? qsearch(b, alpha, beta, nodes) : evaluate(b);
    assert(ply < MAX_PLY && path_len < MAX_PLY);
#ifndef NDEBUG
    assert(b.key == compute_key(b));   // H-0014: incremental Zobrist key matches the oracle
#endif

    int tt_score = 0; Move tt_move = 0;
    if (tt_probe(b.key, depth, alpha, beta, ply, tt_score, tt_move) == 2)
        return tt_score;

    Move moves[256]; int n = generate_moves(b, moves);
    int tt_idx = -1;
    if (tt_move != 0) for (int i = 0; i < n; i++) if (moves[i] == tt_move) { tt_idx = i; break; }

    ScoredMove sm[256];
    int a0 = alpha;
    Color us = b.side;
    for (int i = 0; i < n; i++) {
        int s = score_move(b, moves[i], ply, tt_move);
        if (i == tt_idx) s = SCORE_PV + 1;
        sm[i] = { moves[i], s };
    }
    if (ORDER_STAGE >= 4 && n > 1)
        std::stable_sort(sm, sm + n, [](const ScoredMove& x, const ScoredMove& y) { return x.s > y.s; });

    int best = -INF, best_mv = 0, legal = 0;
    path_keys[path_len++] = b.key;
    for (int i = 0; i < n; i++) {
        Move m = sm[i].m; Undo u; make_move(b, m, u);
        if (attacked_by(b, b.king_sq[~b.side], b.side)) { unmake_move(b, m, u); continue; }
        legal++;
        int sc = -negamax(b, depth - 1, -beta, -alpha, ply + 1, nodes);
        if (sc > best) { best = sc; best_mv = m; }
        if (best > alpha) alpha = best;
        if (alpha >= beta) {
            if (move_flag(m) != PROMOTION && move_flag(m) != EN_PASSANT && b.mailbox[move_to(m)] == 0) {
                if (m != killer[ply][0]) { killer[ply][1] = killer[ply][0]; killer[ply][0] = m; }
                history_tbl[us][move_from(m)][move_to(m)] += depth * depth;
            }
            break;
        }
        if (stop_flag.load(std::memory_order_relaxed)) break;
    }
    path_len--;

    if (legal == 0) {
        if (in_check(b, b.side)) return -MATE + ply;   // checkmated
        return 0;                                       // stalemate
    }
    if (stop_flag.load(std::memory_order_relaxed)) return (best > -INF) ? best : 0;

    int type = (best <= a0) ? 1 : (best >= beta) ? 2 : 0;
    tt_store(b.key, depth, type, best, ply, best_mv);
    return best;
}

static std::string score_str(int sc) {
    if (sc > MATE - 100000)  return "mate " + std::to_string((MATE - sc + 1) / 2);
    if (sc < -MATE + 100000) return "mate " + std::to_string((-MATE - sc + 1) / 2);
    return "cp " + std::to_string(sc);
}

static std::string build_pv(Board root, int maxply) {
    std::string pv;
    for (int i = 0; i < maxply; i++) {
        Move best = 0; int sc = 0;
        tt_probe(root.key, 0, -INF, INF, 0, sc, best);
        if (best == 0) break;
        Move moves[256]; int n = generate_moves(root, moves);
        bool ok = false;
        for (int j = 0; j < n; j++) {
            if (moves[j] != best) continue;
            Undo u; make_move(root, moves[j], u);
            if (!attacked_by(root, root.king_sq[~root.side], root.side)) { ok = true; break; }
            unmake_move(root, moves[j], u);
        }
        if (!ok) break;
        if (!pv.empty()) pv += " ";
        pv += move_to_string(best);
    }
    return pv;
}

Move search_root(Board& b, int max_depth, int time_ms, uint64_t node_limit_in,
                 int& score, uint64_t& nodes, std::string& pv_out, TTStats& stats) {
    if (max_depth < 1) max_depth = 1;
    if (max_depth > MAX_PLY - 4) max_depth = MAX_PLY - 4;
    clear_state();
    stop_flag.store(false, std::memory_order_relaxed);
    t0 = std::chrono::steady_clock::now();
    time_limit_ms = time_ms; node_limit = node_limit_in;

    score = -INF; nodes = 0;
    Move best = 0;

    Move root_moves[256];
    for (int depth = 1; depth <= max_depth; depth++) {
        uint64_t it_nodes = 0;
        int n = generate_moves(b, root_moves);
        if (best != 0) for (int i = 0; i < n; i++)
            if (root_moves[i] == best) { std::swap(root_moves[0], root_moves[i]); break; }
        int alpha = -INF, beta = INF; int it_score = -INF; Move it_best = 0;
        for (int i = 0; i < n; i++) {
            Move m = root_moves[i]; Undo u; make_move(b, m, u);
            if (!attacked_by(b, b.king_sq[~b.side], b.side)) {
                int sc = -negamax(b, depth - 1, -beta, -alpha, 1, it_nodes);
                if (sc > it_score || (it_best == 0 && sc > -INF)) { it_score = sc; it_best = m; }
                if (it_score > alpha) alpha = it_score;
            }
            unmake_move(b, m, u);
            if (stop_flag.load(std::memory_order_relaxed)) break;
        }
        nodes += it_nodes;
        if (!stop_flag.load(std::memory_order_relaxed) || best == 0) {
            score = it_score; best = it_best;
        }
        auto now = std::chrono::steady_clock::now();
        double ms = std::chrono::duration<double, std::milli>(now - t0).count();
        int nps = (ms > 1.0) ? (int)(nodes * 1000.0 / ms) : 0;
        std::string pv = build_pv(b, depth);
        printf("info depth %d score %s nodes %llu nps %d time %.0f pv %s\n",
               depth, score_str(score).c_str(),
               (unsigned long long)nodes, nps, ms, pv.c_str());
        fflush(stdout);
        if (stop_flag.load(std::memory_order_relaxed)) break;
    }
    pv_out = build_pv(b, max_depth);
    stats = tt_stats();
    return best;
}

} // namespace search
'''
with io.open(r"c:\Users\tahae\Kanamecide\src\search.cpp", "a", encoding="utf-8", newline="\n") as f:
    f.write(C.replace("\r\n", "\n"))
print("partC appended:", len(C), "chars")

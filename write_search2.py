#!/usr/bin/env python3
"""Append the O3d search.cpp part 2 (negamax, build_pv, search_root)."""
import io

BODY = r'''
static int negamax(Board& b, int depth, int alpha, int beta, int ply, uint64_t& nodes) {
    if (count_reps(b.key) >= 2) return 0;
    if (b.halfmove >= 100) return 0;
    if (stopped(nodes)) return 0;
    if (depth <= 0) return QSEARCH ? qsearch(b, alpha, beta, nodes) : evaluate(b);

    int tt_score = 0; Move tt_move = 0;
    tt_probe(b.key, depth, alpha, beta, tt_score, tt_move);

    Move moves[256]; int n = generate_moves(b, moves);
    int tt_idx = -1;
    if (tt_move != 0) { for (int i = 0; i < n; i++) if (moves[i] == tt_move) { tt_idx = i; break; } }

    ScoredMove sm[256];
    for (int i = 0; i < n; i++) {
        int s = score_move(b, moves[i], ply, 0);
        if (i == tt_idx) s = SCORE_PV + 1;
        sm[i] = ScoredMove{moves[i], s};
    }
    if (n > 1) std::stable_sort(sm, sm + n, [](const ScoredMove& a, const ScoredMove& b){ return a.s > b.s; });

    int best = -INF, best_mv = 0, legal = 0, a0 = alpha;
    path_keys[path_len++] = b.key;
    for (int i = 0; i < n; i++) {
        Move m = sm[i].m; Undo u; make_move(b, m, u);
        if (!attacked_by(b, b.king_sq[~b.side], b.side)) {
            assert(move_to(m) != b.king_sq[~b.side]);
            legal++;
            int sc = -negamax(b, depth - 1, -beta, -alpha, ply + 1, nodes);
            if (sc > best) { best = sc; best_mv = m; }
            if (best > alpha) alpha = best;
        }
        unmake_move(b, m, u);
        if (alpha >= beta) {
            if (!is_capture_or_promo(b, m)) {
                if (m != killer[ply][0]) { killer[ply][1] = killer[ply][0]; killer[ply][0] = m; }
                history_tbl[~b.side & 1][move_from(m)][move_to(m)] += depth * depth;
            }
            break;
        }
        if (stopped(nodes)) { path_len--; return best > -INF ? best : 0; }
    }
    path_len--;
    if (legal == 0) {
        if (attacked_by(b, b.king_sq[b.side], ~b.side)) return -MATE;
        return 0;
    }
    int type = (best <= a0) ? 1 : (best >= beta) ? 2 : 0;
    tt_store(b.key, depth, type, best, best_mv);
    return best;
}

static std::string build_pv(Board root, int maxlen) {
    std::string pv;
    for (int i = 0; i < maxlen; i++) {
        Move best = 0; int sc = 0;
        if (tt_probe(root.key, 0, -INF, INF, sc, best) == 0 || best == 0) break;
        Move moves[256]; int n = generate_moves(root, moves);
        bool ok = false;
        for (int j = 0; j < n; j++) if (moves[j] == best) {
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
    stop_flag.store(false, std::memory_order_relaxed);
    t0 = std::chrono::steady_clock::now();
    time_limit_ms = time_ms; node_limit = node_limit_in;
    clear_state(); path_len = 0;
    score = -INF; nodes = 0;
    Move best = 0;
    for (int depth = 1; depth <= max_depth; depth++) {
        int it_score = 0; Move it_best = 0; uint64_t it_nodes = 0;
        Move moves[256]; int n = generate_moves(b, moves);
        if (best != 0) { for (int i = 0; i < n; i++) if (moves[i] == best) { std::swap(moves[0], moves[i]); break; } }
        int alpha = -INF, beta = INF;
        for (int i = 0; i < n; i++) {
            Move m = moves[i]; Undo u; make_move(b, m, u);
            if (!attacked_by(b, b.king_sq[~b.side], b.side)) {
                int sc = -negamax(b, depth - 1, -beta, -alpha, 0, it_nodes);
                if (sc > it_score || it_best == 0) { it_score = sc; it_best = m; }
                if (it_score > alpha) alpha = it_score;
            }
            unmake_move(b, m, u);
            if (stopped(it_nodes)) break;
        }
        if (!stopped(it_nodes)) { score = it_score; best = it_best; nodes += it_nodes; }
        else if (best == 0) { best = it_best; score = it_score; nodes += it_nodes; }
        auto now = std::chrono::steady_clock::now();
        double ms = std::chrono::duration<double, std::chrono::milli>(now - t0).count();
        uint64_t nps = (ms > 1.0) ? (uint64_t)(nodes * 1000.0 / ms) : 0;
        std::string linepv = build_pv(b, depth);
        printf("info depth %d score cp %d nodes %llu nps %llu time %.0f pv %s\n",
               depth, score, (unsigned long long)nodes, (unsigned long long)nps, ms, linepv.c_str());
        fflush(stdout);
        if (stopped(nodes)) break;
    }
    pv_out = build_pv(b, max_depth);
    stats = tt_stats();
    return best;
}

} // namespace search
'''

with io.open(r"c:\Users\tahae\Kanamecide\src\search.cpp", "a", encoding="utf-8", newline="") as f:
    f.write(BODY.replace("\r\n", "\n"))
print("part2 appended:", len(BODY), "chars")
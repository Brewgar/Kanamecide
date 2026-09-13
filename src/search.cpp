// O3d - transposition table + iterative deepening + time control + stop + rep/50-move.
// Built on O3c qsearch and O3b ordering (ORDER_STAGE-gated sort).

#include "search.h"
#include "tt.h"
#include "eval.h"

#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

using namespace kana;

#ifndef ORDER_STAGE
#define ORDER_STAGE 4
#endif
#ifndef QSEARCH
#define QSEARCH 1
#endif

namespace search {

static constexpr int VALUE[PIECE_TYPE_NB] = {100, 320, 330, 500, 900, 20000};
static constexpr int MATE = 1000000;
static constexpr int INF  = 2000000;
static constexpr int SCORE_PV      = 4000000;
static constexpr int SCORE_CAPTURE = 2000000;
static constexpr int SCORE_KILLER  = 1000000;
static constexpr int MAX_PLY       = 128;

static int        history_tbl[COLOR_NB][64][64];
static Move       killer[MAX_PLY][2];
static uint64_t   path_keys[MAX_PLY];
static int        path_len = 0;
static std::vector<uint64_t> game_keys;

static std::atomic<bool> stop_flag{false};
static std::chrono::steady_clock::time_point t0;
static int       time_limit_ms = 0;
static uint64_t  node_limit = 0;

void clear_state() {
    std::memset(history_tbl, 0, sizeof(history_tbl));
    std::memset(killer, 0, sizeof(killer));
    path_len = 0;
    stop_flag.store(false, std::memory_order_relaxed);
}

void set_game_keys(const std::vector<uint64_t>& keys) { game_keys = keys; }
void request_stop() { stop_flag.store(true, std::memory_order_relaxed); }
void clear_stop()   { stop_flag.store(false, std::memory_order_relaxed); }

static bool stopped(uint64_t nodes) {
    if (stop_flag.load(std::memory_order_relaxed)) return true;
    if ((nodes & 2047) == 0) {
        if (time_limit_ms > 0) {
            long long m = std::chrono::duration_cast<std::chrono::milliseconds>(
                              std::chrono::steady_clock::now() - t0).count();
            if (m >= time_limit_ms) { stop_flag.store(true, std::memory_order_relaxed); return true; }
        }
        if (node_limit > 0 && nodes >= node_limit) {
            stop_flag.store(true, std::memory_order_relaxed); return true;
        }
    }
    return false;
}

static int count_reps(uint64_t key) {
    int c = 0;
    for (uint64_t k : game_keys) { if (k == key && ++c >= 2) return c; }
    for (int i = 0; i < path_len; ++i) { if (path_keys[i] == key && ++c >= 2) return c; }
    return c;
}

static bool is_capture_or_promo(const Board& b, Move m) {
    if (move_flag(m) == PROMOTION || move_flag(m) == EN_PASSANT) return true;
    return b.mailbox[move_to(m)] != 0;
}

static int mvv_lva(const Board& b, Move m) {
    int victim, attacker;
    if (move_flag(m) == PROMOTION)        { victim = VALUE[move_promo(m)]; attacker = VALUE[PAWN]; }
    else if (move_flag(m) == EN_PASSANT)  { victim = VALUE[PAWN]; attacker = VALUE[PAWN]; }
    else {
        victim   = VALUE[piece_type(b.mailbox[move_to(m)])];
        attacker = VALUE[piece_type(b.mailbox[move_from(m)])];
    }
    return 10 * victim - attacker;
}

static int capture_value(const Board& b, Move m) {
    if (move_flag(m) == PROMOTION)  return VALUE[move_promo(m)];
    if (move_flag(m) == EN_PASSANT) return VALUE[PAWN];
    return VALUE[piece_type(b.mailbox[move_to(m)])];
}

static int score_move(const Board& b, Move m, int ply, Move pv) {
    if (pv != 0 && m == pv) return SCORE_PV;
    if (is_capture_or_promo(b, m)) return SCORE_CAPTURE + mvv_lva(b, m);
    if (m == killer[ply][0]) return SCORE_KILLER + 1;
    if (m == killer[ply][1]) return SCORE_KILLER;
    return history_tbl[b.side][move_from(m)][move_to(m)];
}


struct ScoredMove { Move m; int s; };

static int qsearch(Board& b, int alpha, int beta, uint64_t& nodes) {
    nodes++;
    int best = -INF;
    int sp = kana::evaluate(b);
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
#ifndef NDEBUG
        { uint64_t _ck = compute_key(b); if (_ck != b.key) fprintf(stderr, "QMAKE KEY MISMATCH stored=%llu computed=%llu side=%d\n", (unsigned long long)b.key, (unsigned long long)_ck, (int)b.side); assert(b.key == compute_key(b)); }
#endif
        if (attacked_by(b, b.king_sq[~b.side], b.side)) { unmake_move(b, m, u); continue; }
        legal++;
        int sc = -qsearch(b, -beta, -alpha, nodes);
#ifndef NDEBUG
        { uint64_t _ck = compute_key(b); if (_ck != b.key) fprintf(stderr, "QRECURSE KEY MISMATCH stored=%llu computed=%llu side=%d\n", (unsigned long long)b.key, (unsigned long long)_ck, (int)b.side); assert(b.key == compute_key(b)); }
#endif
        unmake_move(b, m, u);
#ifndef NDEBUG
        { uint64_t _ck = compute_key(b); if (_ck != b.key) fprintf(stderr, "QUNMAKE KEY MISMATCH stored=%llu computed=%llu side=%d\n", (unsigned long long)b.key, (unsigned long long)_ck, (int)b.side); assert(b.key == compute_key(b)); }
#endif
        if (sc > best) best = sc;
        if (best > alpha) alpha = best;
        if (alpha >= beta) break;
    }
    if (in_chk && legal == 0) return -MATE;     // checkmated
    return best;
}

int negamax(Board& b, int depth, int alpha, int beta, int ply, uint64_t& nodes) {
    nodes++;
    if (stop_flag.load(std::memory_order_relaxed)) return 0;
    if (count_reps(b.key) >= 2) return 0;        // threefold repetition
    if (b.halfmove >= 100) return 0;             // 50-move rule
    if (stopped(nodes)) return 0;
    if (depth <= 0) return QSEARCH ? qsearch(b, alpha, beta, nodes) : kana::evaluate(b);
    assert(ply < MAX_PLY && path_len < MAX_PLY);
#ifndef NDEBUG
    uint64_t ck = compute_key(b);
    if (ck != b.key) {
        fprintf(stderr, "KEY MISMATCH ply=%d depth=%d stored=%llu computed=%llu side=%d\\n",
                ply, depth, (unsigned long long)b.key, (unsigned long long)ck, (int)b.side);
        assert(b.key == compute_key(b));   // H-0014: incremental Zobrist key matches the oracle
    }
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

    int best = -INF, legal = 0;
    Move best_mv = 0;
    path_keys[path_len++] = b.key;
    for (int i = 0; i < n; i++) {
        Move m = sm[i].m; Undo u; make_move(b, m, u);
        if (attacked_by(b, b.king_sq[~b.side], b.side)) { unmake_move(b, m, u); continue; }
        legal++;
        int sc = -negamax(b, depth - 1, -beta, -alpha, ply + 1, nodes);
        if (sc > best) { best = sc; best_mv = m; }
        if (best > alpha) alpha = best;
        bool cutoff = (alpha >= beta);
        if (cutoff) {
            if (move_flag(m) != PROMOTION && move_flag(m) != EN_PASSANT && b.mailbox[move_to(m)] == 0) {
                if (m != killer[ply][0]) { killer[ply][1] = killer[ply][0]; killer[ply][0] = m; }
                history_tbl[us][move_from(m)][move_to(m)] += depth * depth;
            }
        }
        unmake_move(b, m, u);
        if (cutoff) break;
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

static long long sr_now_ms() {
    return std::chrono::duration_cast<std::chrono::milliseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}

Move search_root(Board& b, int max_depth, int time_ms, uint64_t node_limit_in,
                 int& score, uint64_t& nodes, std::string& pv_out, TTStats& stats) {
        if (max_depth < 1) max_depth = 1;
    if (max_depth > MAX_PLY - 4) max_depth = MAX_PLY - 4;
    fprintf(stderr, "[SR] %lld enter time_ms=%d maxd=%d\n", sr_now_ms(), time_ms, max_depth);
    clear_state();
    tt_clear();                 // O3d: start each search from a clean transposition table
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
#ifndef NDEBUG
            { uint64_t _ck = compute_key(b); if (_ck != b.key) fprintf(stderr, "ROOT MAKE KEY MISMATCH depth=%d i=%d stored=%llu computed=%llu side=%d\n", depth, i, (unsigned long long)b.key, (unsigned long long)_ck, (int)b.side); assert(b.key == compute_key(b)); }
#endif
            if (!attacked_by(b, b.king_sq[~b.side], b.side)) {
                int sc = -negamax(b, depth - 1, -beta, -alpha, 1, it_nodes);
                if (sc > it_score || (it_best == 0 && sc > -INF)) { it_score = sc; it_best = m; }
                if (it_score > alpha) alpha = it_score;
            }
            unmake_move(b, m, u);
#ifndef NDEBUG
            { uint64_t _ck = compute_key(b); if (_ck != b.key) fprintf(stderr, "ROOT UNMAKE KEY MISMATCH depth=%d i=%d stored=%llu computed=%llu side=%d\n", depth, i, (unsigned long long)b.key, (unsigned long long)_ck, (int)b.side); assert(b.key == compute_key(b)); }
#endif
            if (stop_flag.load(std::memory_order_relaxed)) break;
        }
        nodes += it_nodes;
        if (stop_flag.load(std::memory_order_relaxed))
            fprintf(stderr, "[SR] %lld stop-fired depth=%d\n", sr_now_ms(), depth);
        if (!stop_flag.load(std::memory_order_relaxed) || best == 0) {
            score = it_score; best = it_best;
            // root is not searched inside negamax, so store its exact entry here for PV walk
            tt_store(b.key, depth, 0, it_score, 0, it_best);
        }
        auto now = std::chrono::steady_clock::now();
        double ms = std::chrono::duration<double, std::milli>(now - t0).count();
        int nps = (ms > 1.0) ? (int)(nodes * 1000.0 / ms) : 0;
        std::string pv = build_pv(b, depth);
        TTStats st = tt_stats();
        printf("info depth %d score %s nodes %llu nps %d time %.0f tt_probes %llu tt_hits %llu tt_cutoffs %llu pv %s\n",
               depth, score_str(score).c_str(),
               (unsigned long long)nodes, nps, ms,
               (unsigned long long)st.probes, (unsigned long long)st.hits,
               (unsigned long long)st.cutoffs, pv.c_str());
        fflush(stdout);
        if (stop_flag.load(std::memory_order_relaxed)) break;
    }
    {
        double ex_ms = std::chrono::duration<double, std::milli>(
            std::chrono::steady_clock::now() - t0).count();
        fprintf(stderr, "[SR] %lld loop-exit best=%u stopped=%d ms=%.0f nodes=%llu\n",
                sr_now_ms(), (unsigned)best,
                (int)stop_flag.load(std::memory_order_relaxed), ex_ms,
                (unsigned long long)nodes);
    }
    pv_out = build_pv(b, max_depth);
    fprintf(stderr, "[SR] %lld pv_built len=%zu\n", sr_now_ms(), pv_out.size());
    stats = tt_stats();
    return best;
}

} // namespace search

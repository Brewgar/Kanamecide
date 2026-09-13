#!/usr/bin/env python3
"""Write the complete O3d search.cpp part 1 (header through qsearch)."""
import io

BODY = r'''// O3d - transposition table + iterative deepening + time control + repetition/50-move.
// Built on the O3c qsearch and O3b ordering. The full Phase-2 search stack is now in place.

#include "search.h"
#include "tt.h"

#include <algorithm>
#include <atomic>
#include <cstring>
#include <chrono>
#include <vector>

using namespace kana;

#ifndef ORDER_STAGE
#define ORDER_STAGE 4
#endif

#ifndef QSEARCH
#define QSEARCH 1
#endif

static constexpr int DELTA_MARGIN = 200;
static constexpr int QSEARCH_MAX_PLY = 512;
static constexpr int MAX_PLY = 128;

namespace search {

static constexpr int VALUE[PIECE_TYPE_NB] = {100, 320, 330, 500, 900, 20000};
static constexpr int MATE  = 1000000;
static constexpr int INF   = 2000000;

static constexpr int SCORE_PV      = 4000000;
static constexpr int SCORE_CAPTURE = 2000000;
static constexpr int SCORE_KILLER  = 1000000;

static int       history_tbl[COLOR_NB][64][64];
static Move      killer[MAX_PLY][2];
static uint64_t  path_keys[MAX_PLY];
static int       path_len = 0;
static std::vector<uint64_t> game_keys;

static std::atomic<bool> stop_flag{false};
static std::chrono::steady_clock::time_point t0;
static int      time_limit_ms = 0;
static uint64_t node_limit = 0;

void clear_state() {
    std::memset(history_tbl, 0, sizeof(history_tbl));
    std::memset(killer, 0, sizeof(killer));
    tt_clear();
}

void set_game_keys(const std::vector<uint64_t>& keys) { game_keys = keys; }

static int count_reps(uint64_t key) {
    int c = 0;
    for (uint64_t k : game_keys) { if (k == key && ++c >= 2) return c; }
    for (int i = 0; i < path_len; ++i) { if (path_keys[i] == key && ++c >= 2) return c; }
    return c;
}

static bool is_capture_or_promo(const Board& b, Move m) {
    if (move_flag(m) == PROMOTION || move_flag(m) == EN_PASSANT)
        return true;
    return b.mailbox[move_to(m)] != 0;
}

static int mvv_lva(const Board& b, Move m) {
    int victim, attacker;
    if (move_flag(m) == PROMOTION) { victim = VALUE[move_promo(m)]; attacker = VALUE[PAWN]; }
    else if (move_flag(m) == EN_PASSANT) { victim = VALUE[PAWN]; attacker = VALUE[PAWN]; }
    else { victim = VALUE[piece_type(b.mailbox[move_to(m)])]; attacker = VALUE[piece_type(b.mailbox[move_from(m)])]; }
    return 10 * victim - attacker;
}

static int score_move(const Board& b, Move m, int ply, Move pv) {
    if (pv != 0 && m == pv) return SCORE_PV;
    if (is_capture_or_promo(b, m)) return SCORE_CAPTURE + mvv_lva(b, m);
    if (m == killer[ply][0]) return SCORE_KILLER + 1;
    if (m == killer[ply][1]) return SCORE_KILLER;
    return history_tbl[b.side][move_from(m)][move_to(m)];
}

static int evaluate(const Board& b) {
    int s = 0;
    for (int c = 0; c < COLOR_NB; c++)
        for (int pt = 0; pt < PIECE_TYPE_NB; pt++)
            s += ((c == WHITE) ? 1 : -1) * VALUE[pt] * popcount(b.pieces[c][pt]);
    return (b.side == WHITE) ? s : -s;
}

static inline bool stopped(uint64_t nodes) {
    if ((nodes & 2047) == 0) {
        if (stop_flag.load(std::memory_order_relaxed)) return true;
        if (time_limit_ms > 0) {
            auto dt = std::chrono::steady_clock::now() - t0;
            long long m = std::chrono::duration_cast<std::chrono::milliseconds>(dt).count();
            if (m >= time_limit_ms) { stop_flag.store(true, std::memory_order_relaxed); return true; }
        }
        if (node_limit > 0 && nodes >= node_limit) { stop_flag.store(true, std::memory_order_relaxed); return true; }
    }
    return stop_flag.load(std::memory_order_relaxed);
}

struct ScoredMove { Move m; int s; };

static int capture_value(const Board& b, Move m) {
    if (move_flag(m) == PROMOTION) return VALUE[move_promo(m)];
    if (move_flag(m) == EN_PASSANT) return VALUE[PAWN];
    return VALUE[piece_type(b.mailbox[move_to(m)])];
}

static int qsearch(Board& b, int alpha, int beta, uint64_t& nodes) {
    nodes++;
    const int stand = evaluate(b);
    const bool in_check = attacked_by(b, b.king_sq[b.side], ~b.side);
    if (!in_check) {
        if (stand >= beta) return stand;
        if (stand > alpha) alpha = stand;
    }
    Move moves[256]; int n = generate_moves(b, moves);
    ScoredMove sm[256]; int nc = 0;
    for (int i = 0; i < n; i++) {
        const Move m = moves[i]; const bool cap = is_capture_or_promo(b, m);
        if (!in_check && !cap) continue;
        if (!in_check && stand + capture_value(b, m) + DELTA_MARGIN < alpha) continue;
        sm[nc++] = ScoredMove{m, cap ? SCORE_CAPTURE + mvv_lva(b, m) : 0};
    }
    if (nc > 1) std::stable_sort(sm, sm + nc, [](const ScoredMove& a, const ScoredMove& b){ return a.s > b.s; });
    int best = in_check ? -INF : stand;
    for (int i = 0; i < nc; i++) {
        Move m = sm[i].m; Undo u; make_move(b, m, u);
        if (!attacked_by(b, b.king_sq[~b.side], b.side)) {
            int sc = -qsearch(b, -beta, -alpha, nodes);
            if (sc > best) best = sc;
            if (best > alpha) alpha = best;
        }
        unmake_move(b, m, u); if (alpha >= beta) break;
    }
    if (in_check && best == -INF) return -MATE;
    return best;
}
'''

with io.open(r"c:\Users\tahae\Kanamecide\src\search.cpp", "w", encoding="utf-8", newline="") as f:
    f.write(BODY.replace("\r\n", "\n"))
print("part1 written:", len(BODY), "chars")
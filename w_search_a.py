import io
C = r'''// O3d - transposition table + iterative deepening + time control + stop + rep/50-move.
// Built on O3c qsearch and O3b ordering (ORDER_STAGE-gated sort).

#include "search.h"
#include "tt.h"

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

static int evaluate(const Board& b) {
    int s = 0;
    for (int c = 0; c < COLOR_NB; c++)
        for (int pt = 0; pt < PIECE_TYPE_NB; pt++)
            s += (c == WHITE ? 1 : -1) * VALUE[pt] * popcount(b.pieces[c][pt]);
    return (b.side == WHITE) ? s : -s;
}
'''
with io.open(r"c:\Users\tahae\Kanamecide\src\search.cpp", "w", encoding="utf-8", newline="\n") as f:
    f.write(C.replace("\r\n", "\n"))
print("partA written:", len(C), "chars")

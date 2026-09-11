// O3b - staged move ordering on top of the O3a plain alpha-beta.
// Levers (compile-time ORDER_STAGE): PV-first (1) -> MVV-LVA captures (2) -> killers (3)
// -> history (4). This is the H-0008 experiment; each stage is measured before the next.
// Ordering is SOUND: it only reorders candidates, never removes the DEC-0008 filter, and
// never changes the fixed-depth minimax value (alpha-beta correctness is order-independent).

#include "search.h"

#include <algorithm>
#include <cstring>

using namespace kana;

#ifndef ORDER_STAGE
#define ORDER_STAGE 4
#endif

namespace search {

// Centipawn material values (hand-tuned baseline; Texel tuning is E-EVAL).
static constexpr int VALUE[PIECE_TYPE_NB] = {100, 320, 330, 500, 900, 20000};

static constexpr int MATE = 1000000;   // score for checkmate (side to move is mated)
static constexpr int INF  = 2000000;

// Ordering score tiers (higher = searched first).
static constexpr int SCORE_PV      = 4000000;  // PV slot (huge)
static constexpr int SCORE_CAPTURE = 2000000;  // + MVV-LVA below
static constexpr int SCORE_KILLER  = 1000000;  // + killer slot
// quiets fall to plain history score (0..) so they sort below captures/killers.

static constexpr int MAX_PLY = 128;

// History heuristic: [color][from][to], bumped by depth^2 on quiet beta cutoffs.
static int history_table[COLOR_NB][64][64];
// Killer moves: up to 2 per ply, quiet moves that caused a beta cutoff.
static Move killer[MAX_PLY][2];

void clear_ordering() {
    std::memset(history_table, 0, sizeof(history_table));
    std::memset(killer, 0, sizeof(killer));
}

static bool is_capture_or_promo(const Board& b, Move m) {
    if (move_flag(m) == PROMOTION || move_flag(m) == EN_PASSANT)
        return true;
    return b.mailbox[move_to(m)] != 0;   // enemy piece on destination
}

// MVV-LVA: 10*victim - attacker. Promotions treat the promo piece as victim, pawn attacker.
static int mvv_lva(const Board& b, Move m) {
    int victim, attacker;
    if (move_flag(m) == PROMOTION) {
        victim = VALUE[move_promo(m)];
        attacker = VALUE[PAWN];
    } else if (move_flag(m) == EN_PASSANT) {
        victim = VALUE[PAWN];
        attacker = VALUE[PAWN];
    } else {
        victim = VALUE[piece_type(b.mailbox[move_to(m)])];
        attacker = VALUE[piece_type(b.mailbox[move_from(m)])];
    }
    return 10 * victim - attacker;
}

// Score a candidate for ordering. pv is the stage-1 PV hint (root only).
static int score_move(const Board& b, Move m, int ply, Move pv) {
    if (ORDER_STAGE >= 1 && pv != 0 && m == pv)
        return SCORE_PV;
    if (ORDER_STAGE >= 2 && is_capture_or_promo(b, m))
        return SCORE_CAPTURE + mvv_lva(b, m);
    if (ORDER_STAGE >= 3) {
        if (m == killer[ply][0]) return SCORE_KILLER + 1;
        if (m == killer[ply][1]) return SCORE_KILLER;
    }
    if (ORDER_STAGE >= 4)
        return history_table[b.side][move_from(m)][move_to(m)];
    return 0;
}

// Material-only evaluation, side-to-move perspective (positive = good for side).
static int evaluate(const Board& b) {
    int score = 0;
    for (int c = 0; c < COLOR_NB; c++) {
        for (int pt = 0; pt < PIECE_TYPE_NB; pt++) {
            int sign = (c == WHITE) ? 1 : -1;
            score += sign * VALUE[pt] * popcount(b.pieces[c][pt]);
        }
    }
    return (b.side == WHITE) ? score : -score;
}

struct ScoredMove { Move m; int s; };

int negamax(Board& b, int depth, int alpha, int beta, int ply, uint64_t& nodes) {
    nodes++;
    if (depth <= 0)
        return evaluate(b);

    Move moves[256];
    int n = generate_moves(b, moves);

    ScoredMove sm[256];
    for (int i = 0; i < n; i++)
        sm[i] = ScoredMove{moves[i], ORDER_STAGE >= 1 ? score_move(b, moves[i], ply, 0) : 0};
    if (ORDER_STAGE >= 1 && n > 1)
        std::stable_sort(sm, sm + n,
                         [](const ScoredMove& a, const ScoredMove& b) { return a.s > b.s; });

    int best = -INF;
    int legal = 0;

    for (int i = 0; i < n; i++) {
        Move m = sm[i].m;
        Undo u;
        make_move(b, m, u);

        // DEC-0008 legality filter (named by implementation-engineer, 2026-09-10):
        // after make_move, b.side is the opponent; reject if the mover's king is attacked.
        Color us = ~b.side; // the side that just moved
        if (!attacked_by(b, b.king_sq[us], b.side)) {
            // H-0012: never captured the enemy king (~us = side now to move).
            assert(move_to(m) != b.king_sq[~us]);
            legal++;

            Undo child_u;
            int score = -negamax(b, depth - 1, -beta, -alpha, ply + 1, nodes);
            if (score > best)
                best = score;
            if (best > alpha)
                alpha = best;
        }

        // unmake BEFORE the beta cut so the board is always restored for the parent.
        unmake_move(b, m, u);

        if (alpha >= beta) {
            // Beta cutoff: record ordering hints for QUIET moves only (captures are
            // already handled by MVV-LVA and are unlikely to repeat across unrelated nodes).
            if (!is_capture_or_promo(b, m)) {
                if (ORDER_STAGE >= 3) {
                    if (killer[ply][0] != m) {
                        killer[ply][1] = killer[ply][0];
                        killer[ply][0] = m;
                    }
                }
                if (ORDER_STAGE >= 4) {
                    int& h = history_table[us][move_from(m)][move_to(m)];
                    h += depth * depth;
                    if (h > (1 << 20)) h = (1 << 20); // clamp
                }
            }
            break;
        }
    }

    if (legal == 0) {
        // No legal moves: checkmate (king attacked) or stalemate.
        if (attacked_by(b, b.king_sq[b.side], ~b.side))
            return -MATE;
        return 0;
    }

    return best;
}

Move bestmove(Board& b, int depth, int& score, uint64_t& nodes) {
    nodes = 0;
    score = -INF;

    Move moves[256];
    int n = generate_moves(b, moves);

    // Stage 1 (PV): root-only shallow prior pass to pick the PV move to try first.
    // Full iterative deepening (re-searching 1..N reusing the PV) is O3d; this is the
    // minimal honest seed for "PV move first" in the absence of ID.
    Move pv = 0;
    if (ORDER_STAGE >= 1 && depth >= 2) {
        int bestprior = -INF;
        uint64_t scratch = 0;
        for (int i = 0; i < n; i++) {
            Undo u;
            make_move(b, moves[i], u);
            Color us = ~b.side;
            if (!attacked_by(b, b.king_sq[us], b.side)) {
                int sc = -negamax(b, 1, -INF, INF, 1, scratch);
                if (sc > bestprior) { bestprior = sc; pv = moves[i]; }
            }
            unmake_move(b, moves[i], u);
        }
    }

    ScoredMove sm[256];
    for (int i = 0; i < n; i++)
        sm[i] = ScoredMove{moves[i], ORDER_STAGE >= 1 ? score_move(b, moves[i], 0, pv) : 0};
    if (ORDER_STAGE >= 1 && n > 1)
        std::stable_sort(sm, sm + n,
                         [](const ScoredMove& a, const ScoredMove& b) { return a.s > b.s; });

    Move best = 0;
    int legal = 0;

    for (int i = 0; i < n; i++) {
        Move m = sm[i].m;
        Undo u;
        make_move(b, m, u);
        Color us = ~b.side;
        if (!attacked_by(b, b.king_sq[us], b.side)) {
            legal++;
            int sc = -negamax(b, depth - 1, -INF, INF, 1, nodes);
            if (sc > score || best == 0) { score = sc; best = m; }
        }
        unmake_move(b, m, u);
    }

    if (best == 0 && n > 0)
        best = moves[0]; // fallback (degenerate position)
    return best;
}

} // namespace search
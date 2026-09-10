// O3a — plain alpha-beta (negamax) + material-only evaluation.
// No move ordering, no quiescence, no TT, no null-move, no LMR.
// This is the baseline every later optimization (O3b ordering, O3c quiescence, O3d TT/ID)
// is measured against. Correct first; speed and strength come in later milestones.

#include "search.h"

#include <algorithm>
#include <limits>

using namespace kana;

namespace search {

// Centipawn material values (hand-tuned baseline; Texel tuning is O3b/E-EVAL).
static constexpr int VALUE[PIECE_TYPE_NB] = {100, 320, 330, 500, 900, 20000};

static constexpr int MATE   = 1000000;   // score for checkmate (side to move is mated)
static constexpr int INF    = 2000000;

// Material-only evaluation, from the side-to-move perspective (positive = good for side).
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

int negamax(Board& b, int depth, int alpha, int beta, Undo& u) {
    if (depth <= 0)
        return evaluate(b);

    Move moves[256];
    int n = generate_moves(b, moves);

    int best = -INF;
    int legal = 0;

    for (int i = 0; i < n; i++) {
        make_move(b, moves[i], u);

        // DEC-0008 legality filter (named by implementation-engineer, 2026-09-10):
        // after make_move, b.side is the opponent; reject if the mover's king is attacked.
        Color us = ~b.side; // the side that just moved
        if (!attacked_by(b, b.king_sq[us], b.side)) {
            // H-0012 invariants (debug): the move we made must be legal.
            assert(move_to(moves[i]) != b.king_sq[us]); // never captured the enemy king
            legal++;

            Undo child_u;
            int score = -negamax(b, depth - 1, -beta, -alpha, child_u);
            if (score > best)
                best = score;
            if (best > alpha)
                alpha = best;
        }

        // unmake BEFORE the beta cut so the board is always restored for the parent.
        unmake_move(b, moves[i], u);
        if (alpha >= beta)
            break; // beta cutoff (after restoring state)
    }

    // No legal moves: checkmate (king attacked) or stalemate.
    if (legal == 0) {
        if (attacked_by(b, b.king_sq[b.side], ~b.side))
            return -MATE; // side to move is mated
        return 0;         // stalemate
    }

    return best;
}

} // namespace search
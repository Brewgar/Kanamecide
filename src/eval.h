#pragma once
#include "board.h"
#include "bitboard.h"

namespace kana {

// All named, tuneable coefficients in one struct.
struct EvalCoeffs {
    // Material
    int mg_value[PIECE_TYPE_NB];
    int eg_value[PIECE_TYPE_NB];
    // PSTs (indexed by square from White's perspective; Black uses mirror)
    int mg_pst[PIECE_TYPE_NB][SQ_NB];
    int eg_pst[PIECE_TYPE_NB][SQ_NB];
    // Pawn structure
    int doubled_pawn_mg;
    int doubled_pawn_eg;
    int isolated_pawn_mg;
    int isolated_pawn_eg;
    int passed_pawn_mg[8];  // per rank (0..7 from White's perspective)
    int passed_pawn_eg[8];
    // Mobility (enemy-pawn-discounted)
    int mobility_mg;
    int mobility_eg;
    // Bishop pair
    int bishop_pair_mg;
    int bishop_pair_eg;
    // Open file (rook/queen)
    int open_file_mg;
    int open_file_eg;
    // Semi-open file (rook/queen)
    int semi_open_file_mg;
    int semi_open_file_eg;
    // 7th rank (rook/queen)
    int seventh_rank_mg;
    int seventh_rank_eg;
    // King shield (MG only)
    int king_shield_mg;
    // King centralization (EG only)
    int king_center_eg;
    // Tempo
    int tempo;
};

void eval_init();

// Evaluate position from side-to-move perspective (centipawns).
int evaluate(const Board& b);

// Eval stage control (0..6). Stage 0 = material-only baseline.
int eval_stage();
void set_eval_stage(int stage);

} // namespace kana

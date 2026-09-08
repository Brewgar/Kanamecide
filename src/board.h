#pragma once
#include "defs.h"
#include "bitboard.h"

namespace kana {

struct Board {
  Bitboard pieces[COLOR_NB][PIECE_TYPE_NB] = {};
  Bitboard occ[COLOR_NB] = {};
  uint8_t mailbox[SQ_NB] = {};
  Square king_sq[COLOR_NB] = {};

  Color side = WHITE;
  uint8_t castling = 0;
  Square ep = SQ_NONE;
  int halfmove = 0;
  int fullmove = 1;
  uint64_t key = 0;
};

inline Bitboard occ_all(const Board& b) { return b.occ[WHITE] | b.occ[BLACK]; }

void set_fen(Board& b, const std::string& fen);
void set_startpos(Board& b);
uint64_t compute_key(const Board& b);

bool attacked_by(const Board& b, Square sq, Color by);
bool in_check(const Board& b, Color c);

struct Undo {
  int captured = 0;
  Square capt_sq = SQ_NONE;
  Square ep_prev = SQ_NONE;
  uint8_t castling_prev = 0;
  int halfmove_prev = 0;
  uint64_t key_prev = 0;
};

void make_move(Board& b, Move m, Undo& u);
void unmake_move(Board& b, Move m, const Undo& u);

bool same_position(const Board& a, const Board& b);

} // namespace kana

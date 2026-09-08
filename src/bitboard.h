#pragma once
#include "defs.h"
#include <bit>

namespace kana {

extern Bitboard knight_attacks[SQ_NB];
extern Bitboard king_attacks[SQ_NB];
extern Bitboard pawn_attacks[COLOR_NB][SQ_NB];

void bitboards_init();

Bitboard rook_attacks(Square sq, Bitboard occ);
Bitboard bishop_attacks(Square sq, Bitboard occ);
inline Bitboard queen_attacks(Square sq, Bitboard occ) { return rook_attacks(sq, occ) | bishop_attacks(sq, occ); }

inline int popcount(Bitboard b) { return std::popcount(b); }
inline Square lsb(Bitboard b) { return Square(std::countr_zero(b)); }
inline Square pop_lsb(Bitboard& b) { Square s = lsb(b); b &= b - 1; return s; }

} // namespace kana

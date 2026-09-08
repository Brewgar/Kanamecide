#include "bitboard.h"

namespace kana {

Bitboard knight_attacks[SQ_NB] = {};
Bitboard king_attacks[SQ_NB] = {};
Bitboard pawn_attacks[COLOR_NB][SQ_NB] = {};

static const int KNIGHT_DIRS[8][2] = {
  {2,1},{2,-1},{-2,1},{-2,-1},{1,2},{1,-2},{-1,2},{-1,-2}
};

static bool init_done = false;

void bitboards_init() {
  if (init_done) return;
  init_done = true;

  for (int sq = 0; sq < SQ_NB; sq++) {
    int r = sq >> 3, f = sq & 7;

    Bitboard kb = 0;
    for (const auto& d : KNIGHT_DIRS) {
      int nr = r + d[0], nf = f + d[1];
      if (nr >= 0 && nr < 8 && nf >= 0 && nf < 8) kb |= 1ULL << (nr * 8 + nf);
    }
    knight_attacks[sq] = kb;

    Bitboard kk = 0;
    for (int dr = -1; dr <= 1; dr++)
      for (int df = -1; df <= 1; df++) {
        if (dr == 0 && df == 0) continue;
        int nr = r + dr, nf = f + df;
        if (nr >= 0 && nr < 8 && nf >= 0 && nf < 8) kk |= 1ULL << (nr * 8 + nf);
      }
    king_attacks[sq] = kk;

    Bitboard w = 0, bb = 0;
    if (r < 7) {
      if (f > 0) w |= 1ULL << ((r + 1) * 8 + (f - 1));
      if (f < 7) w |= 1ULL << ((r + 1) * 8 + (f + 1));
    }
    if (r > 0) {
      if (f > 0) bb |= 1ULL << ((r - 1) * 8 + (f - 1));
      if (f < 7) bb |= 1ULL << ((r - 1) * 8 + (f + 1));
    }
    pawn_attacks[WHITE][sq] = w;
    pawn_attacks[BLACK][sq] = bb;
  }
}

// NOTE: simple, obviously-correct ray stepping. A later milestone replaces this
// with magic/PEXT sliding lookups, measured against perft. Correctness first.
Bitboard rook_attacks(Square sq, Bitboard occ) {
  int r = sq >> 3, f = sq & 7;
  Bitboard att = 0;
  for (int rr = r + 1; rr < 8; rr++) { Bitboard b = 1ULL << (rr * 8 + f); att |= b; if (occ & b) break; }
  for (int rr = r - 1; rr >= 0; rr--) { Bitboard b = 1ULL << (rr * 8 + f); att |= b; if (occ & b) break; }
  for (int ff = f + 1; ff < 8; ff++) { Bitboard b = 1ULL << (r * 8 + ff); att |= b; if (occ & b) break; }
  for (int ff = f - 1; ff >= 0; ff--) { Bitboard b = 1ULL << (r * 8 + ff); att |= b; if (occ & b) break; }
  return att;
}

Bitboard bishop_attacks(Square sq, Bitboard occ) {
  int r = sq >> 3, f = sq & 7;
  Bitboard att = 0;
  for (int rr = r + 1, ff = f + 1; rr < 8 && ff < 8; rr++, ff++) { Bitboard b = 1ULL << (rr * 8 + ff); att |= b; if (occ & b) break; }
  for (int rr = r + 1, ff = f - 1; rr < 8 && ff >= 0; rr++, ff--) { Bitboard b = 1ULL << (rr * 8 + ff); att |= b; if (occ & b) break; }
  for (int rr = r - 1, ff = f + 1; rr >= 0 && ff < 8; rr--, ff++) { Bitboard b = 1ULL << (rr * 8 + ff); att |= b; if (occ & b) break; }
  for (int rr = r - 1, ff = f - 1; rr >= 0 && ff >= 0; rr--, ff--) { Bitboard b = 1ULL << (rr * 8 + ff); att |= b; if (occ & b) break; }
  return att;
}

} // namespace kana

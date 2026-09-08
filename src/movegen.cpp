#include "movegen.h"

namespace kana {

int generate_moves(const Board& b_in, Move* list) {
  Board b_nc = b_in;   // writable copy for EP legality probing
  const Board& b = b_in;
  Color us = b.side;
  Color them = ~us;
  int up = (us == WHITE) ? 8 : -8;
  int start_rank = (us == WHITE) ? 1 : 6;
  int promo_rank = (us == WHITE) ? 7 : 0;
  Bitboard occ = b.occ[WHITE] | b.occ[BLACK];
  int n = 0;

  // Pawns
  Bitboard pawns = b.pieces[int(us)][PAWN];
  while (pawns) {
    Square s = pop_lsb(pawns);
    int r = int(s) >> 3, f = int(s) & 7;
    int one = int(s) + up;
    if (one >= 0 && one < 64 && !(occ & (1ULL << one))) {
      if ((one >> 3) == promo_rank) {
        list[n++] = make_promo(s, Square(one), QUEEN);
        list[n++] = make_promo(s, Square(one), ROOK);
        list[n++] = make_promo(s, Square(one), BISHOP);
        list[n++] = make_promo(s, Square(one), KNIGHT);
      } else {
        list[n++] = make_move(s, Square(one));
        if (r == start_rank) {
          int two = int(s) + 2 * up;
          if (!(occ & (1ULL << two))) list[n++] = make_move(s, Square(two));
        }
      }
    }
    int ct[2] = { (f > 0) ? int(s) + up - 1 : -1, (f < 7) ? int(s) + up + 1 : -1 };
    for (int i = 0; i < 2; i++) {
      int t = ct[i];
      if (t < 0 || t > 63) continue;
      if (!(b.occ[int(them)] & (1ULL << t))) continue;
      if ((t >> 3) == promo_rank) {
        list[n++] = make_promo(s, Square(t), QUEEN);
        list[n++] = make_promo(s, Square(t), ROOK);
        list[n++] = make_promo(s, Square(t), BISHOP);
        list[n++] = make_promo(s, Square(t), KNIGHT);
      } else {
        list[n++] = make_move(s, Square(t));
      }
    }
    // En passant legality: the capture must not expose the mover's own king.
    // Verify by make/unmake rather than ray reasoning (handles horizontal double-pin cases).
    if (b.ep != SQ_NONE) {
      int er = int(b.ep) >> 3, ef = int(b.ep) & 7;
      int need_rank = er + (us == WHITE ? -1 : 1);
      if (r == need_rank && (f == ef - 1 || f == ef + 1)) {
        Move epmove = make_special(s, b.ep, EN_PASSANT);
        Undo u;
        make_move(b_nc, epmove, u);
        bool legal = !attacked_by(b_nc, b_nc.king_sq[int(us)], them);
        unmake_move(b_nc, epmove, u);
        if (legal) list[n++] = epmove;
      }
    }
  }

  // Knights
  Bitboard bb = b.pieces[int(us)][KNIGHT];
  while (bb) {
    Square s = pop_lsb(bb);
    Bitboard att = knight_attacks[s] & ~b.occ[int(us)];
    while (att) list[n++] = make_move(s, pop_lsb(att));
  }

  // Bishops
  bb = b.pieces[int(us)][BISHOP];
  while (bb) {
    Square s = pop_lsb(bb);
    Bitboard att = bishop_attacks(s, occ) & ~b.occ[int(us)];
    while (att) list[n++] = make_move(s, pop_lsb(att));
  }

  // Rooks
  bb = b.pieces[int(us)][ROOK];
  while (bb) {
    Square s = pop_lsb(bb);
    Bitboard att = rook_attacks(s, occ) & ~b.occ[int(us)];
    while (att) list[n++] = make_move(s, pop_lsb(att));
  }

  // Queens
  bb = b.pieces[int(us)][QUEEN];
  while (bb) {
    Square s = pop_lsb(bb);
    Bitboard att = queen_attacks(s, occ) & ~b.occ[int(us)];
    while (att) list[n++] = make_move(s, pop_lsb(att));
  }

  // King
  bb = b.pieces[int(us)][KING];
  if (bb) {
    Square ks = pop_lsb(bb);
    Bitboard att = king_attacks[ks] & ~b.occ[int(us)];
    while (att) list[n++] = make_move(ks, pop_lsb(att));
  }

  // Castling
  if (us == WHITE) {
    if ((b.castling & WHITE_OO) && b.mailbox[H1] == make_piece(WHITE, ROOK) &&
        !(occ & ((1ULL << F1) | (1ULL << G1))) &&
        !attacked_by(b, E1, BLACK) && !attacked_by(b, F1, BLACK) && !attacked_by(b, G1, BLACK))
      list[n++] = make_special(E1, G1, CASTLING);
    if ((b.castling & WHITE_OOO) && b.mailbox[A1] == make_piece(WHITE, ROOK) &&
        !(occ & ((1ULL << D1) | (1ULL << C1) | (1ULL << B1))) &&
        !attacked_by(b, E1, BLACK) && !attacked_by(b, D1, BLACK) && !attacked_by(b, C1, BLACK))
      list[n++] = make_special(E1, C1, CASTLING);
  } else {
    if ((b.castling & BLACK_OO) && b.mailbox[H8] == make_piece(BLACK, ROOK) &&
        !(occ & ((1ULL << F8) | (1ULL << G8))) &&
        !attacked_by(b, E8, WHITE) && !attacked_by(b, F8, WHITE) && !attacked_by(b, G8, WHITE))
      list[n++] = make_special(E8, G8, CASTLING);
    if ((b.castling & BLACK_OOO) && b.mailbox[A8] == make_piece(BLACK, ROOK) &&
        !(occ & ((1ULL << D8) | (1ULL << C8) | (1ULL << B8))) &&
        !attacked_by(b, E8, WHITE) && !attacked_by(b, D8, WHITE) && !attacked_by(b, C8, WHITE))
      list[n++] = make_special(E8, C8, CASTLING);
  }

  return n;
}

} // namespace kana

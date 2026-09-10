#include "board.h"
#include "zobrist.h"

#include <cassert>
#include <cctype>
#include <cstring>
#include <cstdlib>
#include <sstream>
#include <stdexcept>
#include <string>

namespace kana {

static void clear_board(Board& b) { std::memset(&b, 0, sizeof(Board)); b.ep = SQ_NONE; }

static void add_piece(Board& b, Square s, int pc) {
  int c = int(piece_color(pc)), t = int(piece_type(pc));
  b.pieces[c][t] |= 1ULL << s;
  b.occ[c] |= 1ULL << s;
  b.mailbox[s] = uint8_t(pc);
  b.key ^= zobrist::psq[pc - 1][s];
  if (t == KING) b.king_sq[c] = s;
}

static void remove_piece(Board& b, Square s) {
  int pc = b.mailbox[s];
  int c = int(piece_color(pc)), t = int(piece_type(pc));
  b.pieces[c][t] &= ~(1ULL << s);
  b.occ[c] &= ~(1ULL << s);
  b.mailbox[s] = 0;
  b.key ^= zobrist::psq[pc - 1][s];
}

void set_fen(Board& b, const std::string& fen) {
  clear_board(b);
  std::istringstream ss(fen);
  std::string tok, parts[6];
  int np = 0;
  while (ss >> tok && np < 6) parts[np++] = tok;
  if (np < 1) throw std::runtime_error("empty FEN");

  const std::string& board_str = parts[0];
  const std::string side = np > 1 ? parts[1] : "w";
  const std::string castle = np > 2 ? parts[2] : "-";
  const std::string ep = np > 3 ? parts[3] : "-";
  int hm = np > 4 ? std::atoi(parts[4].c_str()) : 0;
  int fm = np > 5 ? std::atoi(parts[5].c_str()) : 1;

  int rank = 7, file = 0;
  for (char ch : board_str) {
    if (ch == '/') { rank--; file = 0; continue; }
    if (ch >= '1' && ch <= '8') { file += ch - '0'; continue; }
    Color c = std::isupper((unsigned char)ch) ? WHITE : BLACK;
    PieceType pt;
    switch (char(std::tolower((unsigned char)ch))) {
      case 'p': pt = PAWN; break;
      case 'n': pt = KNIGHT; break;
      case 'b': pt = BISHOP; break;
      case 'r': pt = ROOK; break;
      case 'q': pt = QUEEN; break;
      case 'k': pt = KING; break;
      default: throw std::runtime_error("bad FEN piece");
    }
    add_piece(b, Square(rank * 8 + file), make_piece(c, pt));
    file++;
  }

  b.side = (side == "b") ? BLACK : WHITE;
  b.castling = 0;
  if (castle != "-")
    for (char ch : castle) {
      if (ch == 'K') b.castling |= WHITE_OO;
      else if (ch == 'Q') b.castling |= WHITE_OOO;
      else if (ch == 'k') b.castling |= BLACK_OO;
      else if (ch == 'q') b.castling |= BLACK_OOO;
    }
  b.ep = SQ_NONE;
  if (ep != "-" && ep.size() >= 2)
    b.ep = Square((ep[1] - '1') * 8 + (ep[0] - 'a'));
  b.halfmove = hm;
  b.fullmove = fm;
  b.key = compute_key(b);
}

void set_startpos(Board& b) { set_fen(b, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"); }

uint64_t compute_key(const Board& b) {
  uint64_t k = 0;
  for (int s = 0; s < SQ_NB; s++) { int pc = b.mailbox[s]; if (pc) k ^= zobrist::psq[pc - 1][s]; }
  k ^= zobrist::castling_[b.castling];
  if (b.ep != SQ_NONE) k ^= zobrist::ep_file[b.ep & 7];
  if (b.side == BLACK) k ^= zobrist::side_;
  return k;
}

bool attacked_by(const Board& b, Square sq, Color by) {
  Bitboard occ = occ_all(b);
  if (pawn_attacks[int(~by)][sq] & b.pieces[int(by)][PAWN]) return true;
  if (knight_attacks[sq] & b.pieces[int(by)][KNIGHT]) return true;
  if (king_attacks[sq] & b.pieces[int(by)][KING]) return true;
  if (bishop_attacks(sq, occ) & (b.pieces[int(by)][BISHOP] | b.pieces[int(by)][QUEEN])) return true;
  if (rook_attacks(sq, occ) & (b.pieces[int(by)][ROOK] | b.pieces[int(by)][QUEEN])) return true;
  return false;
}

bool in_check(const Board& b, Color c) { return attacked_by(b, b.king_sq[int(c)], ~c); }

void make_move(Board& b, Move m, Undo& u) {
  Square from = move_from(m), to = move_to(m);
  Color us = b.side;

  // H-0012 guardrail (debug-only): never apply a pseudo-legal move that captures
  // the enemy king. In filtered legal play this is impossible; it guards future
  // fast paths and arbitrary `--fen` input. Compiled out under NDEBUG.
  assert(to != b.king_sq[int(~us)]);

  int pc = b.mailbox[from];
  int pt = int(piece_type(pc));
  MoveFlag fl = move_flag(m);

  int capt_sq = int(SQ_NONE), captured = 0;
  uint64_t key_prev = b.key;
  Square ep_prev = b.ep;
  uint8_t castling_prev = b.castling;
  int halfmove_prev = b.halfmove;

  remove_piece(b, from);

  if (fl == EN_PASSANT) {
    Square cap = Square(us == WHITE ? int(to) - 8 : int(to) + 8);
    captured = b.mailbox[cap];
    capt_sq = int(cap);
    remove_piece(b, cap);
    add_piece(b, to, pc);
  } else if (fl == CASTLING) {
    add_piece(b, to, pc);
    if (to == G1) { remove_piece(b, H1); add_piece(b, F1, make_piece(us, ROOK)); }
    else if (to == C1) { remove_piece(b, A1); add_piece(b, D1, make_piece(us, ROOK)); }
    else if (to == G8) { remove_piece(b, H8); add_piece(b, F8, make_piece(us, ROOK)); }
    else if (to == C8) { remove_piece(b, A8); add_piece(b, D8, make_piece(us, ROOK)); }
  } else {
    if (b.mailbox[to]) { captured = b.mailbox[to]; capt_sq = int(to); remove_piece(b, to); }
    // H-0012 guard (debug): move_promo() must only be read on a real promotion.
    if (fl == PROMOTION)
      assert(int(move_promo(m)) >= KNIGHT && int(move_promo(m)) <= QUEEN);
    add_piece(b, to, fl == PROMOTION ? make_piece(us, move_promo(m)) : pc);
  }

  uint8_t& cr = b.castling;
  if (pt == KING) cr &= uint8_t(us == WHITE ? ~(WHITE_OO | WHITE_OOO) : ~(BLACK_OO | BLACK_OOO));
  if (from == A1 || to == A1) cr &= uint8_t(~WHITE_OOO);
  if (from == H1 || to == H1) cr &= uint8_t(~WHITE_OO);
  if (from == A8 || to == A8) cr &= uint8_t(~BLACK_OOO);
  if (from == H8 || to == H8) cr &= uint8_t(~BLACK_OO);

  b.ep = SQ_NONE;
  if (pt == PAWN && (int(to) - int(from) == 16 || int(from) - int(to) == 16))
    b.ep = Square((int(from) + int(to)) / 2);

  if (b.castling != castling_prev)
    b.key ^= zobrist::castling_[castling_prev] ^ zobrist::castling_[b.castling];
  if (ep_prev != b.ep) {
    if (ep_prev != SQ_NONE) b.key ^= zobrist::ep_file[ep_prev & 7];
    if (b.ep != SQ_NONE) b.key ^= zobrist::ep_file[b.ep & 7];
  }

  b.halfmove = (pt == PAWN || captured != 0) ? 0 : halfmove_prev + 1;

  if (us == BLACK) b.fullmove++;
  b.side = ~us;
  b.key ^= zobrist::side_;

  u.captured = captured;
  u.capt_sq = Square(capt_sq);
  u.ep_prev = ep_prev;
  u.castling_prev = castling_prev;
  u.halfmove_prev = halfmove_prev;
  u.key_prev = key_prev;
}

void unmake_move(Board& b, Move m, const Undo& u) {
  Square from = move_from(m), to = move_to(m);
  Color mover = ~b.side;
  MoveFlag fl = move_flag(m);
  int pc = b.mailbox[to];

  remove_piece(b, to);

  if (fl == PROMOTION) {
    add_piece(b, from, make_piece(mover, PAWN));
    if (u.captured) add_piece(b, u.capt_sq, u.captured);
  } else if (fl == EN_PASSANT) {
    add_piece(b, from, pc);
    if (u.captured) add_piece(b, u.capt_sq, u.captured);
  } else if (fl == CASTLING) {
    add_piece(b, from, pc);
    if (to == G1) { remove_piece(b, F1); add_piece(b, H1, make_piece(mover, ROOK)); }
    else if (to == C1) { remove_piece(b, D1); add_piece(b, A1, make_piece(mover, ROOK)); }
    else if (to == G8) { remove_piece(b, F8); add_piece(b, H8, make_piece(mover, ROOK)); }
    else if (to == C8) { remove_piece(b, D8); add_piece(b, A8, make_piece(mover, ROOK)); }
  } else {
    add_piece(b, from, pc);
    if (u.captured) add_piece(b, u.capt_sq, u.captured);
  }

  b.ep = u.ep_prev;
  b.castling = u.castling_prev;
  b.halfmove = u.halfmove_prev;
  if (mover == BLACK) b.fullmove--;
  b.side = mover;
  b.key = u.key_prev;
}

bool same_position(const Board& a, const Board& b) {
  for (int c = 0; c < COLOR_NB; c++) {
    for (int p = 0; p < PIECE_TYPE_NB; p++) if (a.pieces[c][p] != b.pieces[c][p]) return false;
    if (a.occ[c] != b.occ[c]) return false;
    if (a.king_sq[c] != b.king_sq[c]) return false;
  }
  for (int s = 0; s < SQ_NB; s++) if (a.mailbox[s] != b.mailbox[s]) return false;
  return a.side == b.side && a.castling == b.castling && a.ep == b.ep &&
         a.halfmove == b.halfmove && a.fullmove == b.fullmove && a.key == b.key;
}
} // namespace kana

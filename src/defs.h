#pragma once
#include <cstdint>
#include <string>

namespace kana {

using Bitboard = uint64_t;

enum Color { WHITE = 0, BLACK = 1, COLOR_NB = 2 };
constexpr Color operator~(Color c) { return Color(c ^ 1); }

enum PieceType { PAWN = 0, KNIGHT = 1, BISHOP = 2, ROOK = 3, QUEEN = 4, KING = 5, PIECE_TYPE_NB = 6 };

enum Square {
  A1, B1, C1, D1, E1, F1, G1, H1,
  A2, B2, C2, D2, E2, F2, G2, H2,
  A3, B3, C3, D3, E3, F3, G3, H3,
  A4, B4, C4, D4, E4, F4, G4, H4,
  A5, B5, C5, D5, E5, F5, G5, H5,
  A6, B6, C6, D6, E6, F6, G6, H6,
  A7, B7, C7, D7, E7, F7, G7, H7,
  A8, B8, C8, D8, E8, F8, G8, H8,
  SQ_NB = 64, SQ_NONE = 64
};

// Compact piece code: 0 = empty, otherwise 1 + 6*color + type (1..12).
constexpr int make_piece(Color c, PieceType pt) { return 1 + 6 * int(c) + int(pt); }
constexpr PieceType piece_type(int p) { return PieceType((p - 1) % 6); }
constexpr Color piece_color(int p) { return Color((p - 1) / 6); }

enum CastlingBits : uint8_t {
  WHITE_OO  = 1,
  WHITE_OOO = 2,
  BLACK_OO  = 4,
  BLACK_OOO = 8
};

// 16-bit move encoding: [0..5 from][6..11 to][12..13 promo(0=N..3=Q)][14..15 flag]
using Move = uint16_t;
enum MoveFlag : int { NORMAL = 0, PROMOTION = 1, EN_PASSANT = 2, CASTLING = 3 };

constexpr Move make_move(Square from, Square to) { return Move(int(from)) | Move(int(to) << 6); }
constexpr Move make_promo(Square from, Square to, PieceType pt) {
  return Move(int(from)) | Move(int(to) << 6) | Move((int(pt) - KNIGHT) << 12) | Move(PROMOTION << 14);
}
constexpr Move make_special(Square from, Square to, MoveFlag f) {
  return Move(int(from)) | Move(int(to) << 6) | Move(int(f) << 14);
}

constexpr Square   move_from(Move m) { return Square(m & 63); }
constexpr Square   move_to(Move m)   { return Square((m >> 6) & 63); }
constexpr PieceType move_promo(Move m) { return PieceType(KNIGHT + ((m >> 12) & 3)); }
constexpr MoveFlag move_flag(Move m) { return MoveFlag((m >> 14) & 3); }

inline std::string square_name(Square s) {
  std::string r;
  r += char('a' + (int(s) & 7));
  r += char('1' + (int(s) >> 3));
  return r;
}

inline std::string move_to_string(Move m) {
  std::string r = square_name(move_from(m)) + square_name(move_to(m));
  if (move_flag(m) == PROMOTION) r += "nbrq"[int(move_promo(m)) - KNIGHT];
  return r;
}

} // namespace kana

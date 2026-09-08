#include "perft.h"
#include "board.h"
#include "movegen.h"

namespace kana {

uint64_t perft(Board& b, int depth) {
  if (depth <= 0) return 1;
  Move moves[256];
  int n = generate_moves(b, moves);
  uint64_t nodes = 0;
  Color us = b.side;
  for (int i = 0; i < n; i++) {
    Undo u;
    make_move(b, moves[i], u);
    if (!attacked_by(b, b.king_sq[int(us)], b.side))
      nodes += perft(b, depth - 1);
    unmake_move(b, moves[i], u);
  }
  return nodes;
}

} // namespace kana

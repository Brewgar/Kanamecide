#pragma once
#include "board.h"
#include "movegen.h"

using namespace kana;

namespace search {

// Plain negamax + alpha-beta, material-only evaluation, no quiescence / TT / ordering.
// Honors DEC-0008: every candidate is filtered with the king-safety test AFTER make_move.
// u is the undo buffer for THIS node's move; recursive calls pass their own locals
// (a single shared undo across recursion would clobber the parent record).
int negamax(Board& b, int depth, int alpha, int beta, Undo& u);

} // namespace search
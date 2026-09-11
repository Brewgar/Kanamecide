#pragma once
#include "board.h"
#include "movegen.h"

using namespace kana;

namespace search {

// O3b — staged move ordering, controlled by ORDER_STAGE (compile-time, default 4):
//   0 = unordered (O3a baseline)   1 = + PV move first (root, shallow-prior pass)
//   2 = + MVV-LVA captures         3 = + killers (2 slots/ply)
//   4 = + history heuristic (quiets)
// negamax: alpha-beta + material-only eval; `nodes` counts every node visited;
// DEC-0008 legality filter applied per candidate AFTER make_move; H-0012 assert live.
// Returns side-to-move score.
int negamax(Board& b, int depth, int alpha, int beta, int ply, uint64_t& nodes);

// Root search: returns the best move (Move 0 if none), fills `score` and `nodes`.
Move bestmove(Board& b, int depth, int& score, uint64_t& nodes);

// Reset per-search ordering tables (history, killers, PV hint).
void clear_ordering();

} // namespace search
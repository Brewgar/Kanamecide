#pragma once
#include "board.h"
#include "movegen.h"

using namespace kana;

namespace search {

// O3c — quiescence search hook. When QSEARCH (compile-time, default 1) is enabled, the
// negamax leaf calls qsearch() which resolves captures/promotions (plus ALL moves when
// in check) to a quiet position instead of returning the static material eval directly.
// O3b-order stages controlled by ORDER_STAGE (see src/search.cpp): 0 unordered, 1 +PV,
// 2 +MVV-LVA, 3 +killers, 4 +history.
int negamax(Board& b, int depth, int alpha, int beta, int ply, uint64_t& nodes);

// Root search: returns the best move (Move 0 if none), fills `score` and `nodes`.
Move bestmove(Board& b, int depth, int& score, uint64_t& nodes);

// Reset per-search ordering tables (history, killers, PV hint).
void clear_ordering();

} // namespace search
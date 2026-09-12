#pragma once
#include <string>
#include <vector>
#include "board.h"
#include "movegen.h"
#include "tt.h"

using namespace kana;

namespace search {

// O3d — iterative deepening + TT + time control + repetition/50-move, on top of the
// O3c qsearch and O3b ordering. This is the complete Phase-2 search stack.
//
// Full search. `max_depth` is the target depth; `time_ms` and `node_limit_in` are 0 for
// none. Emits one `info depth ...` line per completed iteration and returns the root best
// move (last completed iteration; a stopped iteration is discarded unless none finished).
// History (for repetition adjudication) comes from set_game_keys().
Move search_root(Board& b, int max_depth, int time_ms, uint64_t node_limit_in,
                 int& score, uint64_t& nodes, std::string& pv, TTStats& stats);

// Reset per-search ordering/TT state.
void clear_state();

// Provide the actual game's history keys (for threefold repetition adjudication).
void set_game_keys(const std::vector<uint64_t>& keys);

// Stop-flag API (set by `stop`, movetime expiry, or node-limit expiry).
void request_stop();
void clear_stop();

int negamax(Board& b, int depth, int alpha, int beta, int ply, uint64_t& nodes);

} // namespace search
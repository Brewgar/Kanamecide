#pragma once
#include "board.h"

namespace search {

struct TTEntry {
    uint64_t key   = 0;
    int32_t  score = 0;        // mate-shifted, root-relative
    kana::Move best  = 0;
    uint8_t  depth = 0;
    uint8_t  type  = 0;        // 0=exact, 1=upper(fail-low), 2=lower(fail-high)
};
static_assert(sizeof(TTEntry) == 16, "TTEntry packs to 16 B");

struct TTStats {
    uint64_t probes  = 0;
    uint64_t hits    = 0;
    uint64_t stores  = 0;
    uint64_t cutoffs = 0;
};

void    tt_init(size_t megabytes = 64);
void    tt_clear();
int     tt_probe(uint64_t key, int depth, int alpha, int beta, int ply,
                 int& score, kana::Move& best);
void    tt_store(uint64_t key, int depth, int type, int score, int ply, kana::Move best);
TTStats tt_stats();

} // namespace search

import io
TT_H = r'''#pragma once
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
'''

TT_CPP = r'''// O3d transposition table. Fixed size, replace-always, keyed by the 64-bit Zobrist key.
// Mate scores are shifted by ply so a single entry is valid at any depth (H-0009).
// 2-entry buckets; the stored best move is verified in search before being played (DEC-0008).

#include "tt.h"

#include <cstring>
#include <vector>

using namespace kana;

namespace search {

static constexpr int MATE_BOUND = 900000;

namespace {
inline int mate_to(int s, int ply) {
    if (s >  MATE_BOUND) return s + ply;
    if (s < -MATE_BOUND) return s - ply;
    return s;
}
inline int mate_from(int s, int ply) {
    if (s >  MATE_BOUND) return s - ply;
    if (s < -MATE_BOUND) return s + ply;
    return s;
}

struct alignas(64) Bucket {
    TTEntry e[2];   // 2 entries per bucket, replace-always
};
std::vector<Bucket> table;
size_t mask = 0;
TTStats gstats;
} // namespace

void tt_init(size_t megabytes) {
    size_t bytes = megabytes * 1024 * 1024;
    size_t p = 1; while (p * 2 <= bytes / sizeof(Bucket)) p *= 2;
    if (p == 0) p = 1;
    table.resize(p);
    mask = p - 1;
    std::memset(table.data(), 0, table.size() * sizeof(Bucket));
    gstats = TTStats{};
}

void tt_clear() {
    if (table.empty()) return;
    std::memset(table.data(), 0, table.size() * sizeof(Bucket));
    gstats = TTStats{};
}

int tt_probe(uint64_t key, int depth, int alpha, int beta, int ply, int& score, Move& best) {
    gstats.probes++;
    if (key == 0 || mask == 0) return 0;
    const Bucket& bk = table[key & mask];
    for (int i = 0; i < 2; i++) {
        const TTEntry& e = bk.e[i];
        if (e.key != key) continue;
        gstats.hits++;
        if ((int)e.depth >= depth) {
            int sc = mate_from(e.score, ply);
            if (e.type == 0)                { score = sc; gstats.cutoffs++; return 2; }
            if (e.type == 2 && sc >= beta)  { score = sc; gstats.cutoffs++; return 2; }
            if (e.type == 1 && sc <= alpha) { score = sc; gstats.cutoffs++; return 2; }
        }
        best = e.best;
        return 1;
    }
    return 0;
}

void tt_store(uint64_t key, int depth, int type, int score, int ply, Move best) {
    if (key == 0 || mask == 0) return;
    gstats.stores++;
    Bucket& bk = table[key & mask];
    int sc = mate_to(score, ply);
    bk.e[1] = bk.e[0];
    bk.e[0] = TTEntry{key, sc, best, (uint8_t)depth, (uint8_t)type};
}

TTStats tt_stats() { return gstats; }

} // namespace search
'''
with io.open(r"c:\Users\tahae\Kanamecide\src\tt.h", "w", encoding="utf-8", newline="\n") as f:
    f.write(TT_H.replace("\r\n", "\n"))
with io.open(r"c:\Users\tahae\Kanamecide\src\tt.cpp", "w", encoding="utf-8", newline="\n") as f:
    f.write(TT_CPP.replace("\r\n", "\n"))
print("tt.h", len(TT_H), "tt.cpp", len(TT_CPP))

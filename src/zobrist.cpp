#include "zobrist.h"

namespace kana {
namespace zobrist {

Bitboard psq[12][SQ_NB] = {};
Bitboard castling_[16] = {};
Bitboard ep_file[8] = {};
Bitboard side_ = 0;

static uint64_t rng_state = 0x9E3779B97F4A7C15ULL;
static uint64_t splitmix64() {
  uint64_t z = (rng_state += 0x9E3779B97F4A7C15ULL);
  z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
  z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
  return z ^ (z >> 31);
}

static bool initialized = false;
void init() {
  if (initialized) return;
  initialized = true;
  for (int p = 0; p < 12; p++)
    for (int s = 0; s < SQ_NB; s++)
      psq[p][s] = splitmix64();
  for (int i = 0; i < 16; i++) castling_[i] = splitmix64();
  for (int i = 0; i < 8; i++) ep_file[i] = splitmix64();
  side_ = splitmix64();
}

} // namespace zobrist
} // namespace kana

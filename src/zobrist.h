#pragma once
#include "defs.h"

namespace kana {
namespace zobrist {

extern Bitboard psq[12][SQ_NB];
extern Bitboard castling_[16];
extern Bitboard ep_file[8];
extern Bitboard side_;

void init();

} // namespace zobrist
} // namespace kana

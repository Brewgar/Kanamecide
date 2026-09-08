#include <cstdio>
#include <cstring>
#include "board.h"
#include "movegen.h"
#include "perft.h"
#include "zobrist.h"
#include <cstdint>

using namespace kana;

static void dump_moves(const Board& b) {
  Move moves[256];
  int n = generate_moves(b, moves);
  printf("%d legal moves:\n", n);
  for (int i = 0; i < n; i++)
    printf("  %d: %s\n", i + 1, move_to_string(moves[i]).c_str());
}

static Board board_55() { Board b; std::memset(&b, 0, sizeof(b)); return b; }

static bool run_perft(Board& b, const char* name, int depth, uint64_t expected) {
  set_startpos(b);
  uint64_t got = perft(b, depth);
  const char* status = (got == expected) ? "PASS" : "FAIL";
  printf("%-4s %-22s d=%2d  got=%-11llu expected=%-11llu %llu diff\n", status, name, depth,
         (unsigned long long)got, (unsigned long long)expected,
         (unsigned long long)(got > expected ? got - expected : expected - got));
  return got == expected;
}

int main(int argc, char** argv) {
  bool list_moves = (argc > 1 && strcmp(argv[1], "--moves") == 0);
  bool fen_mode   = (argc > 1 && strcmp(argv[1], "--fen") == 0);

  bitboards_init();
  kana::zobrist::init();

  if (list_moves) {
    Board b;
    set_startpos(b);
    dump_moves(b);
    return 0;
  }

  if (fen_mode) {
    if (argc < 3) { fprintf(stderr, "Usage: kana.exe --fen <FEN> [depth]\n"); return 2; }
    Board b;
    set_fen(b, argv[2]);
    int depth = (argc > 3) ? atoi(argv[3]) : 1;
    if (depth == 1) {
      uint64_t n = perft(b, 1);
      printf("%llu nodes at depth 1 from %s\n", (unsigned long long)n, argv[2]);
      dump_moves(b);
      return 0;
    }
    // proper depth split table (with legality filtering on root moves)
    Board b2;
    b2 = b;
    Move moves[256];
    int n = generate_moves(b2, moves);
    uint64_t total = 0;
    printf("Depth-%d split for %s (%d roots):\n", depth, argv[2], n);
    for (int i = 0; i < n; i++) {
      Undo u;
      make_move(b2, moves[i], u);
      if (!attacked_by(b2, b2.king_sq[int(b.side)], b2.side)) {  // root move must be legal
        uint64_t sub = perft(b2, depth - 1);
        total += sub;
        printf("  %2d: %s -> %11llu\n", i + 1, move_to_string(moves[i]).c_str(), (unsigned long long)sub);
      }
      unmake_move(b2, moves[i], u);
    }
    printf("  TOTAL: %11llu\n", (unsigned long long)total);
    dump_moves(b);  // show root move list once more
    return 0;
  }

  printf("Kana — chess engine correctness test harness\n");
  printf("CPU: AMD Ryzen 7 9700X (8C/16T, AVX-512)\n");
  printf("Target: correct move generation + make/unmake validated by perft\n\n");

  bitboards_init();
  kana::zobrist::init();

  static_assert(SQ_NB == 64, "square count");
  static_assert(PIECE_TYPE_NB == 6, "piece types");
  static_assert(COLOR_NB == 2, "colors");

  uint64_t all_ok = true;
  Board b0 = board_55();
  all_ok &= run_perft(b0, "startpos", 1, 20);
  b0 = board_55();
  all_ok &= run_perft(b0, "startpos", 2, 400);
  b0 = board_55();
  all_ok &= run_perft(b0, "startpos", 3, 8902);
  b0 = board_55();
  all_ok &= run_perft(b0, "startpos", 4, 197281);
  b0 = board_55();
  all_ok &= run_perft(b0, "startpos", 5, 4865609);

  // Kiwipete (CPW position 1)
  {
    Board b;
    set_fen(b, "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1");
    uint64_t got = perft(b, 3);
    printf("%-4s %-22s d=%2d  got=%-11llu expected=%-11llu %llu diff\n",
           (got == 97862) ? "PASS" : "FAIL", "kiwipete", 3,
           (unsigned long long)got, 97862ULL, 0ULL);
    all_ok &= (got == 97862);
  }

  // CPW position 3: en passant / pins
  {
    Board b;
    set_fen(b, "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1");
    uint64_t got = perft(b, 4);
    printf("%-4s %-22s d=%2d  got=%-11llu expected=%-11llu %llu diff\n",
           (got == 43238) ? "PASS" : "FAIL", "cpw_pos3_epins", 4,
           (unsigned long long)got, 43238ULL, 0ULL);
    all_ok &= (got == 43238);
  }

  // CPW position 4: promotions
  {
    Board b;
    set_fen(b, "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1");
    uint64_t got = perft(b, 4);
    printf("%-4s %-22s d=%2d  got=%-11llu expected=%-11llu %llu diff\n",
           (got == 422333) ? "PASS" : "FAIL", "cpw_pos4_promo", 4,
           (unsigned long long)got, 422333ULL, 0ULL);
    all_ok &= (got == 422333);
  }

  // CPW position 5: promotions
  {
    Board b;
    set_fen(b, "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8");
    uint64_t got = perft(b, 4);
    printf("%-4s %-22s d=%2d  got=%-11llu expected=%-11llu %llu diff\n",
           (got == 2103487) ? "PASS" : "FAIL", "cpw_pos5_promo", 4,
           (unsigned long long)got, 2103487ULL, 0ULL);
    all_ok &= (got == 2103487);
  }

  // CPW position 6: quiet
  {
    Board b;
    set_fen(b, "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10");
    uint64_t got = perft(b, 4);
    printf("%-4s %-22s d=%2d  got=%-11llu expected=%-11llu %llu diff\n",
           (got == 3894594) ? "PASS" : "FAIL", "cpw_pos6_quiet", 4,
           (unsigned long long)got, 3894594ULL, 0ULL);
    all_ok &= (got == 3894594);
  }

  printf("\n=== %s\n", all_ok ? "ALL TESTS PASSED" : "TESTS FAILED");
  return all_ok ? 0 : 1;
}

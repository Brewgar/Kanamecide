#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <iostream>
#include <string>
#include <sstream>
#include "board.h"
#include "movegen.h"
#include "perft.h"
#include "zobrist.h"
#include "bench.h"
#include "search.h"
#include <cstdint>

using namespace kana;

// --- O3a minimal UCI -----------------------------------------------------------
// Deliberately minimal: uci / isready / ucinewgame / position / go depth N / stop / quit.
// Full time control (movetime, wtime/btime, etc.) is O3d — not here.

static constexpr int MATE = 1000000;
static constexpr int INF  = 2000000;

static Move parse_move(Board& b, const std::string& token) {
    // token like "e2e4" or "e7e8q"; find the matching pseudo-legal move and verify legality.
    if (token.size() < 4) return 0;
    int f = (token[0] - 'a') + 8 * (token[1] - '1');
    int t = (token[2] - 'a') + 8 * (token[3] - '1');
    if (f < 0 || f > 63 || t < 0 || t > 63) return 0;
    PieceType promo = PIECE_TYPE_NB;
    if (token.size() >= 5) {
        switch (token[4]) {
            case 'n': promo = KNIGHT; break;
            case 'b': promo = BISHOP; break;
            case 'r': promo = ROOK; break;
            case 'q': promo = QUEEN; break;
            default: return 0;
        }
    }
    Move moves[256];
    int n = generate_moves(b, moves);
    for (int i = 0; i < n; i++) {
        if (int(move_from(moves[i])) != f || int(move_to(moves[i])) != t) continue;
        if (move_flag(moves[i]) == PROMOTION && move_promo(moves[i]) != promo) continue;
        if (move_flag(moves[i]) != PROMOTION && promo != PIECE_TYPE_NB) continue;
        // legality (DEC-0008)
        Undo u;
        make_move(b, moves[i], u);
        Color us = ~b.side;
        bool legal = !attacked_by(b, b.king_sq[us], b.side);
        unmake_move(b, moves[i], u);
        if (legal) return moves[i];
    }
    return 0;
}

static Move search_root(Board& b, int depth, int& nodes) {
    Move moves[256];
    int n = generate_moves(b, moves);
    int best = -INF;
    Move bestmove = 0;
    int legal = 0;
    nodes = 0;
    for (int i = 0; i < n; i++) {
        Undo u;
        make_move(b, moves[i], u);
        Color us = ~b.side;
        if (!attacked_by(b, b.king_sq[us], b.side)) {
            legal++;
            Undo child_u;
            int score = -search::negamax(b, depth - 1, -INF, INF, child_u);
            if (score > best || bestmove == 0) {
                best = score;
                bestmove = moves[i];
            }
        }
        unmake_move(b, moves[i], u);
    }
    if (bestmove == 0 && n > 0) bestmove = moves[0]; // fallback (shouldn't happen in legal pos)
    return bestmove;
}

static void run_uci() {
    Board board;
    set_startpos(board);
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream iss(line);
        std::string token;
        iss >> token;
        if (token == "uci") {
            printf("id name Kanamecide\n");
            printf("id author Kanamecide-collective\n");
            printf("uciok\n");
        } else if (token == "isready") {
            printf("readyok\n");
        } else if (token == "ucinewgame" || token == "setoption") {
            set_startpos(board);
        } else if (token == "position") {
            std::string pos;
            iss >> pos;
            if (pos == "startpos") {
                set_startpos(board);
            } else if (pos == "fen") {
                // read up to 6 FEN fields, stopping at "moves" or end-of-stream
                std::string fen, w;
                int fields = 0;
                while (fields < 6 && iss >> w) {
                    if (w == "moves") break;
                    fen += w;
                    fen += ' ';
                    fields++;
                }
                if (!fen.empty())
                    fen.pop_back(); // drop trailing space
                set_fen(board, fen);
            }
            // apply trailing "moves ..." (re-split the whole line for simplicity)
            std::string mv;
            bool in_moves = false;
            std::istringstream lss(line);
            while (lss >> mv) {
                if (mv == "moves") { in_moves = true; continue; }
                if (in_moves) {
                    Move m = parse_move(board, mv);
                    if (m) { Undo u; make_move(board, m, u); }
                }
            }
        } else if (token == "go") {
            std::string what;
            int depth = 4;
            while (iss >> what) {
                if (what == "depth") { iss >> depth; break; }
            }
            int nodes = 0;
            Move best = search_root(board, depth, nodes);
            if (best == 0) best = 0;
            printf("bestmove %s\n", move_to_string(best ? best : Move(0)).c_str());
        } else if (token == "stop") {
            // O3a has no search thread to interrupt; no-op (time control is O3d).
        } else if (token == "quit") {
            break;
        }
        fflush(stdout);
    }
}

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
  bool bench_mode = (argc > 1 && strcmp(argv[1], "--bench") == 0);
  bool audit_mode = (argc > 1 && strcmp(argv[1], "--audit") == 0);
  bool uci_mode   = (argc > 1 && strcmp(argv[1], "uci") == 0);

  bitboards_init();
  kana::zobrist::init();

  if (uci_mode) {
    run_uci();
    return 0;
  }

  if (bench_mode) {
    int reps = (argc > 2) ? atoi(argv[2]) : 5;
    if (reps < 1) reps = 1;
    return run_bench(reps);
  }

  if (audit_mode) {
#ifdef NDEBUG
    printf("state audit is compiled out under NDEBUG — build Debug to run it.\n");
    return 0;
#else
    int rc = run_state_audit();
    printf("=== %s\n", rc == 0 ? "STATE AUDIT PASSED" : "STATE AUDIT FAILED");
    return rc;
#endif
  }

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

  static_assert(SQ_NB == 64, "square count");
  static_assert(PIECE_TYPE_NB == 6, "piece types");
  static_assert(COLOR_NB == 2, "colors");

  uint64_t all_ok = 1;
  Board b0 = board_55();
  all_ok &= run_perft(b0, "startpos", 1, 20) ? 1ULL : 0ULL;
  b0 = board_55();
  all_ok &= run_perft(b0, "startpos", 2, 400) ? 1ULL : 0ULL;
  b0 = board_55();
  all_ok &= run_perft(b0, "startpos", 3, 8902) ? 1ULL : 0ULL;
  b0 = board_55();
  all_ok &= run_perft(b0, "startpos", 4, 197281) ? 1ULL : 0ULL;
  b0 = board_55();
  all_ok &= run_perft(b0, "startpos", 5, 4865609) ? 1ULL : 0ULL;

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

#ifndef NDEBUG
  {
    // H-0014/H-0012 guardrails: state-integrity audit (same_position + key==compute_key
    // round-trip walk) is a debug-only gate; compiled out of Release.
    int rc = run_state_audit();
    all_ok &= (rc == 0);
    printf("\n=== %s\n", rc == 0 ? "STATE AUDIT PASSED" : "STATE AUDIT FAILED");
  }
#endif

  printf("\n=== %s\n", all_ok ? "ALL TESTS PASSED" : "TESTS FAILED");
  return all_ok ? 0 : 1;
}

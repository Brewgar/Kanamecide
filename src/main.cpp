#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <iostream>
#include <string>
#include <sstream>
#include <chrono>
#include "board.h"
#include "movegen.h"
#include "perft.h"
#include "zobrist.h"
#include "bench.h"
#include "search.h"
#include <cstdint>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <deque>
#include <atomic>

using namespace kana;

// --- O3a minimal UCI -----------------------------------------------------------
// Deliberately minimal: uci / isready / ucinewgame / position / go depth N / stop / quit.
// Full time control (movetime, wtime/btime, etc.) is O3d — not here.

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

static std::mutex              g_qmtx;
static std::condition_variable g_qcv;
static std::deque<std::string> g_q;

static std::string read_line() {
    std::unique_lock lk(g_qmtx);
    g_qcv.wait(lk, []{ return !g_q.empty(); });
    std::string s = g_q.front(); g_q.pop_front();
    return s;
}

static void reader_loop() {
    std::string line;
    while (std::getline(std::cin, line)) {
        { std::lock_guard lk(g_qmtx); g_q.push_back(line); }
        g_qcv.notify_one();
    }
}

static void run_uci() {
    Board board;
    std::vector<uint64_t> game_keys;
    set_startpos(board);
    game_keys.push_back(board.key);
    std::thread reader(reader_loop);
    bool quit_requested = false;

    while (!quit_requested) {
        std::string line = read_line();
        std::istringstream iss(line);
        std::string token;
        iss >> token;

        if (token == "uci") {
            printf("id name Kanamecide\n");
            printf("id author Kanamecide-collective\n");
            printf("option name Hash type spin default 64 min 1 max 1024\n");
            printf("uciok\n");
        } else if (token == "isready") {
            printf("readyok\n");
        } else if (token == "ucinewgame") {
            { std::lock_guard lk(g_qmtx); game_keys.clear(); }
            set_startpos(board);
            game_keys.push_back(board.key);
            search::tt_clear();
            search::clear_state();
        } else if (token == "setoption") {
            std::string n, v;
            if (iss >> n >> v && n == "Hash") {
                int mb = atoi(v.c_str());
                if (mb < 1) mb = 1;
                search::tt_init((size_t)mb);
            }
        } else if (token == "position") {
            std::string pos; iss >> pos;
            if (pos == "startpos") { set_startpos(board); game_keys = std::vector<uint64_t>{board.key}; }
            else if (pos == "fen") {
                std::string fen, w; int fields = 0;
                while (fields < 6 && (iss >> w)) { if (w == "moves") break; fen += w; fen += ' '; fields++; }
                if (!fen.empty()) { fen.pop_back(); set_fen(board, fen); }
                game_keys = std::vector<uint64_t>{board.key};
            }
            {
                std::string mv; bool in_moves = false;
                std::istringstream lss(line); std::string first; lss >> first;
                while (lss >> mv) {
                    if (mv == "moves") { in_moves = true; continue; }
                    if (in_moves) {
                        Move m = parse_move(board, mv);
                        if (m) { Undo u; make_move(board, m, u); game_keys.push_back(board.key); }
                    }
                }
            }
        } else if (token == "go") {
            std::string w; int depth = 0; uint64_t node_limit = 0;
            int movetime = 0, wtime = 0, btime = 0, winc = 0, binc = 0;
            while (iss >> w) {
                if (w == "depth")      iss >> depth;
                else if (w == "nodes") iss >> node_limit;
                else if (w == "movetime") iss >> movetime;
                else if (w == "wtime")  iss >> wtime;
                else if (w == "btime")  iss >> btime;
                else if (w == "winc")   iss >> winc;
                else if (w == "binc")   iss >> binc;
            }
            int our_time = (board.side == WHITE) ? wtime : btime;
            int our_inc  = (board.side == WHITE) ? winc : binc;
            int time_ms  = 0;
            if (movetime > 0) time_ms = movetime;
            else if (our_time > 0) { time_ms = our_time / 30 + our_inc - 50; if (time_ms < 10) time_ms = 10; }
            if (depth <= 0) depth = (time_ms > 0) ? 256 : 4;

            search::set_game_keys(game_keys);
            int score = 0; uint64_t nodes = 0; std::string pv; search::TTStats stats;
            Move best = 0;
            std::atomic<bool> done{false};
            std::thread searcher([&]{
                best = search::search_root(board, depth, time_ms, node_limit, score, nodes, pv, stats);
                done.store(true, std::memory_order_relaxed);
            });
            while (!done.load(std::memory_order_relaxed)) {
                {
                    std::unique_lock lk(g_qmtx);
                    g_qcv.wait_for(lk, std::chrono::milliseconds(2), []{ return !g_q.empty(); });
                    while (!g_q.empty()) {
                        std::istringstream si(g_q.front()); std::string t; si >> t;
                        if (t == "stop")      { search::request_stop(); g_q.pop_front(); }
                        else if (t == "quit") { search::request_stop(); quit_requested = true; g_q.pop_front(); }
                        else break;
                    }
                }
                std::this_thread::yield();
            }
            searcher.join();
            printf("bestmove %s\n", move_to_string(best).c_str());
        } else if (token == "stop") {
            // No search running: nothing to interrupt.
        } else if (token == "quit") {
            quit_requested = true;
        }
        fflush(stdout);
    }
    if (reader.joinable()) reader.detach();
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
  search::tt_init(64);

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

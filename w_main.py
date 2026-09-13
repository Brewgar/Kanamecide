import io
p = r"c:\Users\tahae\Kanamecide\src\main.cpp"
raw = open(p, "r", encoding="utf-8", newline="").read()

raw = raw.replace('#include <cstdint>\r\n',
 '#include <cstdint>\r\n#include <thread>\r\n#include <mutex>\r\n#include <condition_variable>\r\n#include <deque>\r\n#include <atomic>\r\n', 1)

raw = raw.replace('  kana::zobrist::init();\r\n',
                  '  kana::zobrist::init();\r\n  search::tt_init(64);\r\n', 1)

NEW = r'''static std::mutex              g_qmtx;
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
'''
NEW_CRLF = '\r\n'.join(NEW.split('\n'))

start = raw.index('static void run_uci() {')
end = raw.index('static void dump_moves', start)
raw = raw[:start] + NEW_CRLF + raw[end:]
open(p, "w", encoding="utf-8", newline="").write(raw)
print("main.cpp patched")

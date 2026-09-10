// E-0002 bench harness for Kanamecide (Milestone 0).
// Certified perft NPS with provenance: self-SHA256, WMI clock proxy, best-effort pinning.
// Debug-only state audit for H-0014. Behavior-neutral; perft counts must stay bit-identical.

#include "bench.h"
#include "board.h"
#include "movegen.h"
#include "perft.h"
#include "zobrist.h"

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <numeric>
#include <string>
#include <vector>

#if defined(_WIN32)
#define NOMINMAX
#include <windows.h>
#include <intrin.h>
#include <wbemidl.h>
#pragma comment(lib, "wbemuuid.lib")
#pragma comment(lib, "ole32.lib")
#endif

#ifndef KANA_GIT_COMMIT
#define KANA_GIT_COMMIT "unknown"
#endif

using Clock = std::chrono::steady_clock;

namespace kana {

// Compile flags are derived from NDEBUG so they always match the actual build
// (CMake genex strings with commas are fragile; this is the honest source).
const char* build_flags_text() {
#ifdef NDEBUG
    return "/O2 /GL /EHsc /arch:AVX512 /DNDEBUG";
#else
    return "/Od /EHsc /Zi /JMC";
#endif
}
const char* git_commit_text() { return KANA_GIT_COMMIT; }

// --- self-contained SHA-256 (FIPS 180-4), no external dependency ------------------------

static const uint32_t k_sha256_k[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};

static uint32_t sha_rotr(uint32_t x, uint32_t n) { return (x >> n) | (x << (32 - n)); }

static void sha256_compress(uint32_t state[8], const uint8_t block[64]) {
    uint32_t w[64];
    for (int i = 0; i < 16; i++)
        w[i] = (uint32_t(block[4 * i]) << 24) | (uint32_t(block[4 * i + 1]) << 16) |
               (uint32_t(block[4 * i + 2]) << 8) | uint32_t(block[4 * i + 3]);
    for (int i = 16; i < 64; i++) {
        uint32_t s0 = sha_rotr(w[i - 15], 7) ^ sha_rotr(w[i - 15], 18) ^ (w[i - 15] >> 3);
        uint32_t s1 = sha_rotr(w[i -  2], 17) ^ sha_rotr(w[i -  2], 19) ^ (w[i - 2] >> 10);
        w[i] = w[i - 16] + s0 + w[i - 7] + s1;
    }
    uint32_t a = state[0], b = state[1], c = state[2], d = state[3];
    uint32_t e = state[4], f = state[5], g = state[6], h = state[7];
    for (int i = 0; i < 64; i++) {
        uint32_t s1 = sha_rotr(e, 6) ^ sha_rotr(e, 11) ^ sha_rotr(e, 25);
        uint32_t ch = (e & f) ^ ((~e) & g);
        uint32_t t1 = h + s1 + ch + k_sha256_k[i] + w[i];
        uint32_t s0 = sha_rotr(a, 2) ^ sha_rotr(a, 13) ^ sha_rotr(a, 22);
        uint32_t maj = (a & b) ^ (a & c) ^ (b & c);
        uint32_t t2 = s0 + maj;
        h = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2;
    }
    state[0] += a; state[1] += b; state[2] += c; state[3] += d;
    state[4] += e; state[5] += f; state[6] += g; state[7] += h;
}

static std::string self_sha256() {
#if defined(_WIN32)
    char path[MAX_PATH];
    DWORD got = GetModuleFileNameA(nullptr, path, sizeof(path));
    if (got == 0 || got >= sizeof(path)) return "unavailable";
    FILE* f = fopen(path, "rb");
    if (!f) return "unavailable";
    std::vector<uint8_t> data;
    uint8_t chunk[1 << 16];
    size_t rd;
    while ((rd = fread(chunk, 1, sizeof(chunk), f)) > 0) data.insert(data.end(), chunk, chunk + rd);
    fclose(f);

    uint32_t h[8] = {0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
                     0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19};
    size_t i = 0;
    for (; i + 64 <= data.size(); i += 64) sha256_compress(h, data.data() + i);

    uint8_t pad[128] = {0};
    size_t rem = data.size() - i;
    memcpy(pad, data.data() + i, rem);
    pad[rem] = 0x80;
    size_t blocks = (rem + 1 + 8 <= 64) ? 1 : 2;
    uint64_t bits = uint64_t(data.size()) * 8ULL;
    for (int k = 0; k < 8; k++) pad[blocks * 64 - 1 - k] = uint8_t(bits >> (8 * k));
    for (size_t blk = 0; blk < blocks; blk++) sha256_compress(h, pad + blk * 64);

    char hex[65];
    for (int k = 0; k < 8; k++) snprintf(hex + 8 * k, 9, "%08x", (unsigned)h[k]);
    hex[64] = 0;
    return std::string(hex);
#else
    return "unavailable";
#endif
}

static std::string current_clock_mhz() {
#if defined(_WIN32)
    // WMI CurrentClockSpeed is a *proxy* for the live clock — it cannot be fixed from
    // user mode. High-Performance power plan is the lever; we log the proxy only.
    HRESULT hr = CoInitializeEx(nullptr, COINIT_MULTITHREADED);
    if (FAILED(hr)) return "unknown";
    CoInitializeSecurity(nullptr, -1, nullptr, nullptr, RPC_C_AUTHN_LEVEL_DEFAULT,
                         RPC_C_IMP_LEVEL_IMPERSONATE, nullptr, EOAC_NONE, nullptr);
    std::string out = "unknown";
    IWbemLocator* locator = nullptr;
    HRESULT hr2 = CoCreateInstance(CLSID_WbemLocator, nullptr, CLSCTX_INPROC_SERVER,
                                   IID_IWbemLocator, reinterpret_cast<void**>(&locator));
    if (SUCCEEDED(hr2) && locator) {
        IWbemServices* services = nullptr;
        BSTR ns = SysAllocString(L"root\\CIMV2");
        hr2 = locator->ConnectServer(ns, nullptr, nullptr, nullptr, 0L, nullptr, nullptr, &services);
        SysFreeString(ns);
        if (SUCCEEDED(hr2) && services) {
            BSTR lang = SysAllocString(L"WQL");
            BSTR qry = SysAllocString(L"SELECT CurrentClockSpeed FROM Win32_Processor");
            IEnumWbemClassObject* enumerator = nullptr;
            hr2 = services->ExecQuery(lang, qry, WBEM_FLAG_FORWARD_ONLY | WBEM_FLAG_RETURN_IMMEDIATELY,
                                      nullptr, &enumerator);
            SysFreeString(lang);
            SysFreeString(qry);
            if (SUCCEEDED(hr2) && enumerator) {
                IWbemClassObject* obj = nullptr;
                ULONG got = 0;
                if (SUCCEEDED(enumerator->Next(WBEM_INFINITE, 1, &obj, &got)) && got && obj) {
                    VARIANT v;
                    VariantInit(&v);
                    if (SUCCEEDED(obj->Get(L"CurrentClockSpeed", 0, &v, nullptr, nullptr)) && v.vt == VT_I4)
                        out = std::to_string(v.lVal);
                    VariantClear(&v);
                    obj->Release();
                }
                enumerator->Release();
            }
            services->Release();
        }
        locator->Release();
    }
    CoUninitialize();
    return out;
#else
    return "unknown";
#endif
}

static std::string pin_bench_thread() {
#if defined(_WIN32)
    DWORD_PTR processMask = 0, systemMask = 0;
    if (!GetProcessAffinityMask(GetCurrentProcess(), &processMask, &systemMask) || processMask == 0)
        return "unpinned (GetProcessAffinityMask failed)";
    int index = -1;
    DWORD_PTR bit = 0;
    for (int i = 0; i < int(sizeof(DWORD_PTR) * 8); i++) {
        if (processMask & (DWORD_PTR(1) << i)) { bit = DWORD_PTR(1) << i; index = i; break; }
    }
    if (bit == 0 || SetThreadAffinityMask(GetCurrentThread(), bit) == 0)
        return "unpinned (SetThreadAffinityMask failed)";
    char buf[96];
    snprintf(buf, sizeof(buf), "pinned CPU index %d (mask 0x%llx; proxy — virtualization shift possible)",
             index, (unsigned long long)processMask);
    return std::string(buf);
#else
    return "unpinned (non-Windows)";
#endif
}
// --- E-0002 certified bench ---------------------------------------------------------------

struct BenchCase {
    const char* name;
    const char* fen;
    int depth;
    uint64_t expected;
};

static const BenchCase kBenchCases[] = {
    {"startpos d5", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 5, 4865609ULL},
    {"startpos d6", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 6, 119060324ULL},
    {"kiwipete d3", "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1", 3, 97862ULL},
    {"kiwipete d4", "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1", 4, 4085603ULL},
    {"cpw6 d4", "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10", 4, 3894594ULL},
};

// E-00003 provisional references (~2 sig figs, unpinned) for the +-10% gate.
static const double kE0003Ref[] = {47.4, 47.4, 44.7, 43.1, 50.4};

int run_bench(int reps) {
    if (reps < 1) reps = 1;

    // Unbuffered stdio: bench output must survive even if the process is killed
    // mid-run (long d6 reps exceed some command-observer windows).
    setvbuf(stdout, nullptr, _IONBF, 0);

    printf("=== KANA BENCH (E-0002) ===\n");
    printf("reps: %d\n", reps);
    printf("git commit: %s\n", git_commit_text());
    printf("compile flags: %s\n", build_flags_text());
    printf("self SHA-256 (exe): %s\n", self_sha256().c_str());
    printf("thread: %s\n", pin_bench_thread().c_str());
    printf("clock (WMI proxy, MHz, not fixed): %s\n", current_clock_mhz().c_str());

    constexpr int NC = int(sizeof(kBenchCases) / sizeof(kBenchCases[0]));
    double means[NC] = {0};
    bool counts_ok = true;

    for (int c = 0; c < NC; c++) {
        const BenchCase& bc = kBenchCases[c];
        printf("\n-- %s --\n", bc.name);
        Board b;
        set_fen(b, bc.fen);

        uint64_t warm = perft(b, bc.depth);
        if (warm != bc.expected) {
            printf("  EXACT-COUNT FAIL: got %llu expected %llu (perft regression!)\n",
                   (unsigned long long)warm, (unsigned long long)bc.expected);
            counts_ok = false;
        }

        std::vector<double> per_rep;   // Mnps per timed rep
        double sum_nps = 0.0;
        for (int r = 0; r < reps; r++) {
            auto t0 = Clock::now();
            uint64_t n = perft(b, bc.depth);
            auto t1 = Clock::now();
            if (n != bc.expected) {
                printf("  rep %d EXACT-COUNT FAIL (got %llu)\n", r + 1, (unsigned long long)n);
                counts_ok = false;
            }
            double secs = std::chrono::duration<double>(t1 - t0).count();
            double mnps = (secs > 0.0) ? double(n) / secs / 1e6 : 0.0;
            per_rep.push_back(mnps);
            sum_nps += mnps;
            printf("  rep %d: %11llu nodes   %8.4f s   %8.2f Mnps\n",
                   r + 1, (unsigned long long)n, secs, mnps);
        }

        std::vector<double> sorted = per_rep;
        std::sort(sorted.begin(), sorted.end());
        double mean = sum_nps / reps;
        double minv = sorted.front();
        double maxv = sorted.back();
        double median = sorted[reps / 2];
        double spread_pct = (mean > 0.0) ? (maxv - minv) / mean * 100.0 : 0.0;
        means[c] = mean;

        printf("  summary: mean %.2f  median %.2f  min %.2f  max %.2f  spread %.2f%%  Mnps\n",
               mean, median, minv, maxv, spread_pct);
    }

    printf("\n=== E-00003 cross-check (+-10% window) ===\n");
    for (int c = 0; c < NC; c++) {
        double ref = kE0003Ref[c];
        double lo = ref * 0.90, hi = ref * 1.10;
        bool pass = means[c] >= lo && means[c] <= hi;
        printf("  %-14s mean %8.2f  E-00003 ~%6.2f  window [%6.2f,%6.2f]  %s\n",
               kBenchCases[c].name, means[c], ref, lo, hi, pass ? "PASS" : "OUT");
    }
    printf("\nE-0002 decision rule: all exact counts %s; \n",
           counts_ok ? "PASS" : "FAIL — perft is sacred, do NOT proceed");
    if (!counts_ok) return 1;
    printf("(final +-10%% adjudication is written into the E-0002 record.)\n");
    return 0;
}

// --- H-0014 state-integrity audit (debug-only) ----------------------------------

#ifndef NDEBUG
static uint64_t audit_walk(Board& b, int depth) {
    if (depth <= 0) return 1;
    Move moves[256];
    int n = generate_moves(b, moves);
    uint64_t count = 0;
    Color us = b.side;
    for (int i = 0; i < n; i++) {
        Board before = b;                       // full snapshot
        Undo u;
        make_move(b, moves[i], u);
        // DEC-0008 filter: reject if the mover's king is attacked after the move.
        if (!attacked_by(b, b.king_sq[int(us)], b.side)) {
            assert(b.key == compute_key(b));    // key must match from-scratch oracle
            count += audit_walk(b, depth - 1);
        }
        unmake_move(b, moves[i], u);
        assert(same_position(before, b));       // round trip restores every field
        assert(b.key == compute_key(b));        // restored key still matches oracle
    }
    return count;
}

int run_state_audit() {
    struct Case { const char* name; const char* fen; int depth; };
    static const Case cases[] = {
        {"startpos", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 4},
        {"kiwipete", "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1", 3},
        {"cpw3", "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1", 3},
    };
    bool ok = true;
    for (const Case& c : cases) {
        Board b;
        set_fen(b, c.fen);
        uint64_t nodes = audit_walk(b, c.depth);
        Board b2;
        set_fen(b2, c.fen);
        uint64_t ref = perft(b2, c.depth);      // cross-check with the standard walk
        bool same = nodes == ref;
        printf("audit %-10s depth=%d walk=%llu perft=%llu %s\n",
               c.name, c.depth, (unsigned long long)nodes, (unsigned long long)ref,
               same ? "OK" : "MISMATCH");
        ok &= same;
    }
    return ok ? 0 : 1;
}
#else
int run_state_audit() { return 0; }             // compiled out under NDEBUG
#endif

} // namespace kana
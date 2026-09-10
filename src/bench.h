#pragma once

namespace kana {

// E-0002 bench harness (Milestone 0). Best-effort pinned, WMI-clock-proxied perft NPS
// with self-SHA256 provenance. Calls assume bitboards/zobrist are already initialized.
int run_bench(int reps);

// H-0014 debug-only state-integrity audit: make/unmake round trip over a perft walk
// asserting same_position(before, after) and key == compute_key at every node.
// Compiled out (returns 0) under NDEBUG.
int run_state_audit();

// Provenance strings (defined from KANA_GIT_COMMIT / KANA_BUILD_FLAGS in CMake).
const char* build_flags_text();
const char* git_commit_text();

} // namespace kana
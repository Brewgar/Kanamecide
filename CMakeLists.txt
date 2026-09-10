cmake_minimum_required(VERSION 3.15)
project(kana LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(kana
  src/bitboard.cpp
  src/zobrist.cpp
  src/board.cpp
  src/movegen.cpp
  src/perft.cpp
  src/bench.cpp
  src/main.cpp
)

target_compile_options(kana PRIVATE /W4 /EHsc
  $<$<CONFIG:Debug>:/Od /Zi /JMC>
  $<$<CONFIG:Release>:/O2 /GL /arch:AVX512 /DNDEBUG>)
target_link_options(kana PRIVATE
  $<$<CONFIG:Debug>:/DEBUG>
  $<$<CONFIG:Release>:/LTCG>)
set_target_properties(kana PROPERTIES INTERPROCEDURAL_OPTIMIZATION_RELEASE YES)

# --- E-0002 build metadata (for --bench provenance) ---
# git commit hash of the source tree this build came from.
execute_process(
  COMMAND git rev-parse --short HEAD
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  OUTPUT_VARIABLE KANA_GIT_COMMIT
  OUTPUT_STRIP_TRAILING_WHITESPACE
  ERROR_QUIET)
if(NOT KANA_GIT_COMMIT)
  set(KANA_GIT_COMMIT "unknown")
endif()

target_compile_definitions(kana PRIVATE
  KANA_GIT_COMMIT=\"${KANA_GIT_COMMIT}\")

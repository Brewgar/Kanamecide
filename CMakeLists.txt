cmake_minimum_required(VERSION 3.15)
project(kana LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# O3b: move-ordering stage, 0..4 (see src/search.cpp). Default = full ordering.
set(ORDER_STAGE "4" CACHE STRING "Move-ordering stage (0=unordered,1=PV,2=MVV-LVA,3=killers,4=history)")
set(QSEARCH "1" CACHE STRING "Quiescence at leaf (1=on, 0=off for O3b baseline)")

# O3b: add an "Audit" configuration = /O2 WITHOUT NDEBUG (asserts live) and no /DEBUG
# pdb, because Device Guard on this machine blocks any /DEBUG-flagged executable.
set(CMAKE_CONFIGURATION_TYPES "Debug;Release;Audit" CACHE STRING "" FORCE)
set(CMAKE_CXX_FLAGS_AUDIT "/O2 /Ob2 /MD /EHsc" CACHE STRING "" FORCE)
set(CMAKE_EXE_LINKER_FLAGS_AUDIT "" CACHE STRING "" FORCE)

add_executable(kana
  src/bitboard.cpp
  src/zobrist.cpp
  src/board.cpp
  src/movegen.cpp
  src/perft.cpp
  src/bench.cpp
  src/search.cpp
  src/main.cpp
)

target_compile_options(kana PRIVATE /W4 /EHsc
  $<$<CONFIG:Debug>:/Od /Zi /JMC>
  $<$<CONFIG:Release>:/O2 /GL /arch:AVX512 /DNDEBUG>
  $<$<CONFIG:Audit>:/O2 /arch:AVX512>)
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
  KANA_GIT_COMMIT=\"${KANA_GIT_COMMIT}\"
  ORDER_STAGE=${ORDER_STAGE}
  QSEARCH=${QSEARCH})

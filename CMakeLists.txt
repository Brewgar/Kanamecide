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
  src/main.cpp
)

target_compile_options(kana PRIVATE /W4 /Od /Zi /EHsc /JMC)
target_link_options(kana PRIVATE /DEBUG)

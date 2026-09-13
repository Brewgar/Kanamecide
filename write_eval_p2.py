#!/usr/bin/env python3
"""Append PSTs to eval.cpp."""

lines = []
lines.append('// --- PSTs (White perspective, A1=0 .. H8=63) ---')

pst_data = {
    'PST_PAWN_MG': [
        ' 0,  0,  0,  0,  0,  0,  0,  0,',
        '50, 50, 50, 50, 50, 50, 50, 50,',
        '10, 10, 20, 30, 30, 20, 10, 10,',
        ' 5,  5, 10, 25, 25, 10,  5,  5,',
        ' 0,  0,  0, 20, 20,  0,  0,  0,',
        ' 5, -5,-10,  0,  0,-10, -5,  5,',
        ' 5, 10, 10,-20,-20, 10, 10,  5,',
        ' 0,  0,  0,  0,  0,  0,  0,  0',
    ],
    'PST_PAWN_EG': [
        ' 0,  0,  0,  0,  0,  0,  0,  0,',
        '80, 80, 80, 80, 80, 80, 80, 80,',
        '50, 50, 50, 50, 50, 50, 50, 50,',
        '30, 30, 30, 30, 30, 30, 30, 30,',
        '20, 20, 20, 20, 20, 20, 20, 20,',
        '10, 10, 10, 10, 10, 10, 10, 10,',
        ' 0,  0,  0,  0,  0,  0,  0,  0,',
        ' 0,  0,  0,  0,  0,  0,  0,  0',
    ],
    'PST_KNIGHT_MG': [
        '   -50,-40,-30,-30,-30,-30,-40,-50,',
        '   -40,-20,  0,  0,  0,  0,-20,-40,',
        '   -30,  0, 10, 15, 15, 10,  0,-30,',
        '   -30,  5, 15, 20, 20, 15,  5,-30,',
        '   -30,  0, 15, 20, 20, 15,  0,-30,',
        '   -30,  5, 10, 15, 15, 10,  5,-30,',
        '   -40,-20,  0,  5,  5,  0,-20,-40,',
        '   -50,-40,-30,-30,-30,-30,-40,-50',
    ],
}

for name, rows in pst_data.items():
    lines.append(f'static constexpr int {name}[SQ_NB] = {{')
    lines.extend(rows)
    lines.append('};')

# Knight EG = Knight MG
lines.append('static constexpr int PST_KNIGHT_EG[SQ_NB] = {')
for r in pst_data['PST_KNIGHT_MG']:
    lines.append(r)
lines.append('};')

bishop = [
    '   -20,-10,-10,-10,-10,-10,-10,-20,',
    '   -10,  0,  0,  0,  0,  0,  0,-10,',
    '   -10,  0,  5, 10, 10,  5,  0,-10,',
    '   -10,  5,  5, 10, 10,  5,  5,-10,',
    '   -10,  0, 10, 10, 10, 10,  0,-10,',
    '   -10, 10, 10, 10, 10, 10, 10,-10,',
    '   -10,  5,  0,  0,  0,  0,  5,-10,',
    '   -20,-10,-10,-10,-10,-10,-10,-20',
]
lines.append('static constexpr int PST_BISHOP_MG[SQ_NB] = {')
lines.extend(bishop)
lines.append('};')
lines.append('static constexpr int PST_BISHOP_EG[SQ_NB] = {')
lines.extend(bishop)
lines.append('};')

rook = [
    '     0,  0,  0,  0,  0,  0,  0,  0,',
    '     5, 10, 10, 10, 10, 10, 10,  5,',
    '    -5,  0,  0,  0,  0,  0,  0, -5,',
    '    -5,  0,  0,  0,  0,  0,  0, -5,',
    '    -5,  0,  0,  0,  0,  0,  0, -5,',
    '    -5,  0,  0,  0,  0,  0,  0, -5,',
    '    -5,  0,  0,  0,  0,  0,  0, -5,',
    '     0,  0,  0,  5,  5,  0,  0,  0',
]
lines.append('static constexpr int PST_ROOK_MG[SQ_NB] = {')
lines.extend(rook)
lines.append('};')
lines.append('static constexpr int PST_ROOK_EG[SQ_NB] = {')
lines.extend(rook)
lines.append('};')

queen = [
    '   -20,-10,-10, -5, -5,-10,-10,-20,',
    '   -10,  0,  0,  0,  0,  0,  0,-10,',
    '   -10,  0,  5,  5,  5,  5,  0,-10,',
    '    -5,  0,  5,  5,  5,  5,  0, -5,',
    '     0,  0,  5,  5,  5,  5,  0, -5,',
    '   -10,  5,  5,  5,  5,  5,  0,-10,',
    '   -10,  0,  5,  0,  0,  0,  0,-10,',
    '   -20,-10,-10, -5, -5,-10,-10,-20',
]
lines.append('static constexpr int PST_QUEEN_MG[SQ_NB] = {')
lines.extend(queen)
lines.append('};')
lines.append('static constexpr int PST_QUEEN_EG[SQ_NB] = {')
lines.extend(queen)
lines.append('};')

king_mg = [
    '   -30,-40,-40,-50,-50,-40,-40,-30,',
    '   -30,-40,-40,-50,-50,-40,-40,-30,',
    '   -30,-40,-40,-50,-50,-40,-40,-30,',
    '   -30,-40,-40,-50,-50,-40,-40,-30,',
    '   -20,-30,-30,-40,-40,-30,-30,-20,',
    '   -10,-20,-20,-20,-20,-20,-20,-10,',
    '    20, 20,  0,  0,  0,  0, 20, 20,',
    '    20, 30, 10,  0,  0, 10, 30, 20',
]
lines.append('static constexpr int PST_KING_MG[SQ_NB] = {')
lines.extend(king_mg)
lines.append('};')

king_eg = [
    '   -50,-40,-30,-20,-20,-30,-40,-50,',
    '   -30,-20,-10,  0,  0,-10,-20,-30,',
    '   -30,-10, 20, 30, 30, 20,-10,-30,',
    '   -30,-10, 30, 40, 40, 30,-10,-30,',
    '   -30,-10, 30, 40, 40, 30,-10,-30,',
    '   -30,-10, 20, 30, 30, 20,-10,-30,',
    '   -30,-30,  0,  0,  0,  0,-30,-30,',
    '   -50,-30,-30,-30,-30,-30,-30,-50',
]
lines.append('static constexpr int PST_KING_EG[SQ_NB] = {')
lines.extend(king_eg)
lines.append('};')

lines.append('')
lines.append('static constexpr int CENTER_DIST[SQ_NB] = {')
lines.append('     6, 5, 4, 3, 3, 4, 5, 6,')
lines.append('     5, 4, 3, 2, 2, 3, 4, 5,')
lines.append('     4, 3, 2, 1, 1, 2, 3, 4,')
lines.append('     3, 2, 1, 0, 0, 1, 2, 3,')
lines.append('     3, 2, 1, 0, 0, 1, 2, 3,')
lines.append('     4, 3, 2, 1, 1, 2, 3, 4,')
lines.append('     5, 4, 3, 2, 2, 3, 4, 5,')
lines.append('     6, 5, 4, 3, 3, 4, 5, 6')
lines.append('};')
lines.append('')

with open(r'c:\Users\tahae\Kanamecide\src\eval.cpp', 'a') as f:
    f.write('\n'.join(lines))
print('Part 2 written')

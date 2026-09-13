// E-0010 - Tapered hand-tuned evaluation.
// Stage-gated for per-term self-play Elo attribution.
//   Stage 0: flat material only (baseline).
//   Stage 1: tapered material (mg/eg interpolated by phase).
//   Stage 2: + MG/EG PSTs.
//   Stage 3: + pawn structure (doubled/isolated/passed).
//   Stage 4: + enemy-pawn-discounted mobility.
//   Stage 5: + bishop pair / open-semi-open file / 7th rank / king shield / king center.
//   Stage 6: + tempo.

#include "eval.h"
#include "board.h"
#include "bitboard.h"

#include <algorithm>
#include <cstring>

namespace kana {

static EvalCoeffs C;
static int stage =
#ifdef EVAL_STAGE
    EVAL_STAGE
#else
    6
#endif
    ;

static Bitboard file_mask[8];
static Bitboard adj_file_mask[8];
static Bitboard passed_mask[2][SQ_NB];
static Bitboard shelter_mask[2][SQ_NB];

static const int GAME_PHASE_MAX = 24;
static constexpr int FLAT_VALUE[PIECE_TYPE_NB] = {100, 320, 330, 500, 900, 20000};

static inline Square mirror_sq(Square s) { return Square(s ^ 56); }
static inline int file_of(Square s) { return int(s) & 7; }
static inline int rank_of(Square s) { return int(s) >> 3; }

static constexpr int PST_PAWN_MG[SQ_NB] = {
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
};
static constexpr int PST_PAWN_EG[SQ_NB] = {
     0,  0,  0,  0,  0,  0,  0,  0,
    80, 80, 80, 80, 80, 80, 80, 80,
    50, 50, 50, 50, 50, 50, 50, 50,
    30, 30, 30, 30, 30, 30, 30, 30,
    20, 20, 20, 20, 20, 20, 20, 20,
    10, 10, 10, 10, 10, 10, 10, 10,
     0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0
};
static constexpr int PST_KNIGHT_MG[SQ_NB] = {
   -50,-40,-30,-30,-30,-30,-40,-50,
   -40,-20,  0,  0,  0,  0,-20,-40,
   -30,  0, 10, 15, 15, 10,  0,-30,
   -30,  5, 15, 20, 20, 15,  5,-30,
   -30,  0, 15, 20, 20, 15,  0,-30,
   -30,  5, 10, 15, 15, 10,  5,-30,
   -40,-20,  0,  5,  5,  0,-20,-40,
   -50,-40,-30,-30,-30,-30,-40,-50
};
static constexpr int PST_KNIGHT_EG[SQ_NB] = {
   -50,-40,-30,-30,-30,-30,-40,-50,
   -40,-20,  0,  0,  0,  0,-20,-40,
   -30,  0, 10, 15, 15, 10,  0,-30,
   -30,  5, 15, 20, 20, 15,  5,-30,
   -30,  0, 15, 20, 20, 15,  0,-30,
   -30,  5, 10, 15, 15, 10,  5,-30,
   -40,-20,  0,  5,  5,  0,-20,-40,
   -50,-40,-30,-30,-30,-30,-40,-50
};
static constexpr int PST_BISHOP_MG[SQ_NB] = {
   -20,-10,-10,-10,-10,-10,-10,-20,
   -10,  0,  0,  0,  0,  0,  0,-10,
   -10,  0,  5, 10, 10,  5,  0,-10,
   -10,  5,  5, 10, 10,  5,  5,-10,
   -10,  0, 10, 10, 10, 10,  0,-10,
   -10, 10, 10, 10, 10, 10, 10,-10,
   -10,  5,  0,  0,  0,  0,  5,-10,
   -20,-10,-10,-10,-10,-10,-10,-20
};
static constexpr int PST_BISHOP_EG[SQ_NB] = {
   -20,-10,-10,-10,-10,-10,-10,-20,
   -10,  0,  0,  0,  0,  0,  0,-10,
   -10,  0,  5, 10, 10,  5,  0,-10,
   -10,  5,  5, 10, 10,  5,  5,-10,
   -10,  0, 10, 10, 10, 10,  0,-10,
   -10, 10, 10, 10, 10, 10, 10,-10,
   -10,  5,  0,  0,  0,  0,  5,-10,
   -20,-10,-10,-10,-10,-10,-10,-20
};
static constexpr int PST_ROOK_MG[SQ_NB] = {
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0
};
static constexpr int PST_ROOK_EG[SQ_NB] = {
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0
};
static constexpr int PST_QUEEN_MG[SQ_NB] = {
   -20,-10,-10, -5, -5,-10,-10,-20,
   -10,  0,  0,  0,  0,  0,  0,-10,
   -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
   -10,  5,  5,  5,  5,  5,  0,-10,
   -10,  0,  5,  0,  0,  0,  0,-10,
   -20,-10,-10, -5, -5,-10,-10,-20
};
static constexpr int PST_QUEEN_EG[SQ_NB] = {
   -20,-10,-10, -5, -5,-10,-10,-20,
   -10,  0,  0,  0,  0,  0,  0,-10,
   -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
   -10,  5,  5,  5,  5,  5,  0,-10,
   -10,  0,  5,  0,  0,  0,  0,-10,
   -20,-10,-10, -5, -5,-10,-10,-20
};
static constexpr int PST_KING_MG[SQ_NB] = {
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -20,-30,-30,-40,-40,-30,-30,-20,
   -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
};
static constexpr int PST_KING_EG[SQ_NB] = {
   -50,-40,-30,-20,-20,-30,-40,-50,
   -30,-20,-10,  0,  0,-10,-20,-30,
   -30,-10, 20, 30, 30, 20,-10,-30,
   -30,-10, 30, 40, 40, 30,-10,-30,
   -30,-10, 30, 40, 40, 30,-10,-30,
   -30,-10, 20, 30, 30, 20,-10,-30,
   -30,-30,  0,  0,  0,  0,-30,-30,
   -50,-30,-30,-30,-30,-30,-30,-50
};
static constexpr int CENTER_DIST[SQ_NB] = {
     6, 5, 4, 3, 3, 4, 5, 6,
     5, 4, 3, 2, 2, 3, 4, 5,
     4, 3, 2, 1, 1, 2, 3, 4,
     3, 2, 1, 0, 0, 1, 2, 3,
     3, 2, 1, 0, 0, 1, 2, 3,
     4, 3, 2, 1, 1, 2, 3, 4,
     5, 4, 3, 2, 2, 3, 4, 5,
     6, 5, 4, 3, 3, 4, 5, 6
};



void eval_init() {
    C.mg_value[PAWN]   = 82; C.eg_value[PAWN]   = 94;
    C.mg_value[KNIGHT] = 337; C.eg_value[KNIGHT] = 281;
    C.mg_value[BISHOP] = 365; C.eg_value[BISHOP] = 297;
    C.mg_value[ROOK]   = 477; C.eg_value[ROOK]   = 512;
    C.mg_value[QUEEN]  = 1025; C.eg_value[QUEEN]  = 936;

    std::memcpy(C.mg_pst[PAWN],   PST_PAWN_MG,   sizeof(PST_PAWN_MG));
    std::memcpy(C.eg_pst[PAWN],   PST_PAWN_EG,   sizeof(PST_PAWN_EG));
    std::memcpy(C.mg_pst[KNIGHT], PST_KNIGHT_MG, sizeof(PST_KNIGHT_MG));
    std::memcpy(C.eg_pst[KNIGHT], PST_KNIGHT_EG, sizeof(PST_KNIGHT_EG));
    std::memcpy(C.mg_pst[BISHOP], PST_BISHOP_MG, sizeof(PST_BISHOP_MG));
    std::memcpy(C.eg_pst[BISHOP], PST_BISHOP_EG, sizeof(PST_BISHOP_EG));
    std::memcpy(C.mg_pst[ROOK],   PST_ROOK_MG,   sizeof(PST_ROOK_MG));
    std::memcpy(C.eg_pst[ROOK],   PST_ROOK_EG,   sizeof(PST_ROOK_EG));
    std::memcpy(C.mg_pst[QUEEN],  PST_QUEEN_MG,  sizeof(PST_QUEEN_MG));
    std::memcpy(C.eg_pst[QUEEN],  PST_QUEEN_EG,  sizeof(PST_QUEEN_EG));
    std::memcpy(C.mg_pst[KING],   PST_KING_MG,   sizeof(PST_KING_MG));
    std::memcpy(C.eg_pst[KING],   PST_KING_EG,   sizeof(PST_KING_EG));

    C.doubled_pawn_mg=-10; C.doubled_pawn_eg=-20;
    C.isolated_pawn_mg=-10; C.isolated_pawn_eg=-15;
    for(int i=0;i<8;i++){C.passed_pawn_mg[i]=0;C.passed_pawn_eg[i]=0;}
    C.passed_pawn_mg[1]=5; C.passed_pawn_eg[1]=10;
    C.passed_pawn_mg[2]=10; C.passed_pawn_eg[2]=20;
    C.passed_pawn_mg[3]=20; C.passed_pawn_eg[3]=35;
    C.passed_pawn_mg[4]=35; C.passed_pawn_eg[4]=55;
    C.passed_pawn_mg[5]=55; C.passed_pawn_eg[5]=80;
    C.passed_pawn_mg[6]=80; C.passed_pawn_eg[6]=120;

    C.mobility_mg=1; C.mobility_eg=1;
    C.bishop_pair_mg=30; C.bishop_pair_eg=50;
    C.open_file_mg=15; C.open_file_eg=10;
    C.semi_open_file_mg=8; C.semi_open_file_eg=5;
    C.seventh_rank_mg=10; C.seventh_rank_eg=20;
    C.king_shield_mg=5; C.king_center_eg=10; C.tempo=10;

    for(int f=0;f<8;++f){
        file_mask[f]=0;
        for(int r=0;r<8;++r) file_mask[f]|=(1ULL<<(r*8+f));
        adj_file_mask[f]=file_mask[f];
        if(f>0) adj_file_mask[f]|=file_mask[f-1];
        if(f<7) adj_file_mask[f]|=file_mask[f+1];
    }

    for(Square s=A1;s<SQ_NB;s=Square(s+1)){
        int f=file_of(s), r=rank_of(s);
        Bitboard aw=0, ab=0;
        for(int i=r+1;i<8;++i) aw|=(0xFFULL<<(i*8));
        for(int i=0;i<r;++i) ab|=(0xFFULL<<(i*8));
        passed_mask[WHITE][s]=(file_mask[f]|adj_file_mask[f])&aw;
        passed_mask[BLACK][s]=(file_mask[f]|adj_file_mask[f])&ab;

        shelter_mask[WHITE][s]=0; shelter_mask[BLACK][s]=0;
        int fl=std::max(0,f-1), fr=std::min(7,f+1);
        for(int ff=fl;ff<=fr;++ff){
            if(r+1<8) shelter_mask[WHITE][s]|=(1ULL<<((r+1)*8+ff));
            if(r-1>=0) shelter_mask[BLACK][s]|=(1ULL<<((r-1)*8+ff));
        }
    }
}

int eval_stage() { return stage; }
void set_eval_stage(int s) { stage = std::clamp(s, 0, 6); }



int evaluate(const Board& b) {
    if (stage == 0) {
        int sc = 0;
        for (int pt=0; pt<PIECE_TYPE_NB; ++pt)
            sc += FLAT_VALUE[pt]*int(popcount(b.pieces[WHITE][pt])-popcount(b.pieces[BLACK][pt]));
        return b.side==WHITE ? sc : -sc;
    }

    int phase = int(popcount(b.pieces[WHITE][KNIGHT]|b.pieces[BLACK][KNIGHT]))*1
              + int(popcount(b.pieces[WHITE][BISHOP]|b.pieces[BLACK][BISHOP]))*1
              + int(popcount(b.pieces[WHITE][ROOK]|b.pieces[BLACK][ROOK]))*2
              + int(popcount(b.pieces[WHITE][QUEEN]|b.pieces[BLACK][QUEEN]))*4;
    phase = std::min(phase, GAME_PHASE_MAX);

    int mg=0, eg=0;
    for(int pt=PAWN; pt<=QUEEN; ++pt){
        int d=int(popcount(b.pieces[WHITE][pt])-popcount(b.pieces[BLACK][pt]));
        mg+=d*C.mg_value[pt]; eg+=d*C.eg_value[pt];
    }

    if(stage>=2){
        for(Square s=A1;s<SQ_NB;s=Square(s+1)){
            int pc=b.mailbox[s]; if(pc==0) continue;
            Color c=piece_color(pc); PieceType pt=piece_type(pc);
            if(c==WHITE){mg+=C.mg_pst[pt][s]; eg+=C.eg_pst[pt][s];}
            else{Square ms=mirror_sq(s); mg-=C.mg_pst[pt][ms]; eg-=C.eg_pst[pt][ms];}
        }
    }

    if(stage>=3){
        Bitboard wp=b.pieces[WHITE][PAWN], bp=b.pieces[BLACK][PAWN];
        for(int f=0;f<8;++f){
            Bitboard fm=file_mask[f];
            int wc=int(popcount(wp&fm)), bc=int(popcount(bp&fm));
            if(wc>=2){mg+=(wc-1)*C.doubled_pawn_mg; eg+=(wc-1)*C.doubled_pawn_eg;}
            if(bc>=2){mg-=(bc-1)*C.doubled_pawn_mg; eg-=(bc-1)*C.doubled_pawn_eg;}
            if((wp&fm)&&!(wp&(adj_file_mask[f]^fm))){
                int n=int(popcount(wp&fm)); mg+=n*C.isolated_pawn_mg; eg+=n*C.isolated_pawn_eg;
            }
            if((bp&fm)&&!(bp&(adj_file_mask[f]^fm))){
                int n=int(popcount(bp&fm)); mg-=n*C.isolated_pawn_mg; eg-=n*C.isolated_pawn_eg;
            }
        }
        Bitboard wpp=wp;
        while(wpp){Square s=pop_lsb(wpp); if(!(bp&passed_mask[WHITE][s])){int r=rank_of(s); mg+=C.passed_pawn_mg[r]; eg+=C.passed_pawn_eg[r];}}
        Bitboard bpp=bp;
        while(bpp){Square s=pop_lsb(bpp); if(!(wp&passed_mask[BLACK][s])){int r=7-rank_of(s); mg-=C.passed_pawn_mg[r]; eg-=C.passed_pawn_eg[r];}}
    }


    if(stage>=4){
        Bitboard occ=occ_all(b);
        Bitboard bpa=0, wpa=0;
        Bitboard t2=b.pieces[BLACK][PAWN]; while(t2) bpa|=pawn_attacks[BLACK][pop_lsb(t2)];
        t2=b.pieces[WHITE][PAWN]; while(t2) wpa|=pawn_attacks[WHITE][pop_lsb(t2)];

        Bitboard wmob=0;
        Bitboard bb=b.pieces[WHITE][KNIGHT]; while(bb) wmob|=knight_attacks[pop_lsb(bb)];
        bb=b.pieces[WHITE][BISHOP]; while(bb) wmob|=bishop_attacks(pop_lsb(bb),occ);
        bb=b.pieces[WHITE][ROOK]; while(bb) wmob|=rook_attacks(pop_lsb(bb),occ);
        bb=b.pieces[WHITE][QUEEN]; while(bb) wmob|=queen_attacks(pop_lsb(bb),occ);
        wmob&=~b.occ[WHITE]; wmob&=~bpa;

        Bitboard bmob=0;
        bb=b.pieces[BLACK][KNIGHT]; while(bb) bmob|=knight_attacks[pop_lsb(bb)];
        bb=b.pieces[BLACK][BISHOP]; while(bb) bmob|=bishop_attacks(pop_lsb(bb),occ);
        bb=b.pieces[BLACK][ROOK]; while(bb) bmob|=rook_attacks(pop_lsb(bb),occ);
        bb=b.pieces[BLACK][QUEEN]; while(bb) bmob|=queen_attacks(pop_lsb(bb),occ);
        bmob&=~b.occ[BLACK]; bmob&=~wpa;

        mg += (int(popcount(wmob))-int(popcount(bmob)))*C.mobility_mg;
        eg += (int(popcount(wmob))-int(popcount(bmob)))*C.mobility_eg;
    }

    if(stage>=5){
        if(popcount(b.pieces[WHITE][BISHOP])>=2){mg+=C.bishop_pair_mg; eg+=C.bishop_pair_eg;}
        if(popcount(b.pieces[BLACK][BISHOP])>=2){mg-=C.bishop_pair_mg; eg-=C.bishop_pair_eg;}

        Bitboard wp=b.pieces[WHITE][PAWN], bp=b.pieces[BLACK][PAWN];
        for(int f=0;f<8;++f){
            Bitboard fm=file_mask[f];
            bool wp_=(wp&fm)!=0, bp_=(bp&fm)!=0;
            if(!wp_ && !bp_){
                if(b.pieces[WHITE][ROOK]&fm){mg+=C.open_file_mg; eg+=C.open_file_eg;}
                if(b.pieces[WHITE][QUEEN]&fm){mg+=C.open_file_mg/2; eg+=C.open_file_eg/2;}
                if(b.pieces[BLACK][ROOK]&fm){mg-=C.open_file_mg; eg-=C.open_file_eg;}
                if(b.pieces[BLACK][QUEEN]&fm){mg-=C.open_file_mg/2; eg-=C.open_file_eg/2;}
            } else if(!wp_ && bp_){
                if(b.pieces[WHITE][ROOK]&fm){mg+=C.semi_open_file_mg; eg+=C.semi_open_file_eg;}
                if(b.pieces[WHITE][QUEEN]&fm){mg+=C.semi_open_file_mg/2; eg+=C.semi_open_file_eg/2;}
            } else if(wp_ && !bp_){
                if(b.pieces[BLACK][ROOK]&fm){mg-=C.semi_open_file_mg; eg-=C.semi_open_file_eg;}
                if(b.pieces[BLACK][QUEEN]&fm){mg-=C.semi_open_file_mg/2; eg-=C.semi_open_file_eg/2;}
            }
        }

        Bitboard rank7=0xFFULL<<48, rank2=0xFFULL<<8;
        if(b.pieces[WHITE][ROOK]&rank7){mg+=C.seventh_rank_mg; eg+=C.seventh_rank_eg;}
        if(b.pieces[WHITE][QUEEN]&rank7){mg+=C.seventh_rank_mg; eg+=C.seventh_rank_eg;}
        if(b.pieces[BLACK][ROOK]&rank2){mg-=C.seventh_rank_mg; eg-=C.seventh_rank_eg;}
        if(b.pieces[BLACK][QUEEN]&rank2){mg-=C.seventh_rank_mg; eg-=C.seventh_rank_eg;}

        int ws=int(popcount(wp&shelter_mask[WHITE][b.king_sq[WHITE]]));
        int bs=int(popcount(bp&shelter_mask[BLACK][b.king_sq[BLACK]]));
        mg+=ws*C.king_shield_mg; mg-=bs*C.king_shield_mg;

        eg+=(6-CENTER_DIST[b.king_sq[WHITE]])*C.king_center_eg;
        eg-=(6-CENTER_DIST[mirror_sq(b.king_sq[BLACK])])*C.king_center_eg;
    }

    int sc=(mg*phase+eg*(GAME_PHASE_MAX-phase))/GAME_PHASE_MAX;
    // E-0010 symmetry fix: tempo is a bonus for the side TO MOVE. Adding a bare +tempo to
    // a White-positive score means White-to-move gets +T but Black-to-move gets -T (a color
    // asymmetry — the mirror invariant fails by 2T). Sign it by side-to-move first so the
    // mover always gets +T and the full-mirror invariant S(M(b)) == S(b) holds exactly.
    if(stage>=6) sc += (b.side == WHITE ? C.tempo : -C.tempo);
    return b.side==WHITE ? sc : -sc;
}

} // namespace kana

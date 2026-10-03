# FND-0035 F2/F3 - node-count pre/post table (`go depth 6`, Release binary)

EVIDENCE, NOT A DEFECT. No strength interpretation; no SPRT. Metric is cumulative nodes
at fixed depth (`go depth 6`, never `go nodes` - FND-0035 Finding 4).

PRE  = binary 686EA5979415054982703985C543CEB9EE7C0CD47C166903CAF8C79D12276F3B (121344 B),
      src/search.cpp F18A0C3CCDB51BB0DE212F0D552855048D5475FF005C4FF14769DD4809B06F8D
POST = binary A0951F4F40B5B85923BA832362C378009F0F8ED7C4DD20BB39EF70F59B5D8BCF (121856 B),
      src/search.cpp 251C19E8E710C715CFEB0B2DB39EC81A2DA6A5B774565496125E897AA326774E

| # | position | nodes PRE | nodes POST | delta | delta % | bestmove PRE | bestmove POST | bm same |
|---|---|---:|---:|---:|---:|---|---|---|
| 1 | startpos | 1,237,736 | 1,246,725 | +8,989 | +0.7% | `b1c3` | `b1c3` | yes |
| 2 | italian | 1,331,430 | 1,637,354 | +305,924 | +23.0% | `c1g5` | `c1g5` | yes |
| 3 | italian_early | 759,586 | 982,416 | +222,830 | +29.3% | `f3g5` | `f3g5` | yes |
| 4 | qgd | 1,257,357 | 1,100,054 | -157,303 | -12.5% | `f1e1` | `f1e1` | yes |
| 5 | kid | 2,600,599 | 2,772,442 | +171,843 | +6.6% | `c1f4` | `c1f4` | yes |
| 6 | giuoco_2 | 1,101,978 | 1,315,416 | +213,438 | +19.4% | `c1g5` | `c1g5` | yes |
| 7 | q_out | 1,679,991 | 1,890,289 | +210,298 | +12.5% | `c3d5` | `c3d5` | yes |
| 8 | tact_b | 556,176 | 624,025 | +67,849 | +12.2% | `d4c5` | `d4c5` | yes |
| 9 | tact_c | 507,212 | 574,797 | +67,585 | +13.3% | `b1a3` | `b1a3` | yes |
| 10 | tact_d | 2,360,817 | 3,203,859 | +843,042 | +35.7% | `c3b5` | `c3b5` | yes |
| 11 | tact_e | 590,456 | 593,069 | +2,613 | +0.4% | `c1d2` | `c1d2` | yes |
| | **TOTAL (11)** | **13,983,338** | **15,940,446** | **+1,957,108** | **+14.0%** | | | 11/11 |

## Reading this table (bounded, non-strength)

- Node count rose +14.0% in total. **This is the expected direction and is not a
  regression**: F2 adds a threefold scan + halfmove test to every qsearch node (both are
  O(path length) work that did not exist there before), and F3 deletes a fail-high that used
  to return `beta` immediately while in check, so those nodes now expand.
- Best moves are identical on 11/11 positions, so the repair changed the search's mind
  nowhere on this set at depth 6. A changed best move would not by itself have been a defect
  (F3 changes scores at in-check leaves by design); it is recorded either way so the
  adversarial pass can see exactly where, if anywhere, the search moved.
- Nothing here is a strength statement. No SPRT was run and none may be inferred.


p='e0010_match.py'
s=open(p,encoding='utf-8').read().split('\n')
s[66]='    if not eng.send("go wtime 1500 btime 1500 winc 100 binc 100"): return None, "ENGINE-DIED", []'
s[67]='    line, lines = eng.wait_for("bestmove", 5.0)'
open(p,'w',encoding='utf-8').write('\n'.join(s))
import py_compile
py_compile.compile(p,doraise=True)
print('PY_FIXED_OK')

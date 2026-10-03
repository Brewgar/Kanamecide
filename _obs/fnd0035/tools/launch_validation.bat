@echo off
REM FND-0035 F2/F3 repair - launch the three long validation runs DETACHED.
REM (The agent shell kills foreground processes on tool turnover; E-00009's own debugging note
REM  records that every measurement must be launched detached and polled via file reads.)
setlocal
cd /d c:\Users\tahae\Kanamecide

start "" /b cmd /c "python _obs\fnd0035\tools\replay_nodes.py nodes --exe build\Release\kana.exe --depth 6 --out _obs\fnd0035\nodes_post_d6.csv > _obs\fnd0035\logs_nodes_post.txt 2>&1"
start "" /b cmd /c "python _obs\fnd0035\tools\replay_nodes.py replay --exe build\Release\kana.exe --depth 8 --runs 3 --out _obs\fnd0035\replay_d8_x3.json > _obs\fnd0035\logs_replay.txt 2>&1"
start "" /b cmd /c "python _obs\fnd0035\tools\fuzz_selfplay.py --exe build\Release\kana.exe --games 1000 --depth 4 --seed 20261003 --out _obs\fnd0035\fuzz_1000.json > _obs\fnd0035\logs_fuzz.txt 2>&1"
endlocal

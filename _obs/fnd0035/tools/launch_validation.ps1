$ErrorActionPreference = 'Continue'
Set-Location 'c:\Users\tahae\Kanamecide'

# Launch DETACHED and WITHOUT console inheritance: `start /b` shares the console and the
# agent shell's CTRL_C reaches the workers (E-00009's own debugging note requires detached).
# Start-Process -WindowStyle Hidden gives each worker its own process with no shared console.
Start-Process -FilePath 'python' -WindowStyle Hidden -ArgumentList @(
  '_obs\fnd0035\tools\replay_nodes.py','replay',
  '--exe','build\Release\kana.exe','--depth','8','--runs','3',
  '--out','_obs\fnd0035\replay_d8_x3.json'
) -RedirectStandardOutput '_obs\fnd0035\logs_replay.txt' `
  -RedirectStandardError '_obs\fnd0035\logs_replay.err.txt'

Start-Process -FilePath 'python' -WindowStyle Hidden -ArgumentList @(
  '_obs\fnd0035\tools\fuzz_selfplay.py',
  '--exe','build\Release\kana.exe','--games','1000','--depth','4','--seed','20261003',
  '--out','_obs\fnd0035\fuzz_1000.json'
) -RedirectStandardOutput '_obs\fnd0035\logs_fuzz.txt' `
  -RedirectStandardError '_obs\fnd0035\logs_fuzz.err.txt'

'LAUNCHED'

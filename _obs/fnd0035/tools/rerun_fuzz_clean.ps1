$ErrorActionPreference = 'Continue'
Set-Location 'c:\Users\tahae\Kanamecide'
# The previous stdout log is STALE (it is the log of the run that the console CTRL_C killed at
# game 73, and it still contains that run's "crash" line). Its JSON was fresh. Evidence hygiene
# forbids shipping a log that does not belong to the JSON it sits beside, so: discard both and
# re-run cleanly into fresh files. The fuzz is deterministic under --seed, so the re-run must
# reproduce the same counts; that is itself a check.
Remove-Item '_obs\fnd0035\logs_fuzz.txt','_obs\fnd0035\logs_fuzz.err.txt','_obs\fnd0035\fuzz_1000.json' -Force -EA SilentlyContinue
Start-Sleep -Seconds 1
$p = Start-Process -FilePath 'python' -WindowStyle Hidden -PassThru -ArgumentList @(
  '_obs\fnd0035\tools\fuzz_selfplay.py',
  '--exe','build\Release\kana.exe','--games','1000','--depth','4','--seed','20261003',
  '--out','_obs\fnd0035\fuzz_1000.json'
) -RedirectStandardOutput '_obs\fnd0035\logs_fuzz_stdout.txt' `
  -RedirectStandardError '_obs\fnd0035\logs_fuzz_stderr.txt'
"FUZZ_RERUN_STARTED pid=$($p.Id)"

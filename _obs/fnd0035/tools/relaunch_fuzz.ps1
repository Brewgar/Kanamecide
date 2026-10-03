$ErrorActionPreference = 'Continue'
Set-Location 'c:\Users\tahae\Kanamecide'
# Stop ONLY the fuzz worker (the replay worker is still valid and mid-run). The fuzz worker's
# in-memory copy of the gate predates the plycap reclassification, so its JSON would be stale.
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | ForEach-Object {
  if ($_.CommandLine -like '*fuzz_selfplay.py*') {
    "killing fuzz worker pid=$($_.ProcessId)"
    Stop-Process -Id $_.ProcessId -Force -EA SilentlyContinue
  } else {
    "keeping pid=$($_.ProcessId) : $($_.CommandLine)"
  }
}
Start-Sleep -Seconds 2
Start-Process -FilePath 'python' -WindowStyle Hidden -ArgumentList @(
  '_obs\fnd0035\tools\fuzz_selfplay.py',
  '--exe','build\Release\kana.exe','--games','1000','--depth','4','--seed','20261003',
  '--out','_obs\fnd0035\fuzz_1000.json'
) -RedirectStandardOutput '_obs\fnd0035\logs_fuzz.txt' `
  -RedirectStandardError '_obs\fnd0035\logs_fuzz.err.txt'
'FUZZ_RELAUNCHED'

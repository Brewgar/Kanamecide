$ErrorActionPreference = 'Continue'
Set-Location 'c:\Users\tahae\Kanamecide'
$out = @()
foreach ($cfg in @('Release','Audit')) {
  $exe = "build\$cfg\kana.exe"
  $so  = "_obs\fnd0035\perft_$cfg.out.txt"
  $se  = "_obs\fnd0035\perft_$cfg.err.txt"
  $p = Start-Process -FilePath $exe -NoNewWindow -Wait -PassThru `
        -RedirectStandardOutput $so -RedirectStandardError $se
  $out += "=== $cfg exit=$($p.ExitCode) ==="
  $out += (Get-Content $so -EA SilentlyContinue)
}
$out += "=== digests (post-repair) ==="
foreach ($p in @('build/Release/kana.exe','build/Audit/kana.exe','src/search.cpp')) {
  $out += "$p " + (Get-FileHash $p -Algorithm SHA256).Hash + " " + (Get-Item $p).Length
}
$out -join "`n" | Set-Content -Encoding UTF8 '_obs\fnd0035\perft_anchor.txt'

$ErrorActionPreference = 'Stop'
$root = 'c:\Users\tahae\Kanamecide'
Set-Location $root
$out = @()
New-Item -ItemType Directory -Force -Path '_obs\fnd0035\binary' | Out-Null
foreach ($cfg in @('Release','Audit')) {
  $p = "build\$cfg\kana.exe"
  if (Test-Path $p) {
    Copy-Item $p "_obs\fnd0035\binary\kana_pre_$cfg.exe" -Force
    $h = (Get-FileHash $p -Algorithm SHA256).Hash
    $len = (Get-Item $p).Length
    $out += "PRE $cfg $h $len"
  } else { $out += "PRE $cfg MISSING" }
}
$out += "PRE src/search.cpp " + (Get-FileHash 'src\search.cpp' -Algorithm SHA256).Hash
$out += "PRE git HEAD " + (git rev-parse HEAD)
$out -join "`n" | Set-Content -Encoding UTF8 '_obs\fnd0035\binary\pre_build_hashes.txt'
Get-Content '_obs\fnd0035\binary\pre_build_hashes.txt'

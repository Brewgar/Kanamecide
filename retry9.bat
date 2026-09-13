@echo off
cd /d C:\Users\tahae\Kanamecide
(echo uci& echo ucinewgame& echo position startpos& echo go depth 2& echo quit) > uci_o3d.txt
for /L %%i in (1,1,10) do (
  build\Audit\kana.exe uci < uci_o3d.txt > uci_out9.txt 2>&1
  findstr /C:"blocked by your organization" uci_out9.txt >nul
  if errorlevel 1 goto :ok
  timeout /t 5 /nobreak >nul
)
:ok
echo DONE
@echo off
cd /d C:\Users\tahae\Kanamecide
for /L %%i in (1,1,40) do (
  cmd /c "build\Release\kana.exe < nul > _g0_perft.txt 2>&1"
  findstr /C:"blocked by your organization" _g0_perft.txt >nul
  if errorlevel 1 goto :ok
  timeout /t 3 /nobreak >nul
)
:ok
echo G0_PERFT_RUN_DONE
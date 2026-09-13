@echo off
cd /d C:\Users\tahae\Kanamecide
:loop
cmd /c "build\Audit\kana.exe < nul > _g0_audit.txt 2>&1"
findstr /C:"blocked by your organization" _g0_audit.txt >nul
if errorlevel 1 goto :ok
findstr /C:"ALL TESTS PASSED" _g0_audit.txt >nul
if errorlevel 1 goto :retry
goto :ok
:retry
timeout /t 4 /nobreak >nul
goto :loop
:ok
echo G0_AUDIT_RUN_DONE
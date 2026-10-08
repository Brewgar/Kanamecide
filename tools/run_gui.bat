@echo off
REM Windows launcher for the KANAMECIDE Training Control GUI.
REM Lives in tools/ per DEC-0009 repo-root hygiene (no new root files).
setlocal
cd /d "%~dp0\.."
if not exist tools\gui_app.py (
  echo ERROR: tools\gui_app.py not found. Repo root expected above tools\.
  exit /b 1
)
python tools\gui_app.py
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" (
  echo GUI exited with code %RC%.
)
endlocal

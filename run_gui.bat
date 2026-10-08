@echo off
REM Canonical Windows launcher for the KANAMECIDE Training Control GUI.
setlocal
cd /d "%~dp0"
if not exist tools\gui_app.py (
  echo ERROR: tools\gui_app.py not found. Run from the repo root.
  exit /b 1
)
python tools\gui_app.py
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" (
  echo GUI exited with code %RC%.
)
endlocal

@echo off
cd /d C:\Users\tahae\Kanamecide
start "" cmd /c "timeout /t 600 /nobreak >nul && echo WAIT_DONE %TIME% > _wait10m_marker.txt"
echo LAUNCHED_WAIT_600
exit
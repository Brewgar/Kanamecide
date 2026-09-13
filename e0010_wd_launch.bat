@echo off
cd /d C:\Users\tahae\Kanamecide
start "" cmd /c "python e0010_watchdog.py > _watchdog_py.txt 2>&1"
echo WATCHDOG_LAUNCHED
exit
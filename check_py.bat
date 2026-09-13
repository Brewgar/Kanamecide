@echo off
cd /d C:\Users\tahae\Kanamecide
python -m py_compile e0010_watchdog.py e0010_report.py > _pyerr.txt 2>&1
echo PY_COMPILE_RC=%errorlevel% >> _pyerr.txt
exit /b 0
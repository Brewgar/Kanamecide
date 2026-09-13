@echo off
cd /d C:\Users\tahae\Kanamecide
del e0010_k1.txt e0010_k2.txt e0010_k3.txt e0010_k4.txt e0010_k5.txt e0010_k6.txt 2>nul
del e0010_k1_err.txt e0010_k2_err.txt e0010_k3_err.txt e0010_k4_err.txt e0010_k5_err.txt e0010_k6_err.txt 2>nul
del e0010_k1_result.txt e0010_k2_result.txt e0010_k3_result.txt e0010_k4_result.txt e0010_k5_result.txt e0010_k6_result.txt 2>nul
del _watchdog.txt _watchdog_py.txt 2>nul
start "" cmd /c "python e0010_match.py build\Release\kana.exe 1 200 k1 > e0010_k1.txt 2> e0010_k1_err.txt"
start "" cmd /c "python e0010_match.py build\Release\kana.exe 2 200 k2 > e0010_k2.txt 2> e0010_k2_err.txt"
start "" cmd /c "python e0010_match.py build\Release\kana.exe 3 200 k3 > e0010_k3.txt 2> e0010_k3_err.txt"
start "" cmd /c "python e0010_match.py build\Release\kana.exe 4 200 k4 > e0010_k4.txt 2> e0010_k4_err.txt"
start "" cmd /c "python e0010_match.py build\Release\kana.exe 5 200 k5 > e0010_k5.txt 2> e0010_k5_err.txt"
start "" cmd /c "python e0010_match.py build\Release\kana.exe 6 200 k6 > e0010_k6.txt 2> e0010_k6_err.txt"
start "" cmd /c "python e0010_watchdog.py > _watchdog_py.txt 2>&1"
echo RELAUNCHED_K1_K6_HARDENED
exit
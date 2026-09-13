@echo off
cd /d C:\Users\tahae\Kanamecide
start "" cmd /c "python e0010_match.py build\Release\kana.exe 5 200 k5 > e0010_k5.txt 2> e0010_k5_err.txt"
start "" cmd /c "python e0010_match.py build\Release\kana.exe 6 200 k6 > e0010_k6.txt 2> e0010_k6_err.txt"
echo launched k5-k6 detached
exit
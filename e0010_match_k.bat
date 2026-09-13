@echo off
cd /d C:\Users\tahae\Kanamecide
python e0010_match.py build\Release\kana.exe %1 200 k%1 > e0010_k%1.txt 2> e0010_k%1_err.txt
echo E0010_K%1_EXIT
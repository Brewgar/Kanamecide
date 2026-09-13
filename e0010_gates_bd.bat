@echo off
cd /d C:\Users\tahae\Kanamecide
del _g0_sym_all.txt 2>nul
for /L %%s in (0,1,6) do call :do_sym %%s
echo === BENCH (gate d) ===
call :do_bench
echo GATES_BD_DONE
exit /b

:do_sym
for /L %%r in (1,1,40) do (
  cmd /c "build\Release\kana.exe --symmetry 1000 %1" > _sym_tmp.txt 2>&1
  findstr /C:"blocked by your organization" _sym_tmp.txt >nul
  if errorlevel 1 ( type _sym_tmp.txt >> _g0_sym_all.txt & exit /b 0 )
  timeout /t 3 /nobreak >nul
)
exit /b 1

:do_bench
for /L %%r in (1,1,60) do (
  cmd /c "build\Release\kana.exe --bench 5" > _g0_bench.txt 2>&1
  findstr /C:"blocked by your organization" _g0_bench.txt >nul
  if errorlevel 1 exit /b 0
  timeout /t 4 /nobreak >nul
)
exit /b 1
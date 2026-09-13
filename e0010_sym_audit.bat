@echo off
cd /d C:\Users\tahae\Kanamecide
del _g0_sym_audit.txt 2>nul
for /L %%s in (0,1,6) do call :do_sym %%s
echo SYMMETRY_AUDIT_DONE
exit /b

:do_sym
for /L %%r in (1,1,40) do (
  cmd /c "build\Audit\kana.exe --symmetry 1000 %1" > _sym_aud_tmp.txt 2>&1
  findstr /C:"blocked by your organization" _sym_aud_tmp.txt >nul
  if errorlevel 1 ( type _sym_aud_tmp.txt >> _g0_sym_audit.txt & exit /b 0 )
  timeout /t 3 /nobreak >nul
)
exit /b 1
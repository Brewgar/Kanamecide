@echo off
setlocal
set "VCVARS=C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"
set "CMAKE=C:\Program Files\CMake\bin\cmake.exe"

call "%VCVARS%" >nul

cd /d c:\Users\tahae\Kanamecide

REM --- Release ---
"%CMAKE%" --build build --config Release
if errorlevel 1 ( echo RELEASE BUILD FAILED & exit /b 1 )

REM --- Audit (asserts live: /O2 without NDEBUG) ---
"%CMAKE%" --build build --config Audit
if errorlevel 1 ( echo AUDIT BUILD FAILED & exit /b 1 )

echo.
echo Built: build\Release\kana.exe and build\Audit\kana.exe
endlocal

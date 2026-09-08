@echo off
setlocal
set "VCVARS=C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"
set "CMAKE=C:\Program Files\CMake\bin\cmake.exe"

call "%VCVARS%"

cd /d c:\Users\tahae\Kanamecide
if exist build rmdir /s /q build
mkdir build
cd build

"%CMAKE%" -G "Visual Studio 18 2026" -A x64 -DCMAKE_BUILD_TYPE=Release ..
"%CMAKE%" --build . --config Release

cd /d c:\Users\tahae\Kanamecide
echo.
echo Built: build\Release\kana.exe
endlocal
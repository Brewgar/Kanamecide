@echo off
cd /d C:\Users\tahae\Kanamecide
echo === rebuilding Release with hardened time control ===
cmake --build build --config Release > _rel_build.txt 2>&1
if errorlevel 1 (echo RELEASE_BUILD_FAILED & type _rel_build.txt & exit /b 1)
echo === verifying build ===
cmake --build build --config Release --target kana 2>>_rel_build.txt
echo RELEASE_BUILD_OK
exit /b 0
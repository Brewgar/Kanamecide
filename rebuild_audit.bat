@echo off
cd /d C:\Users\tahae\Kanamecide
cmake --build build --config Audit > _audit_build.txt 2>&1
if errorlevel 1 (echo AUDIT_BUILD_FAILED & type _audit_build.txt & exit /b 1)
echo AUDIT_BUILD_OK
exit /b 0
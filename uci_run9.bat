@echo off
cd /d C:\Users\tahae\Kanamecide
copy /Y build\Audit\kana.exe %TEMP%\kana_aud9.exe >nul
(echo uci& echo ucinewgame& echo position startpos& echo go depth 2& echo quit) | %TEMP%\kana_aud9.exe uci > uci_out9.txt 2>&1
echo EXIT=%errorlevel%
@Echo Off
SETLOCAL EnableDelayedExpansion
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do     rem"') do (
  set "DEL=%%a"
)
call :colorEcho 6 "Press ENTER to start the setup..."
echo.
pause>nul
timeout /t 1 /nobreak>nul
echo Download Started:
call :colorEcho a "PyQt5"
echo.
timeout /t 3 /nobreak>nul
pip install PyQt5

echo Creating file start.bat...
echo python main.py > start.bat
echo File start.bat created.

pause

call :colorEcho 4 "If the download does not work, follow the documentation on the official website"
echo.
echo https://pypi.org/project/PyQt5/

pause
exit
:colorEcho
echo off
<nul set /p ".=%DEL%" > "%~2"
findstr /v /a:%1 /R "^$" "%~2" nul
del "%~2" > nul 2>&1i

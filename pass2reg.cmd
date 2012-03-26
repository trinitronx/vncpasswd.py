@echo off
setlocal
if "%1" == "" (
    echo usage: %0 ^<password^>
    exit /b
)
set regkey=HKLM\SOFTWARE\ORL\WinVNC3\Default
set valname=Password

rem clumsy cmd way to set password hash to env var
for /f "delims=" %%H in ('vnc_hash.py %1') do set hash=%%H

echo VNC Hash is: %hash%
echo Writing to: %regkey%\%valname%
reg add %regkey% /v %valname% /t reg_binary /f /d %hash%
echo Writing to: %regkey%\%valname%2
reg add %regkey%  /v %valname%2 /t reg_binary /f /d %hash%

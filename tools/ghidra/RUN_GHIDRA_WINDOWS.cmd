@echo off
setlocal
for %%I in ("%~dp0..\..") do set "ROOT=%%~fI"
set "DLL=%ROOT%\original\asioglld.dll"
if not exist "%DLL%" (
 echo Copy your ORIGINAL asioglld.dll into %ROOT%\original\asioglld.dll
 pause
 exit /b 1
)
for /f "delims=" %%H in ('powershell -NoProfile -Command "(Get-FileHash -Algorithm SHA256 -LiteralPath '%DLL%').Hash.ToLowerInvariant()"') do set "HASH=%%H"
if /i not "%HASH%"=="e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd" (
 echo Hash mismatch, aborting.
 pause
 exit /b 1
)
if not defined GHIDRA_HOME (
 echo Set GHIDRA_HOME to extracted Ghidra directory.
 pause
 exit /b 1
)
set "HEADLESS=%GHIDRA_HOME%\support\analyzeHeadless.bat"
if not exist "%HEADLESS%" (
 echo Ghidra headless script missing: %HEADLESS%
 pause
 exit /b 1
)
if not exist "%ROOT%\local_output\ghidra_projects" mkdir "%ROOT%\local_output\ghidra_projects"
if not exist "%ROOT%\local_output\decompiled" mkdir "%ROOT%\local_output\decompiled"
call "%HEADLESS%" "%ROOT%\local_output\ghidra_projects" ASIOGLLD_RECOVERY -import "%DLL%" -scriptPath "%~dp0" -postScript ExportAsioRecovery.java "%ROOT%\local_output\decompiled" -deleteProject
if errorlevel 1 (echo Failed. See errors above.) else (echo Done: local_output\decompiled)
pause

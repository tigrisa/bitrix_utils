@echo off
setlocal

:: Is pipx installed?
:: you need to install pipx manually
where pipx >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo pipx is not installed.
    echo Please install pipx using 'pip install pipx' and then run 'pipx ensurepath'
    exit /b 1
)

echo Installing the project using pipx...
pipx install .

:: Get the full path to the current directory
set "CURRENT_DIR=%~dp0"

:: Remove the trailing backslash
set "WORKING_DIR=%CURRENT_DIR:~0,-1%"

:: Task name and path to the script
set "TASK_NAME=bitrix_task"
set "EXECUTABLE_NAME=add_task"
set "ARGUMENTS=--date today --randdelay 59"

:: Create a task in Task Scheduler with the working directory
schtasks /create /tn "%TASK_NAME%" /tr "cmd /c cd /d %WORKING_DIR% && %EXECUTABLE_NAME% %ARGUMENTS%" /sc daily /st 09:00 /f

echo Done.
endlocal

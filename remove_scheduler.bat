@echo off
setlocal

:: Name of the task to be removed
set "TASK_NAME=bitrix_task"

:: Stop the task if it's currently running
schtasks /end /tn "%TASK_NAME%"

:: Delete the task from Task Scheduler
schtasks /delete /tn "%TASK_NAME%" /f

echo Task has been successfully deleted.
endlocal

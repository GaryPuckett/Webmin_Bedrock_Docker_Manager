@echo off
setlocal

rem Check if a folder was dragged onto the script
if "%~1"=="" (
    echo Please drag and drop a folder onto this script.
    pause
    exit /b
)

rem Get the full path of the dragged folder
set "sourceFolder=%~1"

rem Check if the dragged item is a directory
if not exist "%sourceFolder%\" (
    echo The dragged item is not a valid folder.
    pause
    exit /b
)

rem Save the current directory
set "currentDir=%cd%"

rem Change to the parent directory of the source folder
cd /d "%~dp1"

rem Define the destination tar file path
set "tarFile=%sourceFolder%.tar"

rem Use tar to compress the folder
tar -cvf "%tarFile%" "%~nx1"

rem Restore the original directory
cd /d "%currentDir%"
@echo off
setlocal enabledelayedexpansion

set "REPO=https://github.com/D0d0ka/whale-engine.git"
set "TEMP_DIR=whale-engine-temp"

if exist "WhaleEngine" rd /s /q "WhaleEngine"

:: Check if Git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed!
    echo Please install Git before running this script.
    exit /b 1
)

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python before running this script.
    exit /b 1
)

echo Cloning whale-engine...

git clone "%REPO%" "%TEMP_DIR%"
if %errorlevel% neq 0 (
    echo ERROR: Git clone failed.
    exit /b 1
)

echo Copying WhaleEngine...

xcopy /e /i /y "%TEMP_DIR%\WhaleEngine" "WhaleEngine"

:: Create main.py if it does not exist
if not exist "main.py" (
    echo main.py not found. Creating it from WhaleEngine/AppBase.py...
    copy "%TEMP_DIR%\AppBase.py" "main.py" >nul
)

:: Create NOTICE if it does not exist
if not exist "NOTICE" (
    echo NOTICE not found. Creating it from WhaleEngine/NOTICE...
    copy "%TEMP_DIR%\NOTICE" "NOTICE" >nul
)

:: Create .gitignore if it does not exist
if not exist ".gitignore" (
    echo .gitignore not found. Creating it from WhaleEngine/.gitignore...
    copy "%TEMP_DIR%\setup\.gitignoretemplate" ".gitignore" >nul
)

echo Deleting clone...

if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"

echo Done!
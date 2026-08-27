@echo off
setlocal

set "REPO=https://github.com/D0d0ka/whale-engine.git"
set "TEMP_DIR=whale-engine-temp"

:: Check if Git is installed
where git >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Git is not installed!
    echo Please install Git before running this script.
    echo.
    pause
    exit /b 1
)

echo Cloning whale-engine...

git clone "%REPO%" "%TEMP_DIR%"
if errorlevel 1 (
    echo.
    echo ERROR: Failed to clone repository!
    echo.
    pause
    exit /b 1
)

echo Copying WhaleEngine...

xcopy "%TEMP_DIR%\WhaleEngine" ".\WhaleEngine" /E /I /Y
if errorlevel 1 (
    echo.
    echo ERROR: Failed to copy WhaleEngine!
    echo.
    pause
    exit /b 1
)

echo Copying requirements...

xcopy "%TEMP_DIR%\requirements" ".\requirements" /E /I /Y
if errorlevel 1 (
    echo.
    echo ERROR: Failed to copy requirements!
    echo.
    pause
    exit /b 1
)

echo Deleting clone...

rmdir /S /Q "%TEMP_DIR%"

echo.
echo Done!
pause
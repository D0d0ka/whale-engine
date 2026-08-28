@echo off
setlocal EnableDelayedExpansion

:: ============================================================
:: WhaleEngine Setup Script - Windows
:: ============================================================

:: Check if Git is installed
where git >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Please install Git before running this script.
    echo You can download Git from:
    echo https://git-scm.com/downloads
    pause
    exit /b 1
)

:: Check if Python is installed
where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python before running this script.
    echo You can download Python from:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

set "REPO=https://github.com/D0d0ka/whale-engine.git"
set "TEMP_DIR=whale-engine-temp"


:: ============================================================
:: Main menu
:: ============================================================

echo.
echo Select what you want to do:
echo.
echo 1 - Install/update/reinstall WhaleEngine
echo 2 - Reinstall or install (more) Dependencies
echo 3 - Download documentation
echo 4 - Make .gitignore
echo 5 - Exit
echo.

set /p "number=Select an option (1-5): "

if "%number%"=="1" goto INSTALL_ENGINE
if "%number%"=="2" goto DEPENDENCIES
if "%number%"=="3" goto DOCUMENTATION
if "%number%"=="4" goto GITIGNORE
if "%number%"=="5" goto EXIT

echo.
echo Invalid option. Please select a number between 1 and 5.
goto FINISH


:: ============================================================
:: Install other dependencies
:: ============================================================

:INSTALL_OTHER_DEPENDENCIES

echo.
set /p "install_opengl=Do you want to install OpenGL dependencies now? (y/n): "

if /i "%install_opengl%"=="y" (
    echo Installing OpenGL dependencies...
    call .venv\Scripts\python.exe -m pip install -r WhaleEngine\requirements\openGLrequirements.txt

    if errorlevel 1 (
        echo ERROR: Failed to install OpenGL dependencies.
        exit /b 1
    )

    echo OpenGL dependencies installed.
)

echo.
set /p "install_vulkan=Do you want to install Vulkan dependencies now? (y/n): "

if /i "%install_vulkan%"=="y" (
    echo Installing Vulkan dependencies...
    call .venv\Scripts\python.exe -m pip install -r WhaleEngine\requirements\vulcanrequirements.txt

    if errorlevel 1 (
        echo ERROR: Failed to install Vulkan dependencies.
        exit /b 1
    )

    echo Vulkan dependencies installed.
)

echo.
set /p "install_webgl=Do you want to install WebGL dependencies now? (y/n): "

if /i "%install_webgl%"=="y" (
    echo Installing WebGL dependencies...
    call .venv\Scripts\python.exe -m pip install -r WhaleEngine\requirements\webGLrequirements.txt

    if errorlevel 1 (
        echo ERROR: Failed to install WebGL dependencies.
        exit /b 1
    )

    echo WebGL dependencies installed.
)

echo.
echo All selected dependencies installed.
exit /b 0


:: ============================================================
:: Install dependencies
:: ============================================================

:INSTALL_DEPENDENCIES

echo.
echo Making environment...

python -m venv .venv

if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    exit /b 1
)

echo Virtual environment created.

echo.
echo Upgrading pip...

call .venv\Scripts\python.exe -m pip install --upgrade pip

if errorlevel 1 (
    echo ERROR: Failed to upgrade pip.
    exit /b 1
)

echo pip upgraded.

echo.
echo Installing main dependencies...

call .venv\Scripts\python.exe -m pip install -r WhaleEngine\requirements\mainrequirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install main dependencies.
    exit /b 1
)

echo Main dependencies installed.

call :INSTALL_OTHER_DEPENDENCIES

if errorlevel 1 (
    exit /b 1
)

exit /b 0


:: ============================================================
:: Option 1 - Install/update/reinstall WhaleEngine
:: ============================================================

:INSTALL_ENGINE

echo.
echo Removing old WhaleEngine installation if it exists...

if exist "WhaleEngine" (
    rmdir /s /q "WhaleEngine"
)

echo Old WhaleEngine installation removed.

echo.
echo Removing old virtual environment if it exists...

if exist ".venv" (
    rmdir /s /q ".venv"
)

echo Old virtual environment removed.

echo.
echo Cloning whale-engine...

git clone "%REPO%" "%TEMP_DIR%"

if errorlevel 1 (
    echo ERROR: Failed to clone whale-engine.
    goto FINISH
)

echo whale-engine cloned.

echo.
echo Copying WhaleEngine...

xcopy "%TEMP_DIR%\WhaleEngine" "WhaleEngine" /E /I /H /Y >nul

if errorlevel 1 (
    echo ERROR: Failed to copy WhaleEngine.
    goto CLEANUP_TEMP
)

echo WhaleEngine copied.


:: Create main.py if it does not exist
if not exist "main.py" (
    echo.
    echo main.py not found. Creating it from WhaleEngine/AppBase.py...
    copy /Y "%TEMP_DIR%\AppBase.py" "main.py" >nul
)

:: Create NOTICE if it does not exist
if not exist "NOTICE" (
    echo.
    echo NOTICE not found. Creating it from WhaleEngine/NOTICE...
    copy /Y "%TEMP_DIR%\NOTICE" "NOTICE" >nul
)

:: Create .gitignore if it does not exist
if not exist ".gitignore" (
    echo.
    echo .gitignore not found. Creating it from WhaleEngine/setup/.gitignoretemplate...
    copy /Y "%TEMP_DIR%\setup\.gitignoretemplate" ".gitignore" >nul
)

:CLEANUP_TEMP

echo.
echo Deleting clone...

if exist "%TEMP_DIR%" (
    rmdir /s /q "%TEMP_DIR%"
)

echo Clone deleted.

echo.
echo Done!

echo.
set /p "install_deps=Do you want to install dependencies now? (y/n): "

if /i "%install_deps%"=="y" (
    call :INSTALL_DEPENDENCIES

    if errorlevel 1 (
        goto FINISH
    )
)

goto FINISH


:: ============================================================
:: Option 2 - Dependencies
:: ============================================================

:DEPENDENCIES

if not exist ".venv" (
    echo.
    echo Installing dependencies...

    call :INSTALL_DEPENDENCIES

    if errorlevel 1 (
        goto FINISH
    )

    echo.
    echo Dependencies installed.
    goto FINISH
)

echo.
echo Select what you want to do:
echo.
echo 1 - Reinstall dependencies
echo 2 - Install more dependencies
echo.

set /p "dep_option=Select an option (1-2): "

if "%dep_option%"=="1" goto REINSTALL_DEPENDENCIES
if "%dep_option%"=="2" goto MORE_DEPENDENCIES

echo.
echo Invalid option. Please select 1 or 2.
goto FINISH


:: ============================================================
:: Reinstall dependencies
:: ============================================================

:REINSTALL_DEPENDENCIES

echo.
echo Reinstalling dependencies...

echo.
echo Deleting old virtual environment...

if exist ".venv" (
    rmdir /s /q ".venv"
)

echo Old virtual environment deleted.

echo.
echo Reinstalling dependencies...

call :INSTALL_DEPENDENCIES

if errorlevel 1 (
    goto FINISH
)

echo.
echo Dependencies reinstalled.
goto FINISH


:: ============================================================
:: Install more dependencies
:: ============================================================

:MORE_DEPENDENCIES

echo.
echo Installing more dependencies...

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment is invalid or missing.
    goto FINISH
)

call :INSTALL_OTHER_DEPENDENCIES

if errorlevel 1 (
    goto FINISH
)

echo.
echo More dependencies installed.
goto FINISH


:: ============================================================
:: Option 3 - Documentation
:: ============================================================

:DOCUMENTATION

echo.
echo Downloading documentation...

echo.
echo Removing old documentation if it exists...

if exist "documentations" (
    rmdir /s /q "documentations"
)

echo Old documentation removed.

echo.
echo Cloning whale-engine...

git clone "%REPO%" "%TEMP_DIR%"

if errorlevel 1 (
    echo ERROR: Failed to clone whale-engine.
    goto FINISH
)

echo whale-engine cloned.

echo.
echo Creating documentation directory...

mkdir "documentations"

echo Documentation directory created.

echo.
echo Copying documentation...

copy /Y "%TEMP_DIR%\documentation.md" "documentations\" >nul

xcopy "%TEMP_DIR%\examples" "documentations\examples" /E /I /H /Y >nul

echo Documentation copied.

echo.
echo Removing temporary directory...

if exist "%TEMP_DIR%" (
    rmdir /s /q "%TEMP_DIR%"
)

echo Temporary directory removed.

echo.
echo Documentation setup completed.

goto FINISH


:: ============================================================
:: Option 4 - .gitignore
:: ============================================================

:GITIGNORE

echo.
echo Making .gitignore...

echo.
echo Removing old .gitignore if it exists...

if exist ".gitignore" (
    del /f /q ".gitignore"
)

echo Old .gitignore removed.

echo.
echo Cloning whale-engine...

git clone "%REPO%" "%TEMP_DIR%"

if errorlevel 1 (
    echo ERROR: Failed to clone whale-engine.
    goto FINISH
)

echo whale-engine cloned.

echo.
echo Copying .gitignore...

copy /Y "%TEMP_DIR%\setup\.gitignoretemplate" ".gitignore" >nul

echo .gitignore copied.

echo.
echo Removing temporary directory...

if exist "%TEMP_DIR%" (
    rmdir /s /q "%TEMP_DIR%"
)

echo Temporary directory removed.

echo.
echo .gitignore setup completed.

goto FINISH


:: ============================================================
:: Exit
:: ============================================================

:EXIT

echo.
echo Exiting...
exit /b 0


:: ============================================================
:: Finish
:: ============================================================

:FINISH

echo.
echo Setup finished.
pause
exit /b 0
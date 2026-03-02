@echo off
echo ============================================
echo   NEWMAN INSTALLATION
echo ============================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js not found!
    echo.
    echo Please install Node.js first:
    echo   https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo [INFO] Node.js found
node --version

echo.
echo [INFO] Installing Newman globally...
npm install -g newman

echo.
echo [INFO] Installing Newman HTML reporter...
npm install -g newman-reporter-htmlextra

echo.
echo ============================================
echo   INSTALLATION COMPLETE
echo ============================================
echo.
echo Newman installed successfully!
echo.
echo To verify: newman --version
echo.

pause
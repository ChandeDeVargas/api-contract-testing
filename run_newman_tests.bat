@echo off
setlocal

echo ============================================
echo   API CONTRACT TESTING - RUNNER
echo ============================================
echo.

:: Define paths
set COLLECTION=postman/collections/users-api-tests.json
set ENVIRONMENT=postman/environments/local.json
set REPORT_DIR=reports
set REPORT_FILE=%REPORT_DIR%/newman-report.html

:: Ensure reports directory exists
if not exist "%REPORT_DIR%" (
    echo [INFO] Creating reports directory...
    mkdir "%REPORT_DIR%"
)

:: Check if collection exists
if not exist "%COLLECTION%" (
    echo [ERROR] Collection file not found: %COLLECTION%
    exit /b 1
)

:: Check if environment exists
if not exist "%ENVIRONMENT%" (
    echo [ERROR] Environment file not found: %ENVIRONMENT%
    exit /b 1
)

echo [INFO] Running Newman tests...
echo        Collection: %COLLECTION%
echo        Environment: %ENVIRONMENT%
echo.

:: Run Newman with CLI and htmlextra reporters
call newman run "%COLLECTION%" ^
  -e "%ENVIRONMENT%" ^
  --reporters cli,htmlextra ^
  --reporter-htmlextra-export "%REPORT_FILE%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [WARNING] Newman execution finished with errors (some tests may have failed).
) else (
    echo.
    echo [SUCCESS] All Newman tests passed!
)

echo.
echo [INFO] Report generated at: %REPORT_FILE%
echo.

pause

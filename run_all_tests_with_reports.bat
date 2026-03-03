@echo off
echo ================================================================
echo    API CONTRACT TESTING FRAMEWORK
echo    Comprehensive Test Suite Execution
echo ================================================================
echo.

REM Check for virtual environment
if exist "venv\Scripts\python.exe" (
    echo [INFO] Using virtual environment
    set "PYTHON_CMD=venv\Scripts\python.exe"
    set "PYTEST_CMD=venv\Scripts\pytest.exe"
) else (
    echo [WARNING] Virtual environment not found, using global Python
    set "PYTHON_CMD=python"
    set "PYTEST_CMD=pytest"
)

REM Set UTF-8 encoding
set PYTHONIOENCODING=utf-8

REM Create reports directory
if not exist "reports" mkdir reports

REM Generate timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,8%_%datetime:~8,6%

REM Set report filename
set REPORT_FILE=reports\contract_test_report_%TIMESTAMP%.html

echo.
echo [INFO] Starting API contract tests...
echo [INFO] Report will be saved to: %REPORT_FILE%
echo.

REM Run all tests with HTML report
%PYTEST_CMD% tests/ ^
    --html=%REPORT_FILE% ^
    --self-contained-html ^
    -v ^
    --tb=short

echo.
echo ================================================================
echo    TEST EXECUTION COMPLETE
echo ================================================================
echo.
echo Report generated: %REPORT_FILE%
echo.
echo Test Categories:
echo   - OpenAPI Validation
echo   - Schema Compliance
echo   - Breaking Change Detection
echo   - Newman Integration
echo.
echo To view the report:
echo   start %REPORT_FILE%
echo.

REM Optional: Run Newman separately
echo.
echo [INFO] Running Newman collection tests...
echo.

where newman >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    newman run postman/collections/users-api-tests.json ^
        -e postman/environments/local.json ^
        --reporters cli,htmlextra ^
        --reporter-htmlextra-export reports/newman_report_%TIMESTAMP%.html
    
    echo.
    echo Newman report: reports/newman_report_%TIMESTAMP%.html
) else (
    echo [WARNING] Newman not installed, skipping Postman tests
    echo Install with: npm install -g newman newman-reporter-htmlextra
)

echo.
pause
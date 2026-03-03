#!/bin/bash

echo "================================================================"
echo "   API CONTRACT TESTING FRAMEWORK"
echo "   Comprehensive Test Suite Execution"
echo "================================================================"
echo

# Check for virtual environment
if [ -f "venv/bin/python" ]; then
    echo "[INFO] Using virtual environment"
    PYTHON_CMD="venv/bin/python"
    PYTEST_CMD="venv/bin/pytest"
else
    echo "[WARNING] Virtual environment not found, using global Python"
    PYTHON_CMD="python3"
    PYTEST_CMD="pytest"
fi

# Set UTF-8 encoding
export PYTHONIOENCODING=utf-8

# Create reports directory
mkdir -p reports

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Set report filename
REPORT_FILE="reports/contract_test_report_${TIMESTAMP}.html"

echo
echo "[INFO] Starting API contract tests..."
echo "[INFO] Report will be saved to: ${REPORT_FILE}"
echo

# Run all tests with HTML report
$PYTEST_CMD tests/ \
    --html=$REPORT_FILE \
    --self-contained-html \
    -v \
    --tb=short

echo
echo "================================================================"
echo "   TEST EXECUTION COMPLETE"
echo "================================================================"
echo
echo "Report generated: ${REPORT_FILE}"
echo
echo "Test Categories:"
echo "  - OpenAPI Validation"
echo "  - Schema Compliance"
echo "  - Breaking Change Detection"
echo "  - Newman Integration"
echo

# Optional: Run Newman separately
echo
echo "[INFO] Running Newman collection tests..."
echo

if command -v newman &> /dev/null; then
    newman run postman/collections/users-api-tests.json \
        -e postman/environments/local.json \
        --reporters cli,htmlextra \
        --reporter-htmlextra-export reports/newman_report_${TIMESTAMP}.html
    
    echo
    echo "Newman report: reports/newman_report_${TIMESTAMP}.html"
else
    echo "[WARNING] Newman not installed, skipping Postman tests"
    echo "Install with: npm install -g newman newman-reporter-htmlextra"
fi

echo

chmod +x run_all_tests.sh
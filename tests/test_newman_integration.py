"""
Newman Integration Tests
Run Postman collections via Newman CLI

Tests that Postman contract tests execute successfully
"""
import pytest
import subprocess
import json
from pathlib import Path

class TestNewmanIntegration:
    """
    Execute Postman collections with Newman.
    
    Purpose: Validate API contracts using Postman/Newman
    """
    @pytest.fixture
    def collection_path(self):
        """Path to Postman collection"""
        return "postman/collections/users-api-tests.json"

    @pytest.fixture
    def environment_path(self):
        """Path to Postman environment"""
        return "postman/environments/local.json"

    def test_collection_file_exists(self, collection_path):
        """
        Test: Postman collection file exists
        
        Basic check before running Newman
        """
        path = Path(collection_path)
        assert path.exists(), \
            f"Collection not found at {collection_path}"

        print(f"\nCollection: Found at {collection_path}")


    def test_environment_file_exists(self, environment_path):
        """
        Test: Environment file exists
        
        Validates environment configuration is present
        """
        path = Path(environment_path)
        assert path.exists(), \
            f"Environment not found at {environment_path}"

        print(f"\nEnvironment: Found at {environment_path}")

    def test_collection_is_valid_json(self, collection_path):
        """
        Test: Collection is valid JSON
        
        Validates collection structure before execution
        """
        try:
            with open(collection_path, 'r') as file:
                collection = json.load(file)

            # Check basic Postman collection structure
            assert 'info' in collection, "Missing 'info' in collection"
            assert 'item' in collection, "Missing 'item' in collection"

            print(f"\nCollection: Valid JSON structure")
            print(f" Name: {collection['info']['name']}")
            print(f" Requests: {len(collection['item'])} groups")

        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in collection: {e}")

    
    def test_newman_installed(self):
        """
        Test: Newman CLI is installed
        
        Validates Newman is available for execution
        """
        try:
            result = subprocess.run(
                ['newman', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"\nNewman: Installed (version {version})")
            else:
                pytest.skip("Newman not installed. Install with: npm install -g newman")
        
        except FileNotFoundError:
            pytest.skip("Newman not installed. Install with: npm install -g newman")
        except subprocess.TimeoutExpired:
            pytest.fail("Newman command timed out")

    def test_run_newman_collection(self, collection_path, environment_path):
        """
        Test: Execute Postman collection with Newman
        
        Runs all contract tests via Newman CLI
        
        Requirements:
        - Newman must be installed: npm install -g newman
        """
        # Check Newman is installed first
        try:
            subprocess.run(
                ['newman', '--version'],
                capture_output=True,
                timeout=5,
                check=True
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            pytest.skip("Newman not installed. Install with: npm install -g newman")
        
        print(f"\n[Newman Execution]")
        print(f"   Collection: {collection_path}")
        print(f"   Environment: {environment_path}")

        # Run Newman
        try:
            result = subprocess.run(
                [
                    'newman', 'run', 'collection_path',
                    '-e', environment_path,
                    '--reporters', 'cli',
                    '--color', 'on'
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            print(f"\n{result.stdout}")

            if result.returncode != 0:
                print(f"\nNewman execution failed:")
                print(result.stderr)
                pytest.fail("Newman tests failed")

            # Parse output for summary
            output = result.stdout

            if 'executed' in output.lower():
                print(f"\nNewman: All tests executed succesfully")

        except subprocess.TimeoutExpired:
            pytest.fail("Newman execution timed out (>30s)")
        except Exception as e:
            pytest.fail(f"Newman execution failed: {e}")

    def test_run_newman_with_json_report(self, collection_path, environment_path):
        """
        Test: Generate Newman JSON report
        
        Creates machine-readable test results
        """
        # Check Newman is installed
        try:
            subprocess.run(['newman', '--version'], 
                          capture_output=True, timeout=5, check=True)
        except:
            pytest.skip("Newman not installed")
        
        report_path = "reports/newman-report.json"
        
        print(f"\n[Newman JSON Report]")
        print(f"   Report will be saved to: {report_path}")
        
        try:
            result = subprocess.run(
                [
                    'newman', 'run', collection_path,
                    '-e', environment_path,
                    '--reporters', 'json',
                    '--reporter-json-export', report_path
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                pytest.fail("Newman execution failed")
            
            # Verify report was created
            report_file = Path(report_path)
            assert report_file.exists(), \
                f"Report not created at {report_path}"
            
            # Parse and display summary
            with open(report_path, 'r') as f:
                report = json.load(f)
            
            stats = report.get('run', {}).get('stats', {})
            assertions = stats.get('assertions', {})
            
            print(f"\nReport Generated:")
            print(f"   Total assertions: {assertions.get('total', 0)}")
            print(f"   Passed: {assertions.get('passed', 0)}")
            print(f"   Failed: {assertions.get('failed', 0)}")
            
        except subprocess.TimeoutExpired:
            pytest.fail("Newman execution timed out")
        except Exception as e:
            pytest.fail(f"Report generation error: {e}")
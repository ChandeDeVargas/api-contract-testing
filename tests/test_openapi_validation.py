"""
OpenAPI Specification Validation Tests
Validate that OpenAPI spec is valid and well-formed

Tests that the contract itself is correct before testing implementations
"""
from _pytest.stash import T
import pytest
import yaml
from pathlib import Path
from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename

class TestOpenAPISpecValidation:
    """
    Validate OpenAPI specification files.
    
    Purpose: Ensure the contract (OpenAPI spec) is valid
    before testing API implementations against it.
    """
    @pytest.fixture
    def users_api_spec_path(self):
        """Path to Users API OpenAPI spec"""
        return Path("contracts/openapi-specs/users-api-v1.yaml")
    
    
    def test_openapi_spec_exists(self, users_api_spec_path):
        """
        Test: OpenAPI spec file exists
        
        Basic check that the contract file is present
        """
        assert users_api_spec_path.exists(), \
            f"OpenAPI spec not found at {users_api_spec_path}"
        
        print(f"\nOpenAPI Spec: File exists at {users_api_spec_path}")
        
    def test_openapi_spec_is_valid_yaml(self, users_api_spec_path):
        """
        Test: OpenAPI spec is valid YAML
        
        Validates YAML syntax before validating OpenAPI structure
        """
        try:
            with open(users_api_spec_path, 'r') as f:
                spec = yaml.safe_load(f)
            
            assert spec is not None, "YAML file is empty"
            assert isinstance(spec, dict), "YAML root must be an object"
            
            print(f"\nYAML Syntax: Valid")
            print(f" Title: {spec.get('info', {}).get('title', 'N/A')}")
            print(f" Version: {spec.get('info', {}).get('version', 'N/A')}")
        
        except yaml.YAMLError as e:
            pytest.fail(f"Invalid YAML syntax: {e}")


    def test_openapi_spec_is_valid_openapi(self, users_api_spec_path):
        """
        Test: OpenAPI spec follows OpenAPI 3.0 standard
        
        Validates:
        - OpenAPI version
        - Required fields (info, paths)
        - Schema definitions
        - Response structures
        """
        try:
            # Read and validate spec
            spec_dict, spec_url = read_from_filename(str(users_api_spec_path))
            validate_spec(spec_dict)
            
            print(f"\nOpenAPI Validation: Spec is valid OpenAPI 3.0")
            print(f"Paths defined: {len(spec_dict.get('paths', {}))}")
            print(f"Schemas defined: {len(spec_dict.get('components', {}).get('schemas', {}))}")
            
        except Exception as e:
            pytest.fail(f"OpenAPI validation failed: {e}")
    def test_required_openapi_fields_present(self, users_api_spec_path):
        """
        Test: All required OpenAPI fields are present
        
        Required by OpenAPI 3.0 spec:
        - openapi (version)
        - info (title, version)
        - paths
        """
        with open(users_api_spec_path, 'r') as f:
            spec = yaml.safe_load(f)
        
        # Check openapi version
        assert 'openapi' in spec, "Missing 'openapi' field"
        assert spec['openapi'].startswith('3.0'), \
            f"Expected OpenAPI 3.0.x, got {spec['openapi']}"
        
        # Check info
        assert 'info' in spec, "Missing 'info' field"
        assert 'title' in spec['info'], "Missing 'info.title'"
        assert 'version' in spec['info'], "Missing 'info.version'"
        
        # Check paths
        assert 'paths' in spec, "Missing 'paths' field"
        assert len(spec['paths']) > 0, "No paths defined"
        
        print(f"\nRequired Fields: All present")
    
    
    def test_all_paths_have_operations(self, users_api_spec_path):
        """
        Test: All paths have at least one operation
        
        Each path should define at least one HTTP method (GET, POST, etc.)
        """
        with open(users_api_spec_path, 'r') as f:
            spec = yaml.safe_load(f)
        
        paths = spec.get('paths', {})
        
        invalid_paths = []
        
        for path, operations in paths.items():
            # Valid HTTP methods in OpenAPI
            http_methods = ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']
            
            has_operation = any(method in operations for method in http_methods)
            
            if not has_operation:
                invalid_paths.append(path)
        
        if invalid_paths:
            pytest.fail(
                f"Paths without operations: {invalid_paths}"
            )
        
        print(f"\nPath Operations: All {len(paths)} paths have operations")
    
    
    def test_all_operations_have_responses(self, users_api_spec_path):
        """
        Test: All operations define responses
        
        Every operation must define at least one response
        """
        with open(users_api_spec_path, 'r') as f:
            spec = yaml.safe_load(f)
        
        paths = spec.get('paths', {})
        
        missing_responses = []
        
        for path, operations in paths.items():
            http_methods = ['get', 'post', 'put', 'delete', 'patch']
            
            for method in http_methods:
                if method in operations:
                    operation = operations[method]
                    
                    if 'responses' not in operation:
                        missing_responses.append(f"{method.upper()} {path}")
                    elif len(operation['responses']) == 0:
                        missing_responses.append(f"{method.upper()} {path} (empty)")
        
        if missing_responses:
            pytest.fail(
                f"Operations without responses:\n" +
                "\n".join(f"  - {op}" for op in missing_responses)
            )
        
        print(f"\nResponses: All operations define responses")
    
    
    def test_schemas_are_well_defined(self, users_api_spec_path):
        """
        Test: All schemas have required properties defined
        
        Validates component schemas are properly structured
        """
        with open(users_api_spec_path, 'r') as f:
            spec = yaml.safe_load(f)
        
        schemas = spec.get('components', {}).get('schemas', {})
        
        issues = []
        
        for schema_name, schema_def in schemas.items():
            # Check type is defined
            if 'type' not in schema_def and '$ref' not in schema_def:
                issues.append(f"{schema_name}: Missing 'type' field")
            
            # If object type, check properties
            if schema_def.get('type') == 'object':
                if 'properties' not in schema_def:
                    issues.append(f"{schema_name}: Object without 'properties'")
        
        if issues:
            pytest.fail(
                f"Schema definition issues:\n" +
                "\n".join(f"  - {issue}" for issue in issues)
            )
        
        print(f"\nSchemas: All {len(schemas)} schemas well-defined")
        for schema_name in schemas.keys():
            print(f"   - {schema_name}")
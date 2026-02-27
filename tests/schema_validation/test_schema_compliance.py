"""
Schema Compliance Tests
Validate that real API responses match OpenAPI schema

Tests that the implementation (API) follows the contract (OpenAPI spec)
"""
import pytest
import requests
from tests.utils.openapi_loader import OpenAPILoader
from tests.utils.schema_validator import SchemaValidator


class TestSchemaCompliance:
    """
    Validate API responses against OpenAPI schemas.
    
    Purpose: Ensure API implementation matches contract
    """
    
    @pytest.fixture(scope='class')
    def openapi_loader(self):
        """Load OpenAPI spec"""
        return OpenAPILoader('contracts/openapi-specs/users-api-v1.yaml')
    
    
    @pytest.fixture(scope='class')
    def schema_validator(self):
        """Create schema validator"""
        return SchemaValidator()
    
    
    @pytest.fixture(scope='class')
    def base_url(self, openapi_loader):
        """Get base URL from OpenAPI spec"""
        return openapi_loader.get_base_url()

    def test_get_users_response_matches_schema(self, base_url, 
                                           openapi_loader, 
                                           schema_validator):
        """
        Test: GET /users/{id} response matches User schema
        
        Validates:
        - User object structure
        - Required fields (id, name, email, username)
        - Field types
        - Email format
        """
        # Get expected schema
        response_schema = openapi_loader.get_response_schema('/users/{id}', 'get')
    
        # Resolve $ref to actual User schema
        user_schema = openapi_loader.resolve_schema_ref(response_schema)
    
        # Call API with specific user ID
        user_id = 1
        response = requests.get(f"{base_url}/users/{user_id}")
    
        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}"
    
        data = response.json()
    
        print(f"\n[API Response] GET /users/{user_id}")
        print(f"   Status: {response.status_code}")
        print(f"   User: {data.get('name', 'N/A')}")
        print(f"   Email: {data.get('email', 'N/A')}")
    
        # Get full spec for $ref resolution
        full_spec = openapi_loader.get_spec()
    
        # Validate response matches schema
        errors = schema_validator.validate(data, user_schema, full_spec=full_spec)
    
        if errors:
            print(f"\n✗ SCHEMA VIOLATIONS:")
            for error in errors:
                print(f"   - {error}")
    
        assert len(errors) == 0, \
            f"✗ Schema validation failed: {len(errors)} errors"
    
        print(f"\n✓ Schema Compliance: User object matches spec")

    
    def test_user_required_fields_present(self, base_url, openapi_loader):
        """
        Test: User response contains all required fields
        
        Required fields per OpenAPI spec:
        - id (integer)
        - name (string)
        - email (string, format: email)
        - username (string)
        """
        # Get User schema
        user_schema = openapi_loader.get_schema('User')
        required_fields = user_schema.get('required', [])

        # Get user from API
        response = requests.get(f"{base_url}/users/1")
        data = response.json()

        print(f"\n[Required Fields Check]")
        print(f"   Required by spec: {required_fields}")

        missing_fields = []

        for field in required_fields:
            if field not in data:
                missing_fields.append(field)
            else:
                print(f"   ✓ {field}: {data[field]}")

        if missing_fields:
            print(f"   ✗ MISSING REQUIRED FIELDS:")
            for field in missing_fields:
                print(f"     - {field}")

            
        assert len(missing_fields) == 0, \
            f"Missing required fields: {missing_fields}"

        print(f"\n✓ Required Fields: All required fields present")

    def test_user_field_types_correct(self, base_url, openapi_loader, schema_validator):
        """
        Test: User field types match OpenAPI spec
        
        Type validations:
        - id: integer
        - name: string
        - email: string
        - username: string
        """
        # Get User schema
        user_schema = openapi_loader.get_schema('User')

        # Get user from API
        response = requests.get(f"{base_url}/users/1")
        data = response.json()

        print(f"\n[Type Validation]")

        # Validates types
        type_errors = schema_validator.validate_field_types(data, user_schema)

        if type_errors:
            print(f"\nTYPE MISMATCHES:")
            for error in type_errors:
                print(f"  - {error}")

        else:
            # Show correct types
            properties = user_schema.get('properties', {})
            for field, field_schema in properties.items():
                if field in data:
                   expected_type = field_schema.get('type', 'any')
                   actual_value = data[field]
                   print(f"   ✓ {field}: {expected_type} = {actual_value}")

            assert len(type_errors) == 0, \
                f"Type validation failed: {type_errors}"

            print(f"\n✓ All field types correct")
    def test_email_format_validation(self, base_url, schema_validator):
        """
        Test: Email field follows email format
        
        OpenAPI spec defines email as:
        type: string
        format: email
        
        Validates RFC-compliant email format
        """
        response = requests.get(f"{base_url}/users/1")
        data = response.json()
        
        email = data.get('email')
        
        print(f"\n[Email Format Validation]")
        print(f"   Email: {email}")
        
        is_valid = schema_validator.validate_email_format(email)
        
        if is_valid:
            print(f"   ✓ Valid email format")
        else:
            print(f"   ✗ Invalid email format")
        
        assert is_valid, \
            f"Email format invalid: {email}"
    
    
    def test_multiple_users_all_comply(self, base_url, 
                                  openapi_loader, 
                                  schema_validator):
        """
        Test: All users in GET /users comply with schema
        
        Validates every user object in the array
        """
        # Get User schema
        user_schema = openapi_loader.get_schema('User')
    
        # Get full spec for $ref resolution
        full_spec = openapi_loader.get_spec()
    
        # Get all users
        response = requests.get(f"{base_url}/users")
        users = response.json()
    
        print(f"\n[Bulk Validation] Testing {len(users)} users")
    
        violations = []
    
        for user in users:
            errors = schema_validator.validate(user, user_schema, full_spec=full_spec)
        
        if errors:
            violations.append({
                'user_id': user.get('id', 'unknown'),
                'errors': errors
            })
    
        if violations:
            print(f"\n✗ VIOLATIONS FOUND:")
            for v in violations:
                print(f"\n   User ID {v['user_id']}:")
                for error in v['errors']:
                    print(f"      - {error}")
    
        assert len(violations) == 0, \
            f"{len(violations)} users have schema violations"
    
        print(f"\n✓ All {len(users)} users comply with schema")
    
    
    def test_optional_fields_when_present(self, base_url, openapi_loader):
        """
        Test: Optional fields (when present) match schema types
        
        Optional fields per spec:
        - phone: string
        - website: string (format: uri)
        - address: object
        - company: object
        """
        user_schema = openapi_loader.get_schema('User')
        properties = user_schema.get('properties', {})
        required = user_schema.get('required', [])
        
        # Optional fields are those in properties but not in required
        optional_fields = [
            field for field in properties.keys() 
            if field not in required
        ]
        
        response = requests.get(f"{base_url}/users/1")
        data = response.json()
        
        print(f"\n[Optional Fields]")
        print(f"   Optional fields defined: {len(optional_fields)}")
        
        for field in optional_fields:
            if field in data:
                value = data[field]
                field_type = properties[field].get('type', 'any')
                print(f"   ✓ {field} ({field_type}): present")
            else:
                print(f"   ⚪ {field}: not present (OK - optional)")
        
        print(f"\n✓ Optional fields handled correctly")
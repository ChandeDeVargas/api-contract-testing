"""
JSON Schema Validator
Validate API responses against OpenAPI schemas
"""
import jsonschema
from typing import Dict, Any, List, Tuple
from jsonschema import Draft7Validator

class SchemaValidator:
    """
    Validate JSON data against schemas.
    
    Usage:
        validator = SchemaValidator()
        errors = validator.validate(data, schema)
        if errors:
            print(f"Validation failed: {errors}")
    """
    def __init__(self):
        """Initialize validator."""
        pass

    def validate(self, data: Any, schema: Dict[str, Any], 
             full_spec: Dict[str, Any] = None) -> List[str]:
        """
        Validate data against JSON schema.
    
        Args:
            data: Data to validate (dict, list, etc.)
            schema: JSON Schema definition
            full_spec: Full OpenAPI spec (needed for $ref resolution)
        
        Returns:
            List of error messages (empty if valid)
        """
        # If we have a full spec with $refs, use RefResolver
        if full_spec and '$ref' in str(schema):
            from jsonschema import RefResolver
        
            # Create resolver with full spec
            resolver = RefResolver.from_schema(full_spec)
            validator = Draft7Validator(schema, resolver=resolver)
        else:
            validator = Draft7Validator(schema)
    
        errors = []
    
        for error in validator.iter_errors(data):
            # Format error message
            path = ' -> '.join(str(p) for p in error.path) if error.path else 'root'
            message = f"{path}: {error.message}"
            errors.append(message)
    
        return errors
    
    def validate_field_types(self, data: Dict[str, Any], 
                            schema: Dict[str, Any]) -> List[str]:
        """
        Validate field types match schema.
        
        Args:
            data: Data object to validate
            schema: Schema with properties definitions
            
        Returns:
            List of type mismatch errors
        """
        errors = []
        properties = schema.get('properties', {})

        for field_name, field_schema in properties.items():
            if field_name not in data:
                continue
            
            field_value = data[field_name]
            expected_type = field_schema.get('type')

            if expected_type:
                if not self._check_type(field_value, expected_type):
                    errors.append(f"Field '{field_name}': expected {expected_type}, "f"got {type(field_value).__name__}")
            
        return errors

    def validate_required_fields(self, data: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
        """
        Validate all required fields are present.
        
        Args:
            data: Data object to validate
            schema: Schema with required field list
            
        Returns:
            List of missing field errors
        """
        required = schema.get('required', [])
        errors = []

        for field in required:
            if field not in data:
                errors.append(f"Required field '{field}' is missing")
        
        return errors

    def validate_email_format(self, email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: Email string to validate
            
        Returns:
            True if valid email format
        """
        import re
        email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        return bool(email_pattern.match(email))

    def validate_format(self, value: Any, format_type: str) -> bool:
        """
        Validate value matches format type.
        
        Args:
            value: Value to validate
            format_type: Format type (email, uri, etc.)
            
        Returns:
            True if valid format
        """
        if format_type == 'email':
            return self.validate_email_format(str(value))
        
        elif format_type == 'uri':
            import re
            uri_pattern = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
                r'localhost|'  # localhost
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            return bool(uri_pattern.match(str(value)))
        
        # Add more format validators as needed
        return True
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """
        Check if value matches expected JSON Schema type.
        
        Args:
            value: Value to check
            expected_type: Expected type string
            
        Returns:
            True if type matches
        """
        type_mapping = {
            'string': str,
            'integer': int,
            'number': (int, float),
            'boolean': bool,
            'array': list,
            'object': dict,
            'null': type(None)
        }
        
        expected_python_type = type_mapping.get(expected_type)
        
        if expected_python_type is None:
            return True  # Unknown type, assume valid
        
        return isinstance(value, expected_python_type)
    
    
    def get_validation_summary(self, data: Any, 
                              schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get complete validation summary.
        
        Args:
            data: Data to validate
            schema: Schema to validate against
            
        Returns:
            Dict with validation results
        """
        all_errors = self.validate(data, schema)
        
        return {
            'valid': len(all_errors) == 0,
            'error_count': len(all_errors),
            'errors': all_errors
        }
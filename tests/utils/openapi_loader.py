"""
OpenAPI Specification Loader Utility
Load and parse OpenAPI specs for testing
"""
import yaml
from pathlib import Path
from typing import Dict, Any

class OpenAPILoader:
    """
    Load and parse OpenAPI specifications.
    
    Usage:
        loader = OpenAPILoader('contracts/openapi-specs/users-api-v1.yaml')
        spec = loader.get_spec()
        schema = loader.get_schema('User')
    """
    def __init__(self, spec_path: str):
        """
        Initialize loader with OpenAPI spec path.
        
        Args:
            spec_path: Path to OpenAPI YAML file
        """
        self.spec_path = Path(spec_path)
        self._spec = None

    def get_spec(self) -> Dict[str, Any]:
        """
        Load and return full OpenAPI spec.
        
        Returns:
            Dict containing full OpenAPI specification
        """
        if self._spec is None:
            with open(self.spec_path, 'r') as f:
                self._spec = yaml.safe_load(f)
        return self._spec

    def get_schema(self, schema_name: str) -> Dict[str, Any]:
        """
        Get a specific schema from components/schemas.
        
        Args:
            schema_name: Name of schema (e.g., 'User', 'Error')
            
        Returns:
            Schema definition dict
            
        Raises:
            KeyError: If schema not found
        """
        spec = self.get_spec()
        schemas = spec.get('components', {}).get('schemas', {})

        if schema_name not in schemas:
            raise KeyError(f"Schema '{schema_name}' not found in spec")

        return schemas[schema_name]

    def get_operation(self, path: str, method: str) -> Dict[str, Any]:
        """
        Get operation definition for a path and method.
        
        Args:
            path: API path (e.g., '/users', '/users/{id}')
            method: HTTP method (e.g., 'get', 'post')
            
        Returns:
            Operation definition dict
            
        Raises:
            KeyError: If path or method not found
        """
        spec = self.get_spec()
        paths = spec.get('paths', {})

        if path not in paths:
            raise KeyError(f"Path '{path}' not found in spec")

        path_item = paths[path]

        if method.lower() not in path_item:
            raise KeyError(f"Method '{method}' not found for path '{path}'")

        return path_item[method.lower()]

    def get_response_schema(self, path: str, method: str, status_code: str = '200') -> Dict[str, Any]:
        """
        Get response schema for a specific operation.
        
        Args:
            path: API path
            method: HTTP method
            status_code: Response status code (default: '200')
            
        Returns:
            Response schema dict
            
        Raises:
            KeyError: If operation or response not found
        """
        operation = self.get_operation(path, method)
        responses = operation.get('responses', {})

        if status_code not in responses:
            raise KeyError(f"Response {status_code} not found for {method.upper()} {path}")

        response = responses[status_code]
        content = response.get('content', {})

        if 'application/json' not in content:
            raise KeyError(f"No JSON response defined for {method.upper()} {path} {status_code}")

        return content['application/json']['schema']

    def get_base_url(self) -> str:
        """
        Get first server URL from spec.
        
        Returns:
            Base URL string
        """
        spec = self.get_spec()
        servers = spec.get('servers', [])

        if not servers:
            raise ValueError("No servers defined in spec")

        return servers[0]['url']

    def resolve_schema_ref(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve $ref in schema to actual schema definition.
        
        Args:
            schema: Schema dict that may contain $ref
            
        Returns:
            Resolved schema dict
        """
        if '$ref' not in schema:
            return schema
        
        # Extract schema name from $ref
        # Example: '#/components/schemas/User' -> 'User'
        ref = schema['$ref']
        schema_name = ref.split('/')[-1]

        return self.get_schema(schema_name)
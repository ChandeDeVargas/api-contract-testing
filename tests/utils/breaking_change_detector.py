"""
Breaking Change Detector
Compare two OpenAPI specs and detect breaking changes

Breaking changes are changes that break existing API consumers:
- Removing fields
- Changing field types
- Adding required fields
- Changing response codes
- Removing enum values
"""
from typing import Dict, Any, List, Tuple
from tests.utils.openapi_loader import OpenAPILoader


class BreakingChange:
    """
    Represents a single breaking change.
    
    Attributes:
        category: Type of breaking change
        severity: critical, high, medium
        path: Location in spec (e.g., '/users', 'User.name')
        old_value: Previous value
        new_value: New value
        description: Human-readable description
        impact: Business impact description
    """
    
    def __init__(self, category: str, severity: str, path: str,
                 old_value: Any, new_value: Any, description: str,
                 impact: str = ""):
        self.category = category
        self.severity = severity
        self.path = path
        self.old_value = old_value
        self.new_value = new_value
        self.description = description
        self.impact = impact
    
    def __repr__(self):
        return (f"BreakingChange({self.severity.upper()}: {self.category} "
                f"at {self.path})")
    
    def to_dict(self):
        """Convert to dictionary for reporting"""
        return {
            'category': self.category,
            'severity': self.severity,
            'path': self.path,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'description': self.description,
            'impact': self.impact
        }


class BreakingChangeDetector:
    """
    Detect breaking changes between two OpenAPI specifications.
    
    Usage:
        detector = BreakingChangeDetector('v1.yaml', 'v2.yaml')
        changes = detector.detect_all_changes()
        if changes:
            print(f"Found {len(changes)} breaking changes!")
    """
    
    def __init__(self, old_spec_path: str, new_spec_path: str):
        """
        Initialize detector with two spec versions.
        
        Args:
            old_spec_path: Path to old/current OpenAPI spec
            new_spec_path: Path to new/proposed OpenAPI spec
        """
        self.old_loader = OpenAPILoader(old_spec_path)
        self.new_loader = OpenAPILoader(new_spec_path)
        
        self.old_spec = self.old_loader.get_spec()
        self.new_spec = self.new_loader.get_spec()
    
    
    def detect_all_changes(self) -> List[BreakingChange]:
        """
        Detect all breaking changes between specs.
        
        Returns:
            List of BreakingChange objects
        """
        changes = []
        
        # Detect schema changes
        changes.extend(self.detect_schema_changes())
        
        # Detect response changes
        changes.extend(self.detect_response_changes())
        
        # Detect required field changes
        changes.extend(self.detect_required_field_changes())
        
        # Detect type changes
        changes.extend(self.detect_type_changes())
        
        return changes
    
    
    def detect_schema_changes(self) -> List[BreakingChange]:
        """
        Detect changes in component schemas.
        
        Breaking changes:
        - Field removed
        - Schema removed
        """
        changes = []
        
        old_schemas = self.old_spec.get('components', {}).get('schemas', {})
        new_schemas = self.new_spec.get('components', {}).get('schemas', {})
        
        # Check for removed schemas
        for schema_name in old_schemas.keys():
            if schema_name not in new_schemas:
                changes.append(BreakingChange(
                    category='schema_removed',
                    severity='critical',
                    path=f'schemas/{schema_name}',
                    old_value=schema_name,
                    new_value=None,
                    description=f"Schema '{schema_name}' was removed",
                    impact=f"All consumers using {schema_name} will break"
                ))
        
        # Check for removed fields in schemas
        for schema_name in old_schemas.keys():
            if schema_name in new_schemas:
                old_properties = old_schemas[schema_name].get('properties', {})
                new_properties = new_schemas[schema_name].get('properties', {})
                
                for field_name in old_properties.keys():
                    if field_name not in new_properties:
                        changes.append(BreakingChange(
                            category='field_removed',
                            severity='critical',
                            path=f'schemas/{schema_name}.{field_name}',
                            old_value=old_properties[field_name],
                            new_value=None,
                            description=f"Field '{field_name}' removed from {schema_name}",
                            impact=f"Consumers expecting '{field_name}' will fail"
                        ))
        
        return changes
    
    
    def detect_type_changes(self) -> List[BreakingChange]:
        """
        Detect field type changes.
        
        Breaking change:
        - Field type changed (e.g., integer → string)
        """
        changes = []
        
        old_schemas = self.old_spec.get('components', {}).get('schemas', {})
        new_schemas = self.new_spec.get('components', {}).get('schemas', {})
        
        for schema_name in old_schemas.keys():
            if schema_name not in new_schemas:
                continue
            
            old_properties = old_schemas[schema_name].get('properties', {})
            new_properties = new_schemas[schema_name].get('properties', {})
            
            for field_name in old_properties.keys():
                if field_name not in new_properties:
                    continue
                
                old_type = old_properties[field_name].get('type')
                new_type = new_properties[field_name].get('type')
                
                if old_type and new_type and old_type != new_type:
                    changes.append(BreakingChange(
                        category='type_changed',
                        severity='critical',
                        path=f'schemas/{schema_name}.{field_name}',
                        old_value=old_type,
                        new_value=new_type,
                        description=f"Field '{field_name}' type changed from {old_type} to {new_type}",
                        impact=f"Type mismatch will cause parsing errors"
                    ))
        
        return changes
    
    
    def detect_required_field_changes(self) -> List[BreakingChange]:
        """
        Detect changes in required fields.
        
        Breaking change:
        - New required field added
        - Required field removed (less common, but notable)
        """
        changes = []
        
        old_schemas = self.old_spec.get('components', {}).get('schemas', {})
        new_schemas = self.new_spec.get('components', {}).get('schemas', {})
        
        for schema_name in old_schemas.keys():
            if schema_name not in new_schemas:
                continue
            
            old_required = set(old_schemas[schema_name].get('required', []))
            new_required = set(new_schemas[schema_name].get('required', []))
            
            # New required fields (breaking)
            added_required = new_required - old_required
            for field in added_required:
                changes.append(BreakingChange(
                    category='required_field_added',
                    severity='high',
                    path=f'schemas/{schema_name}.required',
                    old_value=list(old_required),
                    new_value=list(new_required),
                    description=f"Field '{field}' is now required in {schema_name}",
                    impact=f"Existing requests without '{field}' will fail validation"
                ))
            
            # Removed required fields (less breaking, but notable)
            removed_required = old_required - new_required
            for field in removed_required:
                changes.append(BreakingChange(
                    category='required_field_removed',
                    severity='medium',
                    path=f'schemas/{schema_name}.required',
                    old_value=list(old_required),
                    new_value=list(new_required),
                    description=f"Field '{field}' is no longer required in {schema_name}",
                    impact=f"Field is now optional (usually safe change)"
                ))
        
        return changes
    
    
    def detect_response_changes(self) -> List[BreakingChange]:
        """
        Detect changes in response status codes.
        
        Breaking change:
        - Response code changed (e.g., 201 → 200)
        - Response removed
        """
        changes = []
        
        old_paths = self.old_spec.get('paths', {})
        new_paths = self.new_spec.get('paths', {})
        
        for path, path_item in old_paths.items():
            if path not in new_paths:
                continue
            
            # Check each HTTP method
            for method in ['get', 'post', 'put', 'delete', 'patch']:
                if method not in path_item:
                    continue
                
                if method not in new_paths[path]:
                    changes.append(BreakingChange(
                        category='endpoint_removed',
                        severity='critical',
                        path=f'{method.upper()} {path}',
                        old_value=method,
                        new_value=None,
                        description=f"Endpoint {method.upper()} {path} was removed",
                        impact=f"All consumers calling this endpoint will fail"
                    ))
                    continue
                
                old_responses = path_item[method].get('responses', {})
                new_responses = new_paths[path][method].get('responses', {})
                
                # Check for changed success response codes
                old_success_codes = [code for code in old_responses.keys() 
                                    if code.startswith('2')]
                new_success_codes = [code for code in new_responses.keys() 
                                    if code.startswith('2')]
                
                if old_success_codes and new_success_codes:
                    if old_success_codes[0] != new_success_codes[0]:
                        changes.append(BreakingChange(
                            category='response_code_changed',
                            severity='high',
                            path=f'{method.upper()} {path}',
                            old_value=old_success_codes[0],
                            new_value=new_success_codes[0],
                            description=f"Success response code changed from {old_success_codes[0]} to {new_success_codes[0]}",
                            impact=f"Consumers checking for {old_success_codes[0]} will miss successful responses"
                        ))
        
        return changes
    
    
    def get_summary(self, changes: List[BreakingChange]) -> Dict[str, Any]:
        """
        Get summary statistics of breaking changes.
        
        Args:
            changes: List of BreakingChange objects
            
        Returns:
            Dict with summary statistics
        """
        if not changes:
            return {
                'total': 0,
                'by_severity': {},
                'by_category': {},
                'critical_count': 0
            }
        
        by_severity = {}
        by_category = {}
        
        for change in changes:
            # Count by severity
            by_severity[change.severity] = by_severity.get(change.severity, 0) + 1
            
            # Count by category
            by_category[change.category] = by_category.get(change.category, 0) + 1
        
        return {
            'total': len(changes),
            'by_severity': by_severity,
            'by_category': by_category,
            'critical_count': by_severity.get('critical', 0)
        }
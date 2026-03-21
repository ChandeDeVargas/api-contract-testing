"""
API Validator
Class for validating API responses (OOP pattern)

Features:
- Status code validation
- Header validation
- Response time validation
- Content type validation
- JSON structure validation
"""
from requests import request
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime

class APIValidator:
    """
    API Response Validator.
    
    Validates different aspects of HTTP responses.
    Uses OOP to organize validations.
    """

    def __init__(self, response: requests.Response):
        """
        Initialize validator with response.
        
        Args:
            response: requests.Response object
        """
        self.response = response
        self.status_code = response.status_code
        self.headers = response.headers
        
        # Calculate response time in seconds
        self.response_time = response.elapsed.total_seconds()
        
        # Try to parse JSON
        try:
            self.json_data = response.json()
        except:
            self.json_data = None
            
    # ============================================
    # Status Code Validations
    # ============================================
    
    def assert_status_code(self, expected_code: int) -> 'APIValidator':
        """
        Assert status code equals expected.
        
        Args:
            expected_code: Expected status code
            
        Returns:
            APIValidator: self (for method chaining)
        """
        assert self.status_code == expected_code, \
            f"Expected status {expected_code}, got {self.status_code}"
            
        print(f"Status code {expected_code} OK")
        return self
    
    def assert_status_ok(self) -> 'APIValidator':
        """
        Assert status code is 200 OK.
        
        Returns:
            APIValidator: self (for method chaining)
        """
        return self.assert_status_code(200)
    
    def assert_status_created(self) -> 'APIValidator':
        """
        Assert status code is 201 Created.
        
        Returns:
            APIValidator: self (for method chaining)
        """
        return self.assert_status_code(201)
    
    def assert_status_no_found(self) -> 'APIValidator':
        """
        Assert status code is 404 Not Found.
        
        Returns:
            APIValidator: self (for method chaining)
        """
        return self.assert_status_code(404)
    
    def assert_status_in_range(self, start: int, end: int) -> 'APIValidator':
        """
        Assert status code is within range.
        
        Args:
            start: Start of range (inclusive)
            end: End of range (inclusive)
            
        Returns:
            APIValidator: self (for method chaining)
        """
        assert start <= self.status_code <= end, \
            f"Status {self.status_code} not in range {start}-{end}"
        
        print(f"Status code {self.status_code} in range {start}-{end} OK")
        return self

    def assert_status_success(self) -> 'APIValidator':
        """
        Assert status code is 2xx (success).
        
        Returns:
            APIValidator: self (for method chaining)
        """
        return self.assert_status_in_range(200, 299)
    
    # ============================================
    # Header Validations
    # ============================================
    
    def assert_header_exists(self, header_name: str) -> 'APIValidator':
        """
        Assert header exists in response.
        
        Args:
            header_name: Header name to check
            
        Returns:
            APIValidator: self (for method chaining)
        """
        assert header_name in self.headers, f"Header '{header_name}' not found in response"
        print(f"Header '{header_name}' exists")
        return self
    
    def assert_header_value(self, header_name: str, expected_value: str) -> 'APIValidator':
        """
        Assert header has specific value.
        
        Args:
            header_name: Header name
            expected_value: Expected value
            
        Returns:
            APIValidator: self (for method chaining)
        """
        actual_value = self.headers.get(header_name)
        
        assert actual_value == expected_value, \
            f"Header '{header_name}' expected '{expected_value}', got '{actual_value}'"
        
        print(f"Header '{header_name}' = '{expected_value}'")
        return self
    
    def assert_header_contains(self, header_name: str, expected_substring: str) -> 'APIValidator':
        """
        Assert header value contains substring.
        
        Args:
            header_name: Header name
            expected_substring: Expected substring
            
        Returns:
            APIValidator: self (for method chaining)
        """
        actual_value = self.headers.get(header_name, "")
        
        assert expected_substring in actual_value, \
            f"Header '{header_name}' doesn't contain '{expected_substring}'"
        
        print(f"Header '{header_name}' contains '{expected_substring}'")
        return self
    
    def assert_content_type(self, expected_type: str = "application/json") -> 'APIValidator':
        """
        Assert Content-Type header.
        
        Args:
            expected_type: Expected content type
            
        Returns:
            APIValidator: self (for method chaining)
        """
        return self.assert_header_contains("Content-Type", expected_type)
    
    def assert_content_type_json(self) -> 'APIValidator':
        """
        Assert Content-Type is JSON.
        
        Returns:
            APIValidator: self (for method chaining)
        """
        return self.assert_content_type("application/json")

    # ============================================
    # Response Time Validations
    # ============================================
    
    def assert_response_time_under(self, max_seconds: float) -> 'APIValidator':
        """
        Assert response time is under max seconds.
        
        Args:
            max_seconds: Maximum allowed seconds
            
        Returns:
            APIValidator: self (for method chaining)
        """
        assert self.response_time <= max_seconds, \
            f"Response time {self.response_time:.3f}s exceeds {max_seconds}s"
            
        print(f"Response time {self.response_time:.3f}s (under {max_seconds}s)")
        return self
    
    def assert_response_fast(self) -> 'APIValidator':
        """
        Assert response time under 1 second.
        
        Returns:
            APIValidator: self (for method chaining)
        """
        return self.assert_response_time_under(1.0)
    
    def assert_response_very_fast(self) -> 'APIValidator':
        """
        Assert response time under 500ms.
        
        Returns:
            APIValidator: self (for method chaining)
        """
        return self.assert_response_time_under(0.5)
    
    def get_response_time_ms(self) -> float:
        """
        Get response time in milliseconds.
        
        Returns:
            float: Response time in milliseconds
        """
        return self.response_time * 1000
    
    # ============================================
    # JSON Data Validations
    # ============================================
    
    def assert_json_not_empty(self) -> 'APIValidator':
        """
        Assert response has JSON data.
        
        Returns:
            APIValidator: self (for method chaining)
        """
        assert self.json_data is not None, "Response has no JSON data"
        print("Response has JSON data")
        return self
    
    
    def assert_json_is_list(self) -> 'APIValidator':
        """
        Assert JSON response is a list.
        
        Returns:
            APIValidator: self (for method chaining)
        """
        assert isinstance(self.json_data, list), \
            f"Expected list, got {type(self.json_data).__name__}"
        
        print(f"Response is list with {len(self.json_data)} items")
        return self
    
    
    def assert_json_is_dict(self) -> 'APIValidator':
        """
        Assert JSON response is a dictionary.
        
        Returns:
            APIValidator: self (for method chaining)
        """
        assert isinstance(self.json_data, dict), \
            f"Expected dict, got {type(self.json_data).__name__}"
        
        print("Response is dictionary")
        return self
    
    
    def assert_json_length(self, expected_length: int) -> 'APIValidator':
        """
        Assert JSON list/dict has expected length.
        
        Args:
            expected_length: Expected length
            
        Returns:
            APIValidator: self (for method chaining)
        """
        actual_length = len(self.json_data)
        
        assert actual_length == expected_length, \
            f"Expected length {expected_length}, got {actual_length}"
        
        print(f"JSON length correct: {expected_length}")
        return self
    
    
    def assert_json_min_length(self, min_length: int) -> 'APIValidator':
        """
        Assert JSON has minimum length.
        
        Args:
            min_length: Minimum expected length
            
        Returns:
            APIValidator: self (for method chaining)
        """
        actual_length = len(self.json_data)
        
        assert actual_length >= min_length, \
            f"Expected at least {min_length} items, got {actual_length}"
        
        print(f"JSON has minimum length: {min_length}")
        return self
    
    
    def assert_field_exists(self, field: str) -> 'APIValidator':
        """
        Assert field exists in JSON response.
        
        Args:
            field: Field name to check
            
        Returns:
            APIValidator: self (for method chaining)
        """
        assert field in self.json_data, \
            f"Field '{field}' not found in response"
        
        print(f"Field exists: {field}")
        return self
    
    
    def assert_field_type(self, field: str, expected_type: type) -> 'APIValidator':
        """
        Assert field has expected type.
        
        Args:
            field: Field name
            expected_type: Expected Python type
            
        Returns:
            APIValidator: self (for method chaining)
        """
        value = self.json_data.get(field)
        
        assert isinstance(value, expected_type), \
            f"Field '{field}' is {type(value).__name__}, expected {expected_type.__name__}"
        
        print(f"Field '{field}' has type {expected_type.__name__}")
        return self
    
    
    def assert_field_value(self, field: str, expected_value: Any) -> 'APIValidator':
        """
        Assert field has expected value.
        
        Args:
            field: Field name
            expected_value: Expected value
            
        Returns:
            APIValidator: self (for method chaining)
        """
        actual_value = self.json_data.get(field)
        
        assert actual_value == expected_value, \
            f"Field '{field}' expected '{expected_value}', got '{actual_value}'"
        
        print(f"Field '{field}' = '{expected_value}'")
        return self
    
    
    def assert_field_not_null(self, field: str) -> 'APIValidator':
        """
        Assert field is not null/None.
        
        Args:
            field: Field name
            
        Returns:
            APIValidator: self (for method chaining)
        """
        value = self.json_data.get(field)
        
        assert value is not None, \
            f"Field '{field}' is null"
        
        print(f"Field '{field}' is not null")
        return self
    
    
    # ============================================
    # Get Methods
    # ============================================
    
    def get_json(self) -> Any:
        """Get JSON data"""
        return self.json_data
    
    
    def get_header(self, header_name: str) -> Optional[str]:
        """Get header value"""
        return self.headers.get(header_name)
    
    
    def get_status_code(self) -> int:
        """Get status code"""
        return self.status_code
    
    
    # ============================================
    # Utility Methods
    # ============================================
    
    def print_summary(self) -> None:
        """Print response summary"""
        print("\n" + "="*60)
        print("API RESPONSE SUMMARY")
        print("="*60)
        print(f"Status Code: {self.status_code}")
        print(f"Response Time: {self.response_time:.3f}s ({self.get_response_time_ms():.0f}ms)")
        print(f"Content-Type: {self.get_header('Content-Type')}")
        
        if self.json_data:
            if isinstance(self.json_data, list):
                print(f"Data Type: List ({len(self.json_data)} items)")
            elif isinstance(self.json_data, dict):
                print(f"Data Type: Dict ({len(self.json_data)} fields)")
        
        print("="*60 + "\n")
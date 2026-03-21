"""
API Validator Tests
Tests demonstrating APIValidator class usage

Uses JSONPlaceholder API for testing
"""
import requests
from utils.api_validator import APIValidator

class TestAPIValidator:
    """
    API Validator tests.
    
    Practices OOP with APIValidator class.
    """
    BASE_URL = "https://jsonplaceholder.typicode.com"
    
    def test_get_users_with_validator(self):
        """
        Test: GET /users with APIValidator
        
        Demonstrates method chaining and multiple validations
        """
        # Make request
        response = requests.get(f"{self.BASE_URL}/users")
        
        # Create validator
        validator = APIValidator(response)
        
        validator.assert_status_ok() \
            .assert_content_type_json() \
            .assert_response_time_under(2.0) \
            .assert_json_is_list() \
            .assert_json_min_length(1)
            
        # Summary
        validator.print_summary()
        
        print("Test passed: GET /users validated")
        
    def test_get_single_user(self):
        """Test: GET /users/1 validations"""
        response = requests.get(f"{self.BASE_URL}/users/1")
        
        validator = APIValidator(response)
        
        # Multiple validations
        validator.assert_status_ok() \
            .assert_content_type_json() \
            .assert_response_time_under(2.0) \
            .assert_json_is_dict() \
            .assert_field_exists("id") \
            .assert_field_exists("name") \
            .assert_field_exists("email") \
            .assert_field_type("id", int) \
            .assert_field_type("name", str) \
            .assert_field_type("email", str) \
            .assert_field_value("id", 1)
            
        # Verify email format
        user_data = validator.get_json()
        assert "@" in user_data["email"], "Invalid email format"
         
        print("Test passed: Single user validated")
        
    def test_404_not_found(self):
        """Test: Validate 404 response"""
        response = requests.get(f"{self.BASE_URL}/users/999999")
        
        validator = APIValidator(response)
        
        validator.assert_status_no_found() \
            .assert_content_type_json() \
            .assert_response_fast()
        
        print("Test passed: 404 handled correctly")
    
    def test_response_time_validation(self):
        """Test: Response time validation"""
        response = requests.get(f"{self.BASE_URL}/posts")
        
        validator = APIValidator(response)
        
        # Different time assertions
        validator.assert_response_time_under(2.0) # Under 2 seconds
        
        # Get exact time
        response_time_ms = validator.get_response_time_ms()
        print(f"Response time: {response_time_ms:.0f} ms")
        
        assert response_time_ms < 3000, "Response too slow"
        
        print("Test passed: Response time OK")
        
    def test_headers_validation(self):
        """Test: Header validations"""
        response = requests.get(f"{self.BASE_URL}/users")
        
        validator = APIValidator(response)
        
        # Validate headers exist
        validator.assert_header_exists("Content-Type") \
            .assert_header_exists("Date") \
            .assert_header_contains("Content-Type", "application/json")
        
        # Get specific header
        content_type = validator.get_header("Content-Type")
        print(f"Content-Type: {content_type}")
        
        print("Test passed: Headers validated")
    
    
    def test_posts_endpoint(self):
        """Test: GET /posts validation"""
        response = requests.get(f"{self.BASE_URL}/posts")
        
        validator = APIValidator(response)
        
        validator.assert_status_success() \
            .assert_json_is_list() \
            .assert_json_min_length(50)  # Should have 100 posts
        
        # Validate first post structure
        posts = validator.get_json()
        first_post = posts[0]
        
        # Validate fields
        assert "userId" in first_post
        assert "id" in first_post
        assert "title" in first_post
        assert "body" in first_post
        
        # Validate types
        assert isinstance(first_post["userId"], int)
        assert isinstance(first_post["id"], int)
        assert isinstance(first_post["title"], str)
        assert isinstance(first_post["body"], str)
        
        print("Test passed: Posts endpoint validated")
    
    
    def test_comments_endpoint(self):
        """Test: GET /comments validation"""
        response = requests.get(f"{self.BASE_URL}/comments")
        
        validator = APIValidator(response)
        
        validator.assert_status_ok() \
            .assert_response_time_under(2.0) \
            .assert_json_is_list() \
            .assert_json_min_length(100)
        
        # Validate comment structure
        comments = validator.get_json()
        first_comment = comments[0]
        
        required_fields = ["postId", "id", "name", "email", "body"]
        for field in required_fields:
            assert field in first_comment, f"Missing field: {field}"
        
        # Validate email format
        assert "@" in first_comment["email"]
        
        print("Test passed: Comments endpoint validated")
    
    
    def test_albums_endpoint(self):
        """Test: GET /albums validation"""
        response = requests.get(f"{self.BASE_URL}/albums")
        
        validator = APIValidator(response)
        
        validator.assert_status_ok() \
            .assert_content_type_json() \
            .assert_json_is_list()
        
        # Print summary
        validator.print_summary()
        
        print("Test passed: Albums endpoint validated")
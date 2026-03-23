"""
Parametrized Endpoint Tests
Test multiple endpoints with same validation logic

Uses pytest.mark.parametrize for DRY code
"""
import pytest
from utils.api_helper import APIHelper
from utils.api_logger import logger


class TestParametrizedEndpoints:
    """Test multiple endpoints with parametrization"""
    
    BASE_URL = "https://jsonplaceholder.typicode.com"
    
    @pytest.fixture
    def api(self):
        """Create API Helper instance"""
        return APIHelper(self.BASE_URL)
    
    
    @pytest.mark.parametrize("resource,min_items", [
        ("users", 5),
        ("posts", 50),
        ("comments", 100),
        ("albums", 50),
        ("photos", 100),
        ("todos", 100),
    ])
    def test_get_list_endpoints(self, api, resource, min_items):
        """
        Test: GET list for multiple resources
        
        Tests 6 different endpoints with same validation
        """
        logger.step(f"Testing /{resource} endpoint")
        
        validator = api.get_list(resource)
        
        validator.assert_status_ok() \
            .assert_content_type_json() \
            .assert_response_fast() \
            .assert_json_is_list() \
            .assert_json_min_length(min_items)
        
        items = validator.get_json()
        logger.info(f"/{resource}: {len(items)} items retrieved")
    
    
    @pytest.mark.parametrize("resource,resource_id", [
        ("users", 1),
        ("posts", 1),
        ("comments", 1),
        ("albums", 1),
        ("photos", 1),
        ("todos", 1),
    ])
    def test_get_by_id_endpoints(self, api, resource, resource_id):
        """
        Test: GET by ID for multiple resources
        
        Tests 6 different resources
        """
        logger.step(f"Testing /{resource}/{resource_id}")
        
        validator = api.get_by_id(resource, resource_id)
        
        validator.assert_status_ok() \
            .assert_json_is_dict() \
            .assert_field_exists("id") \
            .assert_field_value("id", resource_id)
        
        logger.info(f"/{resource}/{resource_id} retrieved")
    
    
    @pytest.mark.parametrize("resource", [
        "users",
        "posts",
        "comments",
        "albums",
        "photos",
        "todos",
    ])
    def test_404_not_found(self, api, resource):
        """
        Test: 404 for non-existent resources
        
        Tests error handling across endpoints
        """
        logger.step(f"Testing 404 for /{resource}/999999")
        
        validator = api.get_by_id(resource, 999999)
        
        validator.assert_status_no_found()
        
        logger.info(f"/{resource}/999999 returns 404 correctly")
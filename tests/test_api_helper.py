"""
API Helper Tests
Demonstrates APIHelper class with Faker integration

Tests CRUD operations using JSONPlaceholder API
"""
import pytest
from utils.api_helper import APIHelper
from utils.api_logger import logger


class TestAPIHelper:
    """API Helper tests with CRUD operations"""
    
    BASE_URL = "https://jsonplaceholder.typicode.com"
    
    @pytest.fixture
    def api(self):
        """Create API Helper instance"""
        return APIHelper(self.BASE_URL)
    
    def test_get_users_list(self, api):
        """
        Test: GET list of users using APIHelper
        
        Demonstrates: get_list() method
        """
        logger.step("Get list of users")
        
        validator = api.get_list("users")
        
        validator.assert_status_ok() \
            .assert_content_type_json() \
            .assert_json_is_list() \
            .assert_json_min_length(5)
            
        logger.info("Users list retrieved successfully")
        
    def test_get_user_by_id(self, api):
        """
        Test: GET single user by ID
        
        Demonstrates: get_by_id() method
        """
        logger.step("Get user by ID")
        
        validator = api.get_by_id("users", 1)
        
        validator.assert_status_ok() \
            .assert_json_is_dict() \
            .assert_field_exists("id") \
            .assert_field_exists("name") \
            .assert_field_exists("email") \
            .assert_field_value("id", 1)

        user = validator.get_json()
        logger.info(f"User: {user['name']} ({user['email']})")

        logger.info("User Retrieved successfully")

    def test_create_post_with_faker(self, api, faker):
        """
        Test: POST create new post with Faker data
        
        Demonstrates: create() method + Faker integration
        """
        logger.step("Generate post data with Faker")

        # Generate data with Faker
        post_data = {
            "title": faker.random_sentence(),
            "body": faker.random_text(max_chars=100),
            "userId": faker.random_number(digits=1)
        }

        post_data = {
            "title": faker.random_sentence(),
            "body": faker.random_text(max_chars=100),
            "userId": faker.random_number(digits=1)
        }
        
        logger.info(f"Post data: {post_data}")
        
        logger.step("Create post via API")
        
        validator = api.create("posts", post_data)
        
        validator.assert_status_code(201) \
            .assert_json_is_dict() \
            .assert_field_exists("id")
        
        created_post = validator.get_json()
        logger.info(f"Created post ID: {created_post['id']}")

        # Verify data was sent correclty
        assert created_post['title'] == post_data['title']
        assert created_post['body'] == post_data['body']

        logger.info("Post created successfully")

    def test_update_post(self, api, faker):
        """
        Test: PUT update entire post
        
        Demonstrates: update() method
        """
        logger.step("Update post with new data")
        
        updated_data = {
            "id": 1,
            "title": faker.random_sentence(),
            "body": faker.random_text(max_chars=50),
            "userId": 1
        }
        
        validator = api.update("posts", 1, updated_data)
        
        validator.assert_status_ok() \
            .assert_json_is_dict()
        
        logger.info("Post updated successfully")
    
    
    def test_partial_update_post(self, api):
        """
        Test: PATCH partial update
        
        Demonstrates: partial_update() method
        """
        logger.step("Partially update post (only title)")
        
        partial_data = {
            "title": "Updated title only"
        }
        
        validator = api.partial_update("posts", 1, partial_data)
        
        validator.assert_status_ok() \
            .assert_json_is_dict() \
            .assert_field_value("title", "Updated title only")
        
        logger.info("Post partially updated")
    
    
    def test_delete_post(self, api):
        """
        Test: DELETE resource
        
        Demonstrates: delete_by_id() method
        """
        logger.step("Delete post")
        
        validator = api.delete_by_id("posts", 1)
        
        validator.assert_status_ok()
        
        logger.info("Post deleted successfully")
    
    
    def test_get_with_query_params(self, api):
        """
        Test: GET with query parameters
        
        Demonstrates: get() with params
        """
        logger.step("Get posts filtered by userId")
        
        validator = api.get("/posts", params={"userId": 1})
        
        validator.assert_status_ok() \
            .assert_json_is_list() \
            .assert_json_min_length(1)
        
        posts = validator.get_json()
        
        # Verify all posts belong to userId 1
        for post in posts:
            assert post['userId'] == 1
        
        logger.info(f"Found {len(posts)} posts for user 1")
    
    
    def test_get_with_limit(self, api):
        """
        Test: GET list with limit
        
        Demonstrates: get_list() with limit parameter
        """
        logger.step("Get limited list of posts")
        
        validator = api.get_list("posts", limit=5)
        
        validator.assert_status_ok() \
            .assert_json_is_list() \
            .assert_json_length(5)
        
        logger.info("Retrieved exactly 5 posts")
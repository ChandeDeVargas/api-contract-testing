"""
Performance Tracking Tests
Track and compare response times across endpoints

Demonstrates performance testing concepts
"""
import pytest
from utils.api_helper import APIHelper
from utils.api_logger import logger


class TestPerformanceTracking:
    """Performance tracking and comparison tests"""
    
    BASE_URL = "https://jsonplaceholder.typicode.com"
    
    @pytest.fixture
    def api(self):
        """Create API Helper instance"""
        return APIHelper(self.BASE_URL)
    
    
    def test_response_time_benchmarks(self, api):
        """
        Test: Benchmark response times for different endpoints
        
        Tracks performance across multiple endpoints
        """
        logger.step("Benchmarking endpoint response times")
        
        endpoints_to_test = [
            ("users", "Small list (10 items)"),
            ("posts", "Medium list (100 items)"),
            ("comments", "Large list (500 items)"),
        ]
        
        results = []
        
        for endpoint, description in endpoints_to_test:
            logger.info(f"Testing /{endpoint} - {description}")
            
            validator = api.get_list(endpoint)
            validator.assert_status_ok()
            
            response_time = validator.get_response_time_ms()
            results.append({
                "endpoint": endpoint,
                "time_ms": response_time,
                "description": description
            })
            
            logger.info(f"  Response time: {response_time:.0f}ms")
        
        # Print summary
        logger.info("\n" + "="*60)
        logger.info("PERFORMANCE SUMMARY")
        logger.info("="*60)
        
        for result in sorted(results, key=lambda x: x['time_ms']):
            logger.info(f"  /{result['endpoint']:12} - {result['time_ms']:6.0f}ms - {result['description']}")
        
        logger.info("="*60)
        
        # Assert all under 2 seconds
        for result in results:
            assert result['time_ms'] < 2000, \
                f"/{result['endpoint']} too slow: {result['time_ms']}ms"
        
        logger.info("All endpoints under 2 seconds")
    
    
    def test_compare_get_vs_post_performance(self, api, faker):
        """
        Test: Compare GET vs POST performance
        
        Measures different HTTP methods
        """
        logger.step("Comparing GET vs POST performance")
        
        # GET request
        logger.info("Testing GET /posts/1")
        get_validator = api.get_by_id("posts", 1)
        get_time = get_validator.get_response_time_ms()
        logger.info(f"  GET time: {get_time:.0f}ms")
        
        # POST request
        logger.info("Testing POST /posts")
        post_data = {
            "title": faker.random_sentence(),
            "body": faker.random_text(),
            "userId": 1
        }
        post_validator = api.create("posts", post_data)
        post_time = post_validator.get_response_time_ms()
        logger.info(f"  POST time: {post_time:.0f}ms")
        
        # Compare
        logger.info(f"\nDifference: {abs(get_time - post_time):.0f}ms")
        
        if get_time < post_time:
            logger.info(f"GET is {(post_time/get_time - 1)*100:.1f}% faster")
        else:
            logger.info(f"POST is {(get_time/post_time - 1)*100:.1f}% faster")
        
        logger.info("Performance comparison complete")
    
    
    @pytest.mark.parametrize("limit", [5, 10, 20, 50, 100])
    def test_response_time_vs_payload_size(self, api, limit):
        """
        Test: Response time vs payload size
        
        How does limit affect response time?
        """
        logger.step(f"Testing with limit={limit}")
        
        validator = api.get_list("posts", limit=limit)
        
        validator.assert_status_ok() \
            .assert_json_length(limit)
        
        response_time = validator.get_response_time_ms()
        
        logger.info(f"Limit {limit:3} items: {response_time:.0f}ms")
        
        # Should still be under 2 seconds
        assert response_time < 2000
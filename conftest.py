"""
Pytest configuration and fixtures
"""
import pytest
from test_data.faker_factory import faker_factory

@pytest.fixture
def faker():
    """
    Provide Faker factory instance.
    
    Returns:
        FakerFactory: Faker instance for generating test data
    """
    return faker_factory
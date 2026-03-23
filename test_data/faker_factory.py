"""
Faker Test Data Factory
Generates realistic test data using Faker

Useful for tests that need:
- Usernames
- Emails
- Addresses
- Phone numbers
- Random text
"""
from faker import Faker
from dataclasses import dataclass
from typing import List


class FakerFactory:
    """
    Factory to generate test data with Faker.
    
    Uses Singleton pattern to reuse same instance.
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton - only one instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, locale: str = 'en_US'):
        """
        Initialize Faker.
        
        Args:
            locale: Locale for data (en_US, es_ES, etc)
        """
        if self._initialized:
            return
        
        self.fake = Faker(locale)
        self._initialized = True
    
    # ============================================
    # User Data
    # ============================================
    
    def random_username(self) -> str:
        """Generate random username"""
        return self.fake.user_name()
    
    def random_email(self) -> str:
        """Generate random email"""
        return self.fake.email()
    
    def random_first_name(self) -> str:
        """Generate random first name"""
        return self.fake.first_name()
    
    def random_last_name(self) -> str:
        """Generate random last name"""
        return self.fake.last_name()
    
    def random_full_name(self) -> str:
        """Generate random full name"""
        return self.fake.name()
    
    def random_password(self, length: int = 12) -> str:
        """
        Generate random password.
        
        Args:
            length: Password length
            
        Returns:
            str: Random password
        """
        return self.fake.password(length=length)
    
    def random_phone(self) -> str:
        """Generate random phone number"""
        return self.fake.phone_number()
    
    # ============================================
    # Todo/Task Data
    # ============================================
    
    def random_todo_text(self) -> str:
        """Generate random todo text"""
        return self.fake.sentence(nb_words=5).rstrip('.')
    
    def random_todos(self, count: int = 5) -> List[str]:
        """
        Generate multiple random todos.
        
        Args:
            count: Number of todos to generate
            
        Returns:
            List[str]: List of todo texts
        """
        return [self.random_todo_text() for _ in range(count)]
    
    def random_description(self) -> str:
        """Generate random description/paragraph"""
        return self.fake.paragraph(nb_sentences=3)
    
    # ============================================
    # Text Data
    # ============================================
    
    def random_word(self) -> str:
        """Generate random word"""
        return self.fake.word()
    
    def random_sentence(self) -> str:
        """Generate random sentence"""
        return self.fake.sentence()
    
    def random_text(self, max_chars: int = 200) -> str:
        """
        Generate random text.
        
        Args:
            max_chars: Maximum characters
            
        Returns:
            str: Random text
        """
        return self.fake.text(max_nb_chars=max_chars)
    
    # ============================================
    # Internet Data
    # ============================================
    
    def random_url(self) -> str:
        """Generate random URL"""
        return self.fake.url()
    
    def random_domain(self) -> str:
        """Generate random domain"""
        return self.fake.domain_name()
    
    def random_ipv4(self) -> str:
        """Generate random IPv4"""
        return self.fake.ipv4()
    
    # ============================================
    # Date/Time Data
    # ============================================
    
    def random_date(self) -> str:
        """Generate random date"""
        return str(self.fake.date())
    
    def random_datetime(self) -> str:
        """Generate random datetime"""
        return str(self.fake.date_time())
    
    # ============================================
    # Numbers
    # ============================================
    
    def random_number(self, digits: int = 5) -> int:
        """
        Generate random number.
        
        Args:
            digits: Number of digits
            
        Returns:
            int: Random number
        """
        return self.fake.random_number(digits=digits)
    
    def random_float(self, min_value: float = 0, max_value: float = 1000) -> float:
        """
        Generate random float.
        
        Args:
            min_value: Minimum value
            max_value: Maximum value
            
        Returns:
            float: Random float
        """
        return self.fake.pyfloat(min_value=min_value, max_value=max_value, right_digits=2)
    
    # ============================================
    # Complete User Object
    # ============================================
    
    def create_user(self) -> dict:
        """
        Create complete random user.
        
        Returns:
            dict: User data
        """
        return {
            "username": self.random_username(),
            "email": self.random_email(),
            "first_name": self.random_first_name(),
            "last_name": self.random_last_name(),
            "full_name": self.random_full_name(),
            "password": self.random_password(),
            "phone": self.random_phone()
        }
    
    def create_users(self, count: int = 5) -> List[dict]:
        """
        Create multiple random users.
        
        Args:
            count: Number of users
            
        Returns:
            List[dict]: List of users
        """
        return [self.create_user() for _ in range(count)]


# ============================================
# Global instance
# ============================================
faker_factory = FakerFactory()
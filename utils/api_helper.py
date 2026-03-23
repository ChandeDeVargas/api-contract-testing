"""
API Helper
Wrapper class for HTTP requests using requests library

Features:
- Methods for GET, POST, PUT, PATCH, DELETE
- Automatic request logging
- Integrated response validation
- Headers management
- Timeout configuration
"""
from tkinter import N
import requests
from typing import Dict, Optional
from utils.api_logger import logger
from utils.api_validator import APIValidator

class APIHelper:
    """
    API Helper class.
    
    Wrapper for requests with logging and validation.
    Uses OOP to organize HTTP methods.
    """
    def __init__(self, base_url: str, default_timeout: int = 30):
        """
        Initialize API Helper.
        
        Args:
            base_url: Base URL for API
            default_timeout: Default timeout in seconds
        """
        self.base_url = base_url.rstrip('/') # Remove trailing slash
        self.default_timeout = default_timeout
        self.default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        logger.info(f"API Helper initialized: {self.base_url}")
        
    # ============================================
    # Helper Methods
    # ============================================
    
    def _build_url(self, endpoint: str) -> str:
        """
        Build full URL from endpoint.
        
        Args:
            endpoint: API endpoint (e.g., '/users', '/posts/1')
            
        Returns:
            str: Full URL
        """
        # Remove leading slash from endpoint if present
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"
    
    def _log_request(self, method: str, url: str, **kwargs):
        """Log HTTP request details"""
        logger.info(f"{method} {url}")
        
        if 'params' in kwargs and kwargs['params']:
            logger.debug(f" Params: {kwargs['params']}")
            
        if 'json' in kwargs and kwargs['json']:
            logger.debug(f" Body: {kwargs['json']}")
            
    
    def _log_response(self, response: requests.Response) -> None:
        """Log HTTP response details"""
        logger.info(f"Response: {response.status_code} ({response.elapsed.total_seconds():.3f}s)")
        
    
    # ============================================
    # HTTP Methods
    # ============================================
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None
    ) -> APIValidator:
        """
        Perform GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Custom headers
            timeout: Request timeout
            
        Returns:
            APIValidator: Response validator
        """
        url = self._build_url(endpoint)
        timeout = timeout or self.default_timeout
        request_headers = {**self.default_headers, **(headers or {})}
        
        self._log_request('GET', url, params=params)
        
        response = requests.get(url, params=params, headers=request_headers, timeout=timeout)
        
        self._log_response(response)
        
        return APIValidator(response)
    
    def post(
        self, endpoint: str,
        json_data: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None
    ) -> APIValidator:
        """
        Perform POST request.
        
        Args:
            endpoint: API endpoint
            json_data: JSON body
            data: Form data
            headers: Custom headers
            timeout: Request timeout
            
        Returns:
            APIValidator: Response validator
        """
        url = self._build_url(endpoint)
        timeout = timeout or self.default_timeout
        request_headers = {**self.default_headers, **(headers or {})}
        
        self._log_request('POST', url, json=json_data, data=data)
        
        response = requests.post(
            url,
            json=json_data,
            data=data,
            headers=request_headers,
            timeout=timeout
        )
        
        self._log_response(response)
        
        return APIValidator(response)
        
    def put(
        self,
        endpoint: str,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None
    ) -> APIValidator:
        """
        Perform PUT request.
        
        Args:
            endpoint: API endpoint
            json_data: JSON body
            headers: Custom headers
            timeout: Request timeout
            
        Returns:
            APIValidator: Response validator
        """
        url = self._build_url(endpoint)
        timeout = timeout or self.default_timeout
        request_headers = {**self.default_headers, **(headers or {})}
        
        self._log_request('PUT', url, json=json_data)
        
        response = requests.put(
            url,
            json=json_data,
            headers=request_headers,
            timeout=timeout
        )
        
        self._log_response(response)
        
        return APIValidator(response)
    
    def patch(
        self,
        endpoint: str,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None
    ) -> APIValidator:
        """
        Perform PATCH request.
        
        Args:
            endpoint: API endpoint
            json_data: JSON body
            headers: Custom headers
            timeout: Request timeout
            
        Returns:
            APIValidator: Response validator
        """
        url = self._build_url(endpoint)
        timeout = timeout or self.default_timeout
        request_headers = {**self.default_headers, **(headers or {})}
        
        self._log_request('PATCH', url, json=json_data)
        
        response = requests.patch(
            url,
            json=json_data,
            headers=request_headers,
            timeout=timeout
        )
        
        self._log_response(response)
        
        return APIValidator(response)
    
    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None
    ) -> APIValidator:
        """
        Perform DELETE request.
        
        Args:
            endpoint: API endpoint
            headers: Custom headers
            timeout: Request timeout
            
        Returns:
            APIValidator: Response validator
        """
        url = self._build_url(endpoint)
        timeout = timeout or self.default_timeout
        request_headers = {**self.default_headers, **(headers or {})}
        
        self._log_request('DELETE', url)
        
        response = requests.delete(
            url,
            headers=request_headers,
            timeout=timeout
        )
        
        self._log_response(response)
        
        return APIValidator(response)
    
    # ============================================
    # Convenience Methods
    # ============================================
    
    def get_by_id(self, resource: str, resource_id: int) -> APIValidator:
        """
        GET resource by ID.
        
        Args:
            resource: Resource name (e.g., 'users', 'posts')
            resource_id: Resource ID
            
        Returns:
            APIValidator: Response validator
        """
        endpoint = f"/{resource}/{resource_id}"
        return self.get(endpoint)
    
    def get_list(
        self,
        resource: str,
        limit: Optional[int] = None,
        filters: Optional[Dict] = None
        
    ) -> APIValidator:
        """
        GET list of resources.
        
        Args:
            resource: Resource name
            limit: Limit number of results
            filters: Filter parameters
            
        Returns:
            APIValidator: Response validator
        """
        params = filters or {}
        
        if limit:
            params['_limit'] = limit
            
        return self.get(f"/{resource}", params=params)
    
    def create(self, resource: str, data: Dict) -> APIValidator:
        """
        Create new resource.
        
        Args:
            resource: Resource name
            data: Resource data
            
        Returns:
            APIValidator: Response validator
        """
        return self.post(f"/{resource}", json_data=data)
    
    
    def update(self, resource: str, resource_id: int, data: Dict) -> APIValidator:
        """
        Update resource (full update).
        
        Args:
            resource: Resource name
            resource_id: Resource ID
            data: Updated data
            
        Returns:
            APIValidator: Response validator
        """
        return self.put(f"/{resource}/{resource_id}", json_data=data)
    
    
    def partial_update(self, resource: str, resource_id: int, data: Dict) -> APIValidator:
        """
        Partially update resource.
        
        Args:
            resource: Resource name
            resource_id: Resource ID
            data: Partial data to update
            
        Returns:
            APIValidator: Response validator
        """
        return self.patch(f"/{resource}/{resource_id}", json_data=data)
    
    
    def delete_by_id(self, resource: str, resource_id: int) -> APIValidator:
        """
        Delete resource by ID.
        
        Args:
            resource: Resource name
            resource_id: Resource ID
            
        Returns:
            APIValidator: Response validator
        """
        return self.delete(f"/{resource}/{resource_id}")
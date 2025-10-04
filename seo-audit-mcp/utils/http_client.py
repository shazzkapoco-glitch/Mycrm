"""
HTTP Client Utilities
Helper functions for making HTTP requests.
"""

import aiohttp
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


async def fetch_url(url: str, headers: Optional[Dict[str, str]] = None, 
                   timeout: int = 30) -> Dict[str, Any]:
    """
    Fetch a URL and return response data.
    
    Args:
        url: URL to fetch
        headers: Optional HTTP headers
        timeout: Request timeout in seconds
    
    Returns:
        Dictionary containing response data
    """
    if headers is None:
        headers = {
            'User-Agent': 'SEOAuditBot/1.0'
        }
    
    result = {
        'url': url,
        'status_code': None,
        'headers': {},
        'content': None,
        'error': None
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=timeout) as response:
                result['status_code'] = response.status
                result['headers'] = dict(response.headers)
                result['content'] = await response.text()
                logger.info(f"Fetched {url} - Status: {response.status}")
    except aiohttp.ClientError as e:
        result['error'] = str(e)
        logger.error(f"Error fetching {url}: {str(e)}")
    except Exception as e:
        result['error'] = str(e)
        logger.error(f"Unexpected error fetching {url}: {str(e)}")
    
    return result


async def fetch_multiple_urls(urls: list, headers: Optional[Dict[str, str]] = None,
                              max_concurrent: int = 10) -> list:
    """
    Fetch multiple URLs concurrently.
    
    Args:
        urls: List of URLs to fetch
        headers: Optional HTTP headers
        max_concurrent: Maximum concurrent requests
    
    Returns:
        List of response dictionaries
    """
    import asyncio
    
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_with_semaphore(url):
        async with semaphore:
            return await fetch_url(url, headers)
    
    tasks = [fetch_with_semaphore(url) for url in urls]
    return await asyncio.gather(*tasks)


def check_url_status(url: str, timeout: int = 10) -> int:
    """
    Check HTTP status code of a URL (synchronous).
    
    Args:
        url: URL to check
        timeout: Request timeout in seconds
    
    Returns:
        HTTP status code or 0 if error
    """
    import requests
    
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code
    except requests.RequestException:
        try:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            return response.status_code
        except requests.RequestException as e:
            logger.error(f"Error checking {url}: {str(e)}")
            return 0

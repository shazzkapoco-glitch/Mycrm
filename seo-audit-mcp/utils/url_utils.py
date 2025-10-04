"""
URL Utilities
Helper functions for URL manipulation and validation.
"""

import logging
from typing import Optional, Dict, Any
from urllib.parse import urlparse, urljoin, parse_qs

logger = logging.getLogger(__name__)


def normalize_url(url: str) -> str:
    """
    Normalize URL to a standard format.
    
    Args:
        url: URL to normalize
    
    Returns:
        Normalized URL
    """
    url = url.strip()
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Remove trailing slash
    if url.endswith('/') and url.count('/') > 3:
        url = url.rstrip('/')
    
    return url


def is_valid_url(url: str) -> bool:
    """
    Check if URL is valid.
    
    Args:
        url: URL to validate
    
    Returns:
        True if valid
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def get_domain(url: str) -> str:
    """
    Extract domain from URL.
    
    Args:
        url: URL to parse
    
    Returns:
        Domain name
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return ""


def get_base_url(url: str) -> str:
    """
    Get base URL (protocol + domain).
    
    Args:
        url: URL to parse
    
    Returns:
        Base URL
    """
    try:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        return ""


def is_internal_link(url: str, domain: str) -> bool:
    """
    Check if URL is internal to domain.
    
    Args:
        url: URL to check
        domain: Domain to compare against
    
    Returns:
        True if internal
    """
    try:
        url_domain = get_domain(url)
        return url_domain == domain or url_domain.endswith('.' + domain)
    except Exception:
        return False


def parse_url_parts(url: str) -> Dict[str, Any]:
    """
    Parse URL into components.
    
    Args:
        url: URL to parse
    
    Returns:
        Dictionary with URL components
    """
    parsed = urlparse(url)
    return {
        'scheme': parsed.scheme,
        'netloc': parsed.netloc,
        'path': parsed.path,
        'params': parsed.params,
        'query': parse_qs(parsed.query),
        'fragment': parsed.fragment,
        'domain': parsed.netloc,
        'base_url': f"{parsed.scheme}://{parsed.netloc}"
    }


def join_urls(base: str, relative: str) -> str:
    """
    Join base URL with relative URL.
    
    Args:
        base: Base URL
        relative: Relative URL
    
    Returns:
        Absolute URL
    """
    return urljoin(base, relative)


def remove_query_params(url: str) -> str:
    """
    Remove query parameters from URL.
    
    Args:
        url: URL with query params
    
    Returns:
        URL without query params
    """
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def get_url_extension(url: str) -> str:
    """
    Get file extension from URL.
    
    Args:
        url: URL to parse
    
    Returns:
        File extension or empty string
    """
    parsed = urlparse(url)
    path = parsed.path
    if '.' in path:
        return path.split('.')[-1].lower()
    return ""

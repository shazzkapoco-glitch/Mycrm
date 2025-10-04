"""
HTML Parser Utilities
Helper functions for parsing and extracting data from HTML.
"""

from bs4 import BeautifulSoup
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


def parse_html(html: str, parser: str = 'html.parser') -> Optional[BeautifulSoup]:
    """
    Parse HTML content.
    
    Args:
        html: HTML content
        parser: Parser to use ('html.parser', 'lxml', 'html5lib')
    
    Returns:
        BeautifulSoup object or None if error
    """
    try:
        return BeautifulSoup(html, parser)
    except Exception as e:
        logger.error(f"Error parsing HTML: {str(e)}")
        return None


def extract_title(soup: BeautifulSoup) -> str:
    """
    Extract title tag content.
    
    Args:
        soup: BeautifulSoup object
    
    Returns:
        Title text or empty string
    """
    title_tag = soup.find('title')
    return title_tag.get_text().strip() if title_tag else ""


def extract_meta_description(soup: BeautifulSoup) -> str:
    """
    Extract meta description content.
    
    Args:
        soup: BeautifulSoup object
    
    Returns:
        Meta description or empty string
    """
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    return meta_tag.get('content', '').strip() if meta_tag else ""


def extract_meta_tags(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Extract all meta tags.
    
    Args:
        soup: BeautifulSoup object
    
    Returns:
        Dictionary of meta tags
    """
    meta_tags = {}
    for tag in soup.find_all('meta'):
        name = tag.get('name') or tag.get('property') or tag.get('http-equiv')
        content = tag.get('content')
        if name and content:
            meta_tags[name] = content
    return meta_tags


def extract_headings(soup: BeautifulSoup) -> Dict[str, List[str]]:
    """
    Extract all heading tags (h1-h6).
    
    Args:
        soup: BeautifulSoup object
    
    Returns:
        Dictionary with heading levels and their content
    """
    headings = {
        'h1': [],
        'h2': [],
        'h3': [],
        'h4': [],
        'h5': [],
        'h6': []
    }
    
    for level in headings.keys():
        tags = soup.find_all(level)
        headings[level] = [tag.get_text().strip() for tag in tags]
    
    return headings


def extract_links(soup: BeautifulSoup, base_url: str = "") -> List[Dict[str, str]]:
    """
    Extract all links from HTML.
    
    Args:
        soup: BeautifulSoup object
        base_url: Base URL for resolving relative links
    
    Returns:
        List of link dictionaries
    """
    from urllib.parse import urljoin
    
    links = []
    for tag in soup.find_all('a', href=True):
        url = urljoin(base_url, tag['href'])
        links.append({
            'url': url,
            'text': tag.get_text().strip(),
            'rel': tag.get('rel', []),
            'title': tag.get('title', '')
        })
    
    return links


def extract_images(soup: BeautifulSoup, base_url: str = "") -> List[Dict[str, str]]:
    """
    Extract all images from HTML.
    
    Args:
        soup: BeautifulSoup object
        base_url: Base URL for resolving relative URLs
    
    Returns:
        List of image dictionaries
    """
    from urllib.parse import urljoin
    
    images = []
    for tag in soup.find_all('img'):
        src = tag.get('src', '')
        if src:
            images.append({
                'src': urljoin(base_url, src),
                'alt': tag.get('alt', ''),
                'title': tag.get('title', ''),
                'width': tag.get('width', ''),
                'height': tag.get('height', '')
            })
    
    return images


def extract_canonical(soup: BeautifulSoup) -> str:
    """
    Extract canonical URL.
    
    Args:
        soup: BeautifulSoup object
    
    Returns:
        Canonical URL or empty string
    """
    canonical_tag = soup.find('link', rel='canonical')
    return canonical_tag.get('href', '').strip() if canonical_tag else ""


def extract_schema_json_ld(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """
    Extract JSON-LD structured data.
    
    Args:
        soup: BeautifulSoup object
    
    Returns:
        List of JSON-LD objects
    """
    import json
    
    json_ld_data = []
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            json_ld_data.append(data)
        except (json.JSONDecodeError, AttributeError) as e:
            logger.error(f"Error parsing JSON-LD: {str(e)}")
    
    return json_ld_data


def extract_text_content(soup: BeautifulSoup, remove_scripts: bool = True) -> str:
    """
    Extract visible text content.
    
    Args:
        soup: BeautifulSoup object
        remove_scripts: Whether to remove script and style tags
    
    Returns:
        Text content
    """
    if remove_scripts:
        for script in soup(['script', 'style']):
            script.decompose()
    
    return soup.get_text(separator=' ', strip=True)

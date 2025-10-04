"""
Configuration file for SEO Audit MCP Server
Stores API keys, domains, and other configuration settings.
"""

import os
from typing import List, Dict, Any

# API Keys (should be loaded from environment variables in production)
GOOGLE_ANALYTICS_API_KEY = os.getenv('GOOGLE_ANALYTICS_API_KEY', '')
GOOGLE_SEARCH_CONSOLE_API_KEY = os.getenv('GOOGLE_SEARCH_CONSOLE_API_KEY', '')
LIGHTHOUSE_API_KEY = os.getenv('LIGHTHOUSE_API_KEY', '')
BACKLINK_API_KEY = os.getenv('BACKLINK_API_KEY', '')

# Server Configuration
SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', '8000'))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Audit Configuration
DEFAULT_DOMAINS: List[str] = []
MAX_CONCURRENT_AUDITS = int(os.getenv('MAX_CONCURRENT_AUDITS', '5'))
AUDIT_TIMEOUT = int(os.getenv('AUDIT_TIMEOUT', '300'))  # seconds

# Module Configuration
ENABLED_MODULES: List[str] = [
    'ga4',
    'gsc',
    'lighthouse',
    'sitemap',
    'onpage',
    'backlinks',
    'keywords',
    'crawlability',
    'accessibility',
    'mobile',
    'security',
    'structured_data',
    'content',
    'broken_links',
    'redirects',
    'images',
    'robots',
    'canonical',
    'local_seo',
    'hreflang',
    'amp',
    'analytics_tags',
    'custom_checks',
    'competitive'
]

# Crawler Settings
USER_AGENT = 'SEOAuditBot/1.0 (+https://example.com/bot)'
MAX_CRAWL_DEPTH = 3
MAX_PAGES_PER_DOMAIN = 1000
CRAWL_DELAY = 1  # seconds between requests

# Lighthouse Settings
LIGHTHOUSE_CATEGORIES = ['performance', 'accessibility', 'best-practices', 'seo']
LIGHTHOUSE_DEVICE = 'mobile'  # or 'desktop'

# Content Analysis Settings
THIN_CONTENT_THRESHOLD = 300  # minimum word count
DUPLICATE_CONTENT_THRESHOLD = 0.8  # similarity threshold

# Image Optimization Settings
MAX_IMAGE_SIZE = 500 * 1024  # 500 KB
SUPPORTED_IMAGE_FORMATS = ['webp', 'jpg', 'png', 'svg']

# Security Settings
REQUIRED_SECURITY_HEADERS = [
    'Strict-Transport-Security',
    'X-Content-Type-Options',
    'X-Frame-Options',
    'Content-Security-Policy'
]

# Schema Settings
REQUIRED_SCHEMA_TYPES = ['Organization', 'WebSite', 'BreadcrumbList']

# Local SEO Settings
NAP_CONSISTENCY_CHECK = True  # Name, Address, Phone consistency

# Reporting Settings
REPORT_FORMAT = 'json'  # 'json', 'html', 'pdf'
INCLUDE_RECOMMENDATIONS = True
SEVERITY_LEVELS = ['critical', 'high', 'medium', 'low', 'info']

# Database Configuration (optional)
DATABASE_URL = os.getenv('DATABASE_URL', '')

# Webhook Configuration (optional)
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
WEBHOOK_EVENTS = ['audit_complete', 'audit_failed']


def get_config() -> Dict[str, Any]:
    """
    Get all configuration as a dictionary.
    
    Returns:
        Dictionary containing all configuration values
    """
    return {
        'api_keys': {
            'google_analytics': GOOGLE_ANALYTICS_API_KEY,
            'google_search_console': GOOGLE_SEARCH_CONSOLE_API_KEY,
            'lighthouse': LIGHTHOUSE_API_KEY,
            'backlink': BACKLINK_API_KEY
        },
        'server': {
            'host': SERVER_HOST,
            'port': SERVER_PORT,
            'debug': DEBUG
        },
        'audit': {
            'default_domains': DEFAULT_DOMAINS,
            'max_concurrent_audits': MAX_CONCURRENT_AUDITS,
            'timeout': AUDIT_TIMEOUT,
            'enabled_modules': ENABLED_MODULES
        },
        'crawler': {
            'user_agent': USER_AGENT,
            'max_depth': MAX_CRAWL_DEPTH,
            'max_pages': MAX_PAGES_PER_DOMAIN,
            'delay': CRAWL_DELAY
        },
        'lighthouse': {
            'categories': LIGHTHOUSE_CATEGORIES,
            'device': LIGHTHOUSE_DEVICE
        },
        'content': {
            'thin_threshold': THIN_CONTENT_THRESHOLD,
            'duplicate_threshold': DUPLICATE_CONTENT_THRESHOLD
        },
        'images': {
            'max_size': MAX_IMAGE_SIZE,
            'supported_formats': SUPPORTED_IMAGE_FORMATS
        },
        'security': {
            'required_headers': REQUIRED_SECURITY_HEADERS
        },
        'schema': {
            'required_types': REQUIRED_SCHEMA_TYPES
        },
        'local_seo': {
            'nap_check': NAP_CONSISTENCY_CHECK
        },
        'reporting': {
            'format': REPORT_FORMAT,
            'include_recommendations': INCLUDE_RECOMMENDATIONS,
            'severity_levels': SEVERITY_LEVELS
        }
    }

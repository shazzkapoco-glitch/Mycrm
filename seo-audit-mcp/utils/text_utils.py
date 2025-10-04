"""
Text Utilities
Helper functions for text processing and analysis.
"""

import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def count_words(text: str) -> int:
    """
    Count words in text.
    
    Args:
        text: Text to count
    
    Returns:
        Word count
    """
    return len(text.split())


def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """
    Extract top keywords from text.
    
    Args:
        text: Text to analyze
        top_n: Number of keywords to return
    
    Returns:
        List of keywords
    """
    from collections import Counter
    
    # Simple word frequency approach
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    
    # Remove common stop words
    stop_words = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can',
        'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him',
        'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way',
        'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'
    }
    
    words = [w for w in words if w not in stop_words]
    
    counter = Counter(words)
    return [word for word, count in counter.most_common(top_n)]


def calculate_keyword_density(text: str, keyword: str) -> float:
    """
    Calculate keyword density.
    
    Args:
        text: Text to analyze
        keyword: Keyword to check
    
    Returns:
        Keyword density as percentage
    """
    text_lower = text.lower()
    keyword_lower = keyword.lower()
    
    word_count = count_words(text)
    keyword_count = text_lower.count(keyword_lower)
    
    if word_count == 0:
        return 0.0
    
    return (keyword_count / word_count) * 100


def truncate_text(text: str, max_length: int, suffix: str = '...') -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace.
    
    Args:
        text: Text to clean
    
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_emails(text: str) -> List[str]:
    """
    Extract email addresses from text.
    
    Args:
        text: Text to search
    
    Returns:
        List of email addresses
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)


def extract_phone_numbers(text: str) -> List[str]:
    """
    Extract phone numbers from text.
    
    Args:
        text: Text to search
    
    Returns:
        List of phone numbers
    """
    # Simple pattern for various phone formats
    patterns = [
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',
        r'\+\d{1,3}\s*\d{3}[-.]?\d{3}[-.]?\d{4}'
    ]
    
    phone_numbers = []
    for pattern in patterns:
        phone_numbers.extend(re.findall(pattern, text))
    
    return phone_numbers


def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two texts.
    
    Args:
        text1: First text
        text2: Second text
    
    Returns:
        Similarity score (0-1)
    """
    # Simple word-based similarity
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union)


def get_text_stats(text: str) -> Dict[str, Any]:
    """
    Get comprehensive text statistics.
    
    Args:
        text: Text to analyze
    
    Returns:
        Dictionary with text statistics
    """
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    
    return {
        'character_count': len(text),
        'word_count': len(words),
        'sentence_count': len([s for s in sentences if s.strip()]),
        'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
        'avg_sentence_length': len(words) / len(sentences) if sentences else 0
    }

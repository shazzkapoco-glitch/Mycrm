#!/usr/bin/env python3
"""
Basic test script to verify SEO Audit MCP installation and functionality.
"""

import sys
import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_imports():
    """Test that all modules can be imported."""
    logger.info("Testing imports...")
    
    try:
        import config
        logger.info("✓ Config module imported")
        
        from main import SEOAuditServer
        logger.info("✓ Main module imported")
        
        # Test importing all modules
        from modules import (
            ga4, gsc, lighthouse, sitemap, onpage, backlinks, keywords,
            crawlability, accessibility, mobile, security, structured_data,
            content, broken_links, redirects, images, robots, canonical,
            local_seo, hreflang, amp, analytics_tags, custom_checks, competitive
        )
        logger.info("✓ All 24 modules imported successfully")
        
        # Test importing utils
        from utils import http_client, html_parser, url_utils, text_utils
        logger.info("✓ All utility modules imported")
        
        return True
    except ImportError as e:
        logger.error(f"✗ Import failed: {str(e)}")
        return False


def test_configuration():
    """Test configuration loading."""
    logger.info("\nTesting configuration...")
    
    try:
        import config
        
        # Check required configuration
        assert hasattr(config, 'ENABLED_MODULES'), "ENABLED_MODULES not found"
        assert len(config.ENABLED_MODULES) > 0, "No modules enabled"
        logger.info(f"✓ Configuration loaded: {len(config.ENABLED_MODULES)} modules enabled")
        
        # Test get_config function
        cfg = config.get_config()
        assert 'audit' in cfg, "Audit config missing"
        assert 'server' in cfg, "Server config missing"
        logger.info("✓ Configuration dictionary generated")
        
        return True
    except Exception as e:
        logger.error(f"✗ Configuration test failed: {str(e)}")
        return False


async def test_server_initialization():
    """Test server initialization."""
    logger.info("\nTesting server initialization...")
    
    try:
        from main import SEOAuditServer
        
        server = SEOAuditServer()
        logger.info("✓ Server instance created")
        
        server.load_config()
        logger.info("✓ Configuration loaded")
        
        server.load_modules()
        logger.info(f"✓ Modules loaded: {len(server.modules)} modules")
        
        # Verify all expected modules are loaded
        expected_modules = [
            'ga4', 'gsc', 'lighthouse', 'sitemap', 'onpage', 'backlinks',
            'keywords', 'crawlability', 'accessibility', 'mobile', 'security',
            'structured_data', 'content', 'broken_links', 'redirects', 'images',
            'robots', 'canonical', 'local_seo', 'hreflang', 'amp',
            'analytics_tags', 'custom_checks', 'competitive'
        ]
        
        for module_name in expected_modules:
            assert module_name in server.modules, f"Module {module_name} not loaded"
        
        logger.info("✓ All expected modules present")
        
        return True
    except Exception as e:
        logger.error(f"✗ Server initialization failed: {str(e)}")
        return False


async def test_module_structure():
    """Test module structure and audit functions."""
    logger.info("\nTesting module structure...")
    
    try:
        from modules import onpage, mobile, security
        
        # Check if modules have audit function
        for module in [onpage, mobile, security]:
            assert hasattr(module, 'audit'), f"Module {module.__name__} missing audit function"
            assert asyncio.iscoroutinefunction(module.audit), f"Module {module.__name__} audit is not async"
        
        logger.info("✓ Module structure verified")
        return True
    except Exception as e:
        logger.error(f"✗ Module structure test failed: {str(e)}")
        return False


async def test_utility_functions():
    """Test utility functions."""
    logger.info("\nTesting utility functions...")
    
    try:
        from utils import url_utils, text_utils
        
        # Test URL utilities
        test_url = "https://example.com/path"
        assert url_utils.is_valid_url(test_url), "URL validation failed"
        assert url_utils.get_domain(test_url) == "example.com", "Domain extraction failed"
        logger.info("✓ URL utilities working")
        
        # Test text utilities
        test_text = "This is a test text with multiple words"
        word_count = text_utils.count_words(test_text)
        assert word_count > 0, "Word count failed"
        logger.info("✓ Text utilities working")
        
        return True
    except Exception as e:
        logger.error(f"✗ Utility function test failed: {str(e)}")
        return False


async def test_mock_audit():
    """Test running a mock audit."""
    logger.info("\nTesting mock audit...")
    
    try:
        from main import SEOAuditServer
        import config
        
        server = SEOAuditServer()
        server.load_config()
        server.load_modules()
        
        # Run audit with a subset of modules
        test_domain = "example.com"
        test_modules = ["onpage", "mobile", "security"]
        
        logger.info(f"Running audit for {test_domain} with modules: {test_modules}")
        results = await server.run_audit(test_domain, test_modules)
        
        # Verify results structure
        assert 'domain' in results, "Domain missing from results"
        assert 'timestamp' in results, "Timestamp missing from results"
        assert 'modules' in results, "Modules missing from results"
        assert results['domain'] == test_domain, "Domain mismatch"
        
        logger.info(f"✓ Audit completed for {test_domain}")
        logger.info(f"  - Modules executed: {len(results['modules'])}")
        logger.info(f"  - Timestamp: {results['timestamp']}")
        
        # Check each module result
        for module_name in test_modules:
            assert module_name in results['modules'], f"Module {module_name} not in results"
            module_result = results['modules'][module_name]
            assert 'status' in module_result, f"Status missing from {module_name}"
            logger.info(f"  - {module_name}: {module_result['status']}")
        
        return True
    except Exception as e:
        logger.error(f"✗ Mock audit failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all tests."""
    logger.info("=" * 60)
    logger.info("SEO Audit MCP - Test Suite")
    logger.info("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Server Initialization", test_server_initialization),
        ("Module Structure", test_module_structure),
        ("Utility Functions", test_utility_functions),
        ("Mock Audit", test_mock_audit)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"Test {test_name} crashed: {str(e)}")
            results[test_name] = False
    
    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("Test Summary")
    logger.info("=" * 60)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info("=" * 60)
    logger.info(f"Total: {passed}/{total} tests passed")
    logger.info("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    try:
        success = asyncio.run(run_all_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Test suite crashed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

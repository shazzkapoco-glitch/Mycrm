"""
SEO Audit MCP Server
Main entrypoint for the MCP server that handles API requests, workers, and scheduling.
"""

import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SEOAuditServer:
    """Main SEO Audit MCP Server class."""
    
    def __init__(self):
        """Initialize the SEO Audit Server."""
        self.modules = {}
        self.config = None
        logger.info("Initializing SEO Audit MCP Server")
    
    def load_modules(self):
        """Load all SEO audit modules."""
        from modules import (
            ga4, gsc, lighthouse, sitemap, onpage, backlinks, keywords,
            crawlability, accessibility, mobile, security, structured_data,
            content, broken_links, redirects, images, robots, canonical,
            local_seo, hreflang, amp, analytics_tags, custom_checks, competitive
        )
        
        self.modules = {
            'ga4': ga4,
            'gsc': gsc,
            'lighthouse': lighthouse,
            'sitemap': sitemap,
            'onpage': onpage,
            'backlinks': backlinks,
            'keywords': keywords,
            'crawlability': crawlability,
            'accessibility': accessibility,
            'mobile': mobile,
            'security': security,
            'structured_data': structured_data,
            'content': content,
            'broken_links': broken_links,
            'redirects': redirects,
            'images': images,
            'robots': robots,
            'canonical': canonical,
            'local_seo': local_seo,
            'hreflang': hreflang,
            'amp': amp,
            'analytics_tags': analytics_tags,
            'custom_checks': custom_checks,
            'competitive': competitive
        }
        logger.info(f"Loaded {len(self.modules)} SEO audit modules")
    
    def load_config(self):
        """Load configuration."""
        import config
        self.config = config
        logger.info("Configuration loaded")
    
    async def run_audit(self, domain: str, modules: List[str] = None) -> Dict[str, Any]:
        """
        Run SEO audit on a domain.
        
        Args:
            domain: Domain to audit
            modules: List of module names to run (if None, run all)
        
        Returns:
            Dictionary containing audit results
        """
        if modules is None:
            modules = list(self.modules.keys())
        
        results = {
            'domain': domain,
            'timestamp': datetime.utcnow().isoformat(),
            'modules': {}
        }
        
        logger.info(f"Starting SEO audit for {domain} with {len(modules)} modules")
        
        for module_name in modules:
            if module_name in self.modules:
                try:
                    module = self.modules[module_name]
                    if hasattr(module, 'audit'):
                        logger.info(f"Running {module_name} audit")
                        result = await module.audit(domain, self.config)
                        results['modules'][module_name] = result
                    else:
                        logger.warning(f"Module {module_name} has no audit function")
                except Exception as e:
                    logger.error(f"Error running {module_name} audit: {str(e)}")
                    results['modules'][module_name] = {'error': str(e)}
        
        logger.info(f"Audit completed for {domain}")
        return results
    
    async def start(self):
        """Start the MCP server."""
        logger.info("Starting SEO Audit MCP Server")
        self.load_config()
        self.load_modules()
        logger.info("Server ready to accept requests")
        
        # Keep server running
        while True:
            await asyncio.sleep(1)


async def main():
    """Main entry point."""
    server = SEOAuditServer()
    await server.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise

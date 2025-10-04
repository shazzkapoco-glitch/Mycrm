# Quick Start Guide

Get started with the SEO Audit MCP tool in minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection for API integrations

## Installation

1. **Navigate to the tool directory:**
```bash
cd seo-audit-mcp
```

2. **Create a virtual environment (recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

## Basic Usage

### Test the Installation

```python
# Test configuration
python3 -c "import config; print('Configuration loaded successfully!')"
```

### Running Your First Audit

Create a simple test script (`test_audit.py`):

```python
import asyncio
from main import SEOAuditServer

async def run_test_audit():
    # Initialize the server
    server = SEOAuditServer()
    server.load_config()
    server.load_modules()
    
    # Run a basic audit
    domain = "example.com"
    modules = ["onpage", "mobile", "security"]
    
    print(f"Running audit for {domain}...")
    results = await server.run_audit(domain, modules)
    
    print(f"\nAudit completed!")
    print(f"Modules executed: {list(results['modules'].keys())}")
    print(f"Timestamp: {results['timestamp']}")

# Run the audit
if __name__ == "__main__":
    asyncio.run(run_test_audit())
```

Run the test:
```bash
python3 test_audit.py
```

## Module Overview

### Core Modules

- **onpage**: Title tags, meta descriptions, headers
- **lighthouse**: Performance and Core Web Vitals
- **security**: HTTPS, SSL, security headers
- **mobile**: Mobile-friendliness and responsiveness
- **content**: Content quality and duplication analysis

### Analytics Modules

- **ga4**: Google Analytics 4 integration
- **gsc**: Google Search Console data
- **analytics_tags**: Tracking tag verification

### Technical SEO Modules

- **crawlability**: Indexability and crawl issues
- **sitemap**: XML sitemap validation
- **robots**: robots.txt analysis
- **canonical**: Canonical tag validation
- **redirects**: Redirect chain detection
- **broken_links**: Broken link detection

### Advanced Modules

- **backlinks**: Backlink profile analysis
- **keywords**: Keyword research and gaps
- **local_seo**: Local SEO signals
- **hreflang**: International SEO
- **structured_data**: Schema.org validation
- **competitive**: Competitor analysis

## Example Workflows

### Full Website Audit

```python
# Run all modules
results = await server.run_audit("yoursite.com")
```

### Performance-Focused Audit

```python
# Focus on performance
modules = ["lighthouse", "images", "mobile", "content"]
results = await server.run_audit("yoursite.com", modules)
```

### Technical SEO Audit

```python
# Technical SEO check
modules = ["crawlability", "sitemap", "robots", "canonical", "redirects"]
results = await server.run_audit("yoursite.com", modules)
```

## Configuration Options

Edit `config.py` to customize:

- Crawl depth and page limits
- Timeout values
- Content quality thresholds
- Security requirements
- Report formats

## Troubleshooting

### Import Errors

If you get import errors, ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### API Key Issues

Some modules require API keys. Check `.env` file and ensure keys are set:
- Google Analytics API key for GA4 module
- Google Search Console API key for GSC module
- Lighthouse API key for performance testing
- Backlink API key for backlink analysis

### Module Errors

Modules will return a 'warning' status if dependencies are missing. Check the `issues` field in the results:

```python
if results['modules']['ga4']['status'] == 'warning':
    print(results['modules']['ga4']['issues'])
```

## Next Steps

1. Configure API keys in `.env` for full functionality
2. Review the main `README.md` for detailed documentation
3. Explore individual module documentation
4. Customize thresholds in `config.py` for your needs
5. Set up scheduled audits
6. Integrate with your existing tools

## Getting Help

- Check the main README.md
- Review module-specific documentation
- Check logs for detailed error messages
- Create an issue on GitHub

## Examples

See the `/examples` directory (coming soon) for:
- API integration examples
- Custom check definitions
- Batch audit scripts
- Report generation
- Dashboard integration

Happy auditing! 🚀

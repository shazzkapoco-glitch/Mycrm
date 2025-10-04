# SEO Audit MCP

A comprehensive SEO audit tool built as an MCP (Model Context Protocol) server for analyzing websites and providing detailed SEO insights.

## Features

This SEO audit tool includes the following modules:

### Analytics & Performance
- **Google Analytics 4 (GA4)** - Integration with GA4 for traffic analysis
- **Google Search Console (GSC)** - Search performance and indexing data
- **Lighthouse/PageSpeed** - Core Web Vitals and performance metrics

### Technical SEO
- **Crawlability** - Indexability and crawl simulation
- **Sitemap Analysis** - XML sitemap parsing and orphan page detection
- **Robots.txt** - robots.txt and meta robots analysis
- **Redirects** - Redirect chain and loop detection
- **Broken Links** - Broken internal and external link detection
- **Canonical Tags** - Canonical tag validation and duplicate detection

### On-Page SEO
- **On-Page Analysis** - Title tags, meta descriptions, headers analysis
- **Content Analysis** - Thin content, duplicate content, freshness detection
- **Keywords** - Keyword audit and gap analysis
- **Images** - Image optimization and alt text analysis
- **Structured Data** - Schema.org, OpenGraph, Twitter Cards validation

### Security & Accessibility
- **Security** - HTTPS, SSL, security headers, vulnerability scanning
- **Accessibility** - WCAG and ARIA compliance checking
- **Mobile-Friendliness** - Mobile responsiveness and usability

### SEO Extensions
- **Backlinks** - Backlink profile analysis
- **Local SEO** - NAP consistency, Google My Business integration
- **International SEO** - Hreflang and multi-language support
- **AMP** - Accelerated Mobile Pages validation
- **Analytics Tags** - Tag implementation verification (GA, GTM, Pixel)

### Advanced Features
- **Custom Checks** - User-defined SEO checklists and rules
- **Competitive Analysis** - Compare SEO metrics with competitors

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd seo-audit-mcp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
# Create .env file
cp .env.example .env

# Edit .env with your API keys
GOOGLE_ANALYTICS_API_KEY=your_key_here
GOOGLE_SEARCH_CONSOLE_API_KEY=your_key_here
LIGHTHOUSE_API_KEY=your_key_here
BACKLINK_API_KEY=your_key_here
```

## Usage

### Running the Server

```bash
python main.py
```

### Running an Audit

```python
from main import SEOAuditServer

# Initialize server
server = SEOAuditServer()
server.load_config()
server.load_modules()

# Run audit on a domain
results = await server.run_audit('example.com')

# Run specific modules
results = await server.run_audit('example.com', modules=['onpage', 'lighthouse', 'security'])
```

### API Usage

The server can be integrated with web applications via REST API:

```bash
# Start the API server
python api.py

# Make audit request
curl -X POST http://localhost:8000/audit \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com", "modules": ["onpage", "lighthouse"]}'
```

## Configuration

Configuration is managed in `config.py`. Key settings include:

- **API Keys**: Configure third-party API credentials
- **Server Settings**: Host, port, debug mode
- **Audit Settings**: Concurrent audits, timeouts, enabled modules
- **Crawler Settings**: User agent, crawl depth, delays
- **Thresholds**: Content quality, image size, security requirements

## Module Structure

Each module follows a consistent structure:

```python
async def audit(domain: str, config: Any) -> Dict[str, Any]:
    """
    Perform module-specific audit.
    
    Returns:
        Dictionary containing:
        - status: 'success', 'warning', or 'error'
        - metrics: Module-specific metrics
        - issues: List of identified issues
        - recommendations: List of recommendations
    """
```

## Utility Functions

The `utils/` directory provides helper functions:

- **http_client.py**: HTTP request handling
- **html_parser.py**: HTML parsing and extraction
- **url_utils.py**: URL manipulation and validation
- **text_utils.py**: Text processing and analysis

## Development

### Adding a New Module

1. Create a new file in `modules/` directory
2. Implement the `audit()` function
3. Add module to `modules/__init__.py`
4. Register in `config.py` ENABLED_MODULES

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
# Format code
black .

# Lint code
pylint modules/ utils/
```

## Architecture

```
seo-audit-mcp/
│
├── main.py                   # MCP server entrypoint
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
│
├── modules/                  # SEO audit modules
│   ├── __init__.py
│   ├── ga4.py
│   ├── gsc.py
│   ├── lighthouse.py
│   ├── sitemap.py
│   ├── onpage.py
│   ├── backlinks.py
│   ├── keywords.py
│   ├── crawlability.py
│   ├── accessibility.py
│   ├── mobile.py
│   ├── security.py
│   ├── structured_data.py
│   ├── content.py
│   ├── broken_links.py
│   ├── redirects.py
│   ├── images.py
│   ├── robots.py
│   ├── canonical.py
│   ├── local_seo.py
│   ├── hreflang.py
│   ├── amp.py
│   ├── analytics_tags.py
│   ├── custom_checks.py
│   └── competitive.py
│
├── utils/                    # Helper functions
│   ├── __init__.py
│   ├── http_client.py
│   ├── html_parser.py
│   ├── url_utils.py
│   └── text_utils.py
│
├── static/                   # Frontend assets
└── README.md                 # Documentation
```

## API Reference

### Audit Result Format

```json
{
  "domain": "example.com",
  "timestamp": "2024-01-01T00:00:00Z",
  "modules": {
    "onpage": {
      "status": "success",
      "title_tags": {
        "total": 100,
        "missing": 5,
        "duplicate": 3
      },
      "issues": [...],
      "recommendations": [...]
    }
  }
}
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- GitHub Issues: [Create an issue]
- Documentation: [Link to docs]
- Email: support@example.com

## Roadmap

- [ ] Web dashboard for audit results
- [ ] Scheduled audits
- [ ] Email notifications
- [ ] PDF report generation
- [ ] Integration with more third-party APIs
- [ ] Machine learning-based recommendations
- [ ] Multi-site audit comparison
- [ ] Historical trend analysis

## Credits

Developed by Shahzaib Ul Hassan for Napollo

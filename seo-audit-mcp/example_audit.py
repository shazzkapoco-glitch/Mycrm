#!/usr/bin/env python3
"""
Example SEO audit script demonstrating how to use the SEO Audit MCP tool.
"""

import asyncio
import json
from datetime import datetime
from main import SEOAuditServer


async def example_full_audit():
    """Example: Run a full audit on a domain."""
    print("=" * 60)
    print("Example 1: Full SEO Audit")
    print("=" * 60)
    
    # Initialize server
    server = SEOAuditServer()
    server.load_config()
    server.load_modules()
    
    # Run full audit (all modules)
    domain = "example.com"
    print(f"\nRunning full audit for {domain}...")
    
    results = await server.run_audit(domain)
    
    print(f"\n✓ Audit completed!")
    print(f"Domain: {results['domain']}")
    print(f"Timestamp: {results['timestamp']}")
    print(f"Modules executed: {len(results['modules'])}")
    
    # Show status of each module
    print("\nModule Status:")
    for module_name, module_result in results['modules'].items():
        status = module_result.get('status', 'unknown')
        print(f"  - {module_name:20s}: {status}")
    
    return results


async def example_targeted_audit():
    """Example: Run audit with specific modules."""
    print("\n" + "=" * 60)
    print("Example 2: Targeted SEO Audit")
    print("=" * 60)
    
    # Initialize server
    server = SEOAuditServer()
    server.load_config()
    server.load_modules()
    
    # Run audit with specific modules
    domain = "example.com"
    target_modules = [
        "onpage",       # On-page SEO
        "mobile",       # Mobile-friendliness
        "security",     # Security checks
        "lighthouse",   # Performance
        "accessibility" # Accessibility
    ]
    
    print(f"\nRunning targeted audit for {domain}")
    print(f"Modules: {', '.join(target_modules)}")
    
    results = await server.run_audit(domain, target_modules)
    
    print(f"\n✓ Audit completed!")
    
    # Display results for each module
    for module_name in target_modules:
        if module_name in results['modules']:
            module_result = results['modules'][module_name]
            status = module_result.get('status', 'unknown')
            issues = module_result.get('issues', [])
            
            print(f"\n{module_name.upper()}:")
            print(f"  Status: {status}")
            if issues:
                print(f"  Issues: {len(issues)}")
                for issue in issues[:3]:  # Show first 3 issues
                    print(f"    - {issue}")
    
    return results


async def example_performance_audit():
    """Example: Performance-focused audit."""
    print("\n" + "=" * 60)
    print("Example 3: Performance-Focused Audit")
    print("=" * 60)
    
    server = SEOAuditServer()
    server.load_config()
    server.load_modules()
    
    domain = "example.com"
    performance_modules = [
        "lighthouse",      # Core Web Vitals
        "images",          # Image optimization
        "mobile",          # Mobile performance
        "broken_links",    # Broken links
        "redirects"        # Redirect chains
    ]
    
    print(f"\nAnalyzing performance for {domain}...")
    results = await server.run_audit(domain, performance_modules)
    
    print(f"\n✓ Performance audit completed!")
    print("\nPerformance Metrics:")
    
    # Extract performance-related metrics
    lighthouse = results['modules'].get('lighthouse', {})
    if 'performance_score' in lighthouse:
        print(f"  Performance Score: {lighthouse['performance_score']}/100")
    
    images = results['modules'].get('images', {})
    if 'total_images' in images:
        print(f"  Total Images: {images['total_images']}")
        print(f"  Oversized Images: {len(images.get('oversized_images', []))}")
    
    redirects = results['modules'].get('redirects', {})
    if 'redirect_chains' in redirects:
        print(f"  Redirect Chains: {len(redirects['redirect_chains'])}")
    
    return results


async def example_technical_seo_audit():
    """Example: Technical SEO audit."""
    print("\n" + "=" * 60)
    print("Example 4: Technical SEO Audit")
    print("=" * 60)
    
    server = SEOAuditServer()
    server.load_config()
    server.load_modules()
    
    domain = "example.com"
    technical_modules = [
        "crawlability",    # Crawl issues
        "sitemap",         # Sitemap validation
        "robots",          # Robots.txt
        "canonical",       # Canonical tags
        "structured_data", # Schema markup
        "hreflang"        # International SEO
    ]
    
    print(f"\nRunning technical SEO audit for {domain}...")
    results = await server.run_audit(domain, technical_modules)
    
    print(f"\n✓ Technical audit completed!")
    print("\nTechnical SEO Summary:")
    
    for module_name in technical_modules:
        if module_name in results['modules']:
            module_result = results['modules'][module_name]
            print(f"\n  {module_name.upper()}:")
            print(f"    Status: {module_result.get('status', 'unknown')}")
            
            # Show module-specific metrics
            if module_name == 'sitemap':
                print(f"    Total URLs: {module_result.get('total_urls', 0)}")
            elif module_name == 'canonical':
                print(f"    Pages with canonical: {module_result.get('pages_with_canonical', 0)}")
            elif module_name == 'structured_data':
                schema = module_result.get('schema_org', {})
                print(f"    Schema found: {schema.get('found', False)}")
    
    return results


async def example_save_results():
    """Example: Save audit results to JSON file."""
    print("\n" + "=" * 60)
    print("Example 5: Save Audit Results")
    print("=" * 60)
    
    server = SEOAuditServer()
    server.load_config()
    server.load_modules()
    
    domain = "example.com"
    modules = ["onpage", "mobile", "security"]
    
    print(f"\nRunning audit for {domain}...")
    results = await server.run_audit(domain, modules)
    
    # Save to JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"audit_{domain.replace('.', '_')}_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to {filename}")
    print(f"File size: {len(json.dumps(results))} bytes")
    
    return results


async def example_batch_audit():
    """Example: Audit multiple domains."""
    print("\n" + "=" * 60)
    print("Example 6: Batch Audit")
    print("=" * 60)
    
    server = SEOAuditServer()
    server.load_config()
    server.load_modules()
    
    domains = ["example.com", "example.org", "example.net"]
    modules = ["onpage", "security"]
    
    print(f"\nRunning batch audit for {len(domains)} domains...")
    
    all_results = {}
    for domain in domains:
        print(f"\nAuditing {domain}...")
        results = await server.run_audit(domain, modules)
        all_results[domain] = results
        print(f"  ✓ {domain} completed")
    
    print(f"\n✓ Batch audit completed!")
    print(f"Total domains audited: {len(all_results)}")
    
    return all_results


async def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("SEO Audit MCP - Example Usage")
    print("=" * 60)
    print("\nThis script demonstrates various ways to use the SEO Audit tool.")
    print("\nNote: These examples use mock data. In production, modules will")
    print("fetch real data from websites and APIs.")
    print("\n" + "=" * 60)
    
    try:
        # Run examples
        await example_full_audit()
        await example_targeted_audit()
        await example_performance_audit()
        await example_technical_seo_audit()
        await example_save_results()
        await example_batch_audit()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Configure API keys in .env file")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Customize config.py for your needs")
        print("4. Implement actual API calls in modules")
        print("5. Build your own audit workflows")
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

/**
 * SEO API Integration Module
 * Provides free SEO analysis and monitoring functionality
 * 
 * Free APIs used:
 * 1. Google PageSpeed Insights API - Performance and SEO metrics
 * 2. Meta Tags Analysis - Client-side meta tag validation
 * 3. Open Graph & Twitter Card validation
 */

class SEOAnalyzer {
  constructor() {
    // Google PageSpeed Insights API (free tier, no API key required for basic usage)
    this.pageSpeedApiUrl = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed';
  }

  /**
   * Analyze page using Google PageSpeed Insights API
   * @param {string} url - URL to analyze
   * @param {string} strategy - 'mobile' or 'desktop'
   * @returns {Promise<object>} Analysis results
   */
  async analyzePageSpeed(url, strategy = 'mobile') {
    try {
      const apiUrl = `${this.pageSpeedApiUrl}?url=${encodeURIComponent(url)}&strategy=${strategy}&category=performance&category=seo&category=accessibility&category=best-practices`;
      
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }
      
      const data = await response.json();
      return this.formatPageSpeedResults(data);
    } catch (error) {
      console.error('PageSpeed API Error:', error);
      return { error: error.message };
    }
  }

  /**
   * Format PageSpeed Insights results
   */
  formatPageSpeedResults(data) {
    const lighthouse = data.lighthouseResult;
    const categories = lighthouse.categories;
    
    return {
      url: data.id,
      strategy: lighthouse.configSettings.formFactor,
      scores: {
        performance: Math.round(categories.performance.score * 100),
        seo: Math.round(categories.seo.score * 100),
        accessibility: Math.round(categories.accessibility.score * 100),
        bestPractices: Math.round(categories['best-practices'].score * 100)
      },
      metrics: {
        firstContentfulPaint: lighthouse.audits['first-contentful-paint'].displayValue,
        largestContentfulPaint: lighthouse.audits['largest-contentful-paint'].displayValue,
        totalBlockingTime: lighthouse.audits['total-blocking-time'].displayValue,
        cumulativeLayoutShift: lighthouse.audits['cumulative-layout-shift'].displayValue,
        speedIndex: lighthouse.audits['speed-index'].displayValue
      },
      seoAudits: this.extractSEOAudits(lighthouse.audits)
    };
  }

  /**
   * Extract SEO-specific audits
   */
  extractSEOAudits(audits) {
    const seoAuditKeys = [
      'document-title',
      'meta-description',
      'viewport',
      'robots-txt',
      'canonical',
      'hreflang',
      'image-alt',
      'link-text',
      'crawlable-anchors',
      'is-crawlable',
      'http-status-code',
      'font-size',
      'tap-targets'
    ];

    const results = {};
    seoAuditKeys.forEach(key => {
      if (audits[key]) {
        results[key] = {
          score: audits[key].score,
          title: audits[key].title,
          description: audits[key].description,
          displayValue: audits[key].displayValue
        };
      }
    });

    return results;
  }

  /**
   * Analyze meta tags on current page
   */
  analyzeMetaTags() {
    const metaTags = {
      title: document.title,
      description: this.getMetaContent('description'),
      keywords: this.getMetaContent('keywords'),
      author: this.getMetaContent('author'),
      viewport: this.getMetaContent('viewport'),
      robots: this.getMetaContent('robots'),
      canonical: this.getCanonicalUrl(),
      
      // Open Graph tags
      openGraph: {
        title: this.getMetaContent('og:title'),
        description: this.getMetaContent('og:description'),
        image: this.getMetaContent('og:image'),
        url: this.getMetaContent('og:url'),
        type: this.getMetaContent('og:type'),
        siteName: this.getMetaContent('og:site_name')
      },
      
      // Twitter Card tags
      twitter: {
        card: this.getMetaContent('twitter:card'),
        site: this.getMetaContent('twitter:site'),
        title: this.getMetaContent('twitter:title'),
        description: this.getMetaContent('twitter:description'),
        image: this.getMetaContent('twitter:image')
      }
    };

    return {
      tags: metaTags,
      validation: this.validateMetaTags(metaTags)
    };
  }

  /**
   * Get meta tag content by name or property
   */
  getMetaContent(name) {
    let meta = document.querySelector(`meta[name="${name}"]`);
    if (!meta) {
      meta = document.querySelector(`meta[property="${name}"]`);
    }
    return meta ? meta.getAttribute('content') : null;
  }

  /**
   * Get canonical URL
   */
  getCanonicalUrl() {
    const canonical = document.querySelector('link[rel="canonical"]');
    return canonical ? canonical.getAttribute('href') : null;
  }

  /**
   * Validate meta tags
   */
  validateMetaTags(metaTags) {
    const issues = [];
    const recommendations = [];

    // Title validation
    if (!metaTags.title) {
      issues.push('Missing page title');
    } else if (metaTags.title.length < 30) {
      recommendations.push('Title is too short (< 30 chars). Recommended: 50-60 chars');
    } else if (metaTags.title.length > 60) {
      recommendations.push('Title is too long (> 60 chars). It may be truncated in search results');
    }

    // Description validation
    if (!metaTags.description) {
      issues.push('Missing meta description');
    } else if (metaTags.description.length < 120) {
      recommendations.push('Description is too short (< 120 chars). Recommended: 150-160 chars');
    } else if (metaTags.description.length > 160) {
      recommendations.push('Description is too long (> 160 chars). It may be truncated in search results');
    }

    // Viewport validation
    if (!metaTags.viewport) {
      issues.push('Missing viewport meta tag (required for mobile responsiveness)');
    }

    // Open Graph validation
    if (!metaTags.openGraph.title || !metaTags.openGraph.description || !metaTags.openGraph.image) {
      recommendations.push('Incomplete Open Graph tags (important for social media sharing)');
    }

    // Twitter Card validation
    if (!metaTags.twitter.card || !metaTags.twitter.title || !metaTags.twitter.description) {
      recommendations.push('Incomplete Twitter Card tags (important for Twitter sharing)');
    }

    return { issues, recommendations };
  }

  /**
   * Check structured data (JSON-LD)
   */
  checkStructuredData() {
    const scripts = document.querySelectorAll('script[type="application/ld+json"]');
    const structuredData = [];

    scripts.forEach(script => {
      try {
        const data = JSON.parse(script.textContent);
        structuredData.push({
          type: data['@type'] || 'Unknown',
          data: data,
          valid: true
        });
      } catch (error) {
        structuredData.push({
          error: 'Invalid JSON-LD',
          valid: false
        });
      }
    });

    return {
      count: structuredData.length,
      schemas: structuredData,
      recommendation: structuredData.length === 0 ? 
        'Consider adding structured data (JSON-LD) for better search visibility' : null
    };
  }

  /**
   * Generate SEO report
   */
  async generateSEOReport(url = window.location.href) {
    const report = {
      url: url,
      timestamp: new Date().toISOString(),
      metaTags: this.analyzeMetaTags(),
      structuredData: this.checkStructuredData()
    };

    // Add PageSpeed results if URL is provided
    if (url) {
      console.log('Fetching PageSpeed Insights (this may take a moment)...');
      report.pageSpeed = await this.analyzePageSpeed(url);
    }

    return report;
  }

  /**
   * Display SEO report in console
   */
  async displayReport(url = window.location.href) {
    console.log('=== SEO Analysis Report ===');
    const report = await this.generateSEOReport(url);
    
    console.log('\n📊 Meta Tags Analysis:');
    console.table(report.metaTags.tags);
    
    if (report.metaTags.validation.issues.length > 0) {
      console.warn('\n⚠️ Issues Found:');
      report.metaTags.validation.issues.forEach(issue => console.warn(`  - ${issue}`));
    }
    
    if (report.metaTags.validation.recommendations.length > 0) {
      console.info('\n💡 Recommendations:');
      report.metaTags.validation.recommendations.forEach(rec => console.info(`  - ${rec}`));
    }

    if (report.structuredData.count > 0) {
      console.log('\n📋 Structured Data Found:', report.structuredData.count);
      console.table(report.structuredData.schemas.map(s => ({ type: s.type, valid: s.valid })));
    } else {
      console.warn('\n⚠️ No structured data found');
    }

    if (report.pageSpeed && !report.pageSpeed.error) {
      console.log('\n⚡ PageSpeed Insights Scores:');
      console.table(report.pageSpeed.scores);
      console.log('\n📈 Core Web Vitals:');
      console.table(report.pageSpeed.metrics);
    }

    return report;
  }

  /**
   * Create visual SEO dashboard (inject into page)
   */
  async createDashboard(containerId = 'seo-dashboard') {
    let container = document.getElementById(containerId);
    
    if (!container) {
      container = document.createElement('div');
      container.id = containerId;
      document.body.appendChild(container);
    }

    container.innerHTML = `
      <div style="position: fixed; bottom: 20px; right: 20px; width: 400px; max-height: 600px; 
                  background: white; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.2); 
                  z-index: 10000; overflow-y: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; border-radius: 12px 12px 0 0; position: sticky; top: 0; z-index: 1;">
          <h2 style="margin: 0 0 5px 0; font-size: 20px;">🔍 SEO Analyzer</h2>
          <p style="margin: 0; font-size: 12px; opacity: 0.9;">Real-time SEO metrics</p>
          <button id="close-seo-dashboard" style="position: absolute; top: 15px; right: 15px; 
                  background: rgba(255,255,255,0.2); border: none; color: white; width: 30px; 
                  height: 30px; border-radius: 50%; cursor: pointer; font-size: 18px;">×</button>
        </div>
        <div id="seo-dashboard-content" style="padding: 20px;">
          <div style="text-align: center; padding: 40px 0; color: #666;">
            <div style="font-size: 40px; margin-bottom: 10px;">⏳</div>
            <p>Analyzing SEO metrics...</p>
          </div>
        </div>
      </div>
    `;

    // Close button handler
    document.getElementById('close-seo-dashboard').addEventListener('click', () => {
      container.remove();
    });

    // Generate and display report
    const report = await this.generateSEOReport();
    this.renderDashboardContent(report);
  }

  /**
   * Render dashboard content
   */
  renderDashboardContent(report) {
    const content = document.getElementById('seo-dashboard-content');
    if (!content) return;

    const metaTags = report.metaTags.tags;
    const validation = report.metaTags.validation;
    const pageSpeed = report.pageSpeed;

    let html = '';

    // Meta Tags Section
    html += `
      <div style="margin-bottom: 20px;">
        <h3 style="margin: 0 0 10px 0; font-size: 16px; color: #333;">📝 Meta Tags</h3>
        <div style="background: #f7fafc; padding: 12px; border-radius: 8px; font-size: 13px;">
          <div style="margin-bottom: 8px;">
            <strong>Title:</strong> ${metaTags.title || '❌ Missing'}
            ${metaTags.title ? ` <span style="color: #718096;">(${metaTags.title.length} chars)</span>` : ''}
          </div>
          <div style="margin-bottom: 8px;">
            <strong>Description:</strong> ${metaTags.description || '❌ Missing'}
            ${metaTags.description ? ` <span style="color: #718096;">(${metaTags.description.length} chars)</span>` : ''}
          </div>
        </div>
      </div>
    `;

    // Validation Issues
    if (validation.issues.length > 0 || validation.recommendations.length > 0) {
      html += `<div style="margin-bottom: 20px;">`;
      
      if (validation.issues.length > 0) {
        html += `
          <div style="background: #fff5f5; border-left: 4px solid #fc8181; padding: 12px; border-radius: 8px; margin-bottom: 10px;">
            <div style="font-weight: bold; color: #c53030; margin-bottom: 8px;">⚠️ Issues</div>
            ${validation.issues.map(issue => `<div style="font-size: 13px; color: #742a2a; margin-bottom: 4px;">• ${issue}</div>`).join('')}
          </div>
        `;
      }
      
      if (validation.recommendations.length > 0) {
        html += `
          <div style="background: #fffaf0; border-left: 4px solid #f6ad55; padding: 12px; border-radius: 8px;">
            <div style="font-weight: bold; color: #c05621; margin-bottom: 8px;">💡 Recommendations</div>
            ${validation.recommendations.map(rec => `<div style="font-size: 13px; color: #7c2d12; margin-bottom: 4px;">• ${rec}</div>`).join('')}
          </div>
        `;
      }
      
      html += `</div>`;
    }

    // PageSpeed Scores
    if (pageSpeed && !pageSpeed.error) {
      html += `
        <div style="margin-bottom: 20px;">
          <h3 style="margin: 0 0 10px 0; font-size: 16px; color: #333;">⚡ Performance Scores</h3>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            ${this.renderScoreCard('SEO', pageSpeed.scores.seo)}
            ${this.renderScoreCard('Performance', pageSpeed.scores.performance)}
            ${this.renderScoreCard('Accessibility', pageSpeed.scores.accessibility)}
            ${this.renderScoreCard('Best Practices', pageSpeed.scores.bestPractices)}
          </div>
        </div>
      `;

      // Core Web Vitals
      html += `
        <div style="margin-bottom: 20px;">
          <h3 style="margin: 0 0 10px 0; font-size: 16px; color: #333;">📈 Core Web Vitals</h3>
          <div style="background: #f7fafc; padding: 12px; border-radius: 8px; font-size: 13px;">
            <div style="display: grid; gap: 8px;">
              <div><strong>FCP:</strong> ${pageSpeed.metrics.firstContentfulPaint}</div>
              <div><strong>LCP:</strong> ${pageSpeed.metrics.largestContentfulPaint}</div>
              <div><strong>TBT:</strong> ${pageSpeed.metrics.totalBlockingTime}</div>
              <div><strong>CLS:</strong> ${pageSpeed.metrics.cumulativeLayoutShift}</div>
            </div>
          </div>
        </div>
      `;
    }

    // Structured Data
    html += `
      <div style="margin-bottom: 20px;">
        <h3 style="margin: 0 0 10px 0; font-size: 16px; color: #333;">📋 Structured Data</h3>
        <div style="background: #f7fafc; padding: 12px; border-radius: 8px; font-size: 13px;">
          ${report.structuredData.count > 0 ? 
            `✅ Found ${report.structuredData.count} schema(s)` : 
            '❌ No structured data found'}
        </div>
      </div>
    `;

    // Actions
    html += `
      <div style="display: flex; gap: 10px;">
        <button onclick="seoAnalyzer.displayReport()" style="flex: 1; padding: 10px; background: #667eea; 
                color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600;">
          Console Report
        </button>
        <button onclick="seoAnalyzer.analyzePageSpeed('${window.location.href}', 'desktop').then(r => console.log(r))" 
                style="flex: 1; padding: 10px; background: #48bb78; color: white; border: none; 
                border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600;">
          Analyze Desktop
        </button>
      </div>
    `;

    content.innerHTML = html;
  }

  /**
   * Render score card
   */
  renderScoreCard(label, score) {
    let color = '#fc8181'; // Red
    if (score >= 90) color = '#48bb78'; // Green
    else if (score >= 50) color = '#f6ad55'; // Orange

    return `
      <div style="background: white; border: 1px solid #e2e8f0; padding: 12px; border-radius: 8px; text-align: center;">
        <div style="font-size: 24px; font-weight: bold; color: ${color}; margin-bottom: 4px;">${score}</div>
        <div style="font-size: 12px; color: #718096;">${label}</div>
      </div>
    `;
  }
}

// Initialize global SEO analyzer
const seoAnalyzer = new SEOAnalyzer();

// Add convenience functions to window
window.checkSEO = () => seoAnalyzer.displayReport();
window.showSEODashboard = () => seoAnalyzer.createDashboard();

// Auto-display message on load
console.log('%c🔍 SEO Analyzer Loaded!', 'color: #667eea; font-size: 16px; font-weight: bold;');
console.log('%cAvailable commands:', 'color: #666; font-size: 14px;');
console.log('  • checkSEO() - Generate detailed SEO report in console');
console.log('  • showSEODashboard() - Display interactive SEO dashboard');
console.log('  • seoAnalyzer.analyzePageSpeed(url) - Analyze any URL with PageSpeed Insights');

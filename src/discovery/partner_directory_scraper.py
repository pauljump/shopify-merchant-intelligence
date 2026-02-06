"""
Scrape Shopify partner directories and app directories for example stores.

Sources:
1. Shopify Experts directory (agencies showcase their work)
2. Shopify App Store (top apps with customer examples)
3. Theme developers' showcase pages
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import json
from typing import Set, Dict, List
from urllib.parse import urlparse, urljoin
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PartnerDirectoryScraper:
    """Scrape Shopify partner directories for store domains."""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.domains = set()
        self.sources = {
            'experts': set(),
            'apps': set(),
            'themes': set(),
            'showcases': set()
        }

    def extract_shopify_domain(self, url: str) -> str:
        """Extract clean Shopify domain from URL."""
        if not url:
            return None

        # Handle myshopify.com domains
        if 'myshopify.com' in url:
            match = re.search(r'([\w-]+)\.myshopify\.com', url)
            if match:
                return f"{match.group(1)}.myshopify.com"

        # Handle custom domains - return as-is if it looks like a store
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        domain = domain.lower().strip('/').strip()

        # Remove www prefix
        if domain.startswith('www.'):
            domain = domain[4:]

        # Skip common non-store domains
        skip_patterns = [
            'shopify.com',
            'apps.shopify.com',
            'partners.shopify.com',
            'experts.shopify.com',
            'themes.shopify.com',
            'help.shopify.com',
            'community.shopify.com',
            'shopify.dev',
            'facebook.com',
            'twitter.com',
            'instagram.com',
            'youtube.com',
            'linkedin.com',
            'pinterest.com',
            'tiktok.com',
            'x.com',
            'shop.app',
            'operationhope.org',
            'devdegree.ca',
            'shopifyacademy.com',
            'shopifystatus.com',
            'privacy.shopify.com'
        ]

        # Skip if matches any pattern
        for pattern in skip_patterns:
            if pattern in domain:
                return None

        # Skip if it's a relative path or internal Shopify link
        if not domain or '/' in domain or domain.startswith('about') or domain.startswith('partners'):
            return None

        # Must have a TLD
        if '.' not in domain:
            return None

        return domain

    def scrape_shopify_experts(self, max_pages: int = 10) -> Set[str]:
        """
        Scrape Shopify Experts directory.
        URL: https://experts.shopify.com/
        """
        logger.info("Scraping Shopify Experts directory...")
        base_url = "https://experts.shopify.com"

        try:
            # Get the main experts page
            response = self.session.get(f"{base_url}/", timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all expert/agency profile links
            expert_links = set()
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/experts/' in href or '/agencies/' in href:
                    full_url = urljoin(base_url, href)
                    expert_links.add(full_url)

            logger.info(f"Found {len(expert_links)} expert/agency profiles")

            # Visit each expert page and look for portfolio/case studies
            for i, expert_url in enumerate(list(expert_links)[:max_pages]):
                try:
                    logger.info(f"Scraping expert page {i+1}/{min(len(expert_links), max_pages)}: {expert_url}")
                    response = self.session.get(expert_url, timeout=30)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Look for store URLs in portfolio sections
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        domain = self.extract_shopify_domain(href)
                        if domain:
                            self.sources['experts'].add(domain)
                            logger.info(f"Found store from experts: {domain}")

                    time.sleep(2)  # Be polite

                except Exception as e:
                    logger.error(f"Error scraping expert page {expert_url}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error accessing Shopify Experts: {e}")

        return self.sources['experts']

    def scrape_app_store(self, max_apps: int = 100) -> Set[str]:
        """
        Scrape Shopify App Store for customer examples.
        URL: https://apps.shopify.com/
        """
        logger.info("Scraping Shopify App Store...")
        base_url = "https://apps.shopify.com"

        try:
            # Get popular apps from different categories
            categories = [
                '/browse/store-design',
                '/browse/marketing',
                '/browse/sales-conversion',
                '/browse/customer-support',
                '/browse/shipping-delivery',
                '/browse/inventory-management'
            ]

            app_links = set()

            for category in categories:
                try:
                    logger.info(f"Scraping category: {category}")
                    response = self.session.get(f"{base_url}{category}", timeout=30)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Find app links
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if href.startswith('/') and not any(x in href for x in ['/browse', '/search', '/categories']):
                            full_url = urljoin(base_url, href)
                            if full_url.startswith(f"{base_url}/") and full_url != f"{base_url}/":
                                app_links.add(full_url)

                    time.sleep(2)

                except Exception as e:
                    logger.error(f"Error scraping category {category}: {e}")
                    continue

            logger.info(f"Found {len(app_links)} app pages")

            # Visit each app page and look for customer examples
            for i, app_url in enumerate(list(app_links)[:max_apps]):
                try:
                    logger.info(f"Scraping app page {i+1}/{min(len(app_links), max_apps)}: {app_url}")
                    response = self.session.get(app_url, timeout=30)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Look for customer testimonials, case studies, "powered by" sections
                    # Check for common patterns
                    text = soup.get_text()

                    # Find URLs in the page
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        domain = self.extract_shopify_domain(href)
                        if domain:
                            # Check if it's in a testimonial or customer section
                            parent_text = link.parent.get_text().lower() if link.parent else ""
                            if any(keyword in parent_text for keyword in ['customer', 'client', 'testimonial', 'case study', 'trusted by', 'used by']):
                                self.sources['apps'].add(domain)
                                logger.info(f"Found store from apps: {domain}")

                    time.sleep(2)

                except Exception as e:
                    logger.error(f"Error scraping app page {app_url}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error accessing Shopify App Store: {e}")

        return self.sources['apps']

    def scrape_theme_showcases(self) -> Set[str]:
        """
        Scrape Shopify Theme developers' showcase pages.
        URL: https://themes.shopify.com/
        """
        logger.info("Scraping Shopify Themes...")
        base_url = "https://themes.shopify.com"

        try:
            # Get popular themes
            response = self.session.get(f"{base_url}/themes?sort_by=popularity", timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            theme_links = set()
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/themes/' in href and href != '/themes':
                    full_url = urljoin(base_url, href)
                    theme_links.add(full_url)

            logger.info(f"Found {len(theme_links)} theme pages")

            # Visit each theme page
            for i, theme_url in enumerate(list(theme_links)[:50]):  # Limit to top 50 themes
                try:
                    logger.info(f"Scraping theme page {i+1}/{min(len(theme_links), 50)}: {theme_url}")
                    response = self.session.get(theme_url, timeout=30)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Look for demo stores and example stores
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        domain = self.extract_shopify_domain(href)
                        if domain:
                            # Check if it's a demo or example
                            link_text = link.get_text().lower()
                            if any(keyword in link_text for keyword in ['demo', 'example', 'preview', 'view theme']):
                                self.sources['themes'].add(domain)
                                logger.info(f"Found store from themes: {domain}")

                    time.sleep(2)

                except Exception as e:
                    logger.error(f"Error scraping theme page {theme_url}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error accessing Shopify Themes: {e}")

        return self.sources['themes']

    def scrape_partner_showcases(self) -> Set[str]:
        """
        Scrape Shopify Partners showcase pages.
        These are individual partner agencies that showcase their client work.
        """
        logger.info("Scraping Partner Showcases...")

        # Known popular app developer websites with customer showcases
        app_developer_sites = [
            'https://www.klaviyo.com/customers',
            'https://www.yotpo.com/customers/',
            'https://www.recharge.com/customers',
            'https://www.gorgias.com/customers',
            'https://www.privy.com/customers',
            'https://www.justuno.com/customers',
            'https://www.omnisend.com/customers',
            'https://www.smile.io/customers',
            'https://www.bold.org/clients',  # Bold Commerce
            'https://www.shogun.com/customers',
            'https://www.shipbob.com/customers',
            'https://www.loox.io/customers',
        ]

        try:
            for site_url in app_developer_sites:
                try:
                    logger.info(f"Scraping app developer site: {site_url}")
                    response = self.session.get(site_url, timeout=30)

                    if response.status_code == 404:
                        logger.warning(f"Page not found (404): {site_url}")
                        continue

                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Look for customer links and case studies
                    for link in soup.find_all('a', href=True):
                        href = link['href']

                        # Check if href contains myshopify or looks like a store
                        if any(indicator in href.lower() for indicator in ['myshopify', '.com', '.net', '.co']):
                            domain = self.extract_shopify_domain(href)
                            if domain:
                                self.sources['showcases'].add(domain)
                                logger.info(f"Found store from showcases: {domain}")

                    # Also search the text for domain mentions
                    text = soup.get_text()
                    myshopify_matches = re.findall(r'([\w-]+\.myshopify\.com)', text)
                    for match in myshopify_matches:
                        self.sources['showcases'].add(match)
                        logger.info(f"Found myshopify domain in text: {match}")

                    time.sleep(3)  # Be extra polite to third-party sites

                except Exception as e:
                    logger.error(f"Error scraping app developer site {site_url}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error accessing partner showcases: {e}")

        return self.sources['showcases']

    def scrape_shopify_enterprise_customers(self) -> Set[str]:
        """Scrape Shopify's official customer showcase pages."""
        logger.info("Scraping Shopify Enterprise Customers...")

        showcase_urls = [
            'https://www.shopify.com/plus/customers',
            'https://www.shopify.com/customers',
            'https://www.shopify.com/enterprise',
        ]

        try:
            for url in showcase_urls:
                try:
                    logger.info(f"Scraping Shopify showcase: {url}")
                    response = self.session.get(url, timeout=30)

                    if response.status_code == 404:
                        logger.warning(f"Page not found (404): {url}")
                        continue

                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Find all links
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        domain = self.extract_shopify_domain(href)
                        if domain:
                            self.sources['showcases'].add(domain)
                            logger.info(f"Found enterprise customer: {domain}")

                    # Find myshopify domains in text
                    text = soup.get_text()
                    myshopify_matches = re.findall(r'([\w-]+\.myshopify\.com)', text)
                    for match in myshopify_matches:
                        self.sources['showcases'].add(match)
                        logger.info(f"Found myshopify domain in text: {match}")

                    time.sleep(2)

                except Exception as e:
                    logger.error(f"Error scraping showcase {url}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error accessing Shopify showcases: {e}")

        return self.sources['showcases']

    def scrape_agency_portfolios(self) -> Set[str]:
        """Scrape known Shopify Plus agency portfolio pages."""
        logger.info("Scraping Agency Portfolios...")

        # Top Shopify Plus agencies with public portfolios
        agency_urls = [
            'https://www.weareundercurrent.com/work',
            'https://www.disruptiveagency.com/work',
            'https://www.bluewaterglobal.com/portfolio',
            'https://www.thisiselectric.com/work',
        ]

        try:
            for url in agency_urls:
                try:
                    logger.info(f"Scraping agency portfolio: {url}")
                    response = self.session.get(url, timeout=30)

                    if response.status_code == 404:
                        logger.warning(f"Page not found (404): {url}")
                        continue

                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Find store links in portfolios
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        domain = self.extract_shopify_domain(href)
                        if domain:
                            self.sources['showcases'].add(domain)
                            logger.info(f"Found store from agency portfolio: {domain}")

                    # Find myshopify domains in text
                    text = soup.get_text()
                    myshopify_matches = re.findall(r'([\w-]+\.myshopify\.com)', text)
                    for match in myshopify_matches:
                        self.sources['showcases'].add(match)
                        logger.info(f"Found myshopify domain in agency text: {match}")

                    time.sleep(3)

                except Exception as e:
                    logger.error(f"Error scraping agency portfolio {url}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error accessing agency portfolios: {e}")

        return self.sources['showcases']

    def scrape_all(self, max_experts: int = 10, max_apps: int = 100) -> Dict[str, Set[str]]:
        """Run all scrapers and collect all domains."""
        logger.info("Starting comprehensive partner directory scrape...")

        # Scrape all sources
        # self.scrape_shopify_experts(max_pages=max_experts)  # Skip - not working well
        # self.scrape_app_store(max_apps=max_apps)  # Skip - requires auth
        # self.scrape_theme_showcases()  # Skip - no demo stores found

        # Focus on sources that actually work
        self.scrape_partner_showcases()  # App developer customer pages
        self.scrape_shopify_enterprise_customers()  # Shopify's own showcases
        self.scrape_agency_portfolios()  # Agency portfolio pages

        # Combine all domains
        all_domains = set()
        for source, domains in self.sources.items():
            all_domains.update(domains)

        self.domains = all_domains

        return self.sources

    def get_stats(self) -> Dict:
        """Get statistics about discovered stores."""
        total = len(self.domains)
        breakdown = {source: len(domains) for source, domains in self.sources.items()}

        return {
            'total': total,
            'breakdown': breakdown,
            'sources': self.sources
        }

    def save_domains(self, output_path: str):
        """Save discovered domains to file."""
        with open(output_path, 'w') as f:
            for domain in sorted(self.domains):
                f.write(f"{domain}\n")

        logger.info(f"Saved {len(self.domains)} domains to {output_path}")

    def save_detailed_report(self, output_path: str):
        """Save detailed report with breakdown by source."""
        report = {
            'total_stores': len(self.domains),
            'breakdown': {
                'experts': len(self.sources['experts']),
                'apps': len(self.sources['apps']),
                'themes': len(self.sources['themes']),
                'showcases': len(self.sources['showcases'])
            },
            'stores_by_source': {
                'experts': sorted(list(self.sources['experts'])),
                'apps': sorted(list(self.sources['apps'])),
                'themes': sorted(list(self.sources['themes'])),
                'showcases': sorted(list(self.sources['showcases']))
            }
        }

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Saved detailed report to {output_path}")


def main():
    """Main entry point for partner directory scraping."""
    scraper = PartnerDirectoryScraper()

    # Run all scrapers
    logger.info("=" * 80)
    logger.info("SHOPIFY PARTNER DIRECTORY SCRAPER")
    logger.info("=" * 80)

    sources = scraper.scrape_all(max_experts=10, max_apps=100)

    # Print results
    print("\n" + "=" * 80)
    print("SCRAPING COMPLETE")
    print("=" * 80)

    stats = scraper.get_stats()
    print(f"\nTotal stores discovered: {stats['total']}")
    print("\nBreakdown by source:")
    for source, count in stats['breakdown'].items():
        print(f"  {source.capitalize()}: {count}")

    # Save results
    base_path = "/Users/pjump/Desktop/projects/shopify-merchant-intelligence/data/partner_directory"
    scraper.save_domains(f"{base_path}/domains.txt")
    scraper.save_detailed_report(f"{base_path}/detailed_report.json")

    print(f"\nResults saved to: {base_path}/")
    print("  - domains.txt (all domains)")
    print("  - detailed_report.json (breakdown by source)")

    # Show some notable stores
    if scraper.domains:
        print("\nSample discovered stores:")
        for domain in sorted(list(scraper.domains))[:10]:
            print(f"  - {domain}")


if __name__ == "__main__":
    main()

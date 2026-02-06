"""
Scrape Shopify's own directories for featured stores.

Sources:
- Shopify Plus customers page
- Shopify examples/success stories
- Shopify blog case studies
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import Set, Dict
import time


class ShopifyShowcaseScraper:
    """Scrape Shopify's own showcase of customer stores."""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self.showcase_urls = [
            'https://www.shopify.com/plus/customers',
            'https://www.shopify.com/examples',
            'https://www.shopify.com/blog/successful-ecommerce-stores',
            'https://www.shopify.com/blog/best-shopify-stores',
        ]

    def discover(self) -> Dict[str, Dict]:
        """
        Scrape Shopify's own showcase pages.

        Returns:
            Dict mapping domains to metadata (name, industry, location if found)
        """
        print("🔍 Scraping Shopify's Own Showcase Pages...")
        print(f"📊 Checking {len(self.showcase_urls)} showcase URLs\n")

        all_stores = {}

        for url in self.showcase_urls:
            print(f"🌐 Scraping: {url}")
            try:
                response = requests.get(url, headers=self.headers, timeout=15)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Extract store mentions
                    stores = self._extract_stores(soup, url)

                    if stores:
                        all_stores.update(stores)
                        print(f"  ✅ Found {len(stores)} stores")
                    else:
                        print(f"  ⏭️  No stores extracted")
                else:
                    print(f"  ⚠️  HTTP {response.status_code}")

            except Exception as e:
                print(f"  ⚠️  Error: {e}")

            time.sleep(2)  # Be respectful

        print(f"\n{'='*60}")
        print(f"🎯 Showcase Scraping Complete!")
        print(f"{'='*60}")
        print(f"🌐 Total stores found: {len(all_stores)}")
        print(f"{'='*60}\n")

        # Save results
        self._save_results(all_stores)

        return all_stores

    def _extract_stores(self, soup: BeautifulSoup, source_url: str) -> Dict[str, Dict]:
        """Extract store information from a showcase page."""
        stores = {}

        # Find all links that might be store URLs
        all_links = soup.find_all('a', href=True)

        for link in all_links:
            href = link['href']

            # Check if it's a store URL (not Shopify internal pages)
            if self._is_store_url(href):
                domain = self._clean_domain(href)

                if domain and domain not in stores:
                    # Extract context/metadata
                    metadata = self._extract_metadata(link, soup)
                    metadata['source'] = source_url

                    stores[domain] = metadata

        # Also search for domain mentions in text
        text_stores = self._find_domains_in_text(soup.get_text())
        for domain in text_stores:
            if domain not in stores:
                stores[domain] = {'source': source_url}

        return stores

    def _is_store_url(self, url: str) -> bool:
        """Check if URL is likely a customer store."""
        if not url or len(url) < 5:
            return False

        # Exclude Shopify's own domains
        exclude_domains = [
            'shopify.com',
            'shopify.dev',
            'help.shopify.com',
            'community.shopify.com',
            'apps.shopify.com',
            'partners.shopify.com',
            'twitter.com',
            'facebook.com',
            'instagram.com',
            'linkedin.com',
            'youtube.com',
        ]

        url_lower = url.lower()

        for exclude in exclude_domains:
            if exclude in url_lower:
                return False

        # Check if it looks like a real store URL
        if url.startswith('http'):
            return True

        return False

    def _extract_metadata(self, link_tag, soup: BeautifulSoup) -> Dict:
        """Extract metadata about the store from context."""
        metadata = {}

        # Get link text
        link_text = link_tag.get_text(strip=True)
        if link_text:
            metadata['name'] = link_text

        # Look for parent containers with metadata
        parent = link_tag.find_parent(['div', 'article', 'section'])
        if parent:
            text = parent.get_text()

            # Look for industry keywords
            industries = [
                'fashion', 'apparel', 'clothing',
                'food', 'beverage', 'restaurant',
                'beauty', 'cosmetics',
                'electronics', 'technology',
                'home', 'furniture',
                'sports', 'fitness',
                'jewelry',
                'grocery', 'retail'
            ]

            for industry in industries:
                if industry.lower() in text.lower():
                    metadata['industry'] = industry
                    break

            # Look for location mentions (USA cities/states)
            usa_locations = [
                'USA', 'United States', 'America',
                'New York', 'NYC', 'California', 'Los Angeles', 'LA',
                'Chicago', 'Texas', 'Florida', 'Seattle'
            ]

            for location in usa_locations:
                if location in text:
                    metadata['location_mention'] = location
                    break

        return metadata

    def _find_domains_in_text(self, text: str) -> Set[str]:
        """Find domain mentions in plain text."""
        domains = set()

        # Regex for domains
        domain_pattern = r'https?://([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
        matches = re.findall(domain_pattern, text)

        for match in matches:
            domain = self._clean_domain(match)
            if domain and self._is_store_url(domain):
                domains.add(domain)

        return domains

    def _clean_domain(self, url: str) -> str:
        """Clean and normalize domain."""
        if not url:
            return ""

        url = url.strip().lower()
        url = url.replace('https://', '').replace('http://', '').replace('www.', '')
        domain = url.split('/')[0].split('?')[0]

        # Must have a TLD
        if '.' not in domain:
            return ""

        return domain

    def _save_results(self, stores: Dict):
        """Save discovered stores."""
        import json
        import os

        os.makedirs('data/shopify_showcase', exist_ok=True)

        # Save as JSON with metadata
        with open('data/shopify_showcase/stores_with_metadata.json', 'w') as f:
            json.dump(stores, f, indent=2)

        # Save as simple domain list
        with open('data/shopify_showcase/domains.txt', 'w') as f:
            for domain in sorted(stores.keys()):
                f.write(f"{domain}\n")

        print(f"💾 Saved to data/shopify_showcase/")


if __name__ == '__main__':
    scraper = ShopifyShowcaseScraper()
    results = scraper.discover()

    # Show stats
    usa_stores = {d: m for d, m in results.items() if m.get('location_mention')}
    print(f"\n📊 Statistics:")
    print(f"Total stores: {len(results)}")
    print(f"USA mentions: {len(usa_stores)}")

    if usa_stores:
        print(f"\n🇺🇸 USA Stores:")
        for domain, meta in list(usa_stores.items())[:10]:
            print(f"  - {domain}: {meta.get('name', 'Unknown')} ({meta.get('location_mention', '')})")

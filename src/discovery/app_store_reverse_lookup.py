"""
Reverse lookup: Find stores by scraping Shopify App Store.

Many apps show example stores using them. We can:
1. Find apps related to local delivery/USA markets
2. Extract stores shown as using those apps
3. Those stores are verified Shopify users

Target apps:
- Local delivery apps (Uber Direct, DoorDash, Postmates)
- USA-focused apps
- Apps with customer showcases
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from typing import Set, Dict


class AppStoreReverseLookup:
    """Find Shopify stores via App Store reverse lookup."""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        # Apps related to local delivery / USA markets
        self.target_apps = [
            # Local delivery integration apps
            'local-delivery',
            'uber-direct',
            'doordash',
            'postmates',
            'deliverr',
            'ship-station',

            # USA payment/shipping apps
            'stripe',
            'paypal',
            'usps',
            'fedex',
            'ups',

            # Popular apps (likely used by many USA stores)
            'klaviyo',
            'yotpo',
            'smile-rewards',
            'judge-me',
            'privy',
        ]

    def discover(self, max_apps: int = 20) -> Dict[str, Set[str]]:
        """
        Discover stores via App Store reverse lookup.

        Args:
            max_apps: Maximum number of apps to check

        Returns:
            Dict mapping app names to sets of store domains
        """
        print("🔍 Shopify App Store Reverse Lookup...")
        print(f"📊 Checking {min(len(self.target_apps), max_apps)} apps\n")

        app_stores = {}
        all_domains = set()

        for app_slug in self.target_apps[:max_apps]:
            print(f"📱 App: {app_slug}")

            try:
                # Shopify App Store URL format
                app_url = f"https://apps.shopify.com/{app_slug}"

                response = requests.get(app_url, headers=self.headers, timeout=15)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Extract stores from app page
                    stores = self._extract_stores_from_app_page(soup, app_url)

                    if stores:
                        app_stores[app_slug] = stores
                        all_domains.update(stores)
                        print(f"  ✅ Found {len(stores)} stores")
                    else:
                        print(f"  ⏭️  No stores found")
                elif response.status_code == 404:
                    print(f"  ⚠️  App not found")
                else:
                    print(f"  ⚠️  HTTP {response.status_code}")

            except Exception as e:
                print(f"  ⚠️  Error: {e}")

            time.sleep(2)  # Rate limiting

        print(f"\n{'='*60}")
        print(f"🎯 App Store Reverse Lookup Complete!")
        print(f"{'='*60}")
        print(f"📱 Apps checked: {len(app_stores)}")
        print(f"🌐 Total stores found: {len(all_domains)}")
        print(f"{'='*60}\n")

        # Save results
        self._save_results(app_stores, all_domains)

        return app_stores

    def _extract_stores_from_app_page(self, soup: BeautifulSoup, app_url: str) -> Set[str]:
        """Extract store domains from an app page."""
        domains = set()

        # Look for customer/example store mentions
        all_text = soup.get_text()

        # Find domain patterns in text
        domain_patterns = [
            r'https?://([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)',
            r'([a-zA-Z0-9-]+\.myshopify\.com)',
            r'([a-zA-Z0-9-]+\.com)',
        ]

        for pattern in domain_patterns:
            matches = re.findall(pattern, all_text)
            for match in matches:
                domain = self._clean_domain(match)
                if domain and self._is_likely_store(domain):
                    domains.add(domain)

        # Look for specific sections mentioning customers
        customer_sections = soup.find_all(['div', 'section'], class_=re.compile(r'(customer|testimonial|example|showcase)', re.I))

        for section in customer_sections:
            # Find links in these sections
            links = section.find_all('a', href=True)
            for link in links:
                href = link['href']
                if href and not href.startswith('/'):
                    domain = self._clean_domain(href)
                    if domain and self._is_likely_store(domain):
                        domains.add(domain)

        # Look for featured merchant mentions
        # Many apps list "Trusted by X stores" with examples
        featured_text = soup.find_all(text=re.compile(r'(trusted by|used by|powered|customers include)', re.I))

        for text in featured_text:
            parent = text.parent
            if parent:
                # Look for domains near this text
                nearby_text = parent.get_text()
                for pattern in domain_patterns:
                    matches = re.findall(pattern, nearby_text)
                    for match in matches:
                        domain = self._clean_domain(match)
                        if domain and self._is_likely_store(domain):
                            domains.add(domain)

        return domains

    def _clean_domain(self, url: str) -> str:
        """Clean and normalize domain."""
        if not url:
            return ""

        url = url.strip().lower()
        url = url.replace('https://', '').replace('http://', '').replace('www.', '')
        domain = url.split('/')[0].split('?')[0]

        return domain

    def _is_likely_store(self, domain: str) -> bool:
        """Check if domain is likely a store."""
        if not domain or len(domain) < 4:
            return False

        # Exclude Shopify own domains and common platforms
        exclude = [
            'shopify.com', 'apps.shopify.com', 'help.shopify',
            'google.com', 'facebook.com', 'twitter.com', 'instagram.com',
            'youtube.com', 'linkedin.com', 'github.com',
            'example.com', 'test.com', 'localhost'
        ]

        for exc in exclude:
            if exc in domain:
                return False

        # Must have a TLD
        if '.' not in domain:
            return False

        return True

    def _save_results(self, app_stores: Dict, all_domains: Set):
        """Save results."""
        import json
        import os

        os.makedirs('data/app_store_lookup', exist_ok=True)

        # Save mapping of apps to stores
        serializable = {app: list(stores) for app, stores in app_stores.items()}
        with open('data/app_store_lookup/app_to_stores.json', 'w') as f:
            json.dump(serializable, f, indent=2)

        # Save all domains
        with open('data/app_store_lookup/all_domains.txt', 'w') as f:
            for domain in sorted(all_domains):
                f.write(f"{domain}\n")

        print(f"💾 Saved to data/app_store_lookup/")


if __name__ == '__main__':
    lookup = AppStoreReverseLookup()
    results = lookup.discover(max_apps=20)

    # Show top apps by store count
    print(f"\n📊 Top apps by stores found:")
    sorted_apps = sorted(results.items(), key=lambda x: len(x[1]), reverse=True)
    for app, stores in sorted_apps[:10]:
        print(f"  {app}: {len(stores)} stores")

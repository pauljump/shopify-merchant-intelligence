"""
Certificate Transparency DNS Enumeration

Queries crt.sh (Certificate Transparency logs) to discover all Shopify stores
via their *.myshopify.com subdomains and custom domains with Shopify certificates.

Target: Millions of Shopify stores in minutes.
"""

import requests
import time
from typing import Set, List
import re
from urllib.parse import quote


class CertificateTransparencySearch:
    """Search Certificate Transparency logs for Shopify domains."""

    def __init__(self):
        self.crtsh_url = 'https://crt.sh/'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def discover_myshopify_stores(self, limit: int = 10000) -> Set[str]:
        """
        Discover Shopify stores via *.myshopify.com certificate transparency.

        Args:
            limit: Maximum number of stores to discover (default 10,000)

        Returns:
            Set of myshopify.com subdomains
        """
        print(f"🔍 Searching Certificate Transparency logs for *.myshopify.com...")
        print(f"📊 Target: {limit:,} stores\n")

        # Query crt.sh for all myshopify.com subdomains
        query = '%.myshopify.com'
        domains = self._query_crtsh(query, limit)

        print(f"\n{'='*60}")
        print(f"🎯 Certificate Transparency Discovery Complete!")
        print(f"{'='*60}")
        print(f"🌐 Total *.myshopify.com domains: {len(domains):,}")
        print(f"{'='*60}\n")

        return domains

    def discover_custom_domains(self, limit: int = 5000) -> Set[str]:
        """
        Discover custom domains using Shopify (via Shopify certificates).

        This finds stores using custom domains like store.com instead of store.myshopify.com.

        Args:
            limit: Maximum number of domains to discover

        Returns:
            Set of custom domains
        """
        print(f"🔍 Searching for custom Shopify domains via SSL certificates...")

        # Search for certificates issued by Shopify's CDN providers
        searches = [
            'Shopify',
            'cdn.shopify.com',
        ]

        domains = set()
        for search_term in searches:
            print(f"  🔎 Searching: {search_term}")
            found = self._query_crtsh_by_org(search_term, limit // len(searches))
            domains.update(found)
            print(f"    ✅ Found {len(found):,} domains")
            time.sleep(2)  # Rate limiting

        print(f"\n🌐 Total custom domains: {len(domains):,}\n")
        return domains

    def _query_crtsh(self, query: str, limit: int = 10000) -> Set[str]:
        """
        Query crt.sh for domains matching the pattern.

        Args:
            query: DNS pattern (e.g., '%.myshopify.com')
            limit: Maximum results to fetch

        Returns:
            Set of discovered domains
        """
        domains = set()

        try:
            # crt.sh returns JSON when you add output=json parameter
            url = f'{self.crtsh_url}?q={quote(query)}&output=json'

            print(f"  🌐 Querying: {url}")
            response = self.session.get(url, timeout=60)
            response.raise_for_status()

            data = response.json()
            print(f"  📊 Received {len(data):,} certificate entries")

            # Extract unique domains
            for entry in data[:limit]:
                # Certificate may have common_name and name_value fields
                for field in ['common_name', 'name_value']:
                    if field in entry:
                        domain_str = entry[field]

                        # name_value can contain multiple domains separated by newlines
                        for domain in domain_str.split('\n'):
                            domain = domain.strip()

                            # Clean up domain
                            cleaned = self._clean_domain(domain)
                            if cleaned and self._is_valid_shopify_domain(cleaned):
                                domains.add(cleaned)

                if len(domains) >= limit:
                    break

            print(f"  ✅ Extracted {len(domains):,} unique domains")

        except Exception as e:
            print(f"  ⚠️  Error querying crt.sh: {e}")

        return domains

    def _query_crtsh_by_org(self, org: str, limit: int = 5000) -> Set[str]:
        """Query crt.sh by organization/issuer name."""
        domains = set()

        try:
            url = f'{self.crtsh_url}?O={quote(org)}&output=json'

            print(f"    🌐 Querying: {url}")
            response = self.session.get(url, timeout=60)
            response.raise_for_status()

            data = response.json()

            for entry in data[:limit]:
                for field in ['common_name', 'name_value']:
                    if field in entry:
                        domain_str = entry[field]
                        for domain in domain_str.split('\n'):
                            cleaned = self._clean_domain(domain.strip())
                            if cleaned:
                                domains.add(cleaned)

        except Exception as e:
            print(f"    ⚠️  Error: {e}")

        return domains

    def _clean_domain(self, domain: str) -> str:
        """Clean and normalize domain."""
        if not domain:
            return ""

        # Remove wildcards
        domain = domain.replace('*.', '')

        # Remove protocol if present
        domain = re.sub(r'^https?://', '', domain)

        # Remove www.
        if domain.startswith('www.'):
            domain = domain[4:]

        # Remove path and query strings
        domain = domain.split('/')[0].split('?')[0]

        # Lowercase
        domain = domain.lower()

        return domain

    def _is_valid_shopify_domain(self, domain: str) -> bool:
        """Check if domain is a valid Shopify store domain."""
        if not domain or len(domain) < 4:
            return False

        # Must end with .myshopify.com
        if '.myshopify.com' in domain:
            # Remove .myshopify.com to get store name
            store_name = domain.replace('.myshopify.com', '')

            # Must be just the store name (no additional subdomains except checkout/shop)
            if store_name and '.' not in store_name:
                return True

            # Allow checkout.storename.myshopify.com or shop.storename.myshopify.com
            parts = store_name.split('.')
            if len(parts) == 2 and parts[0] in ['checkout', 'shop', 'admin']:
                return True

        return False

    def save_results(self, domains: Set[str], output_file: str = 'data/crt_myshopify_domains.txt'):
        """Save discovered domains to file."""
        import os

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w') as f:
            for domain in sorted(domains):
                # Extract store name (remove .myshopify.com)
                if '.myshopify.com' in domain:
                    store_name = domain.replace('.myshopify.com', '').split('.')[0]
                    f.write(f"{store_name}.myshopify.com\n")

        print(f"💾 Saved {len(domains):,} domains to: {output_file}")

        return output_file


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Discover Shopify stores via Certificate Transparency')
    parser.add_argument('--limit', type=int, default=10000, help='Max stores to discover')
    parser.add_argument('--custom', action='store_true', help='Also search for custom domains')
    args = parser.parse_args()

    searcher = CertificateTransparencySearch()

    # Discover myshopify.com stores
    myshopify_domains = searcher.discover_myshopify_stores(limit=args.limit)
    searcher.save_results(myshopify_domains, 'data/crt_myshopify_domains.txt')

    # Optionally discover custom domains
    if args.custom:
        custom_domains = searcher.discover_custom_domains(limit=5000)
        searcher.save_results(custom_domains, 'data/crt_custom_domains.txt')

    print(f"\n🎉 Discovery complete!")
    print(f"   - *.myshopify.com stores: {len(myshopify_domains):,}")
    if args.custom:
        print(f"   - Custom domain stores: {len(custom_domains):,}")

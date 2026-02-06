"""
Automated Google dorking to discover Shopify stores.

Uses DuckDuckGo (no API key needed) and Google HTML scraping.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from typing import Set
from urllib.parse import quote_plus, urlparse


class GoogleDorkDiscovery:
    """Discover Shopify stores using search engine dorking."""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Shopify-specific search queries
        self.dork_queries = [
            # Direct Shopify indicators
            '"powered by Shopify" USA',
            '"powered by Shopify" "United States"',
            'site:myshopify.com',

            # Shopify Plus specific
            '"Shopify Plus" store USA',
            '"Shopify Plus" merchant America',

            # Local delivery keywords + Shopify
            '"local delivery" "powered by Shopify"',
            '"same day delivery" "Shopify"',
            '"curbside pickup" "Shopify"',

            # Industry + Location + Shopify
            'grocery "powered by Shopify" USA',
            'restaurant "Shopify" "local delivery"',
            'bakery "Shopify" USA',
            'coffee shop "Shopify" America',

            # USA cities + Shopify
            '"powered by Shopify" "New York"',
            '"powered by Shopify" "Los Angeles"',
            '"powered by Shopify" "Chicago"',
            '"powered by Shopify" "San Francisco"',
            '"powered by Shopify" "Texas"',
        ]

    def discover_via_duckduckgo(self, max_results_per_query: int = 50) -> Set[str]:
        """
        Use DuckDuckGo HTML scraping (no API key needed).

        Args:
            max_results_per_query: Max results per search query

        Returns:
            Set of discovered domains
        """
        print("🦆 Google Dorking via DuckDuckGo...")
        print(f"📊 Running {len(self.dork_queries)} queries\n")

        all_domains = set()

        for query in self.dork_queries:
            print(f"🔎 Query: '{query}'")

            try:
                domains = self._duckduckgo_search(query, max_results=max_results_per_query)

                if domains:
                    all_domains.update(domains)
                    print(f"  ✅ Found {len(domains)} domains")
                else:
                    print(f"  ⏭️  No results")

            except Exception as e:
                print(f"  ⚠️  Error: {e}")

            time.sleep(3)  # Be respectful with rate limiting

        print(f"\n{'='*60}")
        print(f"🎯 Dorking Complete!")
        print(f"{'='*60}")
        print(f"🌐 Total unique domains: {len(all_domains)}")
        print(f"{'='*60}\n")

        # Save results
        self._save_results(all_domains)

        return all_domains

    def _duckduckgo_search(self, query: str, max_results: int = 50) -> Set[str]:
        """Search DuckDuckGo HTML."""
        domains = set()

        try:
            # DuckDuckGo HTML search
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

            response = requests.get(url, headers=self.headers, timeout=15)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract result links
                results = soup.find_all('a', class_='result__a')

                for result in results[:max_results]:
                    href = result.get('href')

                    if href:
                        # DuckDuckGo redirects through their tracker
                        # Extract actual URL from redirect
                        if 'uddg=' in href:
                            match = re.search(r'uddg=([^&]+)', href)
                            if match:
                                from urllib.parse import unquote
                                actual_url = unquote(match.group(1))
                                domain = self._extract_domain(actual_url)

                                if domain and self._is_likely_shopify_store(domain):
                                    domains.add(domain)
                        else:
                            domain = self._extract_domain(href)
                            if domain and self._is_likely_shopify_store(domain):
                                domains.add(domain)

        except Exception as e:
            raise

        return domains

    def _extract_domain(self, url: str) -> str:
        """Extract clean domain from URL."""
        if not url:
            return ""

        try:
            if not url.startswith('http'):
                url = f'https://{url}'

            parsed = urlparse(url)
            domain = parsed.netloc

            # Remove www.
            if domain.startswith('www.'):
                domain = domain[4:]

            return domain.lower()
        except:
            return ""

    def _is_likely_shopify_store(self, domain: str) -> bool:
        """Check if domain is likely a Shopify store."""
        if not domain or len(domain) < 4:
            return False

        # Definitely Shopify
        if '.myshopify.com' in domain:
            return True

        # Exclude non-store domains
        exclude = [
            'shopify.com', 'shopify.dev', 'google.com', 'facebook.com',
            'twitter.com', 'instagram.com', 'youtube.com', 'linkedin.com',
            'help.shopify', 'community.shopify', 'apps.shopify'
        ]

        for exc in exclude:
            if exc in domain:
                return False

        return True

    def _save_results(self, domains: Set[str]):
        """Save discovered domains."""
        import os

        os.makedirs('data/google_dork', exist_ok=True)

        with open('data/google_dork/domains.txt', 'w') as f:
            for domain in sorted(domains):
                f.write(f"{domain}\n")

        print(f"💾 Saved to data/google_dork/domains.txt")


if __name__ == '__main__':
    discoverer = GoogleDorkDiscovery()
    results = discoverer.discover_via_duckduckgo(max_results_per_query=30)

    print(f"\n📊 Sample results:")
    for domain in list(results)[:20]:
        print(f"  - {domain}")

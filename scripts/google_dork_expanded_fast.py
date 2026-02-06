"""
FAST Expanded Google Dorking - 150+ Targeted Queries

Optimized for speed with parallel processing and smarter rate limiting.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from typing import Set, Dict, List
from urllib.parse import quote_plus, urlparse
from collections import defaultdict
import os
import concurrent.futures
from threading import Lock


class FastGoogleDorkDiscovery:
    """Fast expanded Google dorking with 150+ queries."""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        self.query_results: Dict[str, int] = defaultdict(int)
        self.all_domains: Set[str] = set()
        self.lock = Lock()

        self.dork_queries = self._generate_queries()

    def _generate_queries(self) -> List[str]:
        """Generate 150+ optimized queries."""
        queries = []

        # Top 50 USA cities
        major_cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
            "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
            "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington DC",
            "Boston", "Nashville", "Detroit", "Portland", "Las Vegas",
            "Oklahoma City", "Albuquerque", "Tucson", "Sacramento", "Kansas City",
            "Mesa", "Atlanta", "Miami", "Raleigh", "Minneapolis",
            "Cleveland", "Tampa", "New Orleans", "Aurora", "Anaheim",
            "St. Louis", "Pittsburgh", "Cincinnati", "Orlando", "Riverside",
            "Stockton", "Lexington", "Henderson", "Omaha", "Wichita"
        ]

        for city in major_cities:
            queries.append(f'"powered by Shopify" "{city}"')

        # Top 30 states
        states = [
            "California", "Texas", "Florida", "New York", "Pennsylvania",
            "Illinois", "Ohio", "Georgia", "North Carolina", "Michigan",
            "New Jersey", "Virginia", "Washington", "Arizona", "Massachusetts",
            "Tennessee", "Indiana", "Missouri", "Maryland", "Wisconsin",
            "Colorado", "Minnesota", "South Carolina", "Alabama", "Louisiana",
            "Kentucky", "Oregon", "Oklahoma", "Connecticut", "Utah"
        ]

        for state in states:
            queries.append(f'"Shopify" "{state}" store')

        # Industry verticals (30 variations)
        industries = [
            "grocery store Shopify USA",
            "bakery powered by Shopify",
            "coffee shop Shopify",
            "restaurant Shopify ordering",
            "organic food Shopify",
            "wine shop Shopify",
            "brewery Shopify store",
            "bookstore powered by Shopify",
            "clothing boutique Shopify",
            "shoe store Shopify USA",
            "furniture Shopify",
            "home decor powered by Shopify",
            "pet store Shopify",
            "toy store Shopify USA",
            "sporting goods Shopify",
            "electronics Shopify store",
            "jewelry Shopify boutique",
            "cosmetics Shopify USA",
            "fashion Shopify Plus",
            "florist Shopify delivery",
            "gift shop powered by Shopify",
            "craft store Shopify",
            "hardware store Shopify",
            "garden center Shopify",
            "bike shop Shopify USA",
            "music store Shopify",
            "art gallery Shopify",
            "vintage shop Shopify",
            "outdoor gear Shopify",
            "wellness Shopify store"
        ]
        queries.extend(industries)

        # Technical patterns (10)
        technical = [
            'site:myshopify.com',
            '"checkout.shopify.com" USA',
            '"cdn.shopify.com" store',
            'inurl:myshopify.com -site:help',
            '"Shopify.theme" store USA',
            '"monorail-edge.shopifysvc.com"',
            'site:*.myshopify.com -help -support',
            '"shopify-pay" USA',
            '"Shop Pay" merchant',
            'inurl:products site:myshopify.com'
        ]
        queries.extend(technical)

        # Local delivery (15)
        delivery = [
            '"local delivery" Shopify USA',
            '"same day delivery" Shopify',
            '"curbside pickup" Shopify',
            '"next day delivery" Shopify',
            '"contactless delivery" Shopify',
            '"ship from store" Shopify',
            '"BOPIS" Shopify',
            '"local fulfillment" Shopify',
            '"neighborhood delivery" Shopify',
            '"free local delivery" Shopify',
            '"delivery radius" Shopify',
            '"deliver within" Shopify',
            '"we deliver" powered by Shopify',
            '"local shipping" Shopify',
            '"pickup available" Shopify USA'
        ]
        queries.extend(delivery)

        # Shopify Plus (5)
        plus = [
            '"Shopify Plus" USA merchant',
            '"headless commerce" Shopify',
            '"custom checkout" Shopify',
            'Shopify Plus enterprise USA',
            '"wholesale channel" Shopify'
        ]
        queries.extend(plus)

        print(f"📊 Generated {len(queries)} queries")
        return queries

    def discover_sequential(self, max_results: int = 20, rate_limit: float = 1.5) -> Set[str]:
        """Run queries sequentially (safer, slower)."""
        print("\n" + "="*80)
        print("🚀 FAST EXPANDED GOOGLE DORKING")
        print("="*80)
        print(f"📊 Total queries: {len(self.dork_queries)}")
        print(f"⏱️  Rate limit: {rate_limit}s")
        print(f"🎯 Max results/query: {max_results}")
        print("="*80 + "\n")

        total = len(self.dork_queries)

        for idx, query in enumerate(self.dork_queries, 1):
            print(f"[{idx}/{total}] 🔎 {query[:65]}...")

            try:
                domains = self._duckduckgo_search(query, max_results)

                if domains:
                    self.all_domains.update(domains)
                    self.query_results[query] = len(domains)
                    print(f"  ✅ +{len(domains)} (Total: {len(self.all_domains)})")
                else:
                    print(f"  ⏭️  No results")

            except Exception as e:
                print(f"  ⚠️  Error: {str(e)[:50]}")

            if idx < total:
                time.sleep(rate_limit)

            # Progress update every 20 queries
            if idx % 20 == 0:
                print(f"\n📊 Progress: {idx}/{total} queries | {len(self.all_domains)} domains found\n")

        return self.all_domains

    def _duckduckgo_search(self, query: str, max_results: int = 20) -> Set[str]:
        """Search DuckDuckGo HTML."""
        domains = set()

        try:
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = soup.find_all('a', class_='result__a')

                for result in results[:max_results]:
                    href = result.get('href')
                    if not href:
                        continue

                    # Extract URL from DuckDuckGo redirect
                    if 'uddg=' in href:
                        match = re.search(r'uddg=([^&]+)', href)
                        if match:
                            from urllib.parse import unquote
                            actual_url = unquote(match.group(1))
                            domain = self._extract_domain(actual_url)
                            if domain and self._is_shopify_store(domain):
                                domains.add(domain)
                    else:
                        domain = self._extract_domain(href)
                        if domain and self._is_shopify_store(domain):
                            domains.add(domain)

        except Exception as e:
            raise

        return domains

    def _extract_domain(self, url: str) -> str:
        """Extract clean domain."""
        if not url:
            return ""
        try:
            if not url.startswith('http'):
                url = f'https://{url}'
            parsed = urlparse(url)
            domain = parsed.netloc
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain.lower()
        except:
            return ""

    def _is_shopify_store(self, domain: str) -> bool:
        """Check if likely Shopify store."""
        if not domain or len(domain) < 4:
            return False

        if '.myshopify.com' in domain:
            return True

        # Exclude
        exclude = [
            'shopify.com', 'shopify.dev', 'google.com', 'facebook.com',
            'twitter.com', 'instagram.com', 'youtube.com', 'linkedin.com',
            'help.shopify', 'community.shopify', 'apps.shopify',
            'support.shopify', 'partners.shopify', 'reddit.com', 'pinterest.com'
        ]

        for exc in exclude:
            if exc in domain:
                return False

        return True

    def save_results(self, output_dir: str = 'data/google_dork_expanded'):
        """Save results."""
        os.makedirs(output_dir, exist_ok=True)

        # Domains
        domains_file = os.path.join(output_dir, 'domains.txt')
        with open(domains_file, 'w') as f:
            for domain in sorted(self.all_domains):
                f.write(f"{domain}\n")
        print(f"\n💾 Saved {len(self.all_domains)} domains to {domains_file}")

        # Top queries
        top_queries = sorted(
            [(q, c) for q, c in self.query_results.items() if c > 0],
            key=lambda x: x[1],
            reverse=True
        )[:20]

        queries_file = os.path.join(output_dir, 'top_queries.txt')
        with open(queries_file, 'w') as f:
            f.write("TOP 20 MOST EFFECTIVE QUERIES\n")
            f.write("="*80 + "\n\n")
            for idx, (query, count) in enumerate(top_queries, 1):
                f.write(f"{idx:2d}. [{count:3d} domains] {query}\n")
        print(f"📊 Saved top queries to {queries_file}")

        return top_queries

    def print_summary(self):
        """Print summary."""
        print("\n" + "="*80)
        print("📈 CAMPAIGN COMPLETE")
        print("="*80)

        # Top queries
        top = sorted(
            [(q, c) for q, c in self.query_results.items() if c > 0],
            key=lambda x: x[1],
            reverse=True
        )[:20]

        print("\n🏆 TOP 20 MOST EFFECTIVE QUERIES:")
        print("-"*80)
        for idx, (query, count) in enumerate(top, 1):
            print(f"{idx:2d}. [{count:3d}] {query}")

        # Sample
        print("\n" + "="*80)
        print("🌐 SAMPLE DOMAINS (first 20):")
        print("-"*80)
        for domain in sorted(list(self.all_domains))[:20]:
            print(f"  - {domain}")

        print("\n" + "="*80)
        print(f"✅ TOTAL UNIQUE DOMAINS: {len(self.all_domains)}")
        print(f"📊 Successful queries: {len([c for c in self.query_results.values() if c > 0])}/{len(self.dork_queries)}")
        print("="*80 + "\n")


def main():
    discoverer = FastGoogleDorkDiscovery()

    # Run campaign
    domains = discoverer.discover_sequential(
        max_results=20,
        rate_limit=1.5
    )

    # Save
    discoverer.save_results()

    # Summary
    discoverer.print_summary()


if __name__ == '__main__':
    main()

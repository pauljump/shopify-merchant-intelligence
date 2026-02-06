"""
EXPANDED Google Dorking Campaign - 100+ Queries

Targets:
- 50+ major USA cities
- Industry verticals (food, retail, fashion, electronics, etc.)
- Shopify-specific technical patterns
- State names + Shopify
- Local delivery keywords

Uses DuckDuckGo HTML scraping (no API key needed).
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from typing import Set, Dict, List, Tuple
from urllib.parse import quote_plus, urlparse
from collections import defaultdict
import os


class ExpandedGoogleDorkDiscovery:
    """Expanded Google dorking with 100+ targeted queries."""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        # Track query effectiveness
        self.query_results: Dict[str, int] = defaultdict(int)

        # Generate 100+ queries
        self.dork_queries = self._generate_queries()

    def _generate_queries(self) -> List[str]:
        """Generate 100+ targeted Google dork queries."""
        queries = []

        # ===== 1. MAJOR USA CITIES (50+) =====
        major_cities = [
            # Top 25 by population
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
            "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
            "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington DC",
            "Boston", "Nashville", "Detroit", "Portland", "Las Vegas",

            # Additional major metros
            "Oklahoma City", "Albuquerque", "Tucson", "Fresno", "Sacramento",
            "Kansas City", "Mesa", "Atlanta", "Miami", "Raleigh",
            "Omaha", "Minneapolis", "Cleveland", "Wichita", "Arlington",
            "Tampa", "New Orleans", "Bakersfield", "Aurora", "Anaheim",
            "St. Louis", "Pittsburgh", "Cincinnati", "Orlando", "Tampa",
            "Riverside", "Stockton", "Corpus Christi", "Lexington", "Henderson"
        ]

        for city in major_cities:
            queries.append(f'"powered by Shopify" "{city}"')

        # ===== 2. USA STATES + SHOPIFY =====
        states = [
            "California", "Texas", "Florida", "New York", "Pennsylvania",
            "Illinois", "Ohio", "Georgia", "North Carolina", "Michigan",
            "New Jersey", "Virginia", "Washington", "Arizona", "Massachusetts",
            "Tennessee", "Indiana", "Missouri", "Maryland", "Wisconsin",
            "Colorado", "Minnesota", "South Carolina", "Alabama", "Louisiana",
            "Kentucky", "Oregon", "Oklahoma", "Connecticut", "Utah"
        ]

        for state in states:
            queries.append(f'"Shopify" store "{state}"')

        # ===== 3. INDUSTRY VERTICALS + SHOPIFY =====
        industries = [
            # Food & Beverage
            ("grocery", "local delivery"),
            ("bakery", "USA"),
            ("coffee shop", "Shopify"),
            ("restaurant", "online ordering"),
            ("farm fresh", "Shopify"),
            ("organic food", "powered by Shopify"),
            ("butcher", "Shopify"),
            ("wine shop", "Shopify store"),
            ("brewery", "Shopify"),
            ("juice bar", "Shopify"),

            # Retail
            ("bookstore", "powered by Shopify"),
            ("clothing store", "Shopify USA"),
            ("shoe store", "Shopify"),
            ("furniture store", "Shopify"),
            ("home decor", "powered by Shopify"),
            ("pet store", "Shopify"),
            ("toy store", "Shopify"),
            ("sporting goods", "Shopify"),
            ("electronics store", "Shopify"),
            ("hardware store", "Shopify"),

            # Fashion & Beauty
            ("boutique", "powered by Shopify"),
            ("jewelry store", "Shopify"),
            ("cosmetics", "Shopify USA"),
            ("salon products", "Shopify"),
            ("fashion brand", "Shopify Plus"),

            # Specialty
            ("florist", "Shopify delivery"),
            ("gift shop", "powered by Shopify"),
            ("art gallery", "Shopify"),
            ("craft store", "Shopify"),
            ("comic book store", "Shopify"),
        ]

        for industry, keyword in industries:
            queries.append(f'"{industry}" "{keyword}"')

        # ===== 4. SHOPIFY TECHNICAL PATTERNS =====
        technical_patterns = [
            'site:myshopify.com',
            '"checkout.shopify.com" USA',
            '"cdn.shopify.com" store',
            'inurl:myshopify.com',
            '"Shopify.theme" USA',
            '"monorail-edge.shopifysvc.com"',
            'site:*.myshopify.com -site:help.shopify.com',
        ]
        queries.extend(technical_patterns)

        # ===== 5. LOCAL DELIVERY KEYWORDS =====
        delivery_keywords = [
            '"local delivery" "powered by Shopify" USA',
            '"same day delivery" Shopify store',
            '"curbside pickup" "Shopify"',
            '"next day delivery" "powered by Shopify"',
            '"contactless delivery" Shopify',
            '"ship from store" Shopify',
            '"buy online pickup in store" Shopify',
            '"BOPIS" "powered by Shopify"',
            '"local fulfillment" Shopify',
            '"neighborhood delivery" Shopify',
        ]
        queries.extend(delivery_keywords)

        # ===== 6. SHOPIFY PLUS SPECIFIC =====
        plus_queries = [
            '"Shopify Plus" merchant USA',
            '"Shopify Plus" store America',
            '"headless commerce" Shopify USA',
            '"custom checkout" Shopify store',
            'Shopify Plus "enterprise"',
            '"Shopify Scripts" store',
            '"wholesale channel" Shopify',
        ]
        queries.extend(plus_queries)

        # ===== 7. CITY + INDUSTRY COMBOS =====
        top_cities_industries = [
            ("New York", "grocery"),
            ("Los Angeles", "fashion"),
            ("Chicago", "restaurant"),
            ("San Francisco", "specialty food"),
            ("Austin", "boutique"),
            ("Seattle", "coffee"),
            ("Portland", "craft"),
            ("Miami", "lifestyle"),
            ("Denver", "outdoor gear"),
            ("Boston", "bookstore"),
        ]

        for city, industry in top_cities_industries:
            queries.append(f'"{industry}" Shopify "{city}"')

        print(f"📊 Generated {len(queries)} unique queries")
        return queries

    def discover_via_duckduckgo(self, max_results_per_query: int = 30, rate_limit: int = 2) -> Set[str]:
        """
        Run expanded dorking campaign via DuckDuckGo.

        Args:
            max_results_per_query: Max results per search query
            rate_limit: Seconds to wait between queries

        Returns:
            Set of discovered domains
        """
        print("\n" + "="*80)
        print("🚀 EXPANDED GOOGLE DORKING CAMPAIGN")
        print("="*80)
        print(f"📊 Total queries: {len(self.dork_queries)}")
        print(f"⏱️  Rate limit: {rate_limit}s between queries")
        print(f"🎯 Max results per query: {max_results_per_query}")
        print("="*80 + "\n")

        all_domains = set()
        total_queries = len(self.dork_queries)

        for idx, query in enumerate(self.dork_queries, 1):
            progress = f"[{idx}/{total_queries}]"
            print(f"{progress} 🔎 {query[:60]}...")

            try:
                domains = self._duckduckgo_search(query, max_results=max_results_per_query)

                if domains:
                    all_domains.update(domains)
                    self.query_results[query] = len(domains)
                    print(f"  ✅ Found {len(domains)} domains (Total: {len(all_domains)})")
                else:
                    print(f"  ⏭️  No results")

            except Exception as e:
                print(f"  ⚠️  Error: {e}")

            # Rate limiting
            if idx < total_queries:
                time.sleep(rate_limit)

        print("\n" + "="*80)
        print("🎯 DORKING CAMPAIGN COMPLETE!")
        print("="*80)
        print(f"🌐 Total unique domains discovered: {len(all_domains)}")
        print(f"📊 Queries that found results: {len([v for v in self.query_results.values() if v > 0])}/{total_queries}")
        print("="*80 + "\n")

        return all_domains

    def _duckduckgo_search(self, query: str, max_results: int = 30) -> Set[str]:
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
            'help.shopify', 'community.shopify', 'apps.shopify',
            'support.shopify', 'partners.shopify', 'developers.shopify',
            'reddit.com', 'pinterest.com', 'amazon.com', 'ebay.com'
        ]

        for exc in exclude:
            if exc in domain:
                return False

        return True

    def save_results(self, domains: Set[str], output_dir: str = 'data/google_dork_expanded'):
        """Save discovered domains and analysis."""
        os.makedirs(output_dir, exist_ok=True)

        # Save domains
        domains_file = os.path.join(output_dir, 'domains.txt')
        with open(domains_file, 'w') as f:
            for domain in sorted(domains):
                f.write(f"{domain}\n")

        print(f"💾 Saved {len(domains)} domains to {domains_file}")

        # Save top queries
        top_queries = sorted(
            [(query, count) for query, count in self.query_results.items() if count > 0],
            key=lambda x: x[1],
            reverse=True
        )[:20]

        queries_file = os.path.join(output_dir, 'top_queries.txt')
        with open(queries_file, 'w') as f:
            f.write("TOP 20 MOST EFFECTIVE QUERIES\n")
            f.write("="*80 + "\n\n")
            for idx, (query, count) in enumerate(top_queries, 1):
                f.write(f"{idx}. [{count} domains] {query}\n")

        print(f"📊 Saved top queries to {queries_file}")

    def print_summary(self, domains: Set[str]):
        """Print campaign summary."""
        print("\n" + "="*80)
        print("📈 CAMPAIGN SUMMARY")
        print("="*80)

        # Top queries
        print("\n🏆 TOP 20 MOST EFFECTIVE QUERIES:")
        print("-"*80)
        top_queries = sorted(
            [(query, count) for query, count in self.query_results.items() if count > 0],
            key=lambda x: x[1],
            reverse=True
        )[:20]

        for idx, (query, count) in enumerate(top_queries, 1):
            print(f"{idx:2d}. [{count:3d} domains] {query}")

        # Sample domains
        print("\n" + "="*80)
        print("🌐 SAMPLE DISCOVERED DOMAINS (20 random):")
        print("-"*80)
        sample = sorted(list(domains))[:20]
        for domain in sample:
            print(f"  - {domain}")

        print("\n" + "="*80)
        print(f"✅ TOTAL UNIQUE DOMAINS: {len(domains)}")
        print("="*80 + "\n")


def main():
    """Run expanded dorking campaign."""
    discoverer = ExpandedGoogleDorkDiscovery()

    # Run campaign
    domains = discoverer.discover_via_duckduckgo(
        max_results_per_query=30,
        rate_limit=2  # 2 seconds between queries
    )

    # Save results
    discoverer.save_results(domains)

    # Print summary
    discoverer.print_summary(domains)


if __name__ == '__main__':
    main()

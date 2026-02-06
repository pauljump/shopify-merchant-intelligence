"""
Run Google Dork Campaign via Bing Search

Bing is more lenient than DuckDuckGo for automated searches.
Uses HTML scraping (no API key needed).
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import quote_plus, urlparse
import os
from typing import Set, Dict
from collections import defaultdict


class BingDorkCampaign:
    """Run dork campaign via Bing."""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        self.all_domains = set()
        self.query_results = defaultdict(int)

    def load_queries(self, file_path='data/google_dork_expanded/all_queries.txt'):
        """Load queries from file."""
        queries = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip headers and empty lines
                    if line and not line.startswith('=') and not line.startswith('Total') and not line.startswith('USE WITH'):
                        # Extract query (remove numbering if present)
                        match = re.match(r'^\d+\.\s*(.+)$', line)
                        if match:
                            queries.append(match.group(1))
        except FileNotFoundError:
            print(f"⚠️  File not found: {file_path}")
            return []

        return queries

    def search_bing(self, query: str, max_results: int = 15) -> Set[str]:
        """Search Bing and extract domains."""
        domains = set()

        try:
            # Bing search URL
            url = f"https://www.bing.com/search?q={quote_plus(query)}&count=50"

            response = requests.get(url, headers=self.headers, timeout=15)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract search results from Bing's HTML
                # Bing uses <li class="b_algo"> for results
                results = soup.find_all('li', class_='b_algo')

                for result in results[:max_results]:
                    # Find the link
                    link = result.find('a')
                    if link and link.get('href'):
                        url = link.get('href')
                        domain = self._extract_domain(url)

                        if domain and self._is_shopify_store(domain):
                            domains.add(domain)

        except Exception as e:
            raise Exception(f"Bing search failed: {str(e)[:50]}")

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

        # Exclude non-store domains
        exclude = [
            'shopify.com', 'shopify.dev', 'google.com', 'facebook.com',
            'twitter.com', 'instagram.com', 'youtube.com', 'linkedin.com',
            'help.shopify', 'community.shopify', 'apps.shopify',
            'support.shopify', 'partners.shopify', 'reddit.com', 'pinterest.com',
            'bing.com', 'microsoft.com'
        ]

        return not any(exc in domain for exc in exclude)

    def run_campaign(self, queries, rate_limit: float = 2.0, max_queries: int = 100):
        """Run campaign."""
        print("="*80)
        print("🔎 BING DORK CAMPAIGN")
        print("="*80)
        print(f"📊 Total queries loaded: {len(queries)}")
        print(f"🎯 Max queries to run: {max_queries}")
        print(f"⏱️  Rate limit: {rate_limit}s")
        print("="*80 + "\n")

        # Limit to max_queries
        queries = queries[:max_queries]
        total = len(queries)

        for idx, query in enumerate(queries, 1):
            print(f"[{idx}/{total}] {query[:60]:<60} ", end="", flush=True)

            try:
                domains = self.search_bing(query)

                if domains:
                    new_domains = domains - self.all_domains
                    self.all_domains.update(domains)
                    self.query_results[query] = len(domains)
                    print(f"✅ +{len(new_domains):2d} | Total: {len(self.all_domains)}")
                else:
                    print("⏭️")

            except Exception as e:
                print(f"⚠️  {str(e)[:30]}")

            # Progress update
            if idx % 20 == 0:
                print(f"\n📊 Progress: {idx}/{total} queries | {len(self.all_domains)} unique domains\n")

            # Rate limiting
            if idx < total:
                time.sleep(rate_limit)

        return self.all_domains

    def save_results(self, output_dir='data/google_dork_expanded'):
        """Save results."""
        os.makedirs(output_dir, exist_ok=True)

        # Save domains
        domains_file = os.path.join(output_dir, 'domains.txt')
        with open(domains_file, 'w') as f:
            for domain in sorted(self.all_domains):
                f.write(f"{domain}\n")

        print(f"\n💾 Saved {len(self.all_domains)} domains to {domains_file}")

        # Save top queries
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

        print(f"📊 Saved top 20 queries to {queries_file}")

        return top_queries

    def print_summary(self):
        """Print summary."""
        print("\n" + "="*80)
        print("📈 CAMPAIGN COMPLETE")
        print("="*80)

        print(f"\n✅ Total unique domains discovered: {len(self.all_domains)}")
        print(f"📊 Successful queries: {len([c for c in self.query_results.values() if c > 0])}")

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

        # Sample domains
        print("\n🌐 SAMPLE DISCOVERED DOMAINS (first 20):")
        print("-"*80)
        for domain in sorted(self.all_domains)[:20]:
            print(f"  - {domain}")

        print("\n" + "="*80)


def main():
    campaign = BingDorkCampaign()

    # Load queries
    queries = campaign.load_queries()

    if not queries:
        print("⚠️  No queries loaded. Run generate_dork_queries.py first.")
        return

    # Run campaign (limit to 100 queries for now)
    campaign.run_campaign(queries, rate_limit=2.0, max_queries=100)

    # Save results
    campaign.save_results()

    # Print summary
    campaign.print_summary()


if __name__ == '__main__':
    main()

"""
Quick Batch Dorking - 120 High-Value Queries

Runs faster by focusing on highest-value queries.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from typing import Set, Dict
from urllib.parse import quote_plus, urlparse
from collections import defaultdict
import os


class QuickDorkBatch:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.query_results = defaultdict(int)
        self.all_domains = set()

    def generate_high_value_queries(self):
        """120 highest-value queries."""
        queries = []

        # Top 40 USA cities (proven effective)
        cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Diego", "Dallas", "San Jose", "Austin",
            "San Francisco", "Seattle", "Denver", "Boston", "Portland",
            "Miami", "Atlanta", "Nashville", "Las Vegas", "Minneapolis",
            "Tampa", "Orlando", "Sacramento", "Kansas City", "Raleigh",
            "Detroit", "Charlotte", "Indianapolis", "Columbus", "Pittsburgh",
            "Cincinnati", "Cleveland", "St. Louis", "Milwaukee", "Baltimore",
            "Tucson", "Albuquerque", "Mesa", "Fresno", "Oklahoma City"
        ]

        for city in cities:
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
            queries.append(f'Shopify "{state}"')

        # Top 25 industries
        industries = [
            "grocery Shopify USA", "bakery Shopify", "coffee Shopify",
            "restaurant Shopify", "wine Shopify", "brewery Shopify",
            "bookstore Shopify", "boutique Shopify", "jewelry Shopify",
            "furniture Shopify", "pet store Shopify", "toy store Shopify",
            "electronics Shopify", "cosmetics Shopify", "florist Shopify",
            "gift shop Shopify", "hardware Shopify", "bike shop Shopify",
            "sporting goods Shopify", "home decor Shopify",
            "fashion Shopify", "art gallery Shopify", "wellness Shopify",
            "outdoor gear Shopify", "music store Shopify"
        ]
        queries.extend(industries)

        # Technical + delivery (15)
        special = [
            'site:myshopify.com',
            '"checkout.shopify.com" USA',
            '"local delivery" Shopify',
            '"same day delivery" Shopify',
            '"curbside pickup" Shopify',
            '"BOPIS" Shopify',
            '"Shopify Plus" USA',
            '"headless commerce" Shopify',
            '"Shop Pay" USA',
            'inurl:myshopify.com -help',
            '"free delivery" Shopify',
            '"neighborhood delivery" Shopify',
            '"contactless delivery" Shopify',
            '"ship from store" Shopify',
            '"wholesale" Shopify Plus'
        ]
        queries.extend(special)

        # Top city + industry combos (10)
        combos = [
            '"grocery" Shopify "New York"',
            '"fashion" Shopify "Los Angeles"',
            '"restaurant" Shopify "Chicago"',
            '"coffee" Shopify "Seattle"',
            '"boutique" Shopify "Austin"',
            '"wine" Shopify "San Francisco"',
            '"brewery" Shopify "Portland"',
            '"bookstore" Shopify "Boston"',
            '"jewelry" Shopify "Miami"',
            '"art" Shopify "Denver"'
        ]
        queries.extend(combos)

        return queries

    def run(self):
        """Run batch."""
        queries = self.generate_high_value_queries()

        print("="*80)
        print(f"🚀 QUICK BATCH DORKING - {len(queries)} QUERIES")
        print("="*80 + "\n")

        for idx, query in enumerate(queries, 1):
            print(f"[{idx}/{len(queries)}] {query[:60]}...", end=" ")

            try:
                domains = self._search(query)
                if domains:
                    self.all_domains.update(domains)
                    self.query_results[query] = len(domains)
                    print(f"✅ +{len(domains)} (Total: {len(self.all_domains)})")
                else:
                    print("⏭️")
            except Exception as e:
                print(f"⚠️  {str(e)[:30]}")

            if idx % 20 == 0:
                print(f"\n📊 Progress: {len(self.all_domains)} domains\n")

            time.sleep(1.2)

        return self.all_domains

    def _search(self, query):
        """DuckDuckGo search."""
        domains = set()
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

        resp = requests.get(url, headers=self.headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            for result in soup.find_all('a', class_='result__a')[:15]:
                href = result.get('href', '')

                if 'uddg=' in href:
                    match = re.search(r'uddg=([^&]+)', href)
                    if match:
                        from urllib.parse import unquote
                        url = unquote(match.group(1))
                        domain = self._extract_domain(url)
                        if domain and self._is_shopify(domain):
                            domains.add(domain)
        return domains

    def _extract_domain(self, url):
        """Extract domain."""
        try:
            if not url.startswith('http'):
                url = f'https://{url}'
            domain = urlparse(url).netloc
            return domain.lstrip('www.').lower()
        except:
            return ""

    def _is_shopify(self, domain):
        """Check Shopify."""
        if not domain or len(domain) < 4:
            return False
        if '.myshopify.com' in domain:
            return True

        exclude = ['shopify.com', 'google.com', 'facebook.com', 'twitter.com',
                   'instagram.com', 'youtube.com', 'linkedin.com', 'help.shopify',
                   'apps.shopify', 'reddit.com', 'pinterest.com']

        return not any(ex in domain for ex in exclude)

    def save(self):
        """Save results."""
        os.makedirs('data/google_dork_expanded', exist_ok=True)

        # Domains
        with open('data/google_dork_expanded/domains.txt', 'w') as f:
            for d in sorted(self.all_domains):
                f.write(f"{d}\n")

        # Top queries
        top = sorted([(q, c) for q, c in self.query_results.items() if c > 0],
                    key=lambda x: x[1], reverse=True)[:20]

        with open('data/google_dork_expanded/top_queries.txt', 'w') as f:
            f.write("TOP 20 QUERIES\n" + "="*80 + "\n\n")
            for idx, (q, c) in enumerate(top, 1):
                f.write(f"{idx:2d}. [{c:3d}] {q}\n")

        print(f"\n💾 Saved to data/google_dork_expanded/")
        print(f"   - domains.txt ({len(self.all_domains)} domains)")
        print(f"   - top_queries.txt (top 20)\n")

        return top

    def print_summary(self, top_queries):
        """Print summary."""
        print("="*80)
        print("📈 SUMMARY")
        print("="*80)
        print(f"\n✅ Total domains: {len(self.all_domains)}")
        print(f"📊 Successful queries: {len([c for c in self.query_results.values() if c > 0])}")

        print("\n🏆 TOP 20 QUERIES:")
        for idx, (q, c) in enumerate(top_queries, 1):
            print(f"{idx:2d}. [{c:3d}] {q}")

        print("\n🌐 SAMPLE DOMAINS (20):")
        for d in sorted(self.all_domains)[:20]:
            print(f"  - {d}")

        print("\n" + "="*80)


if __name__ == '__main__':
    dork = QuickDorkBatch()
    dork.run()
    top = dork.save()
    dork.print_summary(top)

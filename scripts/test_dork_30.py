"""Test dorking with 30 high-value queries."""

import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import quote_plus, urlparse
import os


def search_duckduckgo(query, headers):
    """Search DuckDuckGo."""
    domains = set()
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            for result in soup.find_all('a', class_='result__a')[:15]:
                href = result.get('href', '')

                if 'uddg=' in href:
                    match = re.search(r'uddg=([^&]+)', href)
                    if match:
                        from urllib.parse import unquote
                        actual_url = unquote(match.group(1))

                        try:
                            if not actual_url.startswith('http'):
                                actual_url = f'https://{actual_url}'
                            domain = urlparse(actual_url).netloc.lstrip('www.').lower()

                            # Check if Shopify
                            if domain and len(domain) >= 4:
                                is_shopify = '.myshopify.com' in domain
                                exclude = ['shopify.com', 'google.com', 'facebook.com',
                                          'help.shopify', 'apps.shopify']
                                is_excluded = any(ex in domain for ex in exclude)

                                if is_shopify or (not is_excluded and domain):
                                    domains.add(domain)
                        except:
                            pass
    except Exception as e:
        print(f"Error: {e}")

    return domains


def main():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

    # 30 highest-value queries
    queries = [
        # Top 10 cities
        '"powered by Shopify" "New York"',
        '"powered by Shopify" "Los Angeles"',
        '"powered by Shopify" "Chicago"',
        '"powered by Shopify" "San Francisco"',
        '"powered by Shopify" "Austin"',
        '"powered by Shopify" "Seattle"',
        '"powered by Shopify" "Boston"',
        '"powered by Shopify" "Portland"',
        '"powered by Shopify" "Miami"',
        '"powered by Shopify" "Denver"',

        # Top 5 states
        'Shopify "California" store',
        'Shopify "Texas" store',
        'Shopify "Florida" store',
        'Shopify "New York" store',
        'Shopify "Washington" store',

        # Industries
        'grocery Shopify USA',
        'restaurant Shopify delivery',
        'bakery Shopify',
        'coffee shop Shopify',
        'boutique Shopify USA',

        # Technical
        'site:myshopify.com',
        '"checkout.shopify.com" USA',
        'inurl:myshopify.com -help',

        # Delivery
        '"local delivery" Shopify',
        '"same day delivery" Shopify',
        '"curbside pickup" Shopify',

        # Plus
        '"Shopify Plus" USA',
        '"headless commerce" Shopify',
        '"Shop Pay" merchant USA',
        '"wholesale" Shopify Plus'
    ]

    print("="*80)
    print(f"🧪 TEST DORKING - {len(queries)} QUERIES")
    print("="*80 + "\n")

    all_domains = set()
    query_results = {}

    for idx, query in enumerate(queries, 1):
        print(f"[{idx}/{len(queries)}] {query[:55]:<55} ", end="", flush=True)

        domains = search_duckduckgo(query, headers)
        if domains:
            all_domains.update(domains)
            query_results[query] = len(domains)
            print(f"✅ +{len(domains):2d} | Total: {len(all_domains)}")
        else:
            print("⏭️")

        time.sleep(1)

    # Save
    os.makedirs('data/google_dork_expanded', exist_ok=True)
    with open('data/google_dork_expanded/domains.txt', 'w') as f:
        for d in sorted(all_domains):
            f.write(f"{d}\n")

    # Top queries
    top = sorted([(q, c) for q, c in query_results.items()], key=lambda x: x[1], reverse=True)[:10]

    print("\n" + "="*80)
    print("📈 RESULTS")
    print("="*80)
    print(f"✅ Total domains: {len(all_domains)}\n")

    print("🏆 TOP 10 QUERIES:")
    for idx, (q, c) in enumerate(top, 1):
        print(f"{idx:2d}. [{c:2d}] {q}")

    print("\n🌐 SAMPLE DOMAINS:")
    for d in sorted(all_domains)[:15]:
        print(f"  - {d}")

    print(f"\n💾 Saved to data/google_dork_expanded/domains.txt")


if __name__ == '__main__':
    main()

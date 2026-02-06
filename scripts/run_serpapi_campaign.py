"""
Run Google Dork Campaign via SerpAPI

Requires SerpAPI key (free tier: 100 searches/month)
Get key at: https://serpapi.com/manage-api-key
"""

import os
import sys
import time
import re
from typing import Set, Dict, List, Tuple
from collections import defaultdict
from urllib.parse import urlparse


def load_queries(file_path='data/google_dork_expanded/all_queries.txt', max_queries=100):
    """Load queries from file."""
    queries = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip headers
                if line and not line.startswith('=') and not line.startswith('Total') and not line.startswith('USE WITH'):
                    match = re.match(r'^\d+\.\s*(.+)$', line)
                    if match:
                        queries.append(match.group(1))
                        if len(queries) >= max_queries:
                            break
    except FileNotFoundError:
        print(f"⚠️  File not found: {file_path}")
        print("   Run: python scripts/generate_dork_queries.py")
        return []

    return queries


def search_with_serpapi(query: str, api_key: str) -> Set[str]:
    """Search using SerpAPI."""
    try:
        from serpapi import GoogleSearch
    except ImportError:
        print("\n⚠️  SerpAPI library not installed.")
        print("Install with: pip install google-search-results")
        sys.exit(1)

    domains = set()

    try:
        params = {
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "num": 20  # Max results per query
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        # Extract organic results
        if "organic_results" in results:
            for result in results["organic_results"]:
                if "link" in result:
                    domain = extract_domain(result["link"])
                    if domain and is_shopify_store(domain):
                        domains.add(domain)

    except Exception as e:
        raise Exception(f"SerpAPI error: {str(e)[:50]}")

    return domains


def extract_domain(url: str) -> str:
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


def is_shopify_store(domain: str) -> bool:
    """Check if likely Shopify store."""
    if not domain or len(domain) < 4:
        return False

    if '.myshopify.com' in domain:
        return True

    exclude = [
        'shopify.com', 'shopify.dev', 'google.com', 'facebook.com',
        'twitter.com', 'instagram.com', 'youtube.com', 'linkedin.com',
        'help.shopify', 'community.shopify', 'apps.shopify',
        'support.shopify', 'partners.shopify', 'reddit.com', 'pinterest.com'
    ]

    return not any(exc in domain for exc in exclude)


def run_campaign(api_key: str, max_queries: int = 100):
    """Run SerpAPI campaign."""
    print("="*80)
    print("🔎 SERPAPI GOOGLE DORK CAMPAIGN")
    print("="*80)

    # Load queries
    queries = load_queries(max_queries=max_queries)

    if not queries:
        return set(), {}

    print(f"📊 Loaded {len(queries)} queries")
    print(f"⏱️  Starting campaign...")
    print("="*80 + "\n")

    all_domains = set()
    query_results = defaultdict(int)

    for idx, query in enumerate(queries, 1):
        print(f"[{idx}/{len(queries)}] {query[:60]:<60} ", end="", flush=True)

        try:
            domains = search_with_serpapi(query, api_key)

            if domains:
                new_domains = domains - all_domains
                all_domains.update(domains)
                query_results[query] = len(domains)
                print(f"✅ +{len(new_domains):2d} | Total: {len(all_domains)}")
            else:
                print("⏭️")

        except Exception as e:
            print(f"⚠️  {str(e)[:30]}")

        # Progress
        if idx % 20 == 0:
            print(f"\n📊 Progress: {idx}/{len(queries)} | {len(all_domains)} unique domains\n")

        # Rate limiting (be respectful)
        time.sleep(0.5)

    return all_domains, query_results


def save_results(domains: Set[str], query_results: Dict[str, int]):
    """Save results."""
    output_dir = 'data/google_dork_expanded'
    os.makedirs(output_dir, exist_ok=True)

    # Save domains
    domains_file = os.path.join(output_dir, 'domains.txt')
    with open(domains_file, 'w') as f:
        for domain in sorted(domains):
            f.write(f"{domain}\n")

    print(f"\n💾 Saved {len(domains)} domains to {domains_file}")

    # Save top queries
    top_queries = sorted(
        [(q, c) for q, c in query_results.items() if c > 0],
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


def print_summary(domains: Set[str], query_results: Dict[str, int]):
    """Print summary."""
    print("\n" + "="*80)
    print("📈 CAMPAIGN COMPLETE")
    print("="*80)

    print(f"\n✅ Total unique domains: {len(domains)}")
    print(f"📊 Successful queries: {len([c for c in query_results.values() if c > 0])}")

    # Top queries
    top = sorted(
        [(q, c) for q, c in query_results.items() if c > 0],
        key=lambda x: x[1],
        reverse=True
    )[:20]

    print("\n🏆 TOP 20 MOST EFFECTIVE QUERIES:")
    print("-"*80)
    for idx, (query, count) in enumerate(top, 1):
        print(f"{idx:2d}. [{count:3d}] {query}")

    # Sample
    print("\n🌐 SAMPLE DOMAINS (first 20):")
    print("-"*80)
    for domain in sorted(domains)[:20]:
        print(f"  - {domain}")

    print("\n" + "="*80)


def main():
    """Main execution."""
    # Check for API key
    api_key = os.environ.get('SERPAPI_KEY')

    if not api_key:
        print("="*80)
        print("⚠️  SERPAPI_KEY not found")
        print("="*80)
        print("\nOptions:")
        print("1. Set environment variable:")
        print("   export SERPAPI_KEY='your-api-key-here'")
        print("\n2. Or pass as argument:")
        print("   python scripts/run_serpapi_campaign.py YOUR_API_KEY")
        print("\n3. Get free API key at:")
        print("   https://serpapi.com/manage-api-key")
        print("   (100 free searches/month)")
        print("="*80)

        if len(sys.argv) > 1:
            api_key = sys.argv[1]
            print(f"\n✅ Using API key from argument")
        else:
            sys.exit(1)

    # Run campaign
    domains, query_results = run_campaign(api_key, max_queries=100)

    if domains:
        # Save results
        save_results(domains, query_results)

        # Print summary
        print_summary(domains, query_results)
    else:
        print("\n⚠️  No domains discovered. Check API key and query file.")


if __name__ == '__main__':
    main()

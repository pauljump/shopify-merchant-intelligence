#!/usr/bin/env python3
"""
Social Media Scraper for Shopify Store Discovery
Mines Reddit, Product Hunt, Hacker News, and other platforms for Shopify store mentions
"""

import re
import requests
from bs4 import BeautifulSoup
from typing import List, Set, Dict, Tuple
import time
from urllib.parse import urlparse, urljoin
import json
from pathlib import Path


class SocialMediaScraper:
    """Scrapes social media platforms for Shopify store mentions"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self.domains = set()
        self.source_breakdown = {
            'reddit': set(),
            'product_hunt': set(),
            'hacker_news': set(),
            'twitter': set()
        }

    def scrape_all_sources(self, max_per_source: int = 100) -> Dict[str, Set[str]]:
        """Scrape all social media sources for Shopify store mentions"""
        print("🔍 Starting social media scraping...")

        # Reddit
        print("\n📱 Scraping Reddit...")
        self.scrape_reddit(max_results=max_per_source)

        # Product Hunt
        print("\n🚀 Scraping Product Hunt...")
        self.scrape_product_hunt(max_results=max_per_source)

        # Hacker News
        print("\n📰 Scraping Hacker News...")
        self.scrape_hacker_news(max_results=max_per_source)

        # Twitter/X (limited without API)
        print("\n🐦 Scraping Twitter mentions...")
        self.scrape_twitter_mentions(max_results=max_per_source)

        return self.source_breakdown

    def scrape_reddit(self, max_results: int = 100) -> Set[str]:
        """Scrape Reddit for Shopify store mentions using old.reddit.com"""
        subreddits = ['shopify', 'ecommerce', 'entrepreneur', 'smallbusiness']
        search_queries = [
            'powered by shopify',
            'my shopify store',
            'shopify store launch',
            'check out my store',
            '.myshopify.com'
        ]

        for subreddit in subreddits:
            print(f"  Searching r/{subreddit}...")

            # Try search within subreddit
            for query in search_queries:
                try:
                    url = f"https://old.reddit.com/r/{subreddit}/search?q={query.replace(' ', '+')}&restrict_sr=on&sort=new"
                    domains = self._extract_domains_from_reddit_page(url)
                    self.source_breakdown['reddit'].update(domains)
                    print(f"    Found {len(domains)} domains for query: {query}")
                    time.sleep(2)  # Be respectful with rate limiting
                except Exception as e:
                    print(f"    Error with query '{query}': {e}")
                    continue

        # Also try general Reddit search
        print("  Searching all of Reddit...")
        try:
            url = "https://old.reddit.com/search?q=site%3Amyshopify.com+OR+%22powered+by+shopify%22&sort=new"
            domains = self._extract_domains_from_reddit_page(url)
            self.source_breakdown['reddit'].update(domains)
            print(f"    Found {len(domains)} domains from general search")
        except Exception as e:
            print(f"    Error with general search: {e}")

        return self.source_breakdown['reddit']

    def _extract_domains_from_reddit_page(self, url: str) -> Set[str]:
        """Extract domains from a Reddit search results page"""
        domains = set()

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all links in post content and comments
            all_links = soup.find_all('a')

            for link in all_links:
                href = link.get('href', '')
                # Extract domain from URL
                domain = self._extract_shopify_domain(href)
                if domain:
                    domains.add(domain)

                # Also check link text for URLs
                text = link.get_text()
                domain = self._extract_shopify_domain(text)
                if domain:
                    domains.add(domain)

            # Also search raw text for URLs that might not be linked
            text_content = soup.get_text()
            domains.update(self._extract_domains_from_text(text_content))

        except Exception as e:
            print(f"    Error extracting from {url}: {e}")

        return domains

    def scrape_product_hunt(self, max_results: int = 100) -> Set[str]:
        """Scrape Product Hunt for Shopify-related products"""
        search_queries = ['shopify', 'ecommerce', 'online store']

        for query in search_queries:
            try:
                print(f"  Searching for: {query}")
                url = f"https://www.producthunt.com/search?q={query}"

                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract all links and text
                all_links = soup.find_all('a')
                for link in all_links:
                    href = link.get('href', '')
                    domain = self._extract_shopify_domain(href)
                    if domain:
                        self.source_breakdown['product_hunt'].add(domain)

                # Extract from page text
                text_content = soup.get_text()
                domains = self._extract_domains_from_text(text_content)
                self.source_breakdown['product_hunt'].update(domains)

                print(f"    Found {len(self.source_breakdown['product_hunt'])} domains so far")
                time.sleep(2)

            except Exception as e:
                print(f"    Error searching Product Hunt for '{query}': {e}")

        return self.source_breakdown['product_hunt']

    def scrape_hacker_news(self, max_results: int = 100) -> Set[str]:
        """Scrape Hacker News for Shopify mentions using Algolia API"""
        search_queries = ['shopify store', 'myshopify', 'shopify plus', 'ecommerce shopify']

        for query in search_queries:
            try:
                print(f"  Searching for: {query}")
                # Use HN's Algolia search API
                url = f"https://hn.algolia.com/api/v1/search?query={query.replace(' ', '+')}&tags=story"

                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                data = response.json()

                # Extract domains from story titles, URLs, and comments
                for hit in data.get('hits', []):
                    # Check story URL
                    story_url = hit.get('url', '')
                    domain = self._extract_shopify_domain(story_url)
                    if domain:
                        self.source_breakdown['hacker_news'].add(domain)

                    # Check title and text
                    title = hit.get('title', '')
                    text = hit.get('story_text', '')
                    combined_text = f"{title} {text}"
                    domains = self._extract_domains_from_text(combined_text)
                    self.source_breakdown['hacker_news'].update(domains)

                print(f"    Found {len(self.source_breakdown['hacker_news'])} domains so far")
                time.sleep(1)

            except Exception as e:
                print(f"    Error searching Hacker News for '{query}': {e}")

        return self.source_breakdown['hacker_news']

    def scrape_twitter_mentions(self, max_results: int = 100) -> Set[str]:
        """Scrape Twitter/X for Shopify store mentions (limited without API)"""
        # Without Twitter API, we can try Google search for Twitter results
        search_queries = [
            'site:twitter.com "my shopify store"',
            'site:twitter.com myshopify.com',
            'site:twitter.com "powered by shopify"'
        ]

        for query in search_queries:
            try:
                print(f"  Searching Twitter via Google: {query}")
                # Use Google search (limited, but free)
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

                response = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract domains from search results
                text_content = soup.get_text()
                domains = self._extract_domains_from_text(text_content)
                self.source_breakdown['twitter'].update(domains)

                print(f"    Found {len(self.source_breakdown['twitter'])} domains so far")
                time.sleep(3)  # Be extra careful with Google

            except Exception as e:
                print(f"    Error searching Twitter mentions: {e}")

        return self.source_breakdown['twitter']

    def _extract_shopify_domain(self, url: str) -> str:
        """Extract Shopify domain from URL if it's a Shopify store"""
        if not url:
            return None

        try:
            # Handle various URL formats
            if not url.startswith('http'):
                if '.myshopify.com' in url:
                    # Extract just the myshopify domain
                    match = re.search(r'([a-zA-Z0-9-]+\.myshopify\.com)', url)
                    if match:
                        return match.group(1)
                elif re.match(r'^[a-zA-Z0-9-]+\.[a-z]{2,}', url):
                    url = 'https://' + url
                else:
                    return None

            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path

            # Clean up domain
            domain = domain.lower().strip().rstrip('/')

            # Check if it's a myshopify.com domain
            if '.myshopify.com' in domain:
                # Extract the subdomain.myshopify.com part
                match = re.search(r'([a-zA-Z0-9-]+\.myshopify\.com)', domain)
                if match:
                    return match.group(1)

            # Check if it might be a custom Shopify domain
            # We'll validate these later with Shopify detection
            if domain and '.' in domain and not any(x in domain for x in ['reddit.com', 'twitter.com', 'producthunt.com', 'google.com', 'facebook.com', 'instagram.com']):
                # Could be a custom domain - return it for validation
                return domain

        except Exception as e:
            pass

        return None

    def _extract_domains_from_text(self, text: str) -> Set[str]:
        """Extract all potential Shopify domains from text using regex"""
        domains = set()

        # Pattern for myshopify.com domains
        myshopify_pattern = r'\b([a-zA-Z0-9-]+\.myshopify\.com)\b'
        matches = re.findall(myshopify_pattern, text, re.IGNORECASE)
        for match in matches:
            domains.add(match.lower())

        # Pattern for custom domains mentioned near Shopify keywords
        # Look for URLs that appear near "shopify", "store", "shop", etc.
        url_pattern = r'https?://([a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+)'
        url_matches = re.findall(url_pattern, text)

        # Also look for domains without http
        domain_pattern = r'\b([a-zA-Z0-9-]+\.[a-zA-Z]{2,})\b'
        domain_matches = re.findall(domain_pattern, text)

        all_possible_domains = set(url_matches + domain_matches)

        # Filter out social media and common non-store domains
        excluded_domains = {
            'reddit.com', 'twitter.com', 'facebook.com', 'instagram.com',
            'youtube.com', 'google.com', 'producthunt.com', 'github.com',
            'linkedin.com', 'medium.com', 't.co', 'bit.ly'
        }

        for domain in all_possible_domains:
            domain = domain.lower().strip()
            if not any(excluded in domain for excluded in excluded_domains):
                # Check if domain appears near Shopify keywords in text
                context_window = 200
                domain_pos = text.lower().find(domain)
                if domain_pos != -1:
                    context = text[max(0, domain_pos - context_window):domain_pos + context_window].lower()
                    if any(keyword in context for keyword in ['shopify', 'store', 'shop', 'ecommerce', 'my site', 'my website', 'launch']):
                        domains.add(domain)

        return domains

    def filter_usa_domains(self, domains: Set[str]) -> Set[str]:
        """Filter domains for USA indicators"""
        usa_domains = set()

        print("\n🇺🇸 Filtering for USA indicators...")

        # Keywords that suggest USA
        usa_keywords = [
            'usa', 'us', 'america', 'american',
            'nyc', 'ny', 'california', 'ca', 'texas', 'tx',
            'florida', 'fl', 'chicago', 'il', 'boston', 'ma',
            'seattle', 'wa', 'portland', 'or', 'denver', 'co'
        ]

        for domain in domains:
            # Check domain name for USA indicators
            domain_lower = domain.lower()
            if any(keyword in domain_lower for keyword in usa_keywords):
                usa_domains.add(domain)
                continue

            # For now, add all domains - we'll validate location later via scraping
            # This allows us to catch stores that don't have location in domain
            usa_domains.add(domain)

        return usa_domains

    def save_domains(self, output_file: str):
        """Save discovered domains to file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Combine all domains
        all_domains = set()
        for source_domains in self.source_breakdown.values():
            all_domains.update(source_domains)

        # Save to file
        with open(output_path, 'w') as f:
            for domain in sorted(all_domains):
                f.write(f"{domain}\n")

        print(f"\n💾 Saved {len(all_domains)} domains to {output_file}")

        return len(all_domains)

    def generate_report(self) -> Dict:
        """Generate summary report of discovered domains"""
        report = {
            'total_domains': 0,
            'by_source': {},
            'all_domains': set()
        }

        for source, domains in self.source_breakdown.items():
            report['by_source'][source] = len(domains)
            report['all_domains'].update(domains)

        report['total_domains'] = len(report['all_domains'])

        return report


def main():
    """Main execution function"""
    scraper = SocialMediaScraper()

    # Scrape all sources
    results = scraper.scrape_all_sources(max_per_source=100)

    # Generate report
    report = scraper.generate_report()

    # Print summary
    print("\n" + "="*60)
    print("📊 SOCIAL MEDIA MINING RESULTS")
    print("="*60)
    print(f"\nTotal unique domains found: {report['total_domains']}")
    print("\nBreakdown by source:")
    for source, count in report['by_source'].items():
        print(f"  {source.replace('_', ' ').title()}: {count} domains")

    # Save domains
    output_file = "/Users/pjump/Desktop/projects/shopify-merchant-intelligence/data/social_media/domains.txt"
    scraper.save_domains(output_file)

    # Save detailed report
    report_file = "/Users/pjump/Desktop/projects/shopify-merchant-intelligence/data/social_media/discovery_report.json"
    Path(report_file).parent.mkdir(parents=True, exist_ok=True)

    # Convert sets to lists for JSON serialization
    json_report = {
        'total_domains': report['total_domains'],
        'by_source': report['by_source'],
        'all_domains': sorted(list(report['all_domains']))
    }

    with open(report_file, 'w') as f:
        json.dump(json_report, f, indent=2)

    print(f"\n📄 Detailed report saved to {report_file}")

    # Quality assessment
    print("\n🎯 Quality Assessment:")
    myshopify_domains = [d for d in report['all_domains'] if '.myshopify.com' in d]
    custom_domains = [d for d in report['all_domains'] if '.myshopify.com' not in d]

    print(f"  MyShopify domains (.myshopify.com): {len(myshopify_domains)}")
    print(f"  Custom domains (require validation): {len(custom_domains)}")

    if myshopify_domains:
        print(f"\n  Sample MyShopify domains:")
        for domain in sorted(myshopify_domains)[:5]:
            print(f"    - {domain}")

    if custom_domains:
        print(f"\n  Sample custom domains (need Shopify validation):")
        for domain in sorted(custom_domains)[:5]:
            print(f"    - {domain}")

    print("\n✅ Social media mining complete!")
    print(f"   Next step: Validate custom domains with Shopify detector")

    return report


if __name__ == "__main__":
    main()

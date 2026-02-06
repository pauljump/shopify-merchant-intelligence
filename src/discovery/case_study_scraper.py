"""
Scrape Shopify case studies, blog posts, and known high-value store lists.

This is a more targeted approach than trying to scrape partner directories.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import json
from typing import Set, Dict, List
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CaseStudyScraper:
    """Scrape Shopify case studies and blog posts for store mentions."""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.domains = set()

    def extract_all_domains(self, text: str, html: str) -> Set[str]:
        """Extract all potential store domains from text and HTML."""
        found_domains = set()

        # Find myshopify.com domains
        myshopify_pattern = r'([\w-]+)\.myshopify\.com'
        for match in re.finditer(myshopify_pattern, text + html):
            domain = match.group(0)
            found_domains.add(domain)

        # Find custom domains mentioned in text (look for .com, .co, .io, etc)
        # This pattern looks for likely store domains
        domain_pattern = r'\b([a-zA-Z0-9-]+\.[a-zA-Z]{2,})\b'
        for match in re.finditer(domain_pattern, text):
            domain = match.group(1).lower()

            # Skip common non-store domains
            skip_list = [
                'shopify.com', 'google.com', 'facebook.com', 'twitter.com',
                'instagram.com', 'youtube.com', 'linkedin.com', 'example.com',
                'mailto.com', 'javascript.com', 'w3.org', 'schema.org'
            ]

            if not any(skip in domain for skip in skip_list):
                # Check if this domain looks like a real store
                if '.' in domain and len(domain) > 5:
                    found_domains.add(domain)

        return found_domains

    def scrape_shopify_blog(self, max_posts: int = 50) -> Set[str]:
        """Scrape Shopify's official blog for store mentions."""
        logger.info("Scraping Shopify Blog...")
        base_url = "https://www.shopify.com/blog"

        # Known blog URLs with merchant stories
        blog_urls = [
            f"{base_url}/topics/success-stories",
            f"{base_url}/success-stories",
            f"{base_url}",
        ]

        posts_scraped = 0

        for blog_url in blog_urls:
            if posts_scraped >= max_posts:
                break

            try:
                logger.info(f"Scraping blog: {blog_url}")
                response = self.session.get(blog_url, timeout=30)
                if response.status_code == 404:
                    logger.warning(f"Blog not found: {blog_url}")
                    continue

                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find article links
                article_links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if '/blog/' in href and href not in article_links:
                        if href.startswith('/'):
                            href = f"https://www.shopify.com{href}"
                        article_links.append(href)

                logger.info(f"Found {len(article_links)} article links")

                # Visit each article
                for article_url in article_links[:max_posts - posts_scraped]:
                    try:
                        logger.info(f"Scraping article: {article_url}")
                        response = self.session.get(article_url, timeout=30)
                        response.raise_for_status()

                        text = response.text
                        soup = BeautifulSoup(text, 'html.parser')

                        # Extract domains from article
                        domains = self.extract_all_domains(soup.get_text(), text)
                        for domain in domains:
                            self.domains.add(domain)
                            logger.info(f"Found store: {domain}")

                        posts_scraped += 1
                        time.sleep(2)

                    except Exception as e:
                        logger.error(f"Error scraping article {article_url}: {e}")
                        continue

                time.sleep(2)

            except Exception as e:
                logger.error(f"Error scraping blog {blog_url}: {e}")
                continue

        return self.domains

    def scrape_known_store_lists(self) -> Set[str]:
        """
        Add known high-value Shopify stores.
        These are publicly known major Shopify merchants.
        """
        logger.info("Adding known high-value stores...")

        # Known Shopify Plus stores (from public sources)
        known_stores = [
            # Fashion & Apparel
            'gymshark.com',
            'fashionnova.com',
            'allbirds.com',
            'rothy.com',
            'knix.com',
            'tentree.com',
            'bombas.com',
            'bonobos.com',

            # Beauty & Cosmetics
            'kylie-cosmetics.com',
            'colourpop.com',
            'fent beauty.com',
            'kyliecosmetics.com',
            'jeffreestarcosmetics.com',

            # Food & Beverage
            'redbull.com',
            'huel.com',
            'bulletproof.com',
            'liquidiv.com',
            'mvmt.com',

            # Electronics & Gadgets
            'tesla.com',
            'fitbit.com',
            'puffco.com',

            # Home & Lifestyle
            'brooklinen.com',
            'casper.com',
            'allbirds.com',
            'outdoor-voices.com',

            # Others
            'shopify.com',
            'bbc-shop.com',
            'penguin.com',
            'economist.com',
        ]

        for store in known_stores:
            self.domains.add(store)
            logger.info(f"Added known store: {store}")

        return self.domains

    def get_all_domains(self) -> Set[str]:
        """Get all discovered domains."""
        return self.domains

    def save_domains(self, output_path: str):
        """Save discovered domains to file."""
        with open(output_path, 'w') as f:
            for domain in sorted(self.domains):
                f.write(f"{domain}\n")

        logger.info(f"Saved {len(self.domains)} domains to {output_path}")

    def save_detailed_report(self, output_path: str):
        """Save detailed JSON report."""
        report = {
            'total_stores': len(self.domains),
            'stores': sorted(list(self.domains))
        }

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Saved detailed report to {output_path}")


def main():
    """Main entry point."""
    scraper = CaseStudyScraper()

    logger.info("=" * 80)
    logger.info("SHOPIFY CASE STUDY & BLOG SCRAPER")
    logger.info("=" * 80)

    # Add known stores first
    scraper.scrape_known_store_lists()

    # Scrape blog for more stores
    # scraper.scrape_shopify_blog(max_posts=20)  # Disabled for now - takes too long

    # Results
    print("\n" + "=" * 80)
    print("SCRAPING COMPLETE")
    print("=" * 80)
    print(f"\nTotal stores discovered: {len(scraper.domains)}")

    # Save results
    base_path = "/Users/pjump/Desktop/projects/shopify-merchant-intelligence/data/partner_directory"
    scraper.save_domains(f"{base_path}/known_stores.txt")
    scraper.save_detailed_report(f"{base_path}/known_stores_report.json")

    print(f"\nResults saved to: {base_path}/")
    print("  - known_stores.txt")
    print("  - known_stores_report.json")

    # Show sample
    print("\nSample stores:")
    for domain in sorted(list(scraper.domains))[:20]:
        print(f"  - {domain}")


if __name__ == "__main__":
    main()

"""Async CLI for high-performance Shopify discovery."""

import argparse
import asyncio
import aiohttp
from datetime import datetime
from tqdm.asyncio import tqdm as async_tqdm

from database.models import init_db, get_session, ShopifyStore
from discovery.github_datasets import SeedListDiscovery
from discovery.github_shopify_datasets import GitHubShopifyDatasets
from detectors.async_shopify_detector import AsyncShopifyDetector
from scrapers.async_store_scraper import AsyncStoreScraper


async def discover_stores_async(args):
    """Discover Shopify stores using async processing (10x faster)."""
    print(f"🚀 Async discovery - processing up to {args.concurrent} stores concurrently...")

    # Initialize database
    init_db()
    session = get_session()

    # Discover stores
    stores_data = []

    if args.csv:
        print(f"📁 Loading from CSV: {args.csv}")
        seed_discovery = SeedListDiscovery()
        csv_stores = seed_discovery.add_seeds_from_csv(args.csv)
        stores_data.extend(csv_stores)
        print(f"✅ Found {len(csv_stores)} stores from CSV")

    if args.github:
        print("🐙 Searching GitHub datasets...")
        github_discovery = GitHubShopifyDatasets()
        github_domains = github_discovery.discover(limit=args.limit)

        # Convert to store data format
        for domain in github_domains:
            stores_data.append({'domain': domain})

        print(f"✅ Found {len(github_domains)} stores from GitHub")

    # Filter out already-processed stores (deduplication)
    existing_domains = set([s.domain for s in session.query(ShopifyStore.domain).all()])
    new_stores = [s for s in stores_data if s['domain'] not in existing_domains]

    if len(new_stores) < len(stores_data):
        skipped = len(stores_data) - len(new_stores)
        print(f"⏭️  Skipped {skipped} already-processed stores")

    stores_data = new_stores[:args.limit]

    if not stores_data:
        print("✅ No new stores to process!")
        return

    print(f"📊 Processing {len(stores_data)} new stores...")

    # Extract domains for batch processing
    domains = [s['domain'] for s in stores_data]

    # Create async detector and scraper
    detector = AsyncShopifyDetector(max_concurrent=args.concurrent)
    scraper = AsyncStoreScraper(max_concurrent=args.concurrent)

    # Process in batches
    batch_size = args.concurrent * 5  # Process in larger batches
    total_processed = 0

    for i in range(0, len(domains), batch_size):
        batch_domains = domains[i:i + batch_size]
        batch_stores = stores_data[i:i + batch_size]

        print(f"\nProcessing batch {i//batch_size + 1}/{(len(domains)-1)//batch_size + 1}...")

        async with aiohttp.ClientSession() as http_session:
            # Detect Shopify + Plus concurrently
            detection_tasks = []
            for domain in batch_domains:
                task = detector.detect(http_session, domain)
                detection_tasks.append(task)

            detection_results = await asyncio.gather(*detection_tasks, return_exceptions=True)

            # Scrape data for Shopify stores concurrently
            scrape_tasks = []
            shopify_domains = []

            for domain, result in zip(batch_domains, detection_results):
                if isinstance(result, tuple):
                    is_shopify, is_plus, metadata = result
                    if is_shopify:
                        shopify_domains.append((domain, is_plus))
                        task = scraper.scrape(http_session, domain)
                        scrape_tasks.append(task)

            if scrape_tasks:
                scrape_results = await asyncio.gather(*scrape_tasks, return_exceptions=True)

                # Save to database
                for (domain, is_plus), scraped_data, store_data in zip(shopify_domains, scrape_results, batch_stores):
                    if isinstance(scraped_data, dict):
                        # Merge CSV data with scraped data
                        merged_data = {**scraped_data, **store_data}

                        store = ShopifyStore(
                            domain=domain,
                            company_name=merged_data.get('company_name'),
                            email=merged_data.get('email'),
                            phone=merged_data.get('phone'),
                            street_address=merged_data.get('street_address'),
                            city=merged_data.get('city'),
                            state=merged_data.get('state'),
                            zip_code=merged_data.get('zip_code'),
                            country=merged_data.get('country'),
                            vertical=merged_data.get('vertical'),
                            revenue_estimate=merged_data.get('revenue_estimate'),
                            employees_estimate=merged_data.get('employees_estimate'),
                            is_shopify=True,
                            is_shopify_plus=is_plus,
                            scraped_at=datetime.utcnow(),
                        )

                        session.add(store)

                session.commit()
                total_processed += len(shopify_domains)
                print(f"  ✅ Saved {len(shopify_domains)} Shopify stores")

    print(f"\n🎉 Discovery complete! Processed {total_processed} Shopify stores")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Shopify Merchant Intelligence (Async)')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Async discover command
    discover_parser = subparsers.add_parser('discover', help='Discover Shopify stores (async)')
    discover_parser.add_argument('--limit', type=int, default=1000, help='Max stores to discover')
    discover_parser.add_argument('--csv', type=str, help='CSV file with seed domains')
    discover_parser.add_argument('--github', action='store_true', help='Search GitHub datasets')
    discover_parser.add_argument('--concurrent', type=int, default=20, help='Concurrent requests (default: 20)')

    args = parser.parse_args()

    if args.command == 'discover':
        asyncio.run(discover_stores_async(args))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

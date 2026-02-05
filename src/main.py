"""Main CLI for Shopify Merchant Intelligence."""

import argparse
import sys
from datetime import datetime
from tqdm import tqdm

from database.models import init_db, get_session, ShopifyStore
from discovery.github_datasets import GitHubDatasetDiscovery, SeedListDiscovery
from detectors.shopify_detector import ShopifyDetector
from scrapers.store_scraper import StoreScraper
from apis.uber_direct import UberDirectClient


def discover_stores(args):
    """Discover Shopify stores."""
    print(f"🔍 Discovering Shopify stores (limit: {args.limit})...")

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

    if args.github and not args.csv:
        print("🐙 Searching GitHub datasets...")
        github_discovery = GitHubDatasetDiscovery()
        github_domains = github_discovery.discover(limit=args.limit)
        # Convert domains to store data format
        stores_data.extend([{'domain': d} for d in github_domains])

    # Limit
    stores_data = stores_data[:args.limit]
    print(f"📊 Processing {len(stores_data)} stores...")

    # Process each store
    detector = ShopifyDetector()
    scraper = StoreScraper()

    for store_data in tqdm(stores_data, desc="Processing stores"):
        domain = store_data['domain']

        # Check if already in database
        existing = session.query(ShopifyStore).filter_by(domain=domain).first()
        if existing:
            continue  # Skip already processed

        # Detect Shopify
        is_shopify, is_plus, metadata = detector.detect(domain)

        if is_shopify:
            # Scrape additional data (addresses if not in CSV)
            scraped_data = scraper.scrape(domain)

            # Merge CSV data with scraped data (CSV takes precedence for address)
            merged_data = {**scraped_data, **store_data}

            # Create database entry
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

    print(f"✅ Discovery complete!")


def check_serviceability(args):
    """Check Uber Direct serviceability for stores."""
    print("🚗 Checking Uber Direct serviceability...")

    session = get_session()
    uber_client = UberDirectClient()

    # Get stores that need serviceability check
    query = session.query(ShopifyStore).filter(
        ShopifyStore.is_shopify == True,
        ShopifyStore.country == 'US',
        ShopifyStore.street_address.isnot(None),
        ShopifyStore.is_uber_serviceable.is_(None)
    )

    if args.plus_only:
        query = query.filter(ShopifyStore.is_shopify_plus == True)

    stores = query.limit(args.limit).all()

    print(f"📍 Checking {len(stores)} stores...")

    for store in tqdm(stores, desc="Checking serviceability"):
        address = uber_client.format_address_from_store(store)

        if address:
            is_serviceable = uber_client.check_serviceability(address)

            store.is_uber_serviceable = is_serviceable
            store.uber_check_date = datetime.utcnow()
            session.commit()

    print("✅ Serviceability check complete!")


def export_data(args):
    """Export data to CSV."""
    print(f"💾 Exporting to {args.output}...")

    session = get_session()

    # Build query
    query = session.query(ShopifyStore).filter(ShopifyStore.is_shopify == True)

    if args.plus_only:
        query = query.filter(ShopifyStore.is_shopify_plus == True)

    if args.serviceable_only:
        query = query.filter(ShopifyStore.is_uber_serviceable == True)

    if args.usa_only:
        query = query.filter(ShopifyStore.country == 'US')

    stores = query.all()

    # Export to CSV
    import csv

    with open(args.output, 'w', newline='') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            'domain', 'company_name', 'email', 'phone',
            'street_address', 'city', 'state', 'zip_code', 'country',
            'is_shopify_plus', 'is_uber_serviceable',
            'revenue_estimate', 'employees_estimate'
        ])

        # Rows
        for store in stores:
            writer.writerow([
                store.domain,
                store.company_name,
                store.email,
                store.phone,
                store.street_address,
                store.city,
                store.state,
                store.zip_code,
                store.country,
                store.is_shopify_plus,
                store.is_uber_serviceable,
                store.revenue_estimate,
                store.employees_estimate,
            ])

    print(f"✅ Exported {len(stores)} stores to {args.output}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Shopify Merchant Intelligence')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Discover command
    discover_parser = subparsers.add_parser('discover', help='Discover Shopify stores')
    discover_parser.add_argument('--limit', type=int, default=500, help='Max stores to discover')
    discover_parser.add_argument('--csv', type=str, help='CSV file with seed domains')
    discover_parser.add_argument('--github', action='store_true', help='Search GitHub datasets')

    # Serviceability command
    service_parser = subparsers.add_parser('check-uber', help='Check Uber Direct serviceability')
    service_parser.add_argument('--limit', type=int, default=1000, help='Max stores to check')
    service_parser.add_argument('--plus-only', action='store_true', help='Only check Plus stores')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export data to CSV')
    export_parser.add_argument('--output', type=str, default='shopify_leads.csv', help='Output CSV file')
    export_parser.add_argument('--plus-only', action='store_true', help='Only export Plus stores')
    export_parser.add_argument('--serviceable-only', action='store_true', help='Only export Uber serviceable stores')
    export_parser.add_argument('--usa-only', action='store_true', help='Only export USA stores')

    args = parser.parse_args()

    if args.command == 'discover':
        discover_stores(args)
    elif args.command == 'check-uber':
        check_serviceability(args)
    elif args.command == 'export':
        export_data(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

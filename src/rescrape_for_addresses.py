"""
Re-scrape existing stores with enhanced address extraction.

Focuses on stores that are missing street addresses, especially USA stores.
"""

import sys
sys.path.insert(0, 'src')

import asyncio
import aiohttp
from database.models import init_db, get_session, ShopifyStore
from scrapers.async_store_scraper import AsyncStoreScraper
from sqlalchemy import and_


async def rescrape_for_addresses(country='US', limit=None):
    """
    Re-scrape stores missing street addresses with enhanced scraper.

    Args:
        country: Focus on specific country (default: US)
        limit: Max stores to rescrape (default: all)
    """
    print(f"🔄 Re-scraping {country} stores for missing addresses...")

    init_db()
    session = get_session()

    # Find stores missing street addresses
    query = session.query(ShopifyStore).filter(
        and_(
            ShopifyStore.is_shopify == True,
            ShopifyStore.street_address == None
        )
    )

    if country:
        query = query.filter(ShopifyStore.country == country)

    stores = query.limit(limit) if limit else query.all()

    print(f"📊 Found {len(stores)} stores missing street addresses")

    if not stores:
        print("✅ No stores need re-scraping!")
        return

    # Re-scrape with enhanced scraper
    scraper = AsyncStoreScraper(max_concurrent=30)
    updated_count = 0
    found_addresses = 0

    async with aiohttp.ClientSession(headers=scraper.headers) as http_session:
        batch_size = 150
        for i in range(0, len(stores), batch_size):
            batch = stores[i:i + batch_size]
            print(f"\n🔄 Processing batch {i//batch_size + 1}/{(len(stores)-1)//batch_size + 1}...")

            # Scrape batch
            tasks = []
            for store in batch:
                task = scraper.scrape(http_session, store.domain)
                tasks.append((store, task))

            # Await results
            for store, task in tasks:
                try:
                    result = await task

                    # Update if we found an address
                    if result.get('street_address'):
                        store.street_address = result.get('street_address')
                        store.city = result.get('city')
                        store.state = result.get('state')
                        store.zip_code = result.get('zip_code')
                        store.country = result.get('country', store.country)

                        # Update email/phone if found
                        if result.get('email') and not store.email:
                            store.email = result.get('email')

                        if result.get('phone') and not store.phone:
                            store.phone = result.get('phone')

                        updated_count += 1
                        found_addresses += 1

                except Exception as e:
                    pass

            # Save batch
            session.commit()
            print(f"  ✅ Updated {found_addresses} stores with addresses")
            found_addresses = 0

    print(f"\n{'='*60}")
    print(f"🎉 Re-scraping Complete!")
    print(f"{'='*60}")
    print(f"Total stores updated: {updated_count}")
    print(f"{'='*60}\n")

    # Show final counts
    usa_with_address = session.query(ShopifyStore).filter(
        and_(
            ShopifyStore.country == 'US',
            ShopifyStore.is_shopify_plus == True,
            ShopifyStore.street_address != None
        )
    ).count()

    print(f"📊 USA Shopify Plus with full addresses: {usa_with_address}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Re-scrape stores for missing addresses')
    parser.add_argument('--country', type=str, default=None, help='Country to focus on (e.g., US)')
    parser.add_argument('--limit', type=int, default=None, help='Max stores to rescrape')
    args = parser.parse_args()

    asyncio.run(rescrape_for_addresses(country=args.country, limit=args.limit))

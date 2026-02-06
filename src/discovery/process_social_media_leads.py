#!/usr/bin/env python3
"""
Process social media discovered domains:
1. Validate they are actually Shopify stores
2. Check if they're Shopify Plus
3. Extract USA location information
4. Save to database
"""

import sys
from pathlib import Path
import asyncio
import aiohttp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.models import Base, ShopifyStore
from detectors.async_shopify_detector import AsyncShopifyDetector
from scrapers.async_store_scraper import AsyncStoreScraper


class SocialMediaLeadProcessor:
    """Process and validate social media discovered domains"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.detector = AsyncShopifyDetector()
        self.scraper = AsyncStoreScraper()

        self.stats = {
            'total_domains': 0,
            'shopify_stores': 0,
            'shopify_plus_stores': 0,
            'usa_stores': 0,
            'with_contact_info': 0,
            'errors': 0
        }

    async def process_domains(self, domains_file: str):
        """Process all domains from file"""
        domains_path = Path(domains_file)

        if not domains_path.exists():
            print(f"❌ Error: {domains_file} not found")
            return

        # Read domains
        with open(domains_path, 'r') as f:
            domains = [line.strip() for line in f if line.strip()]

        self.stats['total_domains'] = len(domains)
        print(f"📥 Processing {len(domains)} domains from social media...")

        # Create aiohttp session
        async with aiohttp.ClientSession() as session:
            # Process in batches
            batch_size = 10
            for i in range(0, len(domains), batch_size):
                batch = domains[i:i+batch_size]
                print(f"\n🔄 Processing batch {i//batch_size + 1}/{(len(domains)-1)//batch_size + 1}")

                tasks = [self.process_single_domain(session, domain) for domain in batch]
                await asyncio.gather(*tasks, return_exceptions=True)

                # Save progress after each batch
                self.session.commit()

        print(f"\n✅ Processing complete!")
        self.print_stats()

    async def process_single_domain(self, session: aiohttp.ClientSession, domain: str):
        """Process a single domain"""
        try:
            # Skip if already in database
            existing = self.session.query(ShopifyStore).filter(ShopifyStore.domain == domain).first()
            if existing:
                print(f"  ⏭️  Skipping {domain} (already in database)")
                return

            print(f"  🔍 Checking {domain}...")

            # Detect if it's a Shopify store
            is_shopify, is_plus, metadata = await self.detector.detect(session, domain)

            if not is_shopify:
                print(f"  ❌ {domain} - Not a Shopify store")
                return

            self.stats['shopify_stores'] += 1

            # Get Plus signals from metadata
            signals = metadata.get('plus_signals', [])

            if is_plus:
                self.stats['shopify_plus_stores'] += 1
                print(f"  ✅ {domain} - Shopify Plus! ({len(signals)} signals)")
            else:
                print(f"  ✅ {domain} - Shopify (not Plus)")

            # Scrape additional information
            scraped_data = await self.scraper.scrape(session, domain)

            # Check if USA
            is_usa = self._is_usa_store(scraped_data)
            if is_usa:
                self.stats['usa_stores'] += 1

            has_contact = bool(scraped_data.get('email') or scraped_data.get('phone'))
            if has_contact:
                self.stats['with_contact_info'] += 1

            # Save to database
            store = ShopifyStore(
                domain=domain,
                is_shopify=True,
                is_shopify_plus=is_plus,
                plus_signals=','.join(signals),
                email=scraped_data.get('email'),
                phone=scraped_data.get('phone'),
                street_address=scraped_data.get('street_address'),
                city=scraped_data.get('city'),
                state=scraped_data.get('state'),
                zip_code=scraped_data.get('zip_code'),
                country=scraped_data.get('country'),
                discovery_source='social_media'
            )

            self.session.add(store)

            if is_usa and is_plus:
                print(f"  🎯 {domain} - USA Shopify Plus lead!")

        except Exception as e:
            self.stats['errors'] += 1
            print(f"  ❌ Error processing {domain}: {e}")

    def _is_usa_store(self, scraped_data: dict) -> bool:
        """Determine if store is USA-based"""
        # Check country from scraped data
        country = scraped_data.get('country', '').lower()
        if country in ['us', 'usa', 'united states', 'america']:
            return True

        # Check state
        usa_states = {
            'alabama', 'al', 'alaska', 'ak', 'arizona', 'az', 'arkansas', 'ar',
            'california', 'ca', 'colorado', 'co', 'connecticut', 'ct', 'delaware', 'de',
            'florida', 'fl', 'georgia', 'ga', 'hawaii', 'hi', 'idaho', 'id',
            'illinois', 'il', 'indiana', 'in', 'iowa', 'ia', 'kansas', 'ks',
            'kentucky', 'ky', 'louisiana', 'la', 'maine', 'me', 'maryland', 'md',
            'massachusetts', 'ma', 'michigan', 'mi', 'minnesota', 'mn', 'mississippi', 'ms',
            'missouri', 'mo', 'montana', 'mt', 'nebraska', 'ne', 'nevada', 'nv',
            'new hampshire', 'nh', 'new jersey', 'nj', 'new mexico', 'nm', 'new york', 'ny',
            'north carolina', 'nc', 'north dakota', 'nd', 'ohio', 'oh', 'oklahoma', 'ok',
            'oregon', 'or', 'pennsylvania', 'pa', 'rhode island', 'ri', 'south carolina', 'sc',
            'south dakota', 'sd', 'tennessee', 'tn', 'texas', 'tx', 'utah', 'ut',
            'vermont', 'vt', 'virginia', 'va', 'washington', 'wa', 'west virginia', 'wv',
            'wisconsin', 'wi', 'wyoming', 'wy', 'washington dc', 'dc'
        }

        state = scraped_data.get('state', '').lower()
        if state in usa_states:
            return True

        # Check phone number (starts with +1 or looks like US number)
        phone = scraped_data.get('phone', '')
        if phone and (phone.startswith('+1') or phone.startswith('1-')):
            return True

        # If no clear indicators but no country specified, assume might be USA
        if not country and not state:
            return True  # We'll validate later

        return False

    def print_stats(self):
        """Print processing statistics"""
        print("\n" + "="*60)
        print("📊 SOCIAL MEDIA LEAD PROCESSING RESULTS")
        print("="*60)
        print(f"\nTotal domains processed: {self.stats['total_domains']}")
        print(f"Shopify stores found: {self.stats['shopify_stores']}")
        print(f"Shopify Plus stores: {self.stats['shopify_plus_stores']}")
        print(f"USA-based stores: {self.stats['usa_stores']}")
        print(f"Stores with contact info: {self.stats['with_contact_info']}")
        print(f"Errors: {self.stats['errors']}")

        if self.stats['shopify_stores'] > 0:
            plus_rate = (self.stats['shopify_plus_stores'] / self.stats['shopify_stores']) * 100
            usa_rate = (self.stats['usa_stores'] / self.stats['shopify_stores']) * 100
            print(f"\n📈 Conversion Rates:")
            print(f"   Shopify Plus rate: {plus_rate:.1f}%")
            print(f"   USA store rate: {usa_rate:.1f}%")

    def close(self):
        """Close database session"""
        self.session.close()


async def main():
    """Main execution"""
    db_path = "/Users/pjump/Desktop/projects/shopify-merchant-intelligence/shopify_leads.db"
    domains_file = "/Users/pjump/Desktop/projects/shopify-merchant-intelligence/data/social_media/clean_domains.txt"

    processor = SocialMediaLeadProcessor(db_path)

    try:
        await processor.process_domains(domains_file)
    finally:
        processor.close()


if __name__ == "__main__":
    asyncio.run(main())

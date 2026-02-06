#!/usr/bin/env python3
"""Test processing social media domains on a small subset"""

import sys
from pathlib import Path
import asyncio

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from discovery.process_social_media_leads import SocialMediaLeadProcessor


async def main():
    """Test on 30 domains"""
    db_path = "/Users/pjump/Desktop/projects/shopify-merchant-intelligence/shopify_leads.db"
    domains_file = "/Users/pjump/Desktop/projects/shopify-merchant-intelligence/data/social_media/test_domains.txt"

    processor = SocialMediaLeadProcessor(db_path)

    try:
        await processor.process_domains(domains_file)
    finally:
        processor.close()


if __name__ == "__main__":
    asyncio.run(main())

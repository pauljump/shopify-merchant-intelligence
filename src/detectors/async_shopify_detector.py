"""Async Shopify and Shopify Plus detection."""

import aiohttp
import asyncio
from typing import Tuple, Dict, Any
import re
from bs4 import BeautifulSoup


class AsyncShopifyDetector:
    """Async detector for Shopify and Shopify Plus stores."""

    def __init__(self, timeout: int = 10, max_concurrent: int = 20):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

    async def detect(self, session: aiohttp.ClientSession, domain: str) -> Tuple[bool, bool, Dict[str, Any]]:
        """
        Detect if site is Shopify and if it's Plus.

        Returns:
            (is_shopify, is_plus, metadata)
        """
        async with self.semaphore:
            if not domain.startswith('http'):
                domain = f'https://{domain}'

            metadata = {}
            is_shopify = False
            is_plus = False

            try:
                # Fetch homepage
                async with session.get(domain, timeout=self.timeout, allow_redirects=True) as response:
                    html = await response.text()

                    # Check for Shopify indicators
                    shopify_indicators = [
                        'Shopify.theme',
                        'shopify-analytics',
                        'cdn.shopify.com',
                        'monorail-edge.shopifysvc.com',
                        '/apps/shopify'
                    ]

                    for indicator in shopify_indicators:
                        if indicator in html:
                            is_shopify = True
                            metadata['detection_method'] = indicator
                            break

                    # If Shopify, check for Plus indicators
                    if is_shopify:
                        plus_indicators = self._check_plus_indicators(domain, html)
                        is_plus = plus_indicators['is_plus']
                        metadata.update(plus_indicators)

            except asyncio.TimeoutError:
                metadata['error'] = 'timeout'
            except aiohttp.ClientError as e:
                metadata['error'] = str(e)
            except Exception as e:
                metadata['error'] = str(e)

            return is_shopify, is_plus, metadata

    def _check_plus_indicators(self, domain: str, html: str) -> Dict[str, Any]:
        """Check for Shopify Plus specific indicators."""
        indicators = {
            'is_plus': False,
            'plus_signals': []
        }

        # 1. Custom checkout domain (Plus feature)
        if 'checkout.shopify.com' in html:
            indicators['plus_signals'].append('standard_checkout')
        else:
            # Check if checkout is on custom domain
            soup = BeautifulSoup(html, 'html.parser')
            cart_links = soup.find_all('a', href=re.compile(r'/cart|/checkout'))
            if cart_links:
                checkout_url = cart_links[0].get('href', '')
                if checkout_url and 'checkout.shopify.com' not in checkout_url:
                    indicators['plus_signals'].append('custom_checkout_domain')
                    indicators['is_plus'] = True

        # 2. Headless/custom storefront (Plus feature)
        if 'storefront-renderer' in html or 'hydrogen' in html.lower():
            indicators['plus_signals'].append('headless_storefront')
            indicators['is_plus'] = True

        # 3. Advanced customization indicators
        if re.search(r'<script[^>]*src=["\'][^"\']*custom[^"\']*\.js', html):
            indicators['plus_signals'].append('custom_javascript')

        # 4. Plus-only apps
        plus_apps = [
            'launchpad',
            'flow.shopify.com',
            'wholesale',
        ]
        for app in plus_apps:
            if app in html.lower():
                indicators['plus_signals'].append(f'plus_app_{app}')
                indicators['is_plus'] = True

        # 5. Multi-currency (enterprise feature)
        if re.search(r'data-currency.*data-currency', html, re.DOTALL):
            indicators['plus_signals'].append('multi_currency')

        # If we have 2+ Plus signals, mark as Plus
        if len(indicators['plus_signals']) >= 2:
            indicators['is_plus'] = True

        return indicators


async def detect_batch(domains: list, max_concurrent: int = 20) -> Dict[str, Tuple[bool, bool, Dict]]:
    """
    Detect Shopify/Plus for a batch of domains concurrently.

    Returns:
        dict of domain -> (is_shopify, is_plus, metadata)
    """
    detector = AsyncShopifyDetector(max_concurrent=max_concurrent)
    results = {}

    async with aiohttp.ClientSession(headers=detector.headers) as session:
        tasks = []
        for domain in domains:
            task = detector.detect(session, domain)
            tasks.append((domain, task))

        # Run all detections concurrently
        for domain, task in tasks:
            try:
                result = await task
                results[domain] = result
            except Exception as e:
                results[domain] = (False, False, {'error': str(e)})

    return results


if __name__ == '__main__':
    # Test async detection
    import time

    test_domains = [
        'allbirds.com',
        'gymshark.com',
        'nike.com',
        'google.com',  # Not Shopify
    ]

    start = time.time()
    results = asyncio.run(detect_batch(test_domains, max_concurrent=10))
    elapsed = time.time() - start

    print(f"\nProcessed {len(test_domains)} domains in {elapsed:.2f}s")
    print(f"Average: {elapsed/len(test_domains):.2f}s per domain\n")

    for domain, (is_shopify, is_plus, metadata) in results.items():
        print(f"{domain}:")
        print(f"  Shopify: {is_shopify}")
        print(f"  Plus: {is_plus}")
        print(f"  Signals: {metadata.get('plus_signals', [])}")
        print()

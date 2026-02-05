"""Detect if a website is using Shopify and if it's Shopify Plus."""

import requests
from typing import Tuple, Dict, Any
import re
from bs4 import BeautifulSoup


class ShopifyDetector:
    """Detect Shopify and Shopify Plus stores."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def detect(self, domain: str) -> Tuple[bool, bool, Dict[str, Any]]:
        """
        Detect if site is Shopify and if it's Plus.

        Returns:
            (is_shopify, is_plus, metadata)
        """
        if not domain.startswith('http'):
            domain = f'https://{domain}'

        metadata = {}
        is_shopify = False
        is_plus = False

        try:
            # Fetch homepage
            response = self.session.get(domain, timeout=self.timeout, allow_redirects=True)
            html = response.text

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
                plus_indicators = self._check_plus_indicators(domain, html, response)
                is_plus = plus_indicators['is_plus']
                metadata.update(plus_indicators)

        except Exception as e:
            metadata['error'] = str(e)

        return is_shopify, is_plus, metadata

    def _check_plus_indicators(self, domain: str, html: str, response) -> Dict[str, Any]:
        """Check for Shopify Plus specific indicators."""
        indicators = {
            'is_plus': False,
            'plus_signals': []
        }

        # 1. Custom checkout domain (Plus feature)
        # Plus stores often use checkout.shopify.com or custom domains
        if 'checkout.shopify.com' in html:
            indicators['plus_signals'].append('standard_checkout')
        else:
            # Check if checkout is on custom domain
            soup = BeautifulSoup(html, 'html.parser')
            cart_links = soup.find_all('a', href=re.compile(r'/cart|/checkout'))
            if cart_links:
                checkout_url = cart_links[0].get('href', '')
                if checkout_url and not 'checkout.shopify.com' in checkout_url:
                    indicators['plus_signals'].append('custom_checkout_domain')
                    indicators['is_plus'] = True

        # 2. Headless/custom storefront (Plus feature)
        if 'storefront-renderer' in html or 'hydrogen' in html.lower():
            indicators['plus_signals'].append('headless_storefront')
            indicators['is_plus'] = True

        # 3. Advanced customization indicators
        if re.search(r'<script[^>]*src=["\'][^"\']*custom[^"\']*\.js', html):
            indicators['plus_signals'].append('custom_javascript')

        # 4. Plus-only apps (check for common Plus apps)
        plus_apps = [
            'launchpad',  # Shopify Plus app
            'flow.shopify.com',  # Shopify Flow (Plus only)
            'wholesale',  # Wholesale features
        ]
        for app in plus_apps:
            if app in html.lower():
                indicators['plus_signals'].append(f'plus_app_{app}')
                indicators['is_plus'] = True

        # 5. High traffic/complexity indicators
        # Check for multiple languages, currencies (enterprise features)
        if re.search(r'data-currency.*data-currency', html, re.DOTALL):
            indicators['plus_signals'].append('multi_currency')

        # If we have 2+ Plus signals, mark as Plus
        if len(indicators['plus_signals']) >= 2:
            indicators['is_plus'] = True

        return indicators


if __name__ == '__main__':
    # Test
    detector = ShopifyDetector()

    # Test with known Shopify store
    test_domains = [
        'allbirds.com',  # Known Plus store
        'gymshark.com',  # Known Plus store
    ]

    for domain in test_domains:
        is_shopify, is_plus, metadata = detector.detect(domain)
        print(f"\n{domain}:")
        print(f"  Shopify: {is_shopify}")
        print(f"  Plus: {is_plus}")
        print(f"  Signals: {metadata.get('plus_signals', [])}")

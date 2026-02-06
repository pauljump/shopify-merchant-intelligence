"""
Reverse IP lookup to discover Shopify stores.

Strategy:
1. Find Shopify's hosting infrastructure IP ranges
2. Query reverse DNS to find all domains hosted on those IPs
3. Extract store domains

Shopify hosts stores on their own infrastructure with known IP patterns.
We can use multiple approaches:
- ViewDNS.info reverse IP lookup
- HackerTarget reverse IP API (free tier)
- DNS enumeration on known Shopify IPs
"""

import requests
import time
import socket
from typing import Set, List
from urllib.parse import quote
import re


class ReverseIPLookup:
    """Discover Shopify stores via reverse IP lookup."""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        # Known Shopify infrastructure domains to start from
        self.seed_shopify_domains = [
            'shopify.com',
            'myshopify.com',
            'shop.app',
            'shopifycdn.net',
            'cdn.shopify.com',
        ]

    def discover(self, max_ips: int = 50) -> Set[str]:
        """
        Discover stores via reverse IP lookup.

        Args:
            max_ips: Maximum number of IPs to check

        Returns:
            Set of discovered store domains
        """
        print("🔍 Reverse IP Lookup Discovery...")
        print(f"📊 Finding Shopify infrastructure IPs\\n")

        all_domains = set()

        # Step 1: Get Shopify's IP ranges
        shopify_ips = self._get_shopify_ips()
        print(f"✅ Found {len(shopify_ips)} Shopify infrastructure IPs\\n")

        # Step 2: Reverse lookup on each IP
        print(f"🔎 Checking up to {min(len(shopify_ips), max_ips)} IPs...\\n")

        for i, ip in enumerate(list(shopify_ips)[:max_ips]):
            print(f"[{i+1}/{min(len(shopify_ips), max_ips)}] IP: {ip}")

            try:
                domains = self._reverse_ip_lookup(ip)

                if domains:
                    all_domains.update(domains)
                    print(f"  ✅ Found {len(domains)} domains")
                else:
                    print(f"  ⏭️  No domains found")

            except Exception as e:
                print(f"  ⚠️  Error: {e}")

            time.sleep(2)  # Rate limiting

        print(f"\\n{'='*60}")
        print(f"🎯 Reverse IP Lookup Complete!")
        print(f"{'='*60}")
        print(f"🌐 Total unique domains: {len(all_domains)}")
        print(f"{'='*60}\\n")

        # Save results
        self._save_results(all_domains)

        return all_domains

    def _get_shopify_ips(self) -> Set[str]:
        """Get Shopify's infrastructure IP addresses."""
        ips = set()

        # Method 1: Resolve known Shopify domains
        for domain in self.seed_shopify_domains:
            try:
                # Get IP for domain
                ip = socket.gethostbyname(domain)
                ips.add(ip)
                print(f"  🌐 {domain} → {ip}")
            except Exception as e:
                print(f"  ⚠️  {domain}: {e}")

        # Method 2: Check common Shopify subdomains
        print(f"\\n🔎 Checking common Shopify subdomains...")
        common_subdomains = [
            'checkout.shopify.com',
            'payments.shopify.com',
            'cdn.shopify.com',
            'cdn1.shopify.com',
            'cdn2.shopify.com',
            'cdn3.shopify.com',
        ]

        for subdomain in common_subdomains:
            try:
                ip = socket.gethostbyname(subdomain)
                if ip not in ips:
                    ips.add(ip)
                    print(f"  🌐 {subdomain} → {ip}")
            except:
                pass

        return ips

    def _reverse_ip_lookup(self, ip: str) -> Set[str]:
        """
        Reverse lookup to find domains hosted on an IP.

        Uses multiple free APIs:
        1. RapidDNS (free, no limits)
        2. DNSDumpster (free)
        3. HackerTarget API (free tier)
        4. ViewDNS.info API (free tier)
        """
        domains = set()

        # Try RapidDNS (free, no API key, no rate limits)
        try:
            domains_rd = self._rapiddns_reverse_ip(ip)
            domains.update(domains_rd)
        except Exception as e:
            print(f"    RapidDNS error: {e}")

        # Try DNSDumpster if RapidDNS didn't work
        if not domains:
            try:
                domains_dd = self._dnsdumpster_reverse_ip(ip)
                domains.update(domains_dd)
            except Exception as e:
                print(f"    DNSDumpster error: {e}")

        # Try HackerTarget API (free, no API key needed)
        if not domains:
            try:
                domains_ht = self._hackertarget_reverse_ip(ip)
                domains.update(domains_ht)
            except Exception as e:
                print(f"    HackerTarget error: {e}")

        # Try ViewDNS.info (free, limited)
        if not domains:
            try:
                domains_vd = self._viewdns_reverse_ip(ip)
                domains.update(domains_vd)
            except Exception as e:
                print(f"    ViewDNS error: {e}")

        return domains

    def _rapiddns_reverse_ip(self, ip: str) -> Set[str]:
        """Use RapidDNS reverse IP lookup (free, no API key)."""
        domains = set()

        # RapidDNS provides free reverse DNS lookup
        url = f"https://rapiddns.io/sameip/{ip}?full=1"

        response = requests.get(url, headers=self.headers, timeout=15)

        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find domain table
            table = soup.find('table', id='table')
            if table:
                for row in table.find_all('tr')[1:]:  # Skip header
                    cols = row.find_all('td')
                    if len(cols) >= 1:
                        domain = cols[0].get_text().strip()
                        if domain and self._is_likely_shopify_store(domain):
                            domains.add(domain)

        return domains

    def _dnsdumpster_reverse_ip(self, ip: str) -> Set[str]:
        """Use DNSDumpster for reverse DNS (free)."""
        domains = set()

        # DNSDumpster requires CSRF token, more complex
        # For now, skip this method - too complex for free tier
        return domains

    def _hackertarget_reverse_ip(self, ip: str) -> Set[str]:
        """Use HackerTarget reverse IP API."""
        domains = set()

        url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"

        response = requests.get(url, headers=self.headers, timeout=10)

        if response.status_code == 200:
            text = response.text.strip()

            # API returns "error check your search parameter" if no results
            if 'error' not in text.lower():
                # Results are line-separated domains
                for line in text.split('\\n'):
                    domain = line.strip()
                    if domain and self._is_likely_shopify_store(domain):
                        domains.add(domain)

        return domains

    def _viewdns_reverse_ip(self, ip: str) -> Set[str]:
        """Use ViewDNS.info reverse IP lookup."""
        domains = set()

        # ViewDNS.info free API
        url = f"https://viewdns.info/reverseip/?host={ip}&t=1"

        response = requests.get(url, headers=self.headers, timeout=10)

        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find domains in table
            table = soup.find('table')
            if table:
                for row in table.find_all('tr')[1:]:  # Skip header
                    cols = row.find_all('td')
                    if cols:
                        domain = cols[0].get_text().strip()
                        if domain and self._is_likely_shopify_store(domain):
                            domains.add(domain)

        return domains

    def _is_likely_shopify_store(self, domain: str) -> bool:
        """Check if domain is likely a Shopify store."""
        if not domain or len(domain) < 4:
            return False

        domain = domain.lower()

        # Include .myshopify.com stores
        if '.myshopify.com' in domain:
            return True

        # Exclude Shopify infrastructure
        exclude = [
            'shopify.com', 'shopifycdn.net', 'shopifycs.com',
            'shopifysvc.com', 'shopifycloud.com', 'myshopify.io',
            'checkout.shopify', 'payments.shopify', 'cdn.shopify',
            'apps.shopify', 'admin.shopify', 'help.shopify',
            'community.shopify', 'google.', 'facebook.', 'twitter.',
            'instagram.', 'youtube.', 'linkedin.'
        ]

        for exc in exclude:
            if exc in domain:
                return False

        return True

    def _save_results(self, domains: Set[str]):
        """Save discovered domains."""
        import os

        os.makedirs('data/reverse_ip', exist_ok=True)

        with open('data/reverse_ip/domains.txt', 'w') as f:
            for domain in sorted(domains):
                f.write(f"{domain}\\n")

        print(f"💾 Saved to data/reverse_ip/domains.txt")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Reverse IP lookup for Shopify stores')
    parser.add_argument('--ipfile', type=str, help='File containing IPs to check (one per line)')
    parser.add_argument('--max-ips', type=int, default=50, help='Maximum number of IPs to check')
    args = parser.parse_args()

    lookup = ReverseIPLookup()

    # If IP file provided, use those IPs
    if args.ipfile:
        print(f"📄 Loading IPs from: {args.ipfile}")
        with open(args.ipfile, 'r') as f:
            file_ips = [line.strip() for line in f if line.strip()]

        print(f"✅ Loaded {len(file_ips)} IPs\n")

        # Override the discover method to use file IPs
        all_domains = set()
        print(f"🔎 Checking {min(len(file_ips), args.max_ips)} IPs...\n")

        for i, ip in enumerate(file_ips[:args.max_ips]):
            print(f"[{i+1}/{min(len(file_ips), args.max_ips)}] IP: {ip}")

            try:
                domains = lookup._reverse_ip_lookup(ip)

                if domains:
                    all_domains.update(domains)
                    print(f"  ✅ Found {len(domains)} domains")
                else:
                    print(f"  ⏭️  No domains found")

            except Exception as e:
                print(f"  ⚠️  Error: {e}")

            time.sleep(2)  # Rate limiting

        print(f"\n{'='*60}")
        print(f"🎯 Reverse IP Lookup Complete!")
        print(f"{'='*60}")
        print(f"🌐 Total unique domains: {len(all_domains)}")
        print(f"{'='*60}\n")

        lookup._save_results(all_domains)
        results = all_domains

    else:
        results = lookup.discover(max_ips=args.max_ips)

    print(f"\n📊 Sample results:")
    for domain in list(results)[:20]:
        print(f"  - {domain}")

"""
Discover Shopify's full IP infrastructure via ASN/WHOIS lookup.

Strategy:
1. Find Shopify's ASN (Autonomous System Number) via WHOIS
2. Query for all IP ranges owned by that ASN
3. Sample IPs from those ranges
4. Run reverse IP lookup on sampled IPs
5. Discover thousands more stores
"""

import socket
import requests
import ipaddress
from typing import Set, List
import time


class ShopifyIPDiscovery:
    """Discover Shopify's IP infrastructure and ranges."""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        self.known_shopify_domains = [
            'shopify.com',
            'myshopify.com',
            'cdn.shopify.com',
            'shop.app',
        ]

    def discover_shopify_ip_ranges(self) -> List[str]:
        """
        Discover Shopify's IP ranges via multiple methods.

        Returns:
            List of IP addresses to check via reverse lookup
        """
        print("🔍 Discovering Shopify IP Infrastructure...")
        print(f"{'='*60}\n")

        all_ips = set()

        # Method 1: Known Shopify domains
        print("📍 Method 1: Resolving known Shopify domains...")
        known_ips = self._get_known_shopify_ips()
        all_ips.update(known_ips)
        print(f"✅ Found {len(known_ips)} IPs from known domains\n")

        # Method 2: ASN lookup via HackerTarget
        print("📍 Method 2: ASN lookup for Shopify...")
        asn_ips = self._get_asn_ips()
        all_ips.update(asn_ips)
        print(f"✅ Found {len(asn_ips)} IPs from ASN lookup\n")

        # Method 3: IP range expansion
        print("📍 Method 3: Expanding IP ranges...")
        expanded_ips = self._expand_ip_ranges(list(all_ips))
        all_ips.update(expanded_ips)
        print(f"✅ Expanded to {len(expanded_ips)} nearby IPs\n")

        print(f"{'='*60}")
        print(f"🎯 IP Discovery Complete!")
        print(f"{'='*60}")
        print(f"📊 Total IPs to check: {len(all_ips)}")
        print(f"{'='*60}\n")

        # Save results
        self._save_results(list(all_ips))

        return list(all_ips)

    def _get_known_shopify_ips(self) -> Set[str]:
        """Resolve known Shopify domains to IPs."""
        ips = set()

        for domain in self.known_shopify_domains:
            try:
                ip = socket.gethostbyname(domain)
                ips.add(ip)
                print(f"  🌐 {domain} → {ip}")
            except Exception as e:
                print(f"  ⚠️  {domain}: {e}")

        # Also check common subdomains
        subdomains = [
            'checkout.shopify.com',
            'cdn1.shopify.com',
            'cdn2.shopify.com',
            'cdn3.shopify.com',
            'payments.shopify.com',
            'api.shopify.com',
        ]

        for subdomain in subdomains:
            try:
                ip = socket.gethostbyname(subdomain)
                if ip not in ips:
                    ips.add(ip)
                    print(f"  🌐 {subdomain} → {ip}")
            except:
                pass

        return ips

    def _get_asn_ips(self) -> Set[str]:
        """
        Get Shopify's IP ranges via ASN lookup.

        Uses HackerTarget ASN lookup API (free).
        """
        ips = set()

        # First, get ASN for shopify.com
        try:
            asn_url = f"https://api.hackertarget.com/aslookup/?q=shopify.com"
            response = requests.get(asn_url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                text = response.text.strip()
                print(f"  📋 ASN Info: {text[:100]}...")

                # Extract ASN number (format: "AS##### Description")
                if text.startswith('AS'):
                    asn_num = text.split()[0]
                    print(f"  ✅ Found ASN: {asn_num}")

                    # Now get IP ranges for this ASN
                    time.sleep(2)  # Rate limiting
                    ranges_url = f"https://api.hackertarget.com/aslookup/?q={asn_num}"
                    response2 = requests.get(ranges_url, headers=self.headers, timeout=10)

                    if response2.status_code == 200:
                        ranges_text = response2.text.strip()
                        print(f"  📋 IP Ranges: {ranges_text[:200]}...")

        except Exception as e:
            print(f"  ⚠️  ASN lookup error: {e}")

        # Alternative: Use ipinfo.io (free tier)
        try:
            time.sleep(2)
            ipinfo_url = "https://ipinfo.io/AS54113"  # Shopify's known ASN
            response = requests.get(ipinfo_url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                print(f"  📋 IPInfo data: {str(data)[:200]}...")

        except Exception as e:
            print(f"  ⚠️  IPInfo error: {e}")

        return ips

    def _expand_ip_ranges(self, seed_ips: List[str], nearby: int = 5) -> Set[str]:
        """
        Expand IP ranges by checking nearby IPs.

        For each known IP like 23.227.38.33, check:
        - 23.227.38.32, 23.227.38.34, etc. (same /24)
        - 23.227.39.33, 23.227.37.33, etc. (nearby /24s)
        """
        expanded = set()

        for ip_str in seed_ips:
            try:
                ip = ipaddress.IPv4Address(ip_str)

                # Get /24 network (e.g., 23.227.38.0/24)
                network = ipaddress.IPv4Network(f"{ip}/24", strict=False)

                # Sample IPs from this /24 (every 10th IP to avoid too many)
                for i in range(0, 256, 10):
                    sample_ip = str(network.network_address + i)
                    expanded.add(sample_ip)

                print(f"  🔄 Expanded {ip_str} → {len(expanded)} IPs in /24 range")

            except Exception as e:
                print(f"  ⚠️  Error expanding {ip_str}: {e}")

        return expanded

    def _save_results(self, ips: List[str]):
        """Save discovered IPs."""
        import os

        os.makedirs('data/shopify_ips', exist_ok=True)

        with open('data/shopify_ips/all_ips.txt', 'w') as f:
            for ip in sorted(ips):
                f.write(f"{ip}\n")

        print(f"💾 Saved to data/shopify_ips/all_ips.txt")


if __name__ == '__main__':
    discovery = ShopifyIPDiscovery()
    ips = discovery.discover_shopify_ip_ranges()

    print(f"\n📊 Sample IPs to check:")
    for ip in list(ips)[:20]:
        print(f"  - {ip}")

    print(f"\n💡 Next: Run reverse IP lookup on these {len(ips)} IPs to find stores")

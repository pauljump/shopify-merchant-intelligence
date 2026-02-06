"""Async scraper for Shopify store data."""

import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
from typing import Dict, Optional, Any
import json


class AsyncStoreScraper:
    """Async scraper for contact info and business data from Shopify stores."""

    def __init__(self, timeout: int = 10, max_concurrent: int = 20):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

    async def scrape(self, session: aiohttp.ClientSession, domain: str) -> Dict[str, Any]:
        """
        Scrape all available data from a store.

        Returns dict with: email, phone, address, city, state, zip, country, etc.
        """
        async with self.semaphore:
            if not domain.startswith('http'):
                domain = f'https://{domain}'

            data = {
                'domain': domain.replace('https://', '').replace('http://', ''),
                'email': None,
                'phone': None,
                'street_address': None,
                'city': None,
                'state': None,
                'zip_code': None,
                'country': None,
                'company_name': None,
                'product_categories': [],
                'has_local_delivery': False,
            }

            try:
                # Try contact page first
                contact_data = await self._scrape_contact_page(session, domain)
                data.update({k: v for k, v in contact_data.items() if v})

                # Try homepage footer if needed
                if not data['street_address']:
                    homepage_data = await self._scrape_homepage_footer(session, domain)
                    data.update({k: v for k, v in homepage_data.items() if v})

                # Try about page if still missing address
                if not data['street_address']:
                    about_data = await self._scrape_about_page(session, domain)
                    data.update({k: v for k, v in about_data.items() if v})

                # Try Schema.org structured data
                if not data['street_address']:
                    schema_data = await self._scrape_schema_org(session, domain)
                    data.update({k: v for k, v in schema_data.items() if v})

                # Check shipping policy
                shipping_data = await self._check_shipping_policy(session, domain)
                data.update(shipping_data)

            except Exception as e:
                data['scrape_error'] = str(e)

            return data

    async def _scrape_contact_page(self, session: aiohttp.ClientSession, domain: str) -> Dict[str, Any]:
        """Scrape contact page."""
        data = {}
        contact_urls = [
            f'{domain}/pages/contact',
            f'{domain}/pages/contact-us',
            f'{domain}/contact',
        ]

        for url in contact_urls:
            try:
                async with session.get(url, timeout=self.timeout) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        if not data.get('email'):
                            email = self._extract_email(soup)
                            if email:
                                data['email'] = email

                        if not data.get('phone'):
                            phone = self._extract_phone(soup)
                            if phone:
                                data['phone'] = phone

                        if not data.get('street_address'):
                            address = self._extract_address(soup)
                            if address:
                                data.update(address)

                        break
            except:
                continue

        return data

    async def _scrape_homepage_footer(self, session: aiohttp.ClientSession, domain: str) -> Dict[str, Any]:
        """Scrape homepage footer for address."""
        data = {}

        try:
            async with session.get(domain, timeout=self.timeout) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                footer = soup.find('footer')
                if footer:
                    if not data.get('email'):
                        email = self._extract_email(footer)
                        if email:
                            data['email'] = email

                    if not data.get('phone'):
                        phone = self._extract_phone(footer)
                        if phone:
                            data['phone'] = phone

                    if not data.get('street_address'):
                        address = self._extract_address(footer)
                        if address:
                            data.update(address)

        except:
            pass

        return data

    async def _scrape_about_page(self, session: aiohttp.ClientSession, domain: str) -> Dict[str, Any]:
        """Scrape about/locations pages for address."""
        data = {}
        about_urls = [
            f'{domain}/pages/about',
            f'{domain}/pages/about-us',
            f'{domain}/pages/locations',
            f'{domain}/pages/our-store',
            f'{domain}/pages/visit-us',
            f'{domain}/about',
        ]

        for url in about_urls:
            try:
                async with session.get(url, timeout=self.timeout) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        if not data.get('street_address'):
                            address = self._extract_address(soup)
                            if address and address.get('street_address'):
                                data.update(address)
                                break
            except:
                continue

        return data

    async def _scrape_schema_org(self, session: aiohttp.ClientSession, domain: str) -> Dict[str, Any]:
        """Extract address from Schema.org structured data (JSON-LD)."""
        data = {}

        try:
            async with session.get(domain, timeout=self.timeout) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                # Find JSON-LD scripts
                scripts = soup.find_all('script', type='application/ld+json')

                for script in scripts:
                    try:
                        schema_data = json.loads(script.string)

                        # Handle both single object and list
                        if isinstance(schema_data, list):
                            schemas = schema_data
                        else:
                            schemas = [schema_data]

                        for schema in schemas:
                            # Look for organization/local business schema
                            if schema.get('@type') in ['Organization', 'LocalBusiness', 'Store']:
                                address_obj = schema.get('address', {})

                                if isinstance(address_obj, dict):
                                    if not data.get('street_address') and address_obj.get('streetAddress'):
                                        data['street_address'] = address_obj.get('streetAddress')
                                        data['city'] = address_obj.get('addressLocality')
                                        data['state'] = address_obj.get('addressRegion')
                                        data['zip_code'] = address_obj.get('postalCode')
                                        data['country'] = address_obj.get('addressCountry', 'US')

                                if not data.get('phone') and schema.get('telephone'):
                                    data['phone'] = schema.get('telephone')

                    except (json.JSONDecodeError, AttributeError):
                        continue

        except:
            pass

        return data

    async def _check_shipping_policy(self, session: aiohttp.ClientSession, domain: str) -> Dict[str, Any]:
        """Check if store offers local delivery."""
        data = {'has_local_delivery': False}

        shipping_urls = [
            f'{domain}/pages/shipping',
            f'{domain}/policies/shipping-policy',
        ]

        local_keywords = [
            'local delivery',
            'same-day delivery',
            'local pickup',
            'deliver locally',
        ]

        for url in shipping_urls:
            try:
                async with session.get(url, timeout=self.timeout) as response:
                    if response.status == 200:
                        text = (await response.text()).lower()

                        for keyword in local_keywords:
                            if keyword in text:
                                data['has_local_delivery'] = True
                                return data
            except:
                continue

        return data

    def _extract_email(self, soup_or_tag) -> Optional[str]:
        """Extract email from HTML."""
        mailto_links = soup_or_tag.find_all('a', href=re.compile(r'^mailto:'))
        if mailto_links:
            return mailto_links[0]['href'].replace('mailto:', '').strip()

        text = soup_or_tag.get_text()
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None

    def _extract_phone(self, soup_or_tag) -> Optional[str]:
        """Extract phone number from HTML."""
        tel_links = soup_or_tag.find_all('a', href=re.compile(r'^tel:'))
        if tel_links:
            return tel_links[0]['href'].replace('tel:', '').strip()

        text = soup_or_tag.get_text()
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        return phones[0] if phones else None

    def _extract_address(self, soup_or_tag) -> Dict[str, Optional[str]]:
        """Extract address from HTML with multiple pattern matching."""
        address_data = {
            'street_address': None,
            'city': None,
            'state': None,
            'zip_code': None,
            'country': None,
        }

        # Try address tags first
        address_tags = soup_or_tag.find_all(['address', 'div', 'p'], class_=re.compile(r'(address|location|contact)', re.I))

        # Also search entire text if no address tags found
        if not address_tags:
            address_tags = [soup_or_tag]

        for tag in address_tags:
            text = tag.get_text()

            # Multiple US address patterns
            patterns = [
                # Pattern 1: 123 Main St, New York, NY 10001
                r'(\d+\s+[^,\n]+),\s*([^,\n]+),\s*([A-Z]{2})\s*(\d{5}(?:-\d{4})?)',
                # Pattern 2: New York, NY 10001 (city, state, zip)
                r'([^,\n]+),\s*([A-Z]{2})\s*(\d{5}(?:-\d{4})?)',
                # Pattern 3: 123 Main Street\nNew York, NY 10001
                r'(\d+\s+[^\n]+)\n\s*([^,\n]+),\s*([A-Z]{2})\s*(\d{5}(?:-\d{4})?)',
            ]

            for pattern in patterns:
                match = re.search(pattern, text)

                if match:
                    if len(match.groups()) == 4:
                        # Full address with street
                        address_data['street_address'] = match.group(1).strip()
                        address_data['city'] = match.group(2).strip()
                        address_data['state'] = match.group(3).strip()
                        address_data['zip_code'] = match.group(4).strip()
                    elif len(match.groups()) == 3:
                        # City, state, zip only
                        address_data['city'] = match.group(1).strip()
                        address_data['state'] = match.group(2).strip()
                        address_data['zip_code'] = match.group(3).strip()

                    address_data['country'] = 'US'
                    break

            if address_data['city']:  # Found something
                break

        return address_data


async def scrape_batch(domains: list, max_concurrent: int = 20) -> Dict[str, Dict[str, Any]]:
    """
    Scrape data for a batch of domains concurrently.

    Returns:
        dict of domain -> scraped_data
    """
    scraper = AsyncStoreScraper(max_concurrent=max_concurrent)
    results = {}

    async with aiohttp.ClientSession(headers=scraper.headers) as session:
        tasks = []
        for domain in domains:
            task = scraper.scrape(session, domain)
            tasks.append((domain, task))

        for domain, task in tasks:
            try:
                result = await task
                results[domain] = result
            except Exception as e:
                results[domain] = {'scrape_error': str(e)}

    return results


if __name__ == '__main__':
    # Test
    import time

    test_domains = ['allbirds.com', 'gymshark.com']

    start = time.time()
    results = asyncio.run(scrape_batch(test_domains))
    elapsed = time.time() - start

    print(f"\nScraped {len(test_domains)} domains in {elapsed:.2f}s\n")

    for domain, data in results.items():
        print(f"{domain}:")
        for key, value in data.items():
            print(f"  {key}: {value}")
        print()

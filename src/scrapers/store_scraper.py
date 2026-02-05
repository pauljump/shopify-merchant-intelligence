"""Scrape data from Shopify stores."""

import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, Optional, Any
import json


class StoreScraper:
    """Scrape contact info and business data from Shopify stores."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def scrape(self, domain: str) -> Dict[str, Any]:
        """
        Scrape all available data from a store.

        Returns dict with: email, phone, address, city, state, zip, country, etc.
        """
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
            # 1. Check contact page
            contact_data = self._scrape_contact_page(domain)
            data.update(contact_data)

            # 2. Check footer (often has address)
            if not data['street_address']:
                homepage_data = self._scrape_homepage_footer(domain)
                data.update(homepage_data)

            # 3. Check Schema.org structured data
            if not data['street_address']:
                schema_data = self._scrape_schema_org(domain)
                data.update(schema_data)

            # 4. Check shipping/delivery policy
            shipping_data = self._check_shipping_policy(domain)
            data.update(shipping_data)

        except Exception as e:
            data['scrape_error'] = str(e)

        return data

    def _scrape_contact_page(self, domain: str) -> Dict[str, Any]:
        """Scrape contact page."""
        data = {}

        # Try common contact URLs
        contact_urls = [
            f'{domain}/pages/contact',
            f'{domain}/pages/contact-us',
            f'{domain}/contact',
            f'{domain}/contact-us',
        ]

        for url in contact_urls:
            try:
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract email
                    if not data.get('email'):
                        email = self._extract_email(soup)
                        if email:
                            data['email'] = email

                    # Extract phone
                    if not data.get('phone'):
                        phone = self._extract_phone(soup)
                        if phone:
                            data['phone'] = phone

                    # Extract address
                    if not data.get('street_address'):
                        address = self._extract_address(soup)
                        if address:
                            data.update(address)

                    break  # Found contact page, stop trying

            except:
                continue

        return data

    def _scrape_homepage_footer(self, domain: str) -> Dict[str, Any]:
        """Scrape homepage footer for address."""
        data = {}

        try:
            response = self.session.get(domain, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Look in footer
            footer = soup.find('footer')
            if footer:
                # Extract email
                if not data.get('email'):
                    email = self._extract_email(footer)
                    if email:
                        data['email'] = email

                # Extract phone
                if not data.get('phone'):
                    phone = self._extract_phone(footer)
                    if phone:
                        data['phone'] = phone

                # Extract address
                if not data.get('street_address'):
                    address = self._extract_address(footer)
                    if address:
                        data.update(address)

        except:
            pass

        return data

    def _scrape_schema_org(self, domain: str) -> Dict[str, Any]:
        """Extract Schema.org structured data."""
        data = {}

        try:
            response = self.session.get(domain, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find JSON-LD scripts
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                try:
                    schema = json.loads(script.string)

                    # Handle arrays
                    if isinstance(schema, list):
                        schema = schema[0] if schema else {}

                    # Look for Organization or LocalBusiness
                    if schema.get('@type') in ['Organization', 'LocalBusiness', 'Store']:
                        if 'address' in schema:
                            addr = schema['address']
                            if isinstance(addr, dict):
                                data['street_address'] = addr.get('streetAddress')
                                data['city'] = addr.get('addressLocality')
                                data['state'] = addr.get('addressRegion')
                                data['zip_code'] = addr.get('postalCode')
                                data['country'] = addr.get('addressCountry')

                        if 'email' in schema:
                            data['email'] = schema['email']

                        if 'telephone' in schema:
                            data['phone'] = schema['telephone']

                        if 'name' in schema:
                            data['company_name'] = schema['name']

                except:
                    continue

        except:
            pass

        return data

    def _check_shipping_policy(self, domain: str) -> Dict[str, Any]:
        """Check if store offers local delivery."""
        data = {'has_local_delivery': False}

        shipping_urls = [
            f'{domain}/pages/shipping',
            f'{domain}/pages/shipping-policy',
            f'{domain}/policies/shipping-policy',
        ]

        local_delivery_keywords = [
            'local delivery',
            'same-day delivery',
            'same day delivery',
            'local pickup',
            'deliver locally',
            'delivery within',
            'local area delivery',
        ]

        for url in shipping_urls:
            try:
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    text = response.text.lower()

                    for keyword in local_delivery_keywords:
                        if keyword in text:
                            data['has_local_delivery'] = True
                            break

                    if data['has_local_delivery']:
                        break

            except:
                continue

        return data

    def _extract_email(self, soup_or_tag) -> Optional[str]:
        """Extract email from HTML."""
        # Find mailto links
        mailto_links = soup_or_tag.find_all('a', href=re.compile(r'^mailto:'))
        if mailto_links:
            email = mailto_links[0]['href'].replace('mailto:', '').strip()
            return email

        # Search for email patterns in text
        text = soup_or_tag.get_text()
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            return emails[0]

        return None

    def _extract_phone(self, soup_or_tag) -> Optional[str]:
        """Extract phone number from HTML."""
        # Find tel links
        tel_links = soup_or_tag.find_all('a', href=re.compile(r'^tel:'))
        if tel_links:
            phone = tel_links[0]['href'].replace('tel:', '').strip()
            return phone

        # Search for phone patterns
        text = soup_or_tag.get_text()
        # US phone patterns
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            return phones[0]

        return None

    def _extract_address(self, soup_or_tag) -> Dict[str, Optional[str]]:
        """Extract address from HTML."""
        address_data = {
            'street_address': None,
            'city': None,
            'state': None,
            'zip_code': None,
            'country': None,
        }

        # Look for address tags or divs
        address_tags = soup_or_tag.find_all(['address', 'div'], class_=re.compile(r'address', re.I))

        for tag in address_tags:
            text = tag.get_text()

            # Try to parse US address
            # Pattern: street, city, state zip
            us_pattern = r'([^,\n]+),\s*([^,\n]+),\s*([A-Z]{2})\s*(\d{5})'
            match = re.search(us_pattern, text)

            if match:
                address_data['street_address'] = match.group(1).strip()
                address_data['city'] = match.group(2).strip()
                address_data['state'] = match.group(3).strip()
                address_data['zip_code'] = match.group(4).strip()
                address_data['country'] = 'US'
                break

        return address_data


if __name__ == '__main__':
    # Test
    scraper = StoreScraper()

    test_domains = [
        'allbirds.com',
    ]

    for domain in test_domains:
        print(f"\n{'='*60}")
        print(f"Scraping: {domain}")
        print('='*60)
        data = scraper.scrape(domain)
        for key, value in data.items():
            print(f"{key}: {value}")

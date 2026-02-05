"""Discover Shopify stores from public GitHub datasets."""

import requests
from typing import List, Set, Dict
import re


class GitHubDatasetDiscovery:
    """Find Shopify stores from public GitHub datasets."""

    def __init__(self):
        self.known_datasets = [
            # Public repos with Shopify store lists
            'https://raw.githubusercontent.com/darenr/public_store_ids/master/shopify_domains.txt',
            # Add more as we find them
        ]

    def discover(self, limit: int = 1000) -> Set[str]:
        """
        Discover Shopify store domains from GitHub datasets.

        Returns:
            Set of domain names
        """
        domains = set()

        # Method 1: Known dataset URLs
        for url in self.known_datasets:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    # Parse domains from response
                    lines = response.text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Clean domain
                            domain = self._clean_domain(line)
                            if domain:
                                domains.add(domain)

                        if len(domains) >= limit:
                            break

            except Exception as e:
                print(f"Error fetching {url}: {e}")

            if len(domains) >= limit:
                break

        # Method 2: Use sample CSV domains as starting point
        # (We can expand this to search for more datasets)

        return domains

    def _clean_domain(self, text: str) -> str:
        """Clean and validate domain name."""
        # Remove http/https
        text = re.sub(r'https?://', '', text)

        # Remove www
        text = re.sub(r'^www\.', '', text)

        # Remove trailing slashes
        text = text.rstrip('/')

        # Remove paths
        if '/' in text:
            text = text.split('/')[0]

        # Basic validation
        if '.' in text and len(text) > 3:
            return text.lower()

        return None


class SeedListDiscovery:
    """Use seed list from CSV files or manual input."""

    def __init__(self, seed_file: str = None):
        self.seed_file = seed_file
        self.seed_domains = set()

    def add_seeds_from_csv(self, csv_path: str) -> List[Dict]:
        """
        Import store data from CSV file.

        Returns list of dicts with domain and metadata.
        """
        import csv

        stores = []

        try:
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Extract actual Shopify subdomains from "Location on Site"
                    location = row.get('Location on Site', '').strip()

                    if location:
                        # Parse subdomains (separated by semicolons)
                        subdomains = location.split(';')

                        for subdomain in subdomains:
                            subdomain = subdomain.strip()

                            # Clean domain
                            subdomain = re.sub(r'https?://', '', subdomain)
                            subdomain = re.sub(r'^www\.', '', subdomain)
                            subdomain = subdomain.split('/')[0]

                            # Skip wildcards
                            if '*' in subdomain or not subdomain:
                                continue

                            # Create store entry with metadata from CSV
                            store_data = {
                                'domain': subdomain.lower(),
                                'company_name': row.get('Company', '').strip(),
                                'city': row.get('City', '').strip() or None,
                                'state': row.get('State', '').strip() or None,
                                'zip_code': row.get('Zip', '').strip() or None,
                                'country': row.get('Country', '').strip() or None,
                                'email': self._parse_emails(row.get('Emails', '')),
                                'phone': self._parse_phones(row.get('Telephones', '')),
                                'vertical': row.get('Vertical', '').strip() or None,
                                'revenue_estimate': self._parse_revenue(row.get('Sales Revenue USD', '')),
                                'employees_estimate': self._parse_employees(row.get('Employees', '')),
                            }

                            stores.append(store_data)

        except Exception as e:
            print(f"Error reading CSV: {e}")

        return stores

    def _parse_emails(self, email_str: str) -> str:
        """Extract first email from semicolon-separated list."""
        if not email_str:
            return None
        emails = email_str.split(';')
        for email in emails:
            email = email.strip()
            if '@' in email and not email.startswith('n/a@'):
                return email
        return None

    def _parse_phones(self, phone_str: str) -> str:
        """Extract first phone from string."""
        if not phone_str:
            return None
        phones = phone_str.split(';')
        for phone in phones:
            phone = phone.replace('ph:', '').strip()
            if phone and len(phone) > 5:
                return phone
        return None

    def _parse_revenue(self, revenue_str: str) -> float:
        """Parse revenue string to float."""
        if not revenue_str:
            return None
        try:
            # Remove $, commas
            revenue_str = revenue_str.replace('$', '').replace(',', '')
            return float(revenue_str)
        except:
            return None

    def _parse_employees(self, emp_str: str) -> int:
        """Parse employee count."""
        if not emp_str:
            return None
        try:
            return int(emp_str)
        except:
            return None

    def discover(self, limit: int = 1000) -> Set[str]:
        """Get seed domains."""
        if self.seed_file:
            return self.add_seeds_from_csv(self.seed_file)
        return set()


if __name__ == '__main__':
    # Test GitHub discovery
    github_discovery = GitHubDatasetDiscovery()
    domains = github_discovery.discover(limit=10)
    print(f"Found {len(domains)} domains from GitHub:")
    for domain in list(domains)[:10]:
        print(f"  - {domain}")

    # Test CSV import
    print("\nTesting CSV import...")
    seed_discovery = SeedListDiscovery()
    csv_path = "/Users/pjump/Downloads/Copy of Shopify Data (Sample) - All-Live-Shopify-Sites.csv"
    csv_domains = seed_discovery.add_seeds_from_csv(csv_path)
    print(f"Found {len(csv_domains)} domains from CSV:")
    for domain in list(csv_domains)[:10]:
        print(f"  - {domain}")

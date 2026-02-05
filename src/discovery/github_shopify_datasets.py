"""Find Shopify store datasets on GitHub."""

import requests
from typing import List, Set
import time


class GitHubShopifyDatasets:
    """Discover Shopify stores from public GitHub datasets."""

    def __init__(self):
        # Known public datasets with Shopify store lists
        self.datasets = [
            # 5,371 Shopify stores (JSON with Domain field)
            'https://raw.githubusercontent.com/durationsyrup/JSON-List-of-5000-Shopify-Stores/master/List.txt',

            # Headless Shopify stores
            'https://raw.githubusercontent.com/isamisushi/awesome-headless-shopify-stores/main/README.md',
        ]

    def fetch_from_url(self, url: str) -> Set[str]:
        """Fetch domains from a single URL."""
        domains = set()

        try:
            print(f"Fetching from: {url}")
            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                content = response.text

                # Handle JSON format (including .txt files with JSON content)
                if url.endswith('.json') or url.endswith('.txt'):
                    import json
                    try:
                        data = json.loads(content)

                        # Handle array of stores
                        if isinstance(data, list):
                            for item in data:
                                # Could be string or object
                                if isinstance(item, str):
                                    domain = self._clean_domain(item)
                                    if domain:
                                        domains.add(domain)
                                elif isinstance(item, dict):
                                    # Look for domain/url fields (case-insensitive)
                                    for key in ['Domain', 'domain', 'url', 'URL', 'store', 'website', 'link']:
                                        if key in item:
                                            domain = self._clean_domain(str(item[key]))
                                            if domain:
                                                domains.add(domain)
                                                break
                    except json.JSONDecodeError:
                        pass

                    # If JSON parsing succeeded, skip text processing
                    if domains:
                        print(f"  Found {len(domains)} domains")
                        return domains

                else:
                    # Handle text/markdown formats
                    lines = content.split('\n')

                    for line in lines:
                        line = line.strip()

                        # Skip comments and empty lines
                        if not line or line.startswith('#'):
                            continue

                        # Extract domains from markdown links [text](url)
                        import re
                        markdown_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', line)
                        for text, url in markdown_links:
                            domain = self._clean_domain(url)
                            if domain:
                                domains.add(domain)

                        # Handle CSV (take first column)
                        if ',' in line:
                            line = line.split(',')[0].strip()

                        # Extract plain domains
                        domain = self._clean_domain(line)
                        if domain:
                            domains.add(domain)

                print(f"  Found {len(domains)} domains")

        except Exception as e:
            print(f"  Error: {e}")

        return domains

    def discover(self, limit: int = 10000) -> Set[str]:
        """
        Discover Shopify store domains from all known datasets.

        Returns:
            Set of domain names
        """
        all_domains = set()

        for url in self.datasets:
            domains = self.fetch_from_url(url)
            all_domains.update(domains)

            if len(all_domains) >= limit:
                break

            time.sleep(1)  # Be nice to GitHub

        return set(list(all_domains)[:limit])

    def search_github_repos(self, query: str = "shopify stores") -> List[str]:
        """
        Search GitHub for repos containing Shopify store lists.

        Note: Requires GitHub API token for higher rate limits.
        """
        # TODO: Implement GitHub API search
        # This would search for repos with files like:
        # - shopify_domains.txt
        # - stores.csv
        # etc.
        pass

    def _clean_domain(self, text: str) -> str:
        """Clean and validate domain name."""
        import re

        # Remove http/https
        text = re.sub(r'https?://', '', text)

        # Remove www
        text = re.sub(r'^www\.', '', text)

        # Remove trailing slashes
        text = text.rstrip('/')

        # Remove paths
        if '/' in text:
            text = text.split('/')[0]

        # Remove quotes
        text = text.strip('"').strip("'")

        # Basic validation
        if '.' in text and len(text) > 3 and not text.startswith('.'):
            return text.lower()

        return None


if __name__ == '__main__':
    # Test
    discovery = GitHubShopifyDatasets()
    domains = discovery.discover(limit=100)

    print(f"\n{'='*60}")
    print(f"Found {len(domains)} Shopify store domains from GitHub datasets")
    print('='*60)

    for i, domain in enumerate(list(domains)[:10], 1):
        print(f"{i}. {domain}")

    if len(domains) > 10:
        print(f"\n... and {len(domains) - 10} more")

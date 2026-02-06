"""
GitHub Mass Search for Shopify Store Datasets

Searches GitHub API for repositories containing Shopify store lists.
Target: Find 10-20 repos with 1K-10K stores each = 50K-200K total stores.
"""

import requests
import time
from typing import List, Set, Dict
import json
import re
from urllib.parse import urlparse


class GitHubMassSearch:
    """Search GitHub for Shopify store datasets at scale."""

    def __init__(self, github_token: str = None):
        """
        Args:
            github_token: Optional GitHub personal access token for higher rate limits
                         (5000 req/hour vs 60 req/hour for unauthenticated)
        """
        self.github_token = github_token
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
        }
        if github_token:
            self.headers['Authorization'] = f'token {github_token}'

        # Search queries targeting Shopify store lists
        self.search_queries = [
            'shopify stores in:readme',
            'shopify domains in:file',
            'shopify sites list',
            'myshopify.com in:file',
            'shopify store list',
            'ecommerce sites shopify',
            'shopify merchants',
            'shopify plus stores',
            'shopify headless stores',
            'shopify store dataset',
        ]

    def discover(self, max_repos_per_query: int = 10) -> Dict[str, List[str]]:
        """
        Search GitHub for Shopify store datasets.

        Args:
            max_repos_per_query: Max repositories to check per search query

        Returns:
            Dictionary mapping repo URLs to lists of discovered store domains
        """
        print(f"🔍 Searching GitHub for Shopify store datasets...")
        print(f"📊 Running {len(self.search_queries)} search queries...")

        discovered_repos = {}
        all_domains = set()

        for query in self.search_queries:
            print(f"\n🔎 Query: '{query}'")
            repos = self._search_repositories(query, max_results=max_repos_per_query)

            for repo in repos:
                repo_url = repo['html_url']

                # Skip if already processed
                if repo_url in discovered_repos:
                    continue

                print(f"  📦 Checking: {repo['full_name']}")

                # Try to find store lists in this repo
                domains = self._extract_domains_from_repo(repo)

                if domains:
                    discovered_repos[repo_url] = list(domains)
                    all_domains.update(domains)
                    print(f"    ✅ Found {len(domains)} domains")
                else:
                    print(f"    ⏭️  No domains found")

                # Rate limit safety
                time.sleep(1)

        print(f"\n{'='*60}")
        print(f"🎯 Discovery Complete!")
        print(f"{'='*60}")
        print(f"📁 Repositories found: {len(discovered_repos)}")
        print(f"🌐 Total unique domains: {len(all_domains)}")
        print(f"{'='*60}\n")

        # Save results
        self._save_results(discovered_repos, all_domains)

        return discovered_repos

    def _search_repositories(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search GitHub repositories."""
        url = 'https://api.github.com/search/repositories'
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': min(max_results, 100)
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('items', [])[:max_results]
        except Exception as e:
            print(f"    ⚠️  Search error: {e}")
            return []

    def _extract_domains_from_repo(self, repo: Dict) -> Set[str]:
        """Extract Shopify domains from a repository."""
        domains = set()

        # Try common file locations
        file_paths = [
            'README.md',
            'stores.txt',
            'stores.json',
            'domains.txt',
            'domains.json',
            'List.txt',
            'shopify_stores.json',
            'shopify_stores.txt',
            'data/stores.json',
            'data/stores.txt',
            'list.txt',
            'list.json',
        ]

        for file_path in file_paths:
            try:
                # Construct raw GitHub URL
                raw_url = f"https://raw.githubusercontent.com/{repo['full_name']}/{repo['default_branch']}/{file_path}"

                response = requests.get(raw_url, timeout=10)
                if response.status_code == 200:
                    content = response.text
                    extracted = self._parse_content_for_domains(content)
                    if extracted:
                        domains.update(extracted)

            except Exception:
                continue

        return domains

    def _parse_content_for_domains(self, content: str) -> Set[str]:
        """Parse content for Shopify domains."""
        domains = set()

        # Try JSON parsing first
        try:
            data = json.loads(content)
            domains.update(self._extract_domains_from_json(data))
        except json.JSONDecodeError:
            # Not JSON, try line-by-line or regex
            pass

        # Regex patterns for domains
        patterns = [
            r'https?://([a-zA-Z0-9-]+\.myshopify\.com)',
            r'https?://([a-zA-Z0-9-]+\.[a-z]{2,})',
            r'"domain":\s*"([^"]+)"',
            r'"Domain":\s*"([^"]+)"',
            r'"url":\s*"([^"]+)"',
            r'"URL":\s*"([^"]+)"',
            r'\b([a-zA-Z0-9-]+\.myshopify\.com)\b',
            r'\b([a-zA-Z0-9-]+\.com)\b',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                domain = self._clean_domain(match)
                if domain and self._is_valid_domain(domain):
                    domains.add(domain)

        return domains

    def _extract_domains_from_json(self, data) -> Set[str]:
        """Recursively extract domains from JSON data."""
        domains = set()

        if isinstance(data, list):
            for item in data:
                domains.update(self._extract_domains_from_json(item))
        elif isinstance(data, dict):
            # Check common keys
            for key in ['domain', 'Domain', 'url', 'URL', 'site', 'website', 'store_url', 'shop_url']:
                if key in data:
                    domain = self._clean_domain(str(data[key]))
                    if domain:
                        domains.add(domain)
            # Recurse into nested objects
            for value in data.values():
                if isinstance(value, (dict, list)):
                    domains.update(self._extract_domains_from_json(value))

        return domains

    def _clean_domain(self, url: str) -> str:
        """Clean and normalize domain."""
        if not url:
            return ""

        # Remove whitespace
        url = url.strip()

        # Add https:// if no protocol
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'

        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path

            # Remove www.
            if domain.startswith('www.'):
                domain = domain[4:]

            # Remove trailing slashes and paths
            domain = domain.split('/')[0]

            return domain.lower()
        except Exception:
            return ""

    def _is_valid_domain(self, domain: str) -> bool:
        """Check if domain looks valid."""
        if not domain or len(domain) < 4:
            return False

        # Must contain at least one dot
        if '.' not in domain:
            return False

        # Skip common false positives
        skip_domains = ['example.com', 'localhost', 'test.com', 'domain.com']
        if domain in skip_domains:
            return False

        return True

    def _save_results(self, discovered_repos: Dict, all_domains: Set):
        """Save discovery results to files."""
        import os

        # Create output directory
        os.makedirs('data/github_mass_search', exist_ok=True)

        # Save repository metadata
        with open('data/github_mass_search/repos_found.json', 'w') as f:
            json.dump(discovered_repos, f, indent=2)

        # Save all domains as simple text file
        with open('data/github_mass_search/all_domains.txt', 'w') as f:
            for domain in sorted(all_domains):
                f.write(f"{domain}\n")

        print(f"💾 Saved results:")
        print(f"   - data/github_mass_search/repos_found.json ({len(discovered_repos)} repos)")
        print(f"   - data/github_mass_search/all_domains.txt ({len(all_domains)} domains)")


if __name__ == '__main__':
    # Run discovery
    searcher = GitHubMassSearch()
    results = searcher.discover(max_repos_per_query=20)

    print("\n📊 Top repositories by domain count:")
    sorted_repos = sorted(results.items(), key=lambda x: len(x[1]), reverse=True)
    for repo_url, domains in sorted_repos[:10]:
        print(f"  {len(domains):5d} domains - {repo_url}")

"""
Targeted GitHub search for USA Shopify stores by industry/location.

Focuses on industries with local delivery (food, grocery, retail).
"""

import requests
import time
from typing import Set
import json


class TargetedGitHubSearch:
    """Search GitHub for USA-focused Shopify store lists."""

    def __init__(self, github_token: str = None):
        self.github_token = github_token
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if github_token:
            self.headers['Authorization'] = f'token {github_token}'

        # Targeted search queries for USA stores with local delivery
        self.search_queries = [
            # Geographic
            'shopify stores USA',
            'shopify stores "United States"',
            'shopify stores NYC',
            'shopify stores "Los Angeles"',
            'shopify stores "San Francisco"',
            'shopify stores Chicago',
            'shopify stores Texas',
            'shopify stores California',

            # Industry - Food/Grocery (high local delivery probability)
            'shopify grocery stores',
            'shopify food delivery',
            'shopify restaurant',
            'shopify bakery',
            'shopify coffee shops',
            'shopify meal kit',
            'shopify farm store',

            # Industry - Retail with local delivery
            'shopify local delivery',
            'shopify same-day delivery',
            'shopify local pickup',
            'shopify curbside',
            'shopify retail stores',
            'shopify boutique',

            # Business directories
            'USA shopify merchants',
            'American shopify stores',
            'shopify plus stores USA',
        ]

    def discover(self, max_repos_per_query: int = 20) -> dict:
        """
        Search GitHub for targeted Shopify store datasets.

        Returns:
            Dict mapping repo URLs to domains found
        """
        print(f"🔍 Targeted GitHub Search for USA Shopify Stores")
        print(f"📊 Running {len(self.search_queries)} targeted queries...\n")

        discovered_repos = {}
        all_domains = set()

        for query in self.search_queries:
            print(f"🔎 Query: '{query}'")

            # Search code and repositories
            code_results = self._search_code(query, max_results=10)
            repo_results = self._search_repositories(query, max_results=10)

            all_results = code_results + repo_results

            if all_results:
                print(f"  ✅ Found {len(all_results)} results")

                for result in all_results:
                    if result['type'] == 'code':
                        # Extract domain from code file
                        domains = self._extract_domains_from_code(result)
                        if domains:
                            repo_url = result.get('repository', {}).get('html_url', 'unknown')
                            if repo_url not in discovered_repos:
                                discovered_repos[repo_url] = []
                            discovered_repos[repo_url].extend(list(domains))
                            all_domains.update(domains)
                    else:
                        # Check repository
                        repo_url = result['html_url']
                        if repo_url not in discovered_repos:
                            domains = self._extract_domains_from_repo(result)
                            if domains:
                                discovered_repos[repo_url] = list(domains)
                                all_domains.update(domains)
            else:
                print(f"  ⏭️  No results")

            time.sleep(2)  # Rate limiting

        print(f"\n{'='*60}")
        print(f"🎯 Targeted Search Complete!")
        print(f"{'='*60}")
        print(f"📁 Results found: {len(discovered_repos)}")
        print(f"🌐 Total unique domains: {len(all_domains)}")
        print(f"{'='*60}\n")

        # Save results
        self._save_results(discovered_repos, all_domains)
        return discovered_repos

    def _search_code(self, query: str, max_results: int = 10):
        """Search GitHub code."""
        url = 'https://api.github.com/search/code'
        params = {
            'q': f'{query} extension:csv OR extension:json OR extension:txt',
            'sort': 'indexed',
            'per_page': max_results
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                return [{'type': 'code', **item} for item in items[:max_results]]
        except Exception as e:
            print(f"    ⚠️  Code search error: {e}")

        return []

    def _search_repositories(self, query: str, max_results: int = 10):
        """Search GitHub repositories."""
        url = 'https://api.github.com/search/repositories'
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': max_results
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                return [{'type': 'repo', **item} for item in items[:max_results]]
        except Exception:
            pass

        return []

    def _extract_domains_from_code(self, code_item: dict) -> Set[str]:
        """Extract domains from a code file."""
        import re

        try:
            # Fetch raw content
            raw_url = code_item.get('download_url') or code_item.get('url', '').replace('api.github.com/repos', 'raw.githubusercontent.com').replace('/contents/', '/master/')

            response = requests.get(raw_url, timeout=10)
            if response.status_code == 200:
                content = response.text

                # Look for domains
                domain_pattern = r'([a-zA-Z0-9-]+\.(myshopify\.com|com|net|org|io))'
                matches = re.findall(domain_pattern, content)
                domains = {match[0] for match in matches if self._is_valid_domain(match[0])}

                return domains
        except:
            pass

        return set()

    def _extract_domains_from_repo(self, repo: dict) -> Set[str]:
        """Extract domains from repository."""
        # Similar to github_mass_search.py implementation
        domains = set()

        file_paths = ['README.md', 'stores.txt', 'stores.json', 'domains.txt', 'list.txt']

        for file_path in file_paths:
            try:
                raw_url = f"https://raw.githubusercontent.com/{repo['full_name']}/{repo['default_branch']}/{file_path}"
                response = requests.get(raw_url, timeout=10)

                if response.status_code == 200:
                    content = response.text

                    # Try JSON
                    try:
                        data = json.loads(content)
                        if isinstance(data, list):
                            for item in data:
                                if isinstance(item, dict):
                                    for key in ['domain', 'Domain', 'url', 'store']:
                                        if key in item:
                                            domain = self._clean_domain(str(item[key]))
                                            if domain:
                                                domains.add(domain)
                    except:
                        pass

                    # Regex patterns
                    import re
                    patterns = [
                        r'([a-zA-Z0-9-]+\.myshopify\.com)',
                        r'([a-zA-Z0-9-]+\.(com|net|org))'
                    ]

                    for pattern in patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            domain = match if isinstance(match, str) else match[0]
                            domain = self._clean_domain(domain)
                            if domain:
                                domains.add(domain)
            except:
                continue

        return domains

    def _clean_domain(self, url: str) -> str:
        """Clean domain."""
        if not url:
            return ""

        url = url.strip().lower()
        url = url.replace('https://', '').replace('http://', '').replace('www.', '')
        domain = url.split('/')[0].split('?')[0]

        return domain if self._is_valid_domain(domain) else ""

    def _is_valid_domain(self, domain: str) -> bool:
        """Check if domain is valid."""
        if not domain or len(domain) < 4:
            return False
        if '.' not in domain:
            return False
        skip_domains = ['example.com', 'localhost', 'test.com', 'domain.com']
        return domain not in skip_domains

    def _save_results(self, discovered_repos: dict, all_domains: Set):
        """Save results."""
        import os

        os.makedirs('data/targeted_search', exist_ok=True)

        with open('data/targeted_search/repos_found.json', 'w') as f:
            json.dump(discovered_repos, f, indent=2)

        with open('data/targeted_search/all_domains.txt', 'w') as f:
            for domain in sorted(all_domains):
                f.write(f"{domain}\n")

        print(f"💾 Saved to data/targeted_search/")


if __name__ == '__main__':
    searcher = TargetedGitHubSearch()
    results = searcher.discover(max_repos_per_query=20)

    print(f"\n📊 Top sources:")
    sorted_repos = sorted(results.items(), key=lambda x: len(x[1]), reverse=True)
    for repo_url, domains in sorted_repos[:10]:
        print(f"  {len(domains):5d} domains - {repo_url}")

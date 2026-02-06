#!/usr/bin/env python3
"""
Clean and validate domains discovered from social media
"""

import re
from pathlib import Path
from typing import Set


def is_valid_myshopify_domain(domain: str) -> bool:
    """Check if domain is a valid myshopify.com domain"""
    # Must end with .myshopify.com (not just .myshopify)
    if not domain.endswith('.myshopify.com'):
        return False

    # Must have a subdomain
    parts = domain.split('.')
    if len(parts) != 3:  # subdomain.myshopify.com
        return False

    # Subdomain must be valid
    subdomain = parts[0]
    if not subdomain or len(subdomain) < 2:
        return False

    # No spaces or invalid characters
    if not re.match(r'^[a-zA-Z0-9-]+$', subdomain):
        return False

    # Exclude obvious test/example domains
    excluded_subdomains = {
        'abc', 'test', 'demo', 'example', 'yourstore',
        'brandname', 'appsfolder', 'admin', 'api', 'apps'
    }
    if subdomain.lower() in excluded_subdomains:
        return False

    return True


def is_valid_custom_domain(domain: str) -> bool:
    """Check if domain is a potentially valid custom domain"""
    # Must have at least one dot
    if '.' not in domain:
        return False

    # Must end with valid TLD
    valid_tlds = ['.com', '.net', '.org', '.co', '.io', '.shop', '.store', '.us']
    if not any(domain.endswith(tld) for tld in valid_tlds):
        return False

    # Must not be a known non-store domain
    excluded_domains = {
        'shopify.com', 'amazon.com', 'google.com', 'apple.com',
        'ahrefs.com', 'booking.com', 'adobe.com', 'blogspot.com',
        '99designs.de', 'boostcommerce.net', 'capitalandgrowth.org',
        'adspify.com'
    }

    domain_lower = domain.lower()
    if domain_lower in excluded_domains:
        return False

    # Must not contain shopify.com subdomains (admin, apps, blog, etc.)
    if 'shopify.com' in domain_lower and domain_lower != 'shopify.com':
        return False

    # Must not be obvious invalid formats
    if domain.startswith('-') or domain.endswith('-'):
        return False

    # Must have valid format
    if not re.match(r'^[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+$', domain):
        return False

    return True


def clean_domains(input_file: str, output_file: str) -> dict:
    """Clean and validate domains from input file"""
    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        print(f"Error: {input_file} not found")
        return {}

    # Read all domains
    with open(input_path, 'r') as f:
        raw_domains = {line.strip() for line in f if line.strip()}

    print(f"📥 Read {len(raw_domains)} raw domains")

    # Validate and clean
    valid_myshopify = set()
    valid_custom = set()
    invalid = set()

    for domain in raw_domains:
        domain = domain.lower().strip().rstrip('.')

        if is_valid_myshopify_domain(domain):
            valid_myshopify.add(domain)
        elif is_valid_custom_domain(domain):
            valid_custom.add(domain)
        else:
            invalid.add(domain)

    # Save cleaned domains
    all_valid = valid_myshopify | valid_custom

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        for domain in sorted(all_valid):
            f.write(f"{domain}\n")

    # Generate report
    report = {
        'total_raw': len(raw_domains),
        'valid_myshopify': len(valid_myshopify),
        'valid_custom': len(valid_custom),
        'total_valid': len(all_valid),
        'invalid': len(invalid)
    }

    print(f"\n✅ Validation Results:")
    print(f"   Valid MyShopify domains: {report['valid_myshopify']}")
    print(f"   Valid custom domains: {report['valid_custom']}")
    print(f"   Total valid: {report['total_valid']}")
    print(f"   Invalid/excluded: {report['invalid']}")

    print(f"\n💾 Saved {report['total_valid']} clean domains to {output_file}")

    # Show samples
    if valid_myshopify:
        print(f"\n📋 Sample MyShopify domains:")
        for domain in sorted(valid_myshopify)[:10]:
            print(f"   - {domain}")

    if valid_custom:
        print(f"\n📋 Sample custom domains (need Shopify validation):")
        for domain in sorted(valid_custom)[:10]:
            print(f"   - {domain}")

    return report


def main():
    input_file = "/Users/pjump/Desktop/projects/shopify-merchant-intelligence/data/social_media/domains.txt"
    output_file = "/Users/pjump/Desktop/projects/shopify-merchant-intelligence/data/social_media/clean_domains.txt"

    report = clean_domains(input_file, output_file)

    return report


if __name__ == "__main__":
    main()

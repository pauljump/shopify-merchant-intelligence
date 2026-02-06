"""
Generate 150+ Google Dork Queries for Manual or API Use

Creates comprehensive list of queries optimized for finding USA Shopify stores.
Output can be used with:
- Manual Google searches
- SerpAPI
- Google Custom Search API
- Other search tools
"""

import os


def generate_all_queries():
    """Generate 150+ targeted queries."""
    queries = []

    # ===== TOP 50 USA CITIES =====
    print("Generating city queries...")
    cities = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
        "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
        "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
        "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington DC",
        "Boston", "Nashville", "Detroit", "Portland", "Las Vegas",
        "Oklahoma City", "Albuquerque", "Tucson", "Sacramento", "Kansas City",
        "Mesa", "Atlanta", "Miami", "Raleigh", "Minneapolis",
        "Cleveland", "Tampa", "New Orleans", "Aurora", "Anaheim",
        "St. Louis", "Pittsburgh", "Cincinnati", "Orlando", "Riverside",
        "Stockton", "Lexington", "Henderson", "Omaha", "Wichita"
    ]

    for city in cities:
        queries.append(f'"powered by Shopify" "{city}"')

    # ===== TOP 30 STATES =====
    print("Generating state queries...")
    states = [
        "California", "Texas", "Florida", "New York", "Pennsylvania",
        "Illinois", "Ohio", "Georgia", "North Carolina", "Michigan",
        "New Jersey", "Virginia", "Washington", "Arizona", "Massachusetts",
        "Tennessee", "Indiana", "Missouri", "Maryland", "Wisconsin",
        "Colorado", "Minnesota", "South Carolina", "Alabama", "Louisiana",
        "Kentucky", "Oregon", "Oklahoma", "Connecticut", "Utah"
    ]

    for state in states:
        queries.append(f'Shopify "{state}" store')

    # ===== INDUSTRY VERTICALS (40) =====
    print("Generating industry queries...")
    industries = [
        # Food & Beverage
        ("grocery store", "Shopify USA"),
        ("bakery", "powered by Shopify"),
        ("coffee shop", "Shopify"),
        ("restaurant", "Shopify ordering"),
        ("farm stand", "Shopify"),
        ("organic food", "Shopify"),
        ("butcher shop", "Shopify"),
        ("wine shop", "Shopify"),
        ("brewery", "Shopify"),
        ("juice bar", "Shopify"),
        ("deli", "Shopify USA"),
        ("catering", "Shopify"),

        # Retail
        ("bookstore", "powered by Shopify"),
        ("clothing boutique", "Shopify"),
        ("shoe store", "Shopify"),
        ("furniture store", "Shopify"),
        ("home decor", "Shopify"),
        ("pet store", "Shopify"),
        ("toy store", "Shopify"),
        ("sporting goods", "Shopify"),
        ("electronics", "Shopify"),
        ("hardware store", "Shopify"),
        ("bike shop", "Shopify"),
        ("outdoor gear", "Shopify"),

        # Fashion & Beauty
        ("jewelry", "Shopify"),
        ("cosmetics", "Shopify USA"),
        ("salon products", "Shopify"),
        ("fashion brand", "Shopify"),
        ("accessories", "Shopify"),
        ("handbags", "Shopify"),

        # Specialty
        ("florist", "Shopify"),
        ("gift shop", "Shopify"),
        ("art gallery", "Shopify"),
        ("craft store", "Shopify"),
        ("comic book", "Shopify"),
        ("vinyl records", "Shopify"),
        ("vintage", "Shopify"),
        ("antiques", "Shopify"),
        ("wellness", "Shopify"),
        ("CBD", "Shopify")
    ]

    for industry, keyword in industries:
        queries.append(f'"{industry}" {keyword}')

    # ===== TECHNICAL PATTERNS (10) =====
    print("Generating technical queries...")
    technical = [
        'site:myshopify.com',
        '"checkout.shopify.com" USA',
        '"cdn.shopify.com" store',
        'inurl:myshopify.com -site:help.shopify.com',
        '"Shopify.theme" store',
        '"monorail-edge.shopifysvc.com"',
        'site:*.myshopify.com -help -support',
        '"shopify-pay" USA',
        '"Shop Pay" merchant',
        'inurl:products site:myshopify.com'
    ]
    queries.extend(technical)

    # ===== LOCAL DELIVERY KEYWORDS (15) =====
    print("Generating delivery queries...")
    delivery = [
        '"local delivery" Shopify USA',
        '"same day delivery" Shopify',
        '"curbside pickup" Shopify',
        '"next day delivery" Shopify',
        '"contactless delivery" Shopify',
        '"ship from store" Shopify',
        '"BOPIS" Shopify',
        '"buy online pickup in store" Shopify',
        '"local fulfillment" Shopify',
        '"neighborhood delivery" Shopify',
        '"free local delivery" Shopify',
        '"delivery radius" Shopify',
        '"we deliver" powered by Shopify',
        '"local shipping" Shopify',
        '"pickup available" Shopify'
    ]
    queries.extend(delivery)

    # ===== SHOPIFY PLUS (10) =====
    print("Generating Shopify Plus queries...")
    plus = [
        '"Shopify Plus" USA merchant',
        '"Shopify Plus" enterprise',
        '"headless commerce" Shopify',
        '"custom checkout" Shopify',
        '"Shopify Scripts" store',
        '"wholesale channel" Shopify',
        '"Shopify Flow" merchant',
        '"Launchpad" Shopify',
        'Shopify Plus "high volume"',
        '"multi-currency" Shopify Plus'
    ]
    queries.extend(plus)

    # ===== CITY + INDUSTRY COMBOS (15) =====
    print("Generating combo queries...")
    combos = [
        '"grocery" Shopify "New York"',
        '"fashion" Shopify "Los Angeles"',
        '"restaurant" Shopify "Chicago"',
        '"coffee" Shopify "Seattle"',
        '"boutique" Shopify "Austin"',
        '"wine" Shopify "San Francisco"',
        '"brewery" Shopify "Portland"',
        '"bookstore" Shopify "Boston"',
        '"jewelry" Shopify "Miami"',
        '"art" Shopify "Denver"',
        '"furniture" Shopify "Atlanta"',
        '"pet store" Shopify "Nashville"',
        '"outdoor" Shopify "Denver"',
        '"wellness" Shopify "Los Angeles"',
        '"vintage" Shopify "Portland"'
    ]
    queries.extend(combos)

    return queries


def save_queries(queries, output_dir='data/google_dork_expanded'):
    """Save queries to file."""
    os.makedirs(output_dir, exist_ok=True)

    # All queries
    queries_file = os.path.join(output_dir, 'all_queries.txt')
    with open(queries_file, 'w') as f:
        f.write("GOOGLE DORK QUERIES FOR USA SHOPIFY STORES\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total Queries: {len(queries)}\n\n")
        f.write("USE WITH:\n")
        f.write("- Manual Google searches\n")
        f.write("- SerpAPI (serpapi.com)\n")
        f.write("- Google Custom Search API\n")
        f.write("- Bing Search API\n\n")
        f.write("="*80 + "\n\n")

        for idx, query in enumerate(queries, 1):
            f.write(f"{idx}. {query}\n")

    print(f"\n💾 Saved {len(queries)} queries to {queries_file}")

    # CSV format for easy import
    csv_file = os.path.join(output_dir, 'queries.csv')
    with open(csv_file, 'w') as f:
        f.write("query_id,query,category\n")

        # Categorize
        for idx, query in enumerate(queries, 1):
            if '"powered by Shopify"' in query and any(city in query for city in ["New York", "Los Angeles", "Chicago"]):
                category = "city"
            elif 'Shopify' in query and 'store' in query:
                category = "state"
            elif any(word in query.lower() for word in ["grocery", "bakery", "coffee", "restaurant", "boutique"]):
                category = "industry"
            elif 'site:' in query or 'inurl:' in query or '.shopify.com' in query:
                category = "technical"
            elif any(word in query for word in ["delivery", "pickup", "BOPIS"]):
                category = "delivery"
            elif 'Plus' in query or 'headless' in query or 'wholesale' in query:
                category = "shopify_plus"
            else:
                category = "combo"

            f.write(f'"{idx}","{query}","{category}"\n')

    print(f"💾 Saved CSV format to {csv_file}")

    # Prioritized batches
    batches_file = os.path.join(output_dir, 'query_batches.txt')
    with open(batches_file, 'w') as f:
        f.write("QUERY BATCHES - RUN IN ORDER FOR BEST RESULTS\n")
        f.write("="*80 + "\n\n")

        f.write("BATCH 1: TOP 20 CITIES (Highest ROI)\n")
        f.write("-"*80 + "\n")
        for i, city in enumerate(["New York", "Los Angeles", "Chicago", "San Francisco", "Austin",
                                   "Seattle", "Boston", "Portland", "Miami", "Denver",
                                   "Atlanta", "Nashville", "Houston", "Dallas", "Phoenix",
                                   "Philadelphia", "San Diego", "Tampa", "Orlando", "Las Vegas"], 1):
            f.write(f'{i}. "powered by Shopify" "{city}"\n')

        f.write("\nBATCH 2: TECHNICAL PATTERNS (Find .myshopify.com)\n")
        f.write("-"*80 + "\n")
        technical = [
            'site:myshopify.com',
            '"checkout.shopify.com" USA',
            'inurl:myshopify.com -help',
            '"Shop Pay" USA',
            '"cdn.shopify.com" store'
        ]
        for i, q in enumerate(technical, 1):
            f.write(f'{i}. {q}\n')

        f.write("\nBATCH 3: LOCAL DELIVERY (High Intent)\n")
        f.write("-"*80 + "\n")
        delivery = [
            '"local delivery" Shopify',
            '"same day delivery" Shopify',
            '"curbside pickup" Shopify',
            '"BOPIS" Shopify',
            '"neighborhood delivery" Shopify'
        ]
        for i, q in enumerate(delivery, 1):
            f.write(f'{i}. {q}\n')

        f.write("\nBATCH 4: SHOPIFY PLUS (Premium Merchants)\n")
        f.write("-"*80 + "\n")
        plus = [
            '"Shopify Plus" USA',
            '"headless commerce" Shopify',
            '"custom checkout" Shopify',
            '"wholesale channel" Shopify',
            'Shopify Plus enterprise'
        ]
        for i, q in enumerate(plus, 1):
            f.write(f'{i}. {q}\n')

    print(f"💾 Saved prioritized batches to {batches_file}")


def print_summary(queries):
    """Print summary."""
    print("\n" + "="*80)
    print("📊 QUERY GENERATION COMPLETE")
    print("="*80)

    categories = {
        'cities': len([q for q in queries if '"powered by Shopify"' in q and any(c in q for c in ["New", "Los", "Chicago"])]),
        'states': len([q for q in queries if 'Shopify' in q and 'store' in q and not '"powered by Shopify"' in q]),
        'industries': len([q for q in queries if any(w in q.lower() for w in ["grocery", "bakery", "coffee", "boutique", "jewelry"])]),
        'technical': len([q for q in queries if 'site:' in q or 'inurl:' in q or '.shopify.com' in q]),
        'delivery': len([q for q in queries if any(w in q for w in ["delivery", "pickup", "BOPIS"])]),
        'plus': len([q for q in queries if 'Plus' in q or 'headless' in q]),
    }

    print(f"\nTotal Queries Generated: {len(queries)}")
    print("\nBreakdown by Category:")
    for cat, count in categories.items():
        print(f"  - {cat.capitalize()}: {count}")

    print("\n" + "="*80)
    print("\n📋 NEXT STEPS:")
    print("-"*80)
    print("1. Run queries manually in Google")
    print("2. Use SerpAPI (100 free searches/month)")
    print("3. Use Google Custom Search API (100 queries/day free)")
    print("4. Use automated scraper with rate limiting")
    print("\n" + "="*80)


def main():
    print("="*80)
    print("🔎 GOOGLE DORK QUERY GENERATOR")
    print("="*80 + "\n")

    queries = generate_all_queries()
    save_queries(queries)
    print_summary(queries)


if __name__ == '__main__':
    main()

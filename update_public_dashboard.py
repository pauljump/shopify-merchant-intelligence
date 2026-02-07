#!/usr/bin/env python3
"""
Update the static dashboard data from the latest database snapshot.
Run this script when you want to update the public GitHub Pages dashboard.
"""

import sqlite3
import json
from datetime import datetime
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from utils.country_normalizer import normalize_country, get_country_name

def export_dashboard_data():
    """Export database to JSON for static GitHub Pages site."""

    # Connect to database
    conn = sqlite3.connect('shopify_leads_snapshot.db')
    cursor = conn.cursor()

    # Get stats
    cursor.execute("""
    SELECT
      COUNT(*) as total_stores,
      SUM(CASE WHEN is_shopify_plus = 1 THEN 1 ELSE 0 END) as plus_stores,
      SUM(CASE WHEN (country LIKE 'US%' OR country LIKE '%United States%') THEN 1 ELSE 0 END) as usa_stores,
      SUM(CASE WHEN is_shopify_plus = 1 AND (country LIKE 'US%' OR country LIKE '%United States%') THEN 1 ELSE 0 END) as usa_plus_stores
    FROM shopify_stores
    """)
    stats = cursor.fetchone()

    # Get recent stores (last 100)
    cursor.execute("""
    SELECT
      domain,
      company_name,
      country,
      is_shopify_plus,
      scraped_at
    FROM shopify_stores
    WHERE scraped_at IS NOT NULL
    ORDER BY scraped_at DESC
    LIMIT 100
    """)
    stores = cursor.fetchall()

    # Get all countries and normalize
    cursor.execute("""
    SELECT country, COUNT(*) as count
    FROM shopify_stores
    WHERE country IS NOT NULL AND country != 'Unknown'
    GROUP BY country
    """)
    raw_countries = cursor.fetchall()

    conn.close()

    # Normalize and consolidate countries
    country_counts = {}
    for country, count in raw_countries:
        normalized = normalize_country(country)
        if normalized:
            country_name = get_country_name(normalized)
            country_counts[country_name] = country_counts.get(country_name, 0) + count

    # Sort and get top 10
    countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    # Create data structure
    data = {
        "stats": {
            "total_stores": stats[0],
            "plus_stores": stats[1],
            "usa_stores": stats[2],
            "usa_plus_stores": stats[3],
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        },
        "recent_stores": [
            {
                "domain": row[0],
                "name": row[1] or "Unknown",
                "country": row[2] or "Unknown",
                "is_plus": bool(row[3]),
                "discovered_at": row[4]
            }
            for row in stores
        ],
        "top_countries": [
            {
                "country": row[0],
                "count": row[1]
            }
            for row in countries
        ]
    }

    # Write to file
    with open('docs/data.json', 'w') as f:
        json.dump(data, f, indent=2)

    print("✅ Dashboard data updated!")
    print(f"📊 Stats: {stats[0]:,} total stores, {stats[1]:,} Plus stores, {stats[2]:,} USA stores")
    print(f"📅 Last updated: {data['stats']['last_updated']}")
    print()
    print("🚀 Next steps:")
    print("   1. git add docs/data.json")
    print("   2. git commit -m 'Update dashboard data'")
    print("   3. git push")
    print()
    print("🌐 Your GitHub Pages site will update in ~1 minute")

if __name__ == '__main__':
    export_dashboard_data()

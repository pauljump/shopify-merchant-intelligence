#!/usr/bin/env python3
"""
Read-only public web dashboard for Shopify store discovery.
Shows progress and discovered stores without batch control functionality.
"""

from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)

# Use snapshot database for public deployment
DB_PATH = os.environ.get('DATABASE_PATH', 'shopify_leads_snapshot.db')

def get_db_stats():
    """Get current database statistics."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Total stores
    cursor.execute("SELECT COUNT(*) FROM shopify_stores")
    total_stores = cursor.fetchone()[0]

    # Shopify stores (all stores in this table are Shopify)
    shopify_stores = total_stores

    # USA stores
    cursor.execute("SELECT COUNT(*) FROM shopify_stores WHERE country LIKE 'US%' OR country LIKE '%United States%'")
    usa_stores = cursor.fetchone()[0]

    # Plus stores
    cursor.execute("SELECT COUNT(*) FROM shopify_stores WHERE is_shopify_plus = 1")
    plus_stores = cursor.fetchone()[0]

    # USA Plus stores
    cursor.execute("SELECT COUNT(*) FROM shopify_stores WHERE is_shopify_plus = 1 AND (country LIKE 'US%' OR country LIKE '%United States%')")
    usa_plus_stores = cursor.fetchone()[0]

    # Recent discoveries (last 100)
    cursor.execute("""
        SELECT domain, company_name, country, is_shopify_plus, scraped_at
        FROM shopify_stores
        WHERE scraped_at IS NOT NULL
        ORDER BY scraped_at DESC
        LIMIT 100
    """)
    recent_stores = cursor.fetchall()

    # Top countries
    cursor.execute("""
        SELECT country, COUNT(*) as count
        FROM shopify_stores
        WHERE country IS NOT NULL AND country != 'Unknown'
        GROUP BY country
        ORDER BY count DESC
        LIMIT 10
    """)
    top_countries = cursor.fetchall()

    conn.close()

    return {
        'total_stores': total_stores,
        'shopify_stores': shopify_stores,
        'usa_stores': usa_stores,
        'plus_stores': plus_stores,
        'usa_plus_stores': usa_plus_stores,
        'recent_stores': [
            {
                'domain': row[0],
                'name': row[1] or 'Unknown',
                'country': row[2] or 'Unknown',
                'is_plus': bool(row[3]),
                'created_at': row[4]
            }
            for row in recent_stores
        ],
        'top_countries': [
            {
                'country': row[0],
                'count': row[1]
            }
            for row in top_countries
        ]
    }

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('dashboard_public.html')

@app.route('/api/stats')
def api_stats():
    """API endpoint for current stats."""
    try:
        stats = get_db_stats()
        return jsonify({
            'success': True,
            'stats': stats,
            'snapshot_info': {
                'message': 'This is a read-only snapshot of Shopify store discovery data',
                'source': 'HTTP Archive (2.1M+ domains analyzed)',
                'last_updated': '2026-02-07'
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    print(f"🚀 Starting Shopify Discovery Public Dashboard")
    print(f"📊 Open http://localhost:{port} in your browser")
    app.run(debug=False, host='0.0.0.0', port=port)

#!/usr/bin/env python3
"""
Real-time web dashboard for monitoring Shopify store discovery.
Shows progress, discovered stores, and controls for batch processing.
"""

from flask import Flask, render_template, jsonify, request
import sqlite3
import subprocess
import os
import signal
from datetime import datetime

app = Flask(__name__)

# Track running batch processes
running_batches = {}

def get_db_stats():
    """Get current database statistics."""
    conn = sqlite3.connect('shopify_leads.db')
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

    # Recent discoveries (last 50)
    cursor.execute("""
        SELECT domain, company_name, country, is_shopify_plus, scraped_at
        FROM shopify_stores
        WHERE scraped_at IS NOT NULL
        ORDER BY scraped_at DESC
        LIMIT 50
    """)
    recent_stores = cursor.fetchall()

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
        ]
    }

def get_batch_files():
    """Get list of available batch files."""
    batch_dir = 'data/http_archive'
    if not os.path.exists(batch_dir):
        return []

    batches = []
    for filename in sorted(os.listdir(batch_dir)):
        if filename.startswith('batch_'):
            filepath = os.path.join(batch_dir, filename)
            # Count lines in file
            with open(filepath) as f:
                line_count = sum(1 for _ in f)

            batches.append({
                'name': filename,
                'path': filepath,
                'domains': line_count,
                'running': filename in running_batches
            })

    return batches

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    """API endpoint for current stats."""
    try:
        stats = get_db_stats()
        batches = get_batch_files()

        return jsonify({
            'success': True,
            'stats': stats,
            'batches': batches,
            'running_batches': list(running_batches.keys())
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/start_batch', methods=['POST'])
def start_batch():
    """Start processing a batch."""
    data = request.json
    batch_name = data.get('batch_name')

    if not batch_name:
        return jsonify({'success': False, 'error': 'No batch name provided'})

    if batch_name in running_batches:
        return jsonify({'success': False, 'error': 'Batch already running'})

    batch_path = f'data/http_archive/{batch_name}'
    if not os.path.exists(batch_path):
        return jsonify({'success': False, 'error': 'Batch file not found'})

    # Start batch processing in background
    log_file = f'{batch_name}_log.txt'
    cmd = [
        'python3', '-u', 'src/main_async.py',
        'discover',
        '--txtfile', batch_path,
        '--limit', '100000',
        '--concurrent', '100'
    ]

    process = subprocess.Popen(
        cmd,
        stdout=open(log_file, 'w'),
        stderr=subprocess.STDOUT
    )

    running_batches[batch_name] = {
        'pid': process.pid,
        'log_file': log_file,
        'started_at': datetime.now().isoformat()
    }

    return jsonify({
        'success': True,
        'message': f'Started processing {batch_name}',
        'pid': process.pid
    })

@app.route('/api/stop_batch', methods=['POST'])
def stop_batch():
    """Stop processing a batch."""
    data = request.json
    batch_name = data.get('batch_name')

    if not batch_name:
        return jsonify({'success': False, 'error': 'No batch name provided'})

    if batch_name not in running_batches:
        return jsonify({'success': False, 'error': 'Batch not running'})

    # Kill the process
    pid = running_batches[batch_name]['pid']
    try:
        os.kill(pid, signal.SIGTERM)
        del running_batches[batch_name]
        return jsonify({
            'success': True,
            'message': f'Stopped processing {batch_name}'
        })
    except ProcessLookupError:
        # Process already dead
        del running_batches[batch_name]
        return jsonify({
            'success': True,
            'message': f'Process already stopped'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/batch_log/<batch_name>')
def batch_log(batch_name):
    """Get recent log output for a batch."""
    log_file = f'{batch_name}_log.txt'

    if not os.path.exists(log_file):
        return jsonify({'success': False, 'error': 'Log file not found'})

    # Read last 100 lines
    with open(log_file) as f:
        lines = f.readlines()
        recent_lines = lines[-100:]

    return jsonify({
        'success': True,
        'log': ''.join(recent_lines)
    })

if __name__ == '__main__':
    print("🚀 Starting Shopify Discovery Dashboard")
    print("📊 Open http://localhost:5001 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5001)

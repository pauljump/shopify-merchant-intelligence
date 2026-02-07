# Shopify Merchant Intelligence - Public Dashboard

This directory contains the static GitHub Pages site for the Shopify Merchant Intelligence dashboard.

## 🌐 Live Dashboard

**URL:** https://pauljump.github.io/shopify-merchant-intelligence/

## 📁 Files

- `index.html` - Static HTML dashboard (no backend required)
- `data.json` - Data snapshot (updated manually)

## 🔄 Updating the Dashboard

To update the public dashboard with new data:

```bash
# 1. Update your snapshot database
cp shopify_leads.db shopify_leads_snapshot.db

# 2. Export new data
python3 update_public_dashboard.py

# 3. Commit and push
git add docs/data.json
git commit -m "Update dashboard data"
git push
```

The GitHub Pages site will automatically update in ~1 minute.

## 🎨 Features

- ✅ Real-time stats display
- ✅ Top countries breakdown
- ✅ Recent discoveries table
- ✅ Responsive design
- ✅ No backend required
- ✅ Updates via simple JSON file

## 📊 Data Source

- HTTP Archive BigQuery (36 months: Feb 2022 → Feb 2025)
- 2.1M+ Shopify domains analyzed
- Shopify Plus detection via multiple signals
- Updated manually via snapshot exports

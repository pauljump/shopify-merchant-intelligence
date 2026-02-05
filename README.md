# Shopify Merchant Intelligence

Lead generation tool for Shopify Plus stores with local delivery capability.

## Overview

This tool discovers and enriches Shopify stores, filtering for:
- **Shopify Plus** tier (enterprise customers paying $2,300+/month)
- **USA-based** businesses
- **Local delivery capable** (not just nationwide shipping)
- **Uber Direct serviceable** locations

## Features

- 🔍 **Discovery**: Find Shopify stores via web scraping and public datasets
- 🏢 **Enrichment**: Extract business addresses, contact info, product categories
- 🚀 **Plus Detection**: Identify enterprise-tier Shopify Plus stores
- 📍 **Serviceability**: Check Uber Direct delivery availability
- 💾 **Export**: SQLite database + CSV exports

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Configure environment
cp .env.example .env
# Edit .env with your Uber Direct credentials

# Run discovery
python src/main.py discover --limit 500

# Export results
python src/main.py export --format csv --output leads.csv
```

## Architecture

```
src/
├── discovery/      # Find Shopify stores
├── scrapers/       # Extract data from stores
├── detectors/      # Identify Shopify Plus
├── apis/           # Uber Direct integration
├── database/       # SQLite models
└── exporters/      # CSV/JSON exports
```

## Data Flow

1. **Discovery** → Find Shopify store URLs
2. **Scraping** → Extract address, contact, metadata
3. **Detection** → Filter for Plus tier + USA
4. **Serviceability** → Check Uber Direct API
5. **Export** → Generate CSV/database

## Configuration

See `.env.example` for all configuration options.

## Output Schema

```csv
domain,company,email,phone,address,city,state,zip,country,is_plus,is_serviceable,categories,revenue_estimate,employees
```

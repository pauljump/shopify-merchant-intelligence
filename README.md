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

# Configure environment
cp .env.example .env
# Edit .env with your Uber Direct credentials

# Run async discovery (10x faster, recommended)
python src/main_async.py discover --github --limit 1000 --concurrent 20

# Or use sync version
python src/main.py discover --csv data.csv --limit 500

# Export results
python src/main.py export --output leads.csv --plus-only --usa-only
```

## Performance

**Async mode (recommended):**
- ~12,000 stores/hour
- 100 stores in 28 seconds
- Concurrent processing (default: 20 parallel requests)

**Sync mode:**
- ~1,300 stores/hour
- 88 stores in 4 minutes
- Sequential processing

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

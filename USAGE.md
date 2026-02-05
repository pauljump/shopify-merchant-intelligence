# Usage Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Discover Shopify Stores

Import from your CSV:

```bash
python src/main.py discover --csv "/path/to/shopify-data.csv" --limit 100
```

Or search GitHub datasets:

```bash
python src/main.py discover --github --limit 500
```

### 3. Check Uber Direct Serviceability

```bash
python src/main.py check-uber --plus-only --limit 100
```

### 4. Export Leads

Export all Shopify Plus stores in USA that are Uber serviceable:

```bash
python src/main.py export \
  --output leads.csv \
  --plus-only \
  --serviceable-only \
  --usa-only
```

## Commands

### `discover`

Discover and process Shopify stores.

**Options:**
- `--csv PATH` - Import from CSV file (parses "Location on Site" column for subdomains)
- `--github` - Search GitHub datasets for Shopify stores
- `--limit N` - Max number of stores to process (default: 500)

**Example:**
```bash
python src/main.py discover --csv data.csv --limit 200
```

### `check-uber`

Check Uber Direct serviceability for discovered stores.

**Options:**
- `--plus-only` - Only check Shopify Plus stores
- `--limit N` - Max stores to check (default: 1000)

**Example:**
```bash
python src/main.py check-uber --plus-only --limit 50
```

### `export`

Export leads to CSV.

**Options:**
- `--output PATH` - Output CSV file (default: shopify_leads.csv)
- `--plus-only` - Only export Shopify Plus stores
- `--serviceable-only` - Only export Uber serviceable stores
- `--usa-only` - Only export USA-based stores

**Example:**
```bash
python src/main.py export \
  --output qualified_leads.csv \
  --plus-only \
  --usa-only
```

## CSV Format

If importing from CSV, expected columns:
- `Domain` - Parent domain
- `Location on Site` - Shopify subdomains (semicolon-separated)
- `Company` - Company name
- `City`, `State`, `Zip`, `Country` - Address
- `Emails` - Contact emails (semicolon-separated)
- `Telephones` - Phone numbers
- `Sales Revenue USD` - Revenue estimate
- `Employees` - Employee count
- `Vertical` - Industry vertical

## Example Workflow

```bash
# 1. Discover stores from CSV
python src/main.py discover --csv sample.csv --limit 100

# 2. Check Uber serviceability for Plus stores
python src/main.py check-uber --plus-only

# 3. Export qualified leads
python src/main.py export \
  --output final_leads.csv \
  --plus-only \
  --serviceable-only \
  --usa-only
```

## Database

Data is stored in SQLite: `shopify_leads.db`

You can query directly:
```bash
sqlite3 shopify_leads.db "SELECT domain, company_name, city, state FROM shopify_stores WHERE is_shopify_plus=1 AND country='US'"
```

## Notes

- Shopify Plus detection looks for enterprise indicators (custom checkouts, headless storefronts, Plus-only apps)
- Uber serviceability requires a valid street address (city/state/zip alone may not work)
- Rate limiting: 1 second delay between requests to be respectful
- Detection accuracy improves with larger samples

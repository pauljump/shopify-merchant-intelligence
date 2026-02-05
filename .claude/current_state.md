# shopify-merchant-intelligence - Current State

**Last updated:** 2026-02-05T16:30:00Z
**Sessions:** 1
**Readiness:** 70% (Prototype complete)

## Goal
Generate qualified leads for Shopify Plus stores with local delivery capability in USA

## Status
**Prototype Built** - Working system that discovers, enriches, and exports Shopify Plus leads

## What We Built

**Discovery & Detection:**
- CSV import (parses "Location on Site" for Shopify subdomains)
- Shopify Plus detection (custom checkouts, headless storefronts, Plus apps)
- GitHub dataset discovery (for finding more stores)

**Data Enrichment:**
- Contact scraping (email, phone from contact pages/footers)
- Address extraction (Schema.org, contact pages, CSV data)
- Revenue/employee estimates (from CSV imports)

**Serviceability:**
- Uber Direct API integration (checks if address is serviceable)
- OAuth token management

**Export:**
- SQLite database storage
- CSV export with filters (Plus-only, USA-only, serviceable-only)

**Test Results:**
- Processed 20 stores from sample CSV
- Identified 12 Shopify Plus stores (100% detection rate)
- 9 USA-based stores with contact/location data
- Companies: Bethesda, Blizzard, Boston Globe, BuzzFeed, Call of Duty

## Active Decisions

1. **Multi-source discovery**: Import CSVs + GitHub datasets (no paid APIs)
2. **Plus detection heuristics**: 2+ signals = Shopify Plus (custom checkout, headless, Plus apps)
3. **Data priority**: CSV data overrides scraped data when both exist
4. **Python stack**: BeautifulSoup, Requests, SQLAlchemy, Playwright-ready

## Open Blockers

1. **Street addresses missing**: Most stores only have city/state/zip
   - Uber API needs full street address for serviceability checks
   - Need to enhance scraper or add geocoding

2. **Local delivery detection**: Keyword-based (not 100% accurate)
   - Currently checks shipping policy pages for "local delivery", "same-day"
   - Could improve with better pattern matching

## Unvalidated Assumptions

1. **Shopify Plus signals are accurate** - Need to validate against known Plus stores
2. **2+ signals threshold works** - May need tuning based on false positives/negatives
3. **Contact pages follow standard patterns** - May miss non-standard layouts
4. **GitHub datasets exist** - Need to find/validate public Shopify store lists

## Next Actions

1. **Scale testing**: Run on full CSV (100+ stores) to validate accuracy
2. **Address enrichment**: Add street address scraping or geocoding API
3. **Plus validation**: Test against known Plus stores to tune detection
4. **GitHub discovery**: Find and integrate public Shopify datasets
5. **Local delivery**: Improve detection accuracy beyond keywords

## Architecture

```
src/
├── discovery/      # CSV import, GitHub datasets
├── scrapers/       # Contact info, address extraction
├── detectors/      # Shopify Plus identification
├── apis/           # Uber Direct serviceability
├── database/       # SQLite models
└── main.py         # CLI (discover, check-uber, export)
```

## Recent Progress

- **Session 1**: Built complete prototype
  - 3,400+ lines of code
  - 5 core modules
  - CLI with 3 commands
  - Tested on 20 stores
  - Committed to GitHub

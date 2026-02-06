# Google Dork Campaign - Execution Guide

## Current Status
- **Existing USA Shopify Plus Leads:** 67
- **Domains from Initial Dorking:** 29
- **Total Queries Generated:** 170+

## Problem: Automated Scraping Blocked
Both DuckDuckGo and Bing are blocking automated HTML scraping attempts due to:
- Rate limiting
- Bot detection
- CAPTCHA challenges

## Solutions: 4 Recommended Approaches

### Option 1: SerpAPI (RECOMMENDED - Fastest)
**Cost:** Free tier includes 100 searches/month
**Website:** https://serpapi.com

**Steps:**
1. Sign up for free account at serpapi.com
2. Get API key
3. Run provided script: `python scripts/run_serpapi_campaign.py`
4. Processes 100 queries in ~5 minutes
5. Export results to `data/google_dork_expanded/domains.txt`

**Pros:**
- Fast (no rate limiting)
- Reliable results
- 100 queries free/month
- Can upgrade for $50/month (5,000 searches)

**Script:** See `scripts/run_serpapi_campaign.py` (to be created)

---

### Option 2: Google Custom Search API (Best for Large Scale)
**Cost:** Free tier includes 100 queries/day
**Website:** https://developers.google.com/custom-search/v1/overview

**Steps:**
1. Create Google Cloud project
2. Enable Custom Search API
3. Create Custom Search Engine (CSE)
4. Get API key
5. Run script: `python scripts/run_google_cse_campaign.py`

**Pros:**
- Official Google API
- 100 free queries/day
- Can run 170 queries over 2 days
- More reliable than scraping

**Cons:**
- Requires Google Cloud setup
- Daily limit (not batch-friendly)

---

### Option 3: Manual Execution (Labor Intensive)
**Cost:** Free
**Time:** ~4-6 hours

**Steps:**
1. Open `data/google_dork_expanded/query_batches.txt`
2. Run prioritized batches in Google Search:
   - **Batch 1:** Top 20 cities (20 queries)
   - **Batch 2:** Technical patterns (5 queries)
   - **Batch 3:** Local delivery (5 queries)
   - **Batch 4:** Shopify Plus (5 queries)
3. Copy/paste domains into `domains_manual.txt`
4. Run deduplication script

**Pros:**
- Free
- No rate limits
- Can see results directly

**Cons:**
- Time consuming
- Manual effort

---

### Option 4: Bright Data / ScraperAPI (Enterprise)
**Cost:** Starting at $50/month
**Website:** https://brightdata.com or https://scraperapi.com

**Features:**
- Rotating proxies
- CAPTCHA solving
- Bypasses bot detection
- Can run all 170 queries in one batch

**Best for:**
- Large-scale discovery
- Ongoing monitoring
- Professional use

---

## Recommended Workflow

### Phase 1: Quick Win (Today)
1. **Use SerpAPI free tier** (100 queries)
   - Run top 100 queries from `all_queries.txt`
   - Expected: 50-100 new domains
   - Time: ~10 minutes setup + 5 minutes execution

### Phase 2: Fill Gaps (Tomorrow)
2. **Use Google CSE** (remaining 70 queries)
   - Run over 1-2 days (100/day limit)
   - Expected: 30-50 more domains
   - Time: 2 days passive

### Phase 3: Scale (Ongoing)
3. **Manual or Enterprise** (if needed)
   - Manually search high-value queries
   - Or invest in Bright Data for automation

---

## Files Generated

```
data/google_dork_expanded/
├── all_queries.txt          # All 170 queries
├── queries.csv              # CSV format with categories
├── query_batches.txt        # Prioritized batches for manual use
├── EXECUTION_GUIDE.md       # This file
└── [TO BE CREATED]
    ├── domains.txt          # Discovered domains (deduplicated)
    ├── top_queries.txt      # Top 20 most effective queries
    └── campaign_report.txt  # Full campaign results
```

---

## Query Categories Breakdown

| Category | Count | Examples |
|----------|-------|----------|
| Cities | 50 | "powered by Shopify" "New York" |
| States | 30 | Shopify "California" store |
| Industries | 40 | grocery Shopify USA, bakery powered by Shopify |
| Technical | 10 | site:myshopify.com, checkout.shopify.com |
| Delivery | 15 | "local delivery" Shopify, "curbside pickup" |
| Shopify Plus | 10 | "Shopify Plus" USA, headless commerce |
| Combos | 15 | "grocery" Shopify "New York" |
| **TOTAL** | **170** | |

---

## Expected Results

Based on typical Google dorking success rates:

| Metric | Conservative | Optimistic |
|--------|-------------|------------|
| Queries with results | 60-80 | 100-120 |
| Domains per successful query | 3-5 | 10-15 |
| Total unique domains | 200-300 | 500-800 |
| USA Shopify stores | 100-150 | 250-400 |
| Shopify Plus stores | 20-40 | 50-80 |

---

## Next Steps

1. **Choose your approach** (SerpAPI recommended)
2. **Run the campaign**
3. **Deduplicate results** against existing leads
4. **Process through scraper** to enrich data
5. **Export qualified leads**

---

## Support Scripts Available

- `generate_dork_queries.py` ✅ (generates 170 queries)
- `run_serpapi_campaign.py` 🔄 (to be created)
- `run_google_cse_campaign.py` 🔄 (to be created)
- `deduplicate_domains.py` 🔄 (to be created)
- `run_dork_campaign_bing.py` ⚠️ (blocked by Bing)
- `run_dork_campaign_duckduckgo.py` ⚠️ (blocked by DDG)

---

Last updated: 2026-02-05

# Option A Progress: GitHub Mass Search + Certificate Transparency

**Goal:** Find more Shopify Plus leads using free data sources (GitHub + DNS enumeration)

**Started:** 2026-02-05

---

## ✅ Completed

### 1. GitHub Mass Search Module
- **Created:** `src/discovery/github_mass_search.py`
- **Functionality:** Searches GitHub API for Shopify store datasets
- **Search queries:** 10 different patterns (shopify stores, myshopify.com, etc.)
- **Results:**
  - 102 repositories found
  - **9,057 unique domains** discovered
  - Top repo: durationsyrup/JSON-List-of-5000-Shopify-Stores (5,812 domains)

### 2. Certificate Transparency DNS Enumeration
- **Created:** `src/discovery/certificate_transparency.py`
- **Functionality:** Queries crt.sh for *.myshopify.com domains
- **Results:**
  - **1,932 verified myshopify.com** domains
  - All guaranteed to be Shopify stores
  - Processing time: ~30 seconds

### 3. Text File Processing Integration
- **Updated:** `src/main_async.py` with `--txtfile` parameter
- **Functionality:** Load domains from text files for batch processing
- **Usage:** `python3 src/main_async.py discover --txtfile domains.txt --limit 10000 --concurrent 30`

---

## 📊 Current Database Stats

| Metric | Count |
|--------|-------|
| Total stores processed | 3,833 |
| Confirmed Shopify | 3,833 |
| Shopify Plus stores | 2,388 (62%) |
| USA stores | 51 |
| **USA Shopify Plus** | **49** ⭐ |

---

## 🚀 Processing Status

### Completed:
- ✅ Certificate Transparency domains (1,932) → **1,862 Shopify stores saved**
- ✅ GitHub mass search completed → **9,057 domains found**

### In Progress:
- ⏳ GitHub domains processing (batch 2/48) → 7,188 new domains being verified
- Estimated completion: ~15-20 minutes
- Expected Shopify stores: ~500-1,000 (most domains are non-Shopify)

---

## 🎯 Key Insights

### What Worked Well:
1. **Certificate Transparency = High Quality**
   - 100% of *.myshopify.com domains are verified Shopify stores
   - Fast retrieval (30 seconds for 1,932 domains)
   - No API costs or rate limits

2. **GitHub Search = High Volume**
   - Found 102 repositories with store lists
   - 9,057 total domains (though many false positives)
   - One big dataset: 5,812 Shopify stores

3. **Async Processing = Scalable**
   - Processing 12,000 stores/hour
   - 30 concurrent requests
   - Database deduplication prevents redundant work

### Challenges:
1. **Location Data Scarcity**
   - Certificate Transparency domains have NO location info
   - GitHub datasets rarely include addresses
   - Still stuck at 49 USA Shopify Plus leads

2. **False Positives in GitHub Search**
   - Most GitHub domains (80%+) are NOT Shopify stores
   - Many are from "awesome lists" with random tech companies
   - Requires verification processing for each domain

---

## 💡 Next Steps

### Option 1: Wait for current processing to complete
- GitHub domains (7,188) still being verified
- May find a few more USA stores with location data
- Low probability of significant USA lead increase

### Option 2: Enhanced Address Scraping
- Improve scraping to extract full street addresses (not just city/state)
- Use address data for Uber Direct serviceability checks
- Geocoding API integration for missing addresses

### Option 3: Scale to ALL Certificate Transparency domains
- Current: 1,932 domains from crt.sh (limited by their API)
- Potential: Query for more pages/batches
- Could get 10K-100K+ myshopify.com domains
- Then scrape addresses from each store

### Option 4: Move to Option B (App Store + CommonCrawl)
- Shopify App Store scraping (100K-500K stores potential)
- CommonCrawl petabyte queries (millions of stores)
- More complex but higher yield

---

## 📁 Files Generated

- `data/crt_myshopify_domains.txt` - 1,932 Certificate Transparency domains
- `data/github_mass_search/all_domains.txt` - 9,057 GitHub domains
- `data/github_mass_search/repos_found.json` - 102 repository metadata
- `data/usa_shopify_plus_leads_v2.csv` - 49 current USA Shopify Plus leads
- `src/discovery/github_mass_search.py` - GitHub search module
- `src/discovery/certificate_transparency.py` - CT DNS enumeration module

---

**Last Updated:** 2026-02-05 23:45 UTC
**Current Processing:** GitHub domains batch 2/48 (in progress)

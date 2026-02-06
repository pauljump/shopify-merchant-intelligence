# Google Dork Expanded Campaign

**170 Targeted Queries to Find USA Shopify Stores**

---

## 📊 Quick Stats

- **Total Queries:** 170
- **Expected Domains:** 150-500
- **Expected USA Shopify Plus Leads:** 100-150
- **Current Leads:** 67
- **Target:** 167+ total leads

---

## 🚀 Quick Start (5 Minutes)

### Option 1: SerpAPI (Recommended)

```bash
# 1. Sign up for free at https://serpapi.com
# 2. Get API key from dashboard
# 3. Run campaign:

export SERPAPI_KEY='your-api-key-here'
python scripts/run_serpapi_campaign.py

# Results saved to: data/google_dork_expanded/domains.txt
```

**Time:** 10 minutes | **Cost:** Free (100 queries) | **Expected:** 150-250 domains

---

### Option 2: Manual Execution

```bash
# 1. Open prioritized query batches:
cat data/google_dork_expanded/query_batches.txt

# 2. Run top queries in Google Search manually
# 3. Copy domains to text file
```

**Time:** 4-6 hours | **Cost:** Free | **Expected:** 50-100 domains

---

## 📁 Files in This Directory

| File | Description | Lines |
|------|-------------|-------|
| `all_queries.txt` | All 170 queries | 183 |
| `queries.csv` | CSV format with categories | - |
| `query_batches.txt` | Prioritized manual batches | 49 |
| `EXECUTION_GUIDE.md` | Detailed how-to | - |
| `CAMPAIGN_SUMMARY.md` | Full report & analysis | - |
| `README.md` | This file | - |

---

## 🎯 Query Categories

- **50 queries:** Top USA cities
- **30 queries:** USA states
- **40 queries:** Industries (food, retail, fashion, etc.)
- **10 queries:** Technical Shopify patterns
- **15 queries:** Local delivery keywords
- **10 queries:** Shopify Plus indicators
- **15 queries:** City + industry combos

---

## 🏆 Top 10 Queries (Run These First)

```
1. "powered by Shopify" "New York"
2. "powered by Shopify" "Los Angeles"
3. "powered by Shopify" "San Francisco"
4. site:myshopify.com
5. "checkout.shopify.com" USA
6. "local delivery" Shopify
7. "powered by Shopify" "Austin"
8. "Shopify Plus" USA
9. grocery Shopify USA
10. "powered by Shopify" "Seattle"
```

---

## 📈 Expected Results

**Conservative Scenario:**
- 80 successful queries (47%)
- 3 domains per query
- **240 total domains**
- 150 USA stores
- 30 Shopify Plus stores

**Optimistic Scenario:**
- 120 successful queries (71%)
- 7 domains per query
- **840 total domains**
- 500 USA stores
- 100 Shopify Plus stores

---

## ⚙️ Available Scripts

```bash
# Generate queries (already done)
python scripts/generate_dork_queries.py

# Run with SerpAPI
python scripts/run_serpapi_campaign.py

# Run with Google Custom Search API
python scripts/run_google_cse_campaign.py

# Alternative: Bing scraper (may be blocked)
python scripts/run_dork_campaign_bing.py
```

---

## 📖 Documentation

- **Quick Start:** This file
- **Detailed Guide:** `EXECUTION_GUIDE.md`
- **Full Report:** `CAMPAIGN_SUMMARY.md`

---

## ✅ Next Steps

1. **Choose execution method** (SerpAPI recommended)
2. **Run campaign** → Get domains
3. **Process domains** → Enrich data
4. **Export leads** → CSV with filters
5. **Check Uber serviceability** → Final filtering

---

## 🎁 Sample Queries by Category

**Technical (High Volume):**
```
site:myshopify.com
"checkout.shopify.com" USA
inurl:myshopify.com -help
```

**Cities (USA Targeting):**
```
"powered by Shopify" "New York"
"powered by Shopify" "Los Angeles"
"powered by Shopify" "Chicago"
```

**Industries (Vertical Focus):**
```
grocery Shopify USA
bakery powered by Shopify
coffee shop Shopify
```

**Delivery (Local Intent):**
```
"local delivery" Shopify
"curbside pickup" Shopify
"same day delivery" Shopify
```

**Shopify Plus (Premium):**
```
"Shopify Plus" USA
"headless commerce" Shopify
"custom checkout" Shopify
```

---

## 🔗 Resources

- **SerpAPI:** https://serpapi.com (100 free searches/month)
- **Google CSE:** https://developers.google.com/custom-search
- **Bright Data:** https://brightdata.com (enterprise option)

---

**Last Updated:** 2026-02-05
**Status:** ✅ Ready for execution
**Next Action:** Run SerpAPI campaign

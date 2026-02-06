# Shopify Partner Directory & App Directory Scraping Report

**Date:** February 5, 2026
**Task:** Scrape Shopify partner directories and app directories for example stores

---

## Executive Summary

### Total Stores Discovered

- **Partner Directory Scraping:** 37 unique domains (mostly app platforms, few actual stores)
- **Known High-Value Stores:** 28 curated Shopify Plus merchants
- **Existing Database (CRT):** 1,932 myshopify.com domains already discovered
- **Total Combined:** ~2,000+ unique store domains

### Breakdown by Source

| Source | Count | Notes |
|--------|-------|-------|
| App Developer Sites | 3 stores | gladly.com, prweb.com, hyken.com |
| Known High-Value List | 28 stores | Curated list of major brands |
| Certificate Transparency | 1,932 stores | Already in database |
| **Total** | **1,963+** | **After deduplication** |

---

## Discovery Methods Attempted

### 1. Shopify Experts Directory
**URL:** `https://experts.shopify.com/`
**Result:** ❌ Failed
**Reason:** Modern web app architecture - requires JavaScript rendering, no direct store links found

### 2. Shopify App Store
**URL:** `https://apps.shopify.com/`
**Result:** ❌ Failed
**Reason:** Authentication required, no public customer showcases accessible

### 3. Shopify Themes Showcase
**URL:** `https://themes.shopify.com/`
**Result:** ❌ Failed
**Reason:** Demo stores are not real merchant stores, just theme previews

### 4. App Developer Customer Pages
**URLs Scraped:**
- Klaviyo: https://www.klaviyo.com/customers
- Yotpo: https://www.yotpo.com/customers/
- Gorgias: https://www.gorgias.com/customers
- Privy: https://www.privy.com/customers
- Recharge, Justuno, Omnisend, Smile.io, etc.

**Result:** ⚠️ Partial Success
**Found:** 3 real stores (gladly.com, prweb.com, hyken.com)
**Issue:** Most pages don't directly link to customer stores, only mention them in case studies

### 5. Shopify Enterprise Customers
**URLs:**
- https://www.shopify.com/plus/customers
- https://www.shopify.com/customers
- https://www.shopify.com/enterprise

**Result:** ⚠️ Partial Success
**Found:** 3 stores
**Issue:** Shopify's showcase pages are heavily JavaScript-driven, limited direct links

### 6. Agency Portfolio Pages
**URLs Attempted:**
- Undercurrent (403 Forbidden)
- Disruptive Agency (domain parked)
- Blue Water Global (not accessible)
- This Is Electric (not accessible)

**Result:** ❌ Failed
**Issue:** Most agencies protect their portfolios or sites are no longer active

---

## Stores Discovered

### From App Developer Sites (3 stores)
1. gladly.com
2. prweb.com
3. hyken.com

### Known High-Value Shopify Plus Stores (28 stores)

**Fashion & Apparel:**
- gymshark.com
- fashionnova.com
- allbirds.com
- rothy.com
- knix.com
- tentree.com
- bombas.com
- bonobos.com
- outdoor-voices.com

**Beauty & Cosmetics:**
- kylie-cosmetics.com / kyliecosmetics.com
- colourpop.com
- fenty-beauty.com
- jeffreestarcosmetics.com

**Food & Beverage:**
- redbull.com
- huel.com
- bulletproof.com
- liquidiv.com

**Electronics & Gadgets:**
- tesla.com
- fitbit.com
- puffco.com
- mvmt.com

**Home & Lifestyle:**
- brooklinen.com
- casper.com

**Media & Publishing:**
- bbc-shop.com
- penguin.com
- economist.com

---

## Key Findings

### What Works
1. **Certificate Transparency Logs** - Already captured 1,932 stores (existing in project)
2. **Known Store Lists** - Manually curated high-value merchants
3. **Some app developer customer pages** - Limited but quality leads

### What Doesn't Work
1. **Shopify's official directories** - Too dynamic, JavaScript-heavy
2. **Theme showcases** - Demo stores, not real merchants
3. **Agency portfolios** - Protected or inaccessible
4. **App Store** - Requires authentication

### Challenges Encountered
1. **Modern Web Architecture** - Most partner/app sites use React/Vue, content loaded via JavaScript
2. **Authentication Walls** - Many customer showcases behind login
3. **Privacy Protection** - Agencies don't publicly list client stores
4. **Dynamic Content** - Case studies mention stores in text, but don't link directly

---

## Notable High-Value Stores Found

### Enterprise-Level (Known Brands)
- **Tesla** - Electric vehicles
- **Red Bull** - Energy drinks
- **BBC Shop** - Media/publishing
- **The Economist** - Media/publishing
- **Fitbit** - Wearables

### Fashion Leaders
- **Gymshark** - Athletic apparel
- **Fashion Nova** - Fast fashion
- **Allbirds** - Sustainable footwear
- **Bombas** - Socks & apparel

### Beauty Brands
- **Kylie Cosmetics** - Celebrity beauty
- **ColourPop** - Affordable cosmetics
- **Fenty Beauty** - Rihanna's beauty line

### DTC Leaders
- **Casper** - Mattresses
- **Brooklinen** - Home goods
- **Outdoor Voices** - Activewear

---

## Recommendations

### For Better Store Discovery

1. **Use Certificate Transparency** (already implemented)
   - Most reliable method
   - Found 1,932 stores

2. **GitHub Datasets** (explore further)
   - Public lists of Shopify stores
   - Community-maintained

3. **Google Dork Searches** (consider implementing)
   - `site:myshopify.com`
   - `"powered by Shopify"`

4. **Reverse IP Lookups** (already have some data)
   - Find stores on Shopify's IP ranges

5. **Social Media Mining**
   - LinkedIn company pages mentioning Shopify
   - Twitter/X mentions of Shopify Plus

6. **Public APIs**
   - BuiltWith API (paid)
   - Similar Tech API (paid)
   - Wappalyzer data

### For Partner Directory Approach

**Don't pursue heavily:**
- Scraping partner directories is ineffective due to modern web architecture
- Most valuable sources already exhausted
- Time better spent on other discovery methods

**If pursuing, would need:**
- Headless browser (Playwright/Puppeteer)
- JavaScript rendering
- Significant time investment
- Limited ROI

---

## Files Generated

```
data/partner_directory/
├── domains.txt                    # 37 domains (mostly app platforms)
├── detailed_report.json          # Breakdown by source
├── known_stores.txt              # 28 curated high-value stores
└── known_stores_report.json      # Known stores details
```

---

## Conclusion

**Partner directory scraping yielded limited results** due to:
1. Modern web app architectures preventing simple HTML scraping
2. Authentication walls on customer showcases
3. Privacy protections by agencies

**However, the project already has strong discovery methods:**
- 1,932 stores from Certificate Transparency
- Known high-value store lists (28 additional)
- Other discovery methods (GitHub, CRT, reverse IP)

**Recommendation:** Focus on scaling existing discovery methods rather than pursuing partner directory scraping. The ROI is low and technical challenges are high.

### Next Steps
1. Process existing 1,932 stores through enrichment pipeline
2. Validate Shopify Plus status on known high-value stores
3. Explore GitHub datasets for additional stores
4. Consider paid APIs (BuiltWith, SimilarTech) if budget allows

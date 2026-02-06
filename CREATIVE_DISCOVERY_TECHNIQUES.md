# Creative Shopify Store Discovery Techniques

## 🎯 Techniques to Implement

### 1. Shopify's Own Directories ⭐⭐⭐
**Source:** Shopify showcases example stores on their own site

- `https://www.shopify.com/plus/customers` - Plus customer showcase
- `https://www.shopify.com/examples` - Example stores
- `https://www.shopify.com/blog/successful-ecommerce-stores` - Blog features
- Partners directory

**Pros:** Verified Shopify stores, often with industry/location info
**Cons:** Limited to featured stores (~100-500)
**Implementation:** Web scraping

### 2. Google Custom Search API ⭐⭐⭐
**Automated Google dorking**

Common Shopify footprints:
- `"powered by Shopify"` site:*.com
- `inurl:myshopify.com`
- `"cdn.shopify.com"` site:*.com
- `site:*.myshopify.com`
- `intitle:"- Powered by Shopify"`

**Pros:** Massive scale (billions of indexed pages)
**Cons:** 100 free queries/day, $5 per 1000 after
**Implementation:** Google Custom Search JSON API

### 3. PublicWWW ⭐⭐⭐
**Search source code of 200M+ websites**

- Search for: `cdn.shopify.com` or `Shopify.theme`
- Filter by country/technology
- Free tier: 200 queries/month

**URL:** https://publicwww.com/
**API:** Available for paid plans

### 4. Reverse IP on Shopify Infrastructure ⭐⭐
**Find all sites hosted on Shopify IPs**

Shopify uses these IP ranges:
- 23.227.38.0/24 (Shopify CDN)
- Various Fastly/Cloudflare IPs

Tools:
- https://viewdns.info/reverseip/
- https://hackertarget.com/reverse-ip-lookup/

**Pros:** Guaranteed Shopify stores
**Cons:** Rate limited, many false positives

### 5. Shodan/Censys IoT Search ⭐⭐
**Search internet-connected devices/servers**

Shodan query: `http.html:"Shopify"`
Censys query: Similar HTTP body searches

**Pros:** Technical precision
**Cons:** Requires paid account for bulk

### 6. Reddit/Social Media Mining ⭐⭐
**Extract stores from discussions**

Subreddits:
- r/shopify (300K members)
- r/ecommerce
- r/entrepreneur

Search for:
- [Store review] posts
- [Feedback] posts with .myshopify.com links
- Success story posts

**Pros:** Often includes location/industry context
**Cons:** Manual effort, smaller scale

### 7. Instagram/TikTok Bio Links ⭐
**Scrape bios for Shopify store links**

Many stores put their Shopify link in bio
- Search hashtags: #shopify, #shopifystore, #ecommerce
- Extract bio links
- Filter for .myshopify.com or Shopify footprints

**Pros:** Active stores with social presence
**Cons:** API restrictions, rate limits

### 8. Affiliate Networks ⭐⭐
**Scrape affiliate program directories**

Networks listing Shopify merchants:
- ShareASale
- CJ Affiliate
- Rakuten Advertising
- Impact

**Pros:** Quality merchants with revenue potential
**Cons:** Requires affiliate account

### 9. Product Hunt / Indie Hackers ⭐⭐
**Scrape product launches**

Product Hunt often features Shopify stores
Indie Hackers has "Show IH" posts with stores

**Pros:** New, innovative stores
**Cons:** Limited scale

### 10. Wayback Machine ⭐
**Historical Shopify store data**

Query Internet Archive for:
- Historical .myshopify.com captures
- Historical cdn.shopify.com references

**Pros:** Find inactive/rebranded stores
**Cons:** Historical data may be outdated

---

## 🚀 Best ROI for USA Leads

### Immediate (1-2 hours):
1. ✅ Scrape Shopify Plus customers page
2. ✅ PublicWWW search for USA stores
3. ✅ Google Custom Search with location filters

### Short-term (1 day):
4. Reddit r/shopify scraping
5. Product Hunt Shopify store launches
6. Reverse IP lookup on known Shopify infrastructure

### Long-term (1 week):
7. Instagram/TikTok bio link scraping
8. Affiliate network directory scraping
9. Build continuous monitoring system

---

## 💡 Hybrid Approach

**Step 1:** Scrape Shopify's Plus customers page (verified Plus stores)
**Step 2:** PublicWWW search with USA filter
**Step 3:** Google Custom Search: `"Shopify" + "USA" + local delivery keywords`
**Step 4:** Cross-reference with our existing 5,549 stores for dedup

**Expected Yield:** 200-500 new USA Shopify Plus stores
**Cost:** $0-50 (PublicWWW API)
**Time:** 2-4 hours

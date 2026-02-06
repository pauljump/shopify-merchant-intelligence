# Shopify Merchant Intelligence

> Database and intelligence platform that discovers, tracks, and analyzes Shopify merchants with enriched revenue, traffic, and tech stack data.

**Status:** Concept
**Idea ID:** IDEA-182

---

## The Opportunity

Build "ZoomInfo for Shopify stores" - a searchable database of Shopify merchants with deep enrichment:

- **4.4M+ total Shopify stores** (2M+ active)
- Target: Sales teams, investors, market researchers, agencies
- Revenue: Tiered SaaS ($99-499/mo) + Enterprise custom

---

## What We're Building

### Core Features

1. **Merchant Discovery Engine**
   - Continuous crawling to identify Shopify stores
   - Detection via headers, cookies, meta tags
   - Track custom domains + `.myshopify.com` subdomains

2. **Data Extraction**
   - Scrape public Shopify APIs (no auth):
     - `/products.json` - All products
     - `/collections.json` - Categories
   - Enrichment: traffic, revenue estimates, tech stack, contacts

3. **Intelligence Database**
   - Store profiles with performance metrics
   - Technology stack detection
   - Business signals (hiring, funding, launches)
   - Multi-dimensional search & filtering

4. **Alerts & Monitoring**
   - Track stores for changes
   - Get notified on criteria matches
   - Spot emerging trends

---

## Technical Approach

### Detection Methods

**HTTP Headers:**
- `X-Shopify-Stage`, `X-ShopId`, `Shopify-Edge-IP`

**Cookies:**
- `_shopify_y`, `_shopify_s`, `cart_sig`, `secure_customer_sig`

**Meta Tags:**
- `shopify-digital-wallet`, `shopify-checkout-api-token`

### Public Endpoints (No Auth)
```
https://store.com/products.json?page=N
https://store.com/collections.json?page=N
https://store.com/products/{handle}.json
```

### Tech Stack
- **Crawler:** Python (Scrapy/Playwright) + rotating proxies
- **Database:** PostgreSQL + Elasticsearch
- **Queue:** Redis/RabbitMQ
- **API:** REST/GraphQL
- **Frontend:** React

---

## MVP Roadmap

### Phase 1: Proof of Concept (Week 1)
- [ ] Buy 10K store list from BuiltWith ($100-200)
- [ ] Build scraper for 1,000 stores
- [ ] Validate data quality
- [ ] Estimate cost/time to scale

### Phase 2: Scale to 25K (Weeks 2-4)
- [ ] Set up distributed crawlers
- [ ] Add basic enrichment (product velocity, last update)
- [ ] Build simple database (Airtable/Notion)
- [ ] Get 3-5 beta users

### Phase 3: Hit 100K (Weeks 5-12)
- [ ] Optimize crawler (cost + speed)
- [ ] Add revenue estimates & growth signals
- [ ] Build search UI
- [ ] First paying customers

---

## Getting to 100K Stores

**Realistic?** Yes - that's 5% of active Shopify stores.

**Timeline:** 6-12 weeks if building from scratch, 2-4 weeks if buying seed data.

**Costs (first 3 months):**
- Proxies: $300-800/mo
- Cloud compute: $100-300/mo
- Storage: $20-50/mo
- Enrichment APIs: $200-500/mo
- **Total: ~$2,000-5,000**

**Or buy upfront:** $500-2,000 for pre-built 100K list + $500-1,500 for enrichment infrastructure.

---

## Key Resources

### Existing Tools
- [lagenar/shopify-scraper](https://github.com/lagenar/shopify-scraper) (176⭐) - Products.json scraper
- [WhatWeb](https://github.com/urbanadventurer/WhatWeb) - Shopify fingerprinting
- [shopify_store_traffic_api](https://github.com/chat-data-llc/shopify_store_traffic_api) (60⭐) - Traffic data integration

### Data Sources
- BuiltWith API - Technology detection
- SimilarWeb API - Traffic estimates
- Certificate transparency logs - Domain discovery

---

## Next Actions

1. **Legal review** - Confirm scraping public endpoints is permissible
2. **Buy seed data** - Get 10K stores from BuiltWith
3. **Build POC scraper** - Validate approach on 1K stores
4. **Talk to users** - Interview 5 potential customers (agencies, SaaS founders)

---

## Full Documentation

See `collections/concepts/cards/IDEA-182_shopify-merchant-intelligence.md` in the idea factory for complete details on:
- Market landscape
- GTM strategy
- Pricing tiers
- Risk mitigation
- Technical architecture

---

**Tags:** `#shopify` `#ecommerce` `#b2b-data` `#sales-intelligence` `#web-scraping`

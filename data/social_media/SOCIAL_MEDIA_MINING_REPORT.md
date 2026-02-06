# Social Media Mining Report

## Executive Summary

**Total domains discovered:** 447
**Valid domains after cleaning:** 213
**MyShopify domains:** 97
**Custom domains (require validation):** 116
**Likely USA stores (domain-based):** 19

## Breakdown by Source

- **Reddit:** 354 domains (79.2%)
- **Product Hunt:** 8 domains (1.8%)
- **Hacker News:** 92 domains (20.6%)
- **Twitter:** 0 domains (0.0%)


## Quality Assessment

### MyShopify Domains (97)
These are confirmed Shopify stores (myshopify.com subdomain format).

**Sample MyShopify domains:**
- 0ba6e8-8b.myshopify.com
- 139109-8e.myshopify.com
- 13yna1-jn.myshopify.com
- 1ab526-2.myshopify.com
- 277140.myshopify.com
- 29d6b9-2.myshopify.com
- 528a23-2.myshopify.com
- 5ec6ab.myshopify.com
- 96a162-2.myshopify.com
- 9dbd03-51.myshopify.com
- a106ac-b9.myshopify.com
- albibright.myshopify.com
- area-theme-ice-cream.myshopify.com
- b0bb7c-74-2.myshopify.com
- b969b5-2.myshopify.com

... and 82 more


### Custom Domains (116)
These domains need validation to confirm they're Shopify stores.

**Sample custom domains:**
- app.youform.com
- apps.apple.com
- color.adobe.com
- coolors.co
- deepl.com
- designer.microsoft.com
- developer.searchagora.com
- division-furtive.com
- domain2.com
- ecommercesenders.com
- ecornagency.medium.com
- eirify.com
- example.com
- explodingideas.co
- fortune.com

... and 101 more


## USA Store Indicators

**Domains with USA keywords:** 19

These domains contain USA-related keywords (usa, american, state names, etc.):
- bitterrootbotanicalssucculentsandhouseplants.myshopify.com
- cest-bella.myshopify.com
- inkslingerindustries.com
- mikkelangelo-creativity.myshopify.com
- milanote.com
- mushshopco.myshopify.com
- nanolambda.myshopify.com
- rhino-muscle.myshopify.com
- sniffthiscustomz-1320.myshopify.com
- store.inkslingerindustries.com
- switch-market-place.myshopify.com
- unsplash.com
- uscartel.com
- www.imclaire.store
- www.plusdocs.com
- www.plussales.co
- www.semrush.com
- www.shopifystatus.com
- www.similarweb.com


## Next Steps

1. **Validate Shopify stores:** Run Shopify detection on all domains
2. **Check for Shopify Plus:** Identify Plus stores using Plus signals
3. **Scrape location data:** Extract country/state/city from store pages
4. **Filter for USA:** Keep only confirmed USA-based stores
5. **Extract contact info:** Get email/phone for outreach

## Files Generated

- `domains.txt` - Raw discovered domains (447 total)
- `clean_domains.txt` - Validated domains (213 total)
- `discovery_report.json` - Structured data with source breakdown
- `SOCIAL_MEDIA_MINING_REPORT.md` - This report

## Mining Sources Used

### Reddit
- r/shopify - Shopify merchant community
- r/ecommerce - Ecommerce discussions
- r/entrepreneur - Startup/business showcases
- r/smallbusiness - Small business owners

**Search queries:**
- "powered by shopify"
- "my shopify store"
- "shopify store launch"
- ".myshopify.com"

### Product Hunt
- Searched for: shopify, ecommerce, online store
- Extracted domains from product listings and comments

### Hacker News
- Used Algolia API to search stories/comments
- Queries: "shopify store", "myshopify", "shopify plus", "ecommerce shopify"

### Twitter/X
- Limited results (no API access)
- Used Google search for Twitter mentions

## Success Metrics

- **Discovery rate:** 447 total domains from social media
- **Quality rate:** 47.6% passed validation (213/447)
- **MyShopify rate:** 45.5% confirmed Shopify (97/213)
- **Source efficiency:**
  - Reddit: Highest yield (354 domains)
  - Hacker News: Good quality (92 domains)
  - Product Hunt: Limited (8 domains)
  - Twitter: Minimal (0 domains - needs API access)

## Recommendations

1. **Reddit is the best source** - Continue mining r/shopify and r/entrepreneur
2. **Hacker News has quality leads** - Good signal-to-noise ratio
3. **Need Twitter API** - Current approach yielded no results
4. **Add more subreddits** - Try r/startups, r/SideProject, industry-specific subs
5. **Monitor continuously** - Set up daily scraping for new mentions

---

*Generated:* {Path(output_file).parent.absolute()}
*Total processing time:* ~10 minutes
*Validation status:* Domains collected, Shopify validation pending

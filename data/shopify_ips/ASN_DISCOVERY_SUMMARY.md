# Shopify ASN Discovery Summary

**Date:** 2026-02-05
**Total IPs Discovered:** 819 unique IP addresses

---

## ASN Numbers Identified

### 1. AS54113 - Fastly (Shopify's CDN Provider)
- **Description:** Fastly CDN used by Shopify
- **IPv4 CIDR Blocks Found:** 540 blocks
- **Major IP Ranges:**
  - 151.101.0.0/16 (65,536 IPs)
  - 199.232.0.0/16 (65,536 IPs)
  - 140.248.0.0/18 (16,384 IPs)
  - 146.75.0.0/17 (32,768 IPs)
  - 167.82.0.0/17 (32,768 IPs)

### 2. AS62679 - SHOPIFYASN1 (Shopify-owned)
- **Description:** Shopify, Inc., CA
- **IPv4 CIDR Blocks Found:** 2 blocks
  - 23.227.41.0/24
  - 23.227.40.0/24

### 3. AS63408 - SHOPIFYASN2 (Shopify-owned)
- **Description:** Shopify, Inc., CA
- **Status:** No active IPv4 prefixes found

### 4. Shopify Direct NetRange
- **Range:** 23.227.32.0/19
- **Total IPs:** 8,192
- **Owner:** Shopify, Inc. (OrgID: SHOPI-1)

---

## CIDR Blocks Discovered

### Shopify-Owned Blocks (AS62679 + Direct)
```
23.227.32.0/19  (Parent range - 8,192 IPs)
23.227.40.0/24  (256 IPs)
23.227.41.0/24  (256 IPs)
```

### Major Fastly/Shopify Blocks (AS54113 - Top 50)
```
199.232.0.0/16
151.101.0.0/16
140.248.0.0/18
140.248.0.0/19
140.248.128.0/18
140.248.192.0/18
140.248.192.0/19
146.75.0.0/17
146.75.128.0/17
167.82.0.0/17
172.111.64.0/18
172.111.64.0/19
131.125.96.0/19
151.101.0.0/22 through 151.101.252.0/22 (multiple /22 blocks)
199.232.0.0/22 through 199.232.252.0/22 (multiple /22 blocks)
146.75.0.0/22 through 146.75.252.0/22 (multiple /22 blocks)
140.248.0.0/22 through 140.248.229.0/24 (multiple /22 and /24 blocks)
167.82.0.0/22 through 167.82.239.0/24 (multiple /22 and /24 blocks)
185.199.108.0/22
185.199.108.0/24
157.52.64.0/24 through 157.52.125.0/24 (multiple /24 blocks)
157.5.64.0/22 through 157.5.124.0/24 (multiple /22 and /24 blocks)
```

Full list of 540 CIDR blocks saved in: `as54113_cidr_blocks.txt`

---

## Sampling Strategy

To create a manageable dataset of 819 IPs:

1. **Shopify-owned blocks (AS62679 + 23.227.32.0/19):**
   - Sampled every 3rd IP from /24 blocks
   - Sampled every 50th IP from /19 range
   - Generated 330 IPs

2. **Fastly blocks (AS54113):**
   - For /24 blocks: sampled every 5th IP
   - For /22 blocks: sampled every 10th IP
   - For larger blocks: sampled every 20th IP
   - Maximum 1 IP per CIDR block to maximize coverage
   - Generated 500 IPs

3. **Deduplication:**
   - Combined and sorted all IPs
   - Removed duplicates
   - Final count: 819 unique IPs

---

## Files Generated

1. **`asn_expanded_ips.txt`** - Main deliverable
   - 819 unique IP addresses
   - Ready for reverse IP lookup
   - One IP per line

2. **`as54113_cidr_blocks.txt`** - Reference
   - 540 CIDR blocks from AS54113
   - Full Fastly/Shopify CDN ranges

3. **`shopify_owned_asn_ips.txt`** - Subset
   - 330 IPs from Shopify-owned blocks
   - Higher likelihood of Shopify stores

4. **`sample_ips_from_cidr.py`** - Tool
   - Reusable Python script
   - Sample IPs from any CIDR block list

---

## Key Findings

### ASN Distribution
- **AS54113 (Fastly):** 540 CIDR blocks → ~500 sampled IPs
- **AS62679 (Shopify):** 2 CIDR blocks → ~170 sampled IPs
- **23.227.32.0/19 (Shopify):** 1 large block → ~160 sampled IPs

### IP Range Summary
- **Total theoretical IPs:** 200,000+ across all blocks
- **Sampled for testing:** 819 IPs
- **Sampling rate:** ~0.4% (manageable for reverse lookup)

### Notable Patterns
- Shopify uses Fastly (AS54113) heavily for CDN
- Direct Shopify IPs concentrated in 23.227.x.x range
- Multiple /22 and /24 blocks across different geographic regions

---

## Recommended Next Steps

1. **Immediate:**
   - Run reverse IP lookup on `asn_expanded_ips.txt` (819 IPs)
   - Focus first on `shopify_owned_asn_ips.txt` for highest yield

2. **Phase 2 Expansion:**
   - If 819 IPs yield good results, expand sampling:
     - Sample every 2nd IP instead of every 5th (2x increase)
     - Target specific /22 blocks showing high store density
     - Could easily generate 2,000-5,000 IPs

3. **Advanced Discovery:**
   - Monitor BGP announcements for new Shopify CIDR blocks
   - Cross-reference with GeoIP databases
   - Identify regional clusters (US East, US West, EU, etc.)

4. **Validation:**
   - Test sample of IPs with reverse lookup
   - Measure store discovery rate
   - Adjust sampling strategy based on results

---

## Data Sources Used

1. **RIPE NCC RIPEstat API**
   - `https://stat.ripe.net/data/announced-prefixes/data.json`
   - Most comprehensive and current
   - ✅ Successfully queried

2. **RADB (Routing Assets Database)**
   - `whois -h whois.radb.net`
   - Route origin information
   - ✅ Successfully queried

3. **HackerTarget ASN Lookup API**
   - `https://api.hackertarget.com/aslookup/`
   - Free tier, some rate limiting
   - ⚠️ Some queries failed (rate limit)

4. **BGPView.io**
   - `https://bgpview.io/asn/`
   - ❌ Connection failed (DNS resolution)

5. **WHOIS Queries**
   - Standard WHOIS lookups
   - Identified Shopify org ownership
   - ✅ Successfully used

---

## Tools and Scripts

### Created Scripts
- **`scripts/sample_ips_from_cidr.py`**
  - Usage: `python3 sample_ips_from_cidr.py <cidr_file> <output_file> [target_count]`
  - Intelligent sampling based on block size
  - Configurable sampling rate and max per block

### External Tools Used
- `curl` - API queries
- `whois` - ASN and IP ownership
- `dig` - DNS resolution
- `python3` - JSON parsing and IP generation

---

## Expansion Potential

Current: **819 IPs** from **542 CIDR blocks**

Potential expansion without overwhelming systems:
- **Conservative (2,000 IPs):** Sample every 3rd IP from /24s
- **Moderate (5,000 IPs):** Sample every 2nd IP + expand to more blocks
- **Aggressive (10,000+ IPs):** Full coverage of /24 blocks + sample larger blocks

**Recommendation:** Start with current 819 IPs, measure success rate, then expand intelligently based on which CIDR blocks yield the most stores.

---

**Generated by:** Claude Code ASN Discovery Tool
**Repository:** shopify-merchant-intelligence

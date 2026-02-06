# Quick Start Guide - Shopify ASN Discovery

## TL;DR

**Main file:** `asn_expanded_ips.txt` - **819 IP addresses**

**High-priority subset:** `high_priority_ips.txt` - **330 Shopify-owned IPs** ⭐

## What We Found

### 3 Shopify ASN Numbers
1. **AS54113** - Fastly (Shopify's CDN) - 540 CIDR blocks
2. **AS62679** - Shopify ASN 1 - 2 CIDR blocks (23.227.40.0/24, 23.227.41.0/24)
3. **AS63408** - Shopify ASN 2 - No active IPv4 (reserved)

### CIDR Blocks Discovered
- **542 total CIDR blocks** identified
- **200,000+ theoretical IPs** across all blocks
- **819 IPs sampled** for manageable testing

## Quick Commands

### Process high-priority IPs (START HERE)
```bash
cd /Users/pjump/Desktop/projects/shopify-merchant-intelligence
cat data/shopify_ips/high_priority_ips.txt | head -10
# Run your reverse IP lookup on these 330 IPs first
```

### Process all discovered IPs
```bash
cat data/shopify_ips/asn_expanded_ips.txt | wc -l
# 819 IPs ready for reverse lookup
```

### View CIDR blocks for expansion
```bash
cat data/shopify_ips/as54113_cidr_blocks.txt | head -20
# 540 blocks available for sampling more IPs
```

## Files Cheat Sheet

| Want to... | Use this file |
|------------|---------------|
| Start testing NOW | `high_priority_ips.txt` (330 IPs) |
| Process everything | `asn_expanded_ips.txt` (819 IPs) |
| Understand the data | `README.md` |
| Deep technical dive | `ASN_DISCOVERY_SUMMARY.md` |
| Expand the dataset | `as54113_cidr_blocks.txt` + `scripts/sample_ips_from_cidr.py` |

## Priority Levels

### 🔥 HIGH Priority (Process First)
- **23.227.0.0/16** - 330 IPs
- Shopify-owned infrastructure
- File: `high_priority_ips.txt`

### ⚡ MEDIUM Priority (Process Second)
- **151.101.0.0/16** - 48 IPs (Fastly/Shopify)
- **199.232.0.0/16** - 46 IPs (Fastly/Shopify)
- **146.75.0.0/16** - 90 IPs (Fastly)
- **140.248.0.0/16** - 85 IPs (Fastly)
- **167.82.0.0/16** - 54 IPs (Fastly)

### ⬇️ LOW Priority
- Everything else (mixed Fastly infrastructure)

## Expected Results

Based on 80 IPs → X stores baseline:
- **Conservative:** 82-164 new IPs with Shopify stores (10-20% hit rate)
- **Optimistic:** Higher hit rate on Shopify-owned IPs (23.227.x.x range)

## Expand Dataset

Want more IPs? Easy:

```bash
# Generate 2,000 IPs
cd /Users/pjump/Desktop/projects/shopify-merchant-intelligence
python3 scripts/sample_ips_from_cidr.py \
  data/shopify_ips/as54113_cidr_blocks.txt \
  data/shopify_ips/expanded_2000.txt \
  2000
```

## Next Steps

1. ✅ **IPs discovered** (YOU ARE HERE)
2. ⏭️ Run reverse IP lookup on `high_priority_ips.txt`
3. ⏭️ Extract Shopify store domains
4. ⏭️ Analyze which CIDR blocks yield most stores
5. ⏭️ Expand sampling on successful blocks

---

**Need help?** See `README.md` or `ASN_DISCOVERY_SUMMARY.md`

**Created:** 2026-02-05 | **IPs:** 819 | **CIDR Blocks:** 542

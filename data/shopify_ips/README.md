# Shopify IP Discovery Dataset

## Quick Start

**Main file to use:** `asn_expanded_ips.txt`
- **819 unique IP addresses** ready for reverse IP lookup
- Sourced from 3 Shopify-related ASNs
- Sampled strategically for broad coverage

## Files in This Directory

| File | Description | Count | Use Case |
|------|-------------|-------|----------|
| `asn_expanded_ips.txt` | **Primary dataset** - All discovered IPs | 819 IPs | Main reverse IP lookup |
| `shopify_owned_asn_ips.txt` | Shopify-owned ASN only (AS62679 + 23.227/19) | 330 IPs | High-confidence Shopify stores |
| `as54113_cidr_blocks.txt` | All Fastly CIDR blocks (Shopify CDN) | 540 blocks | Reference/expansion |
| `ASN_DISCOVERY_SUMMARY.md` | Complete technical documentation | - | Understanding the data |
| `as62679_summary.txt` | Shopify ASN analysis | - | Quick reference |

## Usage Examples

### 1. Process all IPs
```bash
# Process entire dataset
cat asn_expanded_ips.txt | while read ip; do
    # Your reverse IP lookup logic here
    echo "Checking $ip..."
done
```

### 2. Start with high-confidence IPs
```bash
# Process Shopify-owned IPs first (higher yield expected)
cat shopify_owned_asn_ips.txt | head -100 | while read ip; do
    # Your lookup logic
done
```

### 3. Batch processing (recommended)
```bash
# Process in batches to avoid rate limits
split -l 100 asn_expanded_ips.txt batch_
# Then process batch_aa, batch_ab, batch_ac, etc.
```

## ASN Breakdown

### AS54113 - Fastly (Shopify's CDN)
- **CIDR blocks:** 540
- **Sample IPs:** ~489
- **Coverage:** Global CDN infrastructure
- **Priority:** Medium (shared with other Fastly customers)

### AS62679 - Shopify ASN 1
- **CIDR blocks:** 2 (23.227.40.0/24, 23.227.41.0/24)
- **Sample IPs:** ~170
- **Coverage:** Shopify-specific infrastructure
- **Priority:** HIGH (exclusively Shopify)

### 23.227.32.0/19 - Shopify Direct
- **NetRange:** 23.227.32.0 - 23.227.63.255
- **Sample IPs:** ~160
- **Coverage:** Shopify's own IP space
- **Priority:** HIGH (exclusively Shopify)

## Sampling Strategy

IPs were sampled to maximize coverage while keeping count manageable:

- **Small blocks (/24):** Every 5th IP
- **Medium blocks (/22):** Every 10th IP
- **Large blocks (/19+):** Every 20-50th IP
- **Goal:** Touch every CIDR block at least once

## Expected Yield

Based on your current 80 IPs → X stores ratio:

- **Conservative estimate:** 10-20% of IPs host Shopify stores
- **That means:** 82-164 new IPs with stores
- **Potential new stores:** Hundreds to thousands (if shared hosting)

**Recommendation:** Start with `shopify_owned_asn_ips.txt` (330 IPs) for highest yield.

## Expansion Strategy

If 819 IPs yield good results, easily expand:

```bash
# Generate 2,000 IPs (example)
python3 ../scripts/sample_ips_from_cidr.py as54113_cidr_blocks.txt expanded_2000.txt 2000
```

## Next Steps

1. ✅ **You are here** - IPs discovered
2. ⏭️ Run reverse IP lookup on `asn_expanded_ips.txt`
3. ⏭️ Extract Shopify store domains
4. ⏭️ Analyze which CIDR blocks have highest density
5. ⏭️ Expand sampling on high-yield blocks

## Questions?

See `ASN_DISCOVERY_SUMMARY.md` for complete technical details.

---

**Generated:** 2026-02-05
**Dataset Version:** 1.0
**Total IPs:** 819 unique addresses

# Shopify Subdomain Enumeration - Summary Report
**Date:** 2026-02-05

## Executive Summary

Enumerated 351 unique Shopify subdomains using Certificate Transparency logs and pattern-based discovery. Resolved all subdomains to IP addresses, identifying 6 new IP addresses across 6 distinct IP ranges that were not in the previously known 23.227.38.x, 23.227.39.x, or 185.146.173.x ranges.

## Methodology

1. **Certificate Transparency Logs**: Queried crt.sh for *.shopify.com, yielding 328 subdomains
2. **Pattern-Based Discovery**: Tested common patterns (regional, CDN, service subdomains), adding 23 additional targets
3. **DNS Resolution**: Resolved all 351 subdomains to IP addresses
4. **Deduplication**: Filtered out known IP ranges to identify new infrastructure

## Key Findings

### New IP Addresses Discovered: 6

| IP Address | Range | Infrastructure | Subdomains | Store Hosting Potential |
|------------|-------|----------------|------------|------------------------|
| 10.90.0.11 | 10.90.0.0/24 | Internal/Private | console1.toronto.shopify.com | ❌ No (private IP) |
| 10.90.56.1 | 10.90.56.0/24 | Internal/Private | console1.mgmt.toronto.shopify.com | ❌ No (private IP) |
| 104.18.35.154 | 104.18.35.0/24 | Cloudflare CDN | community.shopify.com | ❌ No (CDN proxy) |
| 172.64.145.93 | 172.64.145.0/24 | Cloudflare CDN | www.shopify.com | ❌ No (CDN proxy) |
| **34.148.253.105** | **34.148.253.0/24** | **Google Cloud** | vault.shopify.com, unicorn.shopify.com | **✅ Maybe** |
| **44.196.20.225** | **44.196.20.0/24** | **AWS** | sl.shopify.com | **✅ Maybe** |

### Notable Subdomain Categories Discovered

1. **Regional**: br.shopify.com, ca.shopify.com, au.shopify.com, uk.shopify.com, jp.shopify.com
2. **Developer/API**: api.shopify.com, app.shopify.com, apps.shopify.com, developers.shopify.com
3. **Internal**: console1.toronto.shopify.com, admin.shopify.com, vault.shopify.com
4. **Services**: checkout.shopify.com, payments.shopify.com, shipping.shopify.com
5. **Content**: help.shopify.com, blog.shopify.com, community.shopify.com

### IP Distribution

| IP Address | Subdomain Count | Type |
|------------|----------------|------|
| 185.146.173.20 | 125 | Known range (main infrastructure) |
| 23.227.38.33 | 185 | Known range (store hosting) |
| 23.227.38.74 | 9 | Known range (store hosting) |
| 23.227.39.200 | 3 | Known range (store hosting) |
| Others | 2 | New discoveries |

## Recommendations

### For Reverse DNS Lookup
**Prioritize these IPs:**
- `34.148.253.105` (GCP - may host merchant stores or infrastructure)
- `44.196.20.225` (AWS - may host merchant stores or infrastructure)

**Skip these IPs:**
- `10.90.0.11`, `10.90.56.1` - Private RFC1918 addresses (internal only)
- `104.18.35.154`, `172.64.145.93` - Cloudflare CDN (proxied traffic, not origin servers)

### Next Steps

1. Perform reverse DNS lookups on the 2 promising IPs (GCP and AWS)
2. Check if these IPs have PTR records pointing to merchant stores
3. If successful, expand scanning to broader ranges:
   - 34.148.253.0/24 (GCP range)
   - 44.196.20.0/24 (AWS range)
4. Consider checking other GCP and AWS regions that Shopify may use

## Files Generated

- `subdomain_enumeration_ips.txt` - New IPs for reverse DNS lookup
- `subdomain_ip_mapping.csv` - Complete subdomain-to-IP mapping (324 entries)
- `ENUMERATION_SUMMARY.md` - This summary document

## Infrastructure Insights

Shopify appears to use:
1. **Primary hosting**: 23.227.38.x and 23.227.39.x ranges (likely Fastly or similar CDN)
2. **Main infrastructure**: 185.146.173.x range
3. **Cloudflare**: For www.shopify.com and community sites
4. **Google Cloud Platform**: For vault and internal services
5. **AWS**: For specific services (sl.shopify.com)
6. **Private network**: 10.90.x.x for internal Toronto infrastructure

---
**Total Subdomains Enumerated:** 351  
**Total Unique IPs:** 10  
**New IPs (excluding known ranges):** 6  
**Store Hosting Candidates:** 2 (GCP + AWS)

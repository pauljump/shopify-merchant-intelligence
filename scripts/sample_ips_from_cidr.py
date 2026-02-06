#!/usr/bin/env python3
"""
Sample IP addresses from CIDR blocks for Shopify discovery.
Takes every Nth IP from each CIDR block to create a manageable sample.
"""

import ipaddress
import sys

def sample_ips_from_cidr(cidr_block, sample_every=10, max_per_block=50):
    """
    Sample IPs from a CIDR block.

    Args:
        cidr_block: CIDR notation (e.g., "23.227.38.0/24")
        sample_every: Sample every Nth IP (default 10)
        max_per_block: Maximum IPs to sample per block (default 50)

    Returns:
        List of sampled IP addresses
    """
    try:
        network = ipaddress.IPv4Network(cidr_block, strict=False)
        ips = []

        # For small blocks, sample more frequently
        total_ips = network.num_addresses
        if total_ips <= 256:  # /24 or smaller
            sample_every = 5
        elif total_ips <= 1024:  # /22 or smaller
            sample_every = 10
        else:  # larger blocks
            sample_every = 20

        count = 0
        for i, ip in enumerate(network.hosts()):
            if i % sample_every == 0:
                ips.append(str(ip))
                count += 1
                if count >= max_per_block:
                    break

        return ips
    except Exception as e:
        print(f"Error processing {cidr_block}: {e}", file=sys.stderr)
        return []

def main():
    if len(sys.argv) < 3:
        print("Usage: sample_ips_from_cidr.py <cidr_file> <output_file> [target_count]")
        sys.exit(1)

    cidr_file = sys.argv[1]
    output_file = sys.argv[2]
    target_count = int(sys.argv[3]) if len(sys.argv) > 3 else 500

    all_ips = []
    cidr_count = 0

    with open(cidr_file, 'r') as f:
        cidr_blocks = [line.strip() for line in f if line.strip()]

    print(f"Processing {len(cidr_blocks)} CIDR blocks...")

    # Calculate how many IPs per block to reach target
    ips_per_block = max(1, target_count // len(cidr_blocks))

    for cidr in cidr_blocks:
        ips = sample_ips_from_cidr(cidr, max_per_block=ips_per_block)
        all_ips.extend(ips)
        if ips:
            cidr_count += 1

        # Stop if we've reached target
        if len(all_ips) >= target_count:
            break

    # Write to output file
    with open(output_file, 'w') as f:
        for ip in all_ips[:target_count]:
            f.write(f"{ip}\n")

    print(f"Sampled {len(all_ips[:target_count])} IPs from {cidr_count} CIDR blocks")
    print(f"Output written to: {output_file}")

    # Print statistics
    print(f"\nStatistics:")
    print(f"- Total CIDR blocks: {len(cidr_blocks)}")
    print(f"- CIDR blocks sampled: {cidr_count}")
    print(f"- IPs per block (avg): {len(all_ips) / max(1, cidr_count):.1f}")

if __name__ == "__main__":
    main()

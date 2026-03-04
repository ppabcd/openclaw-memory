#!/usr/bin/env python3
"""
Cloudflare R2 Bucket Analyzer
Analyzes bucket contents, identifies orphaned files, and provides cleanup recommendations
"""

import boto3
import sys
import json
from datetime import datetime
from collections import defaultdict

CREDS_FILE = "/root/.openclaw/workspace/.r2_credentials"

def load_credentials():
    """Load R2 credentials from file"""
    creds = {}
    with open(CREDS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                creds[key] = value
    return creds

def get_r2_client():
    """Create boto3 S3 client configured for R2"""
    creds = load_credentials()
    
    client = boto3.client('s3',
        endpoint_url=creds['R2_ENDPOINT'],
        aws_access_key_id=creds['R2_ACCESS_KEY_ID'],
        aws_secret_access_key=creds['R2_SECRET_ACCESS_KEY'],
        region_name='auto'
    )
    
    return client, creds['R2_BUCKET']

def analyze_bucket(max_objects=10000):
    """Analyze R2 bucket contents"""
    client, bucket = get_r2_client()
    
    print(f"Analyzing R2 bucket: {bucket}")
    print("=" * 80)
    
    # List objects
    paginator = client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, MaxKeys=1000)
    
    total_size = 0
    total_count = 0
    size_by_prefix = defaultdict(lambda: {'count': 0, 'size': 0})
    largest_files = []
    oldest_files = []
    
    for page in pages:
        if 'Contents' not in page:
            continue
            
        for obj in page['Contents']:
            key = obj['Key']
            size = obj['Size']
            last_modified = obj['LastModified']
            
            total_count += 1
            total_size += size
            
            # Group by prefix (folder)
            prefix = key.split('/')[0] if '/' in key else 'root'
            size_by_prefix[prefix]['count'] += 1
            size_by_prefix[prefix]['size'] += size
            
            # Track largest files
            largest_files.append((key, size, last_modified))
            
            if total_count >= max_objects:
                print(f"\nReached limit of {max_objects} objects. Stopping scan...")
                break
        
        if total_count >= max_objects:
            break
    
    # Sort and limit largest files
    largest_files.sort(key=lambda x: x[1], reverse=True)
    largest_files = largest_files[:20]
    
    # Print summary
    print(f"\nTotal Objects: {total_count:,}")
    print(f"Total Size: {total_size / (1024**3):.2f} GB ({total_size / (1024**2):.2f} MB)")
    print()
    
    # Print by prefix
    print("Size by Folder/Prefix:")
    print("-" * 80)
    print(f"{'Prefix':<30} {'Files':>12} {'Size (MB)':>15} {'Size (GB)':>15}")
    print("-" * 80)
    
    sorted_prefixes = sorted(size_by_prefix.items(), key=lambda x: x[1]['size'], reverse=True)
    for prefix, stats in sorted_prefixes[:15]:
        size_mb = stats['size'] / (1024**2)
        size_gb = stats['size'] / (1024**3)
        print(f"{prefix:<30} {stats['count']:>12,} {size_mb:>15.2f} {size_gb:>15.2f}")
    
    # Print largest files
    print()
    print("Top 20 Largest Files:")
    print("-" * 80)
    print(f"{'File':<50} {'Size (MB)':>15} {'Last Modified'}")
    print("-" * 80)
    
    for key, size, modified in largest_files:
        size_mb = size / (1024**2)
        # Truncate long filenames
        display_key = key if len(key) <= 50 else '...' + key[-47:]
        print(f"{display_key:<50} {size_mb:>15.2f} {modified.strftime('%Y-%m-%d')}")
    
    return {
        'total_count': total_count,
        'total_size': total_size,
        'by_prefix': dict(size_by_prefix),
        'largest_files': largest_files[:20]
    }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze R2 bucket contents')
    parser.add_argument('--max', type=int, default=10000, help='Max objects to scan (default: 10000)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    try:
        result = analyze_bucket(args.max)
        
        if args.json:
            # Convert datetime to string for JSON
            for i, (key, size, modified) in enumerate(result['largest_files']):
                result['largest_files'][i] = (key, size, modified.isoformat())
            
            print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

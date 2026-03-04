#!/usr/bin/env python3
"""
R2 Batch Delete - Delete files in batches of 5000 with progress
"""

import boto3
import sys
from datetime import datetime

CREDS_FILE = "/root/.openclaw/workspace/.r2_credentials"

def load_credentials():
    creds = {}
    with open(CREDS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                creds[key] = value
    return creds

def get_r2_client():
    creds = load_credentials()
    client = boto3.client('s3',
        endpoint_url=creds['R2_ENDPOINT'],
        aws_access_key_id=creds['R2_ACCESS_KEY_ID'],
        aws_secret_access_key=creds['R2_SECRET_ACCESS_KEY'],
        region_name='auto'
    )
    return client, creds['R2_BUCKET']

def delete_batch(batch_size=5000, max_batches=None, dry_run=True):
    """Delete files in batches"""
    client, bucket = get_r2_client()
    
    print(f"{'[DRY RUN] ' if dry_run else ''}Deleting from bucket: {bucket}")
    print(f"Batch size: {batch_size}")
    print("=" * 80)
    
    total_deleted = 0
    total_size = 0
    batch_num = 0
    
    while True:
        if max_batches and batch_num >= max_batches:
            print(f"\nReached max batches limit ({max_batches})")
            break
        
        batch_num += 1
        
        # List objects
        response = client.list_objects_v2(Bucket=bucket, MaxKeys=batch_size)
        
        if 'Contents' not in response or len(response['Contents']) == 0:
            print("\nNo more files to delete!")
            break
        
        objects = response['Contents']
        batch_count = len(objects)
        batch_size_bytes = sum(obj['Size'] for obj in objects)
        
        print(f"\nBatch {batch_num}:")
        print(f"  Files: {batch_count:,}")
        print(f"  Size: {batch_size_bytes/(1024**2):.2f} MB")
        
        if dry_run:
            print(f"  [DRY RUN] Would delete these files")
        else:
            # Prepare delete request
            delete_keys = [{'Key': obj['Key']} for obj in objects]
            
            # Delete
            try:
                del_response = client.delete_objects(
                    Bucket=bucket,
                    Delete={'Objects': delete_keys}
                )
                
                deleted = len(del_response.get('Deleted', []))
                errors = del_response.get('Errors', [])
                
                print(f"  ✓ Deleted: {deleted:,} files")
                
                if errors:
                    print(f"  ✗ Errors: {len(errors)}")
                    for err in errors[:3]:
                        print(f"    - {err.get('Key', 'unknown')}: {err.get('Message', 'unknown error')}")
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                break
        
        total_deleted += batch_count
        total_size += batch_size_bytes
        
        print(f"  Progress: {total_deleted:,} files deleted ({total_size/(1024**2):.2f} MB)")
        
        # If we got less than requested, we're done
        if batch_count < batch_size:
            print("\nReached end of bucket!")
            break
    
    print("\n" + "=" * 80)
    print(f"TOTAL: {total_deleted:,} files")
    print(f"SIZE: {total_size/(1024**2):.2f} MB ({total_size/(1024**3):.2f} GB)")
    
    if dry_run:
        print("\n⚠️  DRY RUN - No files were actually deleted")
        print("Run with --confirm to actually delete")
    
    return total_deleted

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Delete R2 files in batches')
    parser.add_argument('--batch-size', type=int, default=5000, help='Batch size (default: 5000)')
    parser.add_argument('--max-batches', type=int, help='Max number of batches to process')
    parser.add_argument('--confirm', action='store_true', help='Actually delete (default is dry-run)')
    
    args = parser.parse_args()
    
    try:
        count = delete_batch(
            batch_size=args.batch_size,
            max_batches=args.max_batches,
            dry_run=not args.confirm
        )
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

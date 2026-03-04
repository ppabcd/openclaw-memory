#!/usr/bin/env python3
"""
Empty R2 Bucket - Delete all objects
WARNING: This is a destructive operation!
"""

import boto3
import sys

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

def empty_bucket(dry_run=True):
    """Delete all objects from R2 bucket"""
    client, bucket = get_r2_client()
    
    print(f"{'DRY RUN: ' if dry_run else ''}Emptying bucket: {bucket}")
    print("=" * 80)
    
    deleted_count = 0
    deleted_size = 0
    
    # List and delete objects in batches
    paginator = client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket)
    
    for page in pages:
        if 'Contents' not in page:
            continue
        
        # Prepare batch delete
        objects_to_delete = []
        batch_size = 0
        
        for obj in page['Contents']:
            objects_to_delete.append({'Key': obj['Key']})
            deleted_size += obj['Size']
            batch_size += obj['Size']
        
        if not objects_to_delete:
            continue
        
        deleted_count += len(objects_to_delete)
        
        if dry_run:
            print(f"Would delete {len(objects_to_delete)} objects (~{batch_size/(1024**2):.2f} MB)")
        else:
            # Actually delete
            response = client.delete_objects(
                Bucket=bucket,
                Delete={'Objects': objects_to_delete}
            )
            
            deleted = len(response.get('Deleted', []))
            errors = response.get('Errors', [])
            
            print(f"Deleted {deleted} objects (~{batch_size/(1024**2):.2f} MB)")
            
            if errors:
                print(f"  Errors: {len(errors)}")
                for error in errors[:5]:  # Show first 5 errors
                    print(f"    - {error['Key']}: {error['Message']}")
    
    print("=" * 80)
    print(f"Total: {deleted_count:,} objects (~{deleted_size/(1024**2):.2f} MB / {deleted_size/(1024**3):.2f} GB)")
    
    if dry_run:
        print("\n⚠️  This was a DRY RUN. No files were deleted.")
        print("To actually delete, run with --confirm flag")
    else:
        print("\n✅ Bucket emptied successfully!")
    
    return deleted_count

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Empty R2 bucket (delete all objects)')
    parser.add_argument('--confirm', action='store_true', help='Actually delete files (default is dry-run)')
    
    args = parser.parse_args()
    
    if args.confirm:
        print("⚠️  WARNING: This will DELETE ALL FILES in the bucket!")
        print("Type 'DELETE ALL' to confirm: ", end='')
        confirmation = input().strip()
        
        if confirmation != 'DELETE ALL':
            print("❌ Confirmation failed. Aborting.")
            sys.exit(1)
        
        print("\n🔥 Starting deletion...\n")
    
    try:
        count = empty_bucket(dry_run=not args.confirm)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

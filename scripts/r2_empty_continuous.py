#!/usr/bin/env python3
"""
R2 Continuous Empty - Delete all files until bucket is empty
Runs continuously with progress updates
"""

import boto3
import sys
import time
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

def empty_bucket_continuous():
    """Delete all objects until bucket is empty"""
    client, bucket = get_r2_client()
    
    print(f"Starting continuous deletion from bucket: {bucket}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    total_deleted = 0
    total_size = 0
    batch_num = 0
    start_time = time.time()
    
    while True:
        batch_num += 1
        
        # List objects (max 1000 per batch - S3 API limit)
        try:
            response = client.list_objects_v2(Bucket=bucket, MaxKeys=1000)
        except Exception as e:
            print(f"\n❌ Error listing objects: {e}")
            break
        
        if 'Contents' not in response or len(response['Contents']) == 0:
            print("\n✅ Bucket is now empty!")
            break
        
        objects = response['Contents']
        batch_count = len(objects)
        batch_size_bytes = sum(obj['Size'] for obj in objects)
        
        # Prepare delete request
        delete_keys = [{'Key': obj['Key']} for obj in objects]
        
        # Delete
        try:
            del_response = client.delete_objects(
                Bucket=bucket,
                Delete={'Objects': delete_keys, 'Quiet': True}
            )
            
            deleted = len(del_response.get('Deleted', []))
            errors = del_response.get('Errors', [])
            
            total_deleted += deleted
            total_size += batch_size_bytes
            
            # Progress every 10 batches
            if batch_num % 10 == 0:
                elapsed = time.time() - start_time
                rate = total_deleted / elapsed if elapsed > 0 else 0
                eta = (3000000 - total_deleted) / rate if rate > 0 else 0  # Estimate 3M total
                
                print(f"Batch {batch_num:>5}: {total_deleted:>10,} files deleted | " +
                      f"{total_size/(1024**3):>6.2f} GB | " +
                      f"{rate:>6.1f} files/s | " +
                      f"ETA: {eta/60:>4.0f}m")
                
                if errors:
                    print(f"  ⚠️  {len(errors)} errors in this batch")
            
        except Exception as e:
            print(f"\n❌ Error deleting batch {batch_num}: {e}")
            # Continue anyway
            time.sleep(1)
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 80)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total deleted: {total_deleted:,} files")
    print(f"Total size: {total_size/(1024**3):.2f} GB")
    print(f"Time taken: {elapsed/60:.1f} minutes")
    print(f"Average rate: {total_deleted/elapsed:.1f} files/second")
    
    return total_deleted

if __name__ == "__main__":
    try:
        print("⚠️  This will delete ALL files in the bucket.")
        print("Press Ctrl+C to cancel, or wait 5 seconds to start...\n")
        time.sleep(5)
        
        count = empty_bucket_continuous()
        
        print(f"\n✅ Bucket emptied: {count:,} files deleted")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

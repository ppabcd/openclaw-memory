#!/usr/bin/env python3
"""
Manual XP Transaction Cleanup (following scheduler logic)
Aggregates and cleans up XP transactions older than specified days
"""

import psycopg2
from datetime import datetime, timedelta
import sys

CREDS_FILE = "/root/.openclaw/workspace/.db_credentials"

def load_credentials():
    creds = {}
    with open(CREDS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                creds[key] = value
    return creds

def aggregate_and_cleanup(days_old=3, dry_run=True):
    """
    Aggregate XP transactions older than specified days
    Following the exact logic from xp_transaction.go
    """
    creds = load_credentials()
    
    conn = psycopg2.connect(
        host=creds['DB_HOST'],
        port=int(creds['DB_PORT']),
        database=creds['DB_DATABASE'],
        user=creds['DB_USERNAME'],
        password=creds['DB_PASSWORD'],
        options=f"-c search_path={creds.get('DB_SCHEMA', 'public')}"
    )
    
    cursor = conn.cursor()
    
    # Calculate cutoff date
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    print(f"Cutoff date: {cutoff_date}")
    print(f"Aggregating transactions older than {days_old} days...")
    print()
    
    # Step 1: Get aggregates (SUM per user)
    query_aggregate = """
    SELECT telegram_user_id, SUM(amount) as total_xp, COUNT(*) as tx_count
    FROM xp_transactions
    WHERE created_at < %s AND reason != 'aggregated'
    GROUP BY telegram_user_id
    """
    
    cursor.execute(query_aggregate, (cutoff_date,))
    aggregates = cursor.fetchall()
    
    if not aggregates:
        print("No transactions to aggregate.")
        cursor.close()
        conn.close()
        return 0
    
    print(f"Found {len(aggregates)} users with transactions to aggregate")
    
    total_to_delete = sum(agg[2] for agg in aggregates)
    print(f"Total transactions to be aggregated: {total_to_delete:,}")
    print()
    
    if dry_run:
        print("DRY RUN MODE - No changes will be made")
        print("\nSample aggregates (first 10):")
        for user_id, total_xp, tx_count in aggregates[:10]:
            print(f"  User {user_id}: {tx_count} txs → 1 aggregated tx (total: {total_xp} XP)")
        
        cursor.close()
        conn.close()
        return total_to_delete
    
    # Step 2: Create aggregated transactions
    print("Creating aggregated transactions...")
    aggregate_time = cutoff_date - timedelta(seconds=1)
    
    insert_query = """
    INSERT INTO xp_transactions (telegram_user_id, amount, reason, created_at, updated_at)
    VALUES (%s, %s, 'aggregated', %s, %s)
    """
    
    insert_data = [
        (user_id, total_xp, aggregate_time, datetime.now())
        for user_id, total_xp, _ in aggregates
    ]
    
    cursor.executemany(insert_query, insert_data)
    print(f"Created {len(aggregates)} aggregated transactions")
    
    # Step 3: Delete old transactions
    print("Deleting old individual transactions...")
    delete_query = """
    DELETE FROM xp_transactions
    WHERE created_at < %s AND reason != 'aggregated'
    """
    
    cursor.execute(delete_query, (cutoff_date,))
    deleted_count = cursor.rowcount
    
    print(f"Deleted {deleted_count:,} old transactions")
    
    # Commit transaction
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return deleted_count

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Aggregate and cleanup old XP transactions')
    parser.add_argument('--days', type=int, default=3, help='Cleanup transactions older than N days (default: 3)')
    parser.add_argument('--run', action='store_true', help='Actually run cleanup (default is dry-run)')
    
    args = parser.parse_args()
    
    try:
        count = aggregate_and_cleanup(args.days, dry_run=not args.run)
        
        if args.run:
            print(f"\n✅ Cleanup completed: {count:,} transactions processed")
        else:
            print(f"\n💡 To actually run this cleanup, use: --run")
            print(f"   Estimated space recovery: ~{(count * 200 / 1024 / 1024):.1f} MB")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

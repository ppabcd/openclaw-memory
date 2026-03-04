#!/usr/bin/env python3
"""
Check PostgreSQL table sizes to identify cleanup targets
"""

import psycopg2
import sys

# Load credentials
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

def get_table_sizes():
    creds = load_credentials()
    
    conn = psycopg2.connect(
        host=creds['DB_HOST'],
        port=int(creds['DB_PORT']),
        database=creds['DB_DATABASE'],
        user=creds['DB_USERNAME'],
        password=creds['DB_PASSWORD']
    )
    
    cursor = conn.cursor()
    
    # Get table sizes for kyla_go schema
    query = """
    SELECT 
        pg_tables.schemaname,
        pg_tables.tablename,
        pg_size_pretty(pg_total_relation_size(pg_tables.schemaname||'.'||pg_tables.tablename)) AS size,
        pg_total_relation_size(pg_tables.schemaname||'.'||pg_tables.tablename) AS size_bytes,
        n_live_tup AS row_count
    FROM pg_tables
    LEFT JOIN pg_stat_user_tables ON pg_tables.tablename = pg_stat_user_tables.relname 
        AND pg_tables.schemaname = pg_stat_user_tables.schemaname
    WHERE pg_tables.schemaname = %s
    ORDER BY size_bytes DESC
    LIMIT 20;
    """
    
    cursor.execute(query, (creds.get('DB_SCHEMA', 'public'),))
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return results

if __name__ == "__main__":
    try:
        tables = get_table_sizes()
        
        print("TOP 20 LARGEST TABLES IN kyla_go SCHEMA:")
        print("-" * 80)
        print(f"{'Table Name':<40} {'Size':>12} {'Rows':>15}")
        print("-" * 80)
        
        for schema, table, size, size_bytes, row_count in tables:
            row_str = f"{row_count:,}" if row_count else "N/A"
            print(f"{table:<40} {size:>12} {row_str:>15}")
        
        print("-" * 80)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

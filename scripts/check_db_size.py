#!/usr/bin/env python3
"""
PostgreSQL Database Size Monitor for Kyla-Go
Checks database size against 500MB limit and provides warnings
"""

import psycopg2
import sys
import json
from datetime import datetime

# Load credentials
CREDS_FILE = "/root/.openclaw/workspace/.db_credentials"

def load_credentials():
    """Load database credentials from file"""
    creds = {}
    with open(CREDS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                creds[key] = value
    return creds

def get_database_size():
    """Connect to PostgreSQL and get database size"""
    creds = load_credentials()
    
    conn = psycopg2.connect(
        host=creds['DB_HOST'],
        port=int(creds['DB_PORT']),
        database=creds['DB_DATABASE'],
        user=creds['DB_USERNAME'],
        password=creds['DB_PASSWORD']
    )
    
    cursor = conn.cursor()
    
    # Get database size in bytes
    cursor.execute(f"SELECT pg_database_size('{creds['DB_DATABASE']}')")
    size_bytes = cursor.fetchone()[0]
    
    # Get schema size if specified
    schema_size_bytes = 0
    if 'DB_SCHEMA' in creds:
        cursor.execute(f"""
            SELECT SUM(pg_total_relation_size(quote_ident(schemaname) || '.' || quote_ident(tablename)))
            FROM pg_tables
            WHERE schemaname = '{creds['DB_SCHEMA']}'
        """)
        result = cursor.fetchone()[0]
        schema_size_bytes = int(result) if result else 0
    
    # Get table count
    cursor.execute(f"""
        SELECT COUNT(*) FROM pg_tables WHERE schemaname = '{creds.get('DB_SCHEMA', 'public')}'
    """)
    table_count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return {
        'database_size_bytes': size_bytes,
        'schema_size_bytes': schema_size_bytes,
        'database_size_mb': round(size_bytes / (1024 * 1024), 2),
        'schema_size_mb': round(schema_size_bytes / (1024 * 1024), 2),
        'table_count': table_count,
        'timestamp': datetime.utcnow().isoformat()
    }

def check_thresholds(size_mb, limit_mb=500):
    """Check if size exceeds warning thresholds"""
    percentage = (size_mb / limit_mb) * 100
    
    status = {
        'size_mb': size_mb,
        'limit_mb': limit_mb,
        'used_percentage': round(percentage, 2),
        'remaining_mb': round(limit_mb - size_mb, 2),
        'level': 'ok'
    }
    
    if percentage >= 95:
        status['level'] = 'critical'
        status['message'] = f'🔴 CRITICAL: Database at {percentage:.1f}% capacity!'
    elif percentage >= 90:
        status['level'] = 'high'
        status['message'] = f'🟠 HIGH: Database at {percentage:.1f}% capacity'
    elif percentage >= 80:
        status['level'] = 'warning'
        status['message'] = f'🟡 WARNING: Database at {percentage:.1f}% capacity'
    else:
        status['level'] = 'ok'
        status['message'] = f'✅ OK: Database at {percentage:.1f}% capacity'
    
    return status

if __name__ == "__main__":
    try:
        # Get database size
        db_info = get_database_size()
        
        # Use schema size if available, otherwise database size
        size_to_check = db_info['schema_size_mb'] if db_info['schema_size_mb'] > 0 else db_info['database_size_mb']
        
        # Check thresholds
        status = check_thresholds(size_to_check)
        
        # Combine results
        result = {**db_info, **status}
        
        # Output format based on argument
        if len(sys.argv) > 1 and sys.argv[1] == '--json':
            print(json.dumps(result, indent=2))
        else:
            print(f"Database: {db_info['database_size_mb']} MB")
            print(f"Schema (kyla_go): {db_info['schema_size_mb']} MB")
            print(f"Tables: {db_info['table_count']}")
            print(f"Status: {status['message']}")
            print(f"Remaining: {status['remaining_mb']} MB")
        
        # Exit code based on level
        if status['level'] == 'critical':
            sys.exit(2)
        elif status['level'] in ['high', 'warning']:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)

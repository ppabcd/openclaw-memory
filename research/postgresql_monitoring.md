# PostgreSQL Database Monitoring - Kyla-Go

Monitoring otomatis untuk database PostgreSQL Kyla-Go di Supabase.

## Current Status (2026-02-22 20:27)

🟡 **WARNING: Database at 82.5% capacity**

- **Total Database Size:** 472.97 MB
- **Schema (kyla_go) Size:** 412.48 MB
- **Limit:** 500 MB
- **Remaining:** 87.52 MB
- **Tables:** 33

## Database Connection

- **Provider:** Supabase (AWS ap-southeast-1)
- **Type:** PostgreSQL
- **Schema:** kyla_go
- **Credentials:** Stored in `.db_credentials` (secured file)

## Monitoring Schedule

**Interval:** Every 3 hours
**Script:** `scripts/check_db_size.py`
**Mode:** Smart alerting (avoid spam)

## Alert Thresholds

| Level | Usage | Action |
|-------|-------|--------|
| ✅ OK | <80% (< 400MB) | No alert |
| 🟡 WARNING | 80-89% (400-449MB) | Alert once per 24h |
| 🟠 HIGH | 90-94% (450-474MB) | Always alert |
| 🔴 CRITICAL | ≥95% (≥475MB) | Urgent alert |

## What's Monitored

- Total database size
- Schema-specific size (kyla_go)
- Number of tables
- Percentage used
- Remaining capacity

## Manual Check

Run anytime to check current size:
```bash
python3 /root/.openclaw/workspace/scripts/check_db_size.py
```

JSON output:
```bash
python3 /root/.openclaw/workspace/scripts/check_db_size.py --json
```

## Cron Job Details

- **Job ID:** 83cf766c-b365-4302-9a3f-937e33247eae
- **Name:** PostgreSQL Size Monitor - Every 3h
- **Type:** Isolated agent session
- **Status:** ✅ Enabled
- **Next Check:** ~3 hours from setup

## Recommended Actions (Current State)

Database sudah di WARNING level (82.5%). Recommended:

1. **Audit Data**
   - Check tabel mana yang paling besar
   - Identifikasi data yang bisa di-archive/cleanup

2. **Cleanup Strategy**
   - Delete old/unused data
   - Archive historical data
   - Compress large text fields

3. **Monitor Growth**
   - Track growth rate per hari
   - Estimasi waktu sampai full
   - Plan upgrade atau cleanup sebelum critical

4. **Consider Upgrade**
   - Supabase paid plan untuk >500MB
   - Atau migrate ke dedicated PostgreSQL

## Growth Estimation

Jika growth rate stabil, database akan full dalam:
- (Estimasi perlu tracking beberapa hari)

## Alert Example

When database reaches thresholds, you'll receive:

```
⚠️ Kyla-Go Database Alert
Size: 412.48 MB / 500 MB (82.5%)
Remaining: 87.52 MB
Tables: 33
```

If critical:
```
🔴 URGENT: Database hampir penuh! Perlu cleanup segera.
```

## Managing Monitoring

### Check Now
"Cek database size sekarang"

### Pause/Resume
"Pause database monitoring"
"Resume database monitoring"

### Change Interval
"Ubah database monitoring jadi setiap 6 jam"
"Ubah database monitoring jadi setiap 1 jam"

## Security Note

Database credentials tersimpan di `.db_credentials` (hidden file).
File ini tidak di-commit ke Git dan hanya accessible di VPS.

---
*Setup by LemonAi on 2026-02-22*
*Current Status: WARNING - Cleanup recommended*

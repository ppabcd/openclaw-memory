# Daily Asset Report - Automation

Laporan harian otomatis untuk monitoring asset dan spending Reza.

## Schedule

**Waktu:** Setiap hari jam 08:00 WIB (01:00 UTC)
**Delivery:** WhatsApp (+6281282895180)

## What's Reported

### Total Assets Value Only
- Nilai total dari semua asset (Rp XXX,XXX,XXX)
- Diambil dari sheet "Assets" row 8

**Source:** Sheet "Assets" dari Asset Management spreadsheet

### Error Detection
- Deteksi cell dengan #NUM! error di Total Assets Value
- Reminder untuk refresh data jika ada error

## Spreadsheets Monitored

1. **Asset Management**
   - ID: 1wcnQ2DMwQfC6C9h05xEOGqwNqnB0pbAPiG0oEDEEfE8
   - Sheet: Assets
   - Cell: Total Assets Value (row 8, column D)

## Cron Job Details

- **Job ID:** a1b8a119-649e-452d-9415-ef0ce4972587
- **Name:** Daily Asset Report - 8 AM
- **Type:** Isolated agent session
- **Timeout:** 120 seconds
- **Status:** ✅ Enabled

## First Run

Next run: **23 Februari 2026, 08:00 WIB**

## Managing the Job

### Check Status
```bash
# Via OpenClaw cron tool (ask LemonAi)
"Cek status daily report"
```

### Pause/Resume
```bash
# Disable
"Pause daily report"

# Enable
"Resume daily report"
```

### Change Time
```bash
# Update schedule
"Ubah daily report jadi jam 9 pagi"
```

## Troubleshooting

### Report Tidak Masuk
1. Cek status cron job
2. Pastikan WhatsApp gateway connected
3. Cek logs session isolated

### Data Error
1. Buka Google Sheets manual
2. Klik Data → Refresh
3. Atau force recalculate dengan edit cell kosong

---
*Setup by LemonAi on 2026-02-22*

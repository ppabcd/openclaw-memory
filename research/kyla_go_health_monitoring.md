# Kyla-Go Health Monitoring

Monitoring otomatis untuk health endpoints aplikasi Kyla-Go.

## Schedule

**Interval:** Setiap 30 menit
**Mode:** Silent monitoring (alert hanya kalau ada masalah)
**Delivery:** WhatsApp (+6281282895180)

## Endpoints Monitored

1. **Main:** https://go.kyla.my.id/health
2. **Test:** https://go-test.kyla.my.id/health
3. **Production:** https://go-prod.kyla.my.id/health

## Health Checks

Untuk setiap endpoint, sistem mengecek:
- HTTP status code (harus 200)
- JSON response: `status` harus "ok"
- JSON response: `redis` harus "ok"
- Response time (warn jika >500ms, alert jika >1000ms)

## Alert Conditions

Alert dikirim ke WhatsApp HANYA jika:
- Endpoint return non-200 status
- `status` != "ok" atau `redis` != "ok"
- Endpoint unreachable/timeout
- Response time >1000ms

## Alert Format

```
⚠️ Kyla-Go Health Alert
- [Endpoint name]: [issue description]
```

## Silent Monitoring

Jika semua endpoint sehat (200 OK, status ok, redis ok, response time bagus):
- TIDAK ada notifikasi
- Monitoring tetap jalan di background
- Cek ulang otomatis 30 menit kemudian

## Cron Job Details

- **Job ID:** 1c127ab3-9481-4b59-a057-d6b8182aeea3
- **Name:** Kyla-Go Health Monitor - Every 30min
- **Type:** Isolated agent session
- **Timeout:** 90 seconds
- **Status:** ✅ Enabled

## Baseline Health (2026-02-22 18:07)

Semua endpoint sehat saat setup:
- go.kyla.my.id: 200 OK, redis ok, 79ms
- go-test.kyla.my.id: 200 OK, redis ok, 75ms
- go-prod.kyla.my.id: 200 OK, redis ok, 72ms

## Managing the Monitor

### Check Status
"Cek status monitoring Kyla-Go"

### Pause/Resume
"Pause monitoring Kyla-Go"
"Resume monitoring Kyla-Go"

### Change Interval
"Ubah monitoring Kyla-Go jadi setiap 15 menit"
"Ubah monitoring Kyla-Go jadi setiap 1 jam"

### Manual Check Now
"Cek health Kyla-Go sekarang"

## Troubleshooting

### False Alerts
Jika dapat alert tapi endpoint sebenernya sehat:
1. Cek manual via browser
2. Mungkin temporary network issue
3. Adjust timeout atau retry logic

### Missing Alerts
Jika endpoint down tapi nggak dapat alert:
1. Cek cron job status masih enabled
2. Cek logs session isolated
3. Verify WhatsApp gateway connected

---
*Setup by LemonAi on 2026-02-22*

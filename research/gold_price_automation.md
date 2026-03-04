# Gold Price Auto-Update

Otomasi update harga buyback emas Antam ke Google Sheets.

## Schedule

**Waktu:** Setiap hari jam 05:00 WIB (22:00 UTC)
**Target:** Sheet "Gold" cell E2 di Asset Management spreadsheet
**Mode:** Silent (tidak ada notifikasi kecuali error)

## What's Updated

**Cell:** Gold!E2 (kolom "Harga Emas")
**Value:** Harga buyback emas Antam per gram (angka saja, tanpa format Rp)

Contoh: 2793000 (untuk Rp 2.793.000)

## How It Works

1. Setiap jam 5 pagi, cron job akan jalan
2. Search harga buyback emas Antam terbaru via web
3. Extract angka harga buyback
4. Update ke cell Gold!E2
5. Selesai tanpa notifikasi (silent mode)

## Spreadsheet Details

- **Spreadsheet:** Asset Management
- **ID:** 1wcnQ2DMwQfC6C9h05xEOGqwNqnB0pbAPiG0oEDEEfE8
- **Sheet:** Gold
- **Cell:** E2 (Harga Emas)

## Current Structure

Sheet "Gold" punya kolom:
- A: Wallet
- B: Unit
- C: Price in IDR
- D: Harga Beli
- E: Harga Emas (ini yang di-update otomatis)
- F: Total Emas

## Cron Job Details

- **Job ID:** cca47156-efef-4d66-ad5f-976e28d8e00c
- **Name:** Update Gold Buyback Price - 5 AM
- **Type:** Isolated agent session (silent)
- **Status:** ✅ Enabled

## First Run

Next run: **23 Februari 2026, 05:00 WIB**

## Managing the Job

### Check Status
"Cek status update harga emas"

### Pause/Resume
"Pause update harga emas"
"Resume update harga emas"

### Manual Update
Kalau mau update sekarang tanpa tunggu jam 5 pagi, tinggal bilang:
"Update harga emas sekarang"

## Error Handling

Kalau ada error (misal gagal ambil harga atau gagal nulis ke sheet), system akan kirim notifikasi error ke WhatsApp.

---
*Setup by LemonAi on 2026-02-22*

# Google Sheets Integration Setup

Integrasi Google Sheets menggunakan Service Account dari Google Cloud.

## Credential Information

- **Project ID:** spending-management-441616
- **Service Account Email:** spendingmanagement@spending-management-441616.iam.gserviceaccount.com
- **Credential File:** `.gcloud_service_account.json` (hidden file di workspace)

## Libraries Installed

- `gspread` - Google Sheets API wrapper
- `google-auth` - Authentication library

## PENTING: Cara Sharing Google Sheets

Sebelum bisa dibaca oleh LemonAi, kamu HARUS share Google Sheets ke email service account:

```
spendingmanagement@spending-management-441616.iam.gserviceaccount.com
```

**Langkah-langkah:**
1. Buka Google Sheets yang mau diakses
2. Klik tombol "Share" (Bagikan)
3. Masukkan email: `spendingmanagement@spending-management-441616.iam.gserviceaccount.com`
4. Pilih permission: "Viewer" (untuk baca saja) atau "Editor" (untuk tulis juga)
5. Klik "Send"

## Script Helper

Script Python tersedia di: `scripts/google_sheets_reader.py`

### Usage Examples

#### 1. Baca Data dari Sheet

```bash
python3 scripts/google_sheets_reader.py read "SHEET_URL_OR_ID"
```

Contoh dengan URL lengkap:
```bash
python3 scripts/google_sheets_reader.py read "https://docs.google.com/spreadsheets/d/1ABC..."
```

Contoh dengan Sheet ID saja:
```bash
python3 scripts/google_sheets_reader.py read "1ABC..."
```

#### 2. Baca Sheet Tertentu

```bash
python3 scripts/google_sheets_reader.py read "SHEET_ID" "Sheet2"
```

#### 3. Baca Range Tertentu

```bash
python3 scripts/google_sheets_reader.py read "SHEET_ID" "Sheet1" "A1:D10"
```

#### 4. Get Sheet Info

```bash
python3 scripts/google_sheets_reader.py info "SHEET_ID"
```

Output:
```json
{
  "title": "My Spreadsheet",
  "id": "1ABC...",
  "url": "https://docs.google.com/spreadsheets/...",
  "worksheets": [
    {
      "title": "Sheet1",
      "id": 0,
      "rows": 1000,
      "cols": 26
    }
  ]
}
```

#### 5. Tulis Data ke Sheet

```bash
python3 scripts/google_sheets_reader.py write "SHEET_ID" '[["A1", "B1"], ["A2", "B2"]]'
```

#### 6. Append Row

```bash
python3 scripts/google_sheets_reader.py append "SHEET_ID" '["Data 1", "Data 2", "Data 3"]'
```

## Python API

Jika mau pakai langsung dari Python code:

```python
from scripts.google_sheets_reader import read_sheet, write_sheet, append_row, get_sheet_info

# Read data
data = read_sheet("SHEET_URL", "Sheet1", "A1:D10")
print(data)

# Write data
write_sheet("SHEET_URL", [["Name", "Age"], ["John", "30"]])

# Append row
append_row("SHEET_URL", ["Jane", "25"])

# Get info
info = get_sheet_info("SHEET_URL")
print(info)
```

## Capabilities

LemonAi sekarang bisa:
- ✅ Membaca data dari Google Sheets (semua sheet atau range tertentu)
- ✅ Menulis/update data ke Google Sheets
- ✅ Append rows baru
- ✅ Mendapatkan metadata spreadsheet
- ✅ Akses multiple worksheets dalam satu spreadsheet

## Security

- Credential disimpan lokal di VPS (file hidden `.gcloud_service_account.json`)
- Service account hanya punya akses ke sheets yang explicitly di-share
- Bisa dicabut aksesnya kapan saja dengan "Remove" di Google Sheets sharing settings

## Troubleshooting

### Error: "Error opening spreadsheet"

**Penyebab:** Sheet belum di-share ke service account email.

**Solusi:** Share sheet ke `spendingmanagement@spending-management-441616.iam.gserviceaccount.com`

### Error: "Permission denied"

**Penyebab:** Service account cuma punya "Viewer" permission tapi kamu coba write.

**Solusi:** Update permission ke "Editor" di sharing settings.

---
*Setup completed by LemonAi on 2026-02-22*

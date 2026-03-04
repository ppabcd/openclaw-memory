# GitHub PR Monitoring Setup

Sistem monitoring otomatis untuk repository **Kyla-Chat/Kyla-Go**.

## Cara Kerja

LemonAi akan secara otomatis:
1. Memeriksa pull request baru setiap kali heartbeat (setiap ~30 menit)
2. Menganalisis perubahan kode dalam PR
3. Memberikan komentar otomatis dengan saran improvement
4. Melacak PR yang sudah direview agar tidak duplikat komentar

## File yang Dibuat

### 1. Token Storage
- **Lokasi:** `.github_token` (hidden file)
- **Isi:** Personal Access Token untuk akses GitHub API

### 2. State Tracking
- **Lokasi:** `memory/github_pr_state.json`
- **Fungsi:** Menyimpan daftar PR yang sudah direview

### 3. Scripts
- **`scripts/check_prs.sh`:** Script cepat untuk cek PR manual
- **`scripts/github_pr_monitor.sh`:** Monitor untuk cron job (optional)
- **`scripts/github_pr_reviewer.py`:** Python reviewer (butuh pip install requests)

### 4. Heartbeat Configuration
- **Lokasi:** `HEARTBEAT.md`
- **Fungsi:** Instruksi otomatis untuk cek PR setiap heartbeat

## Review Criteria

LemonAi akan mengecek hal-hal berikut pada setiap PR:

### Code Quality
- Ukuran changeset (warning jika >300 lines)
- Penggunaan TODO/FIXME comments
- Error handling yang proper

### Go-Specific Checks
- Penggunaan `panic()` (sebaiknya pakai error returns)
- `fmt.Print` statements (sebaiknya pakai logger)
- Komentar yang belum resolved

## Cara Kerja Manual

Jika ingin trigger review manual:

```bash
# Cek PR yang ada
bash /root/.openclaw/workspace/scripts/check_prs.sh

# Review PR tertentu (misalnya PR #5)
# Tinggal mention ke LemonAi: "Review PR #5 di Kyla-Go"
```

## Contoh Output

Ketika ada PR baru, LemonAi akan post komentar seperti:

```markdown
## 🤖 Automated Code Review

Hi! LemonAi here 😼 I've reviewed this PR and have some suggestions:

### `main.go`
- Large changeset (350 additions). Consider breaking into smaller PRs for easier review.
- Contains fmt.Print statements. Consider using proper logging instead.

---
*This is an automated review. Human review is still recommended!*
```

## Keamanan

- Token disimpan lokal di VPS (tidak di cloud)
- Token memiliki akses admin ke repo Kyla-Chat/Kyla-Go
- Bisa direvoke kapan saja di GitHub Settings

## Next Steps

1. ✅ Token tersimpan dan terverifikasi
2. ✅ Heartbeat monitoring aktif
3. ⏳ Menunggu PR baru untuk direview
4. 🔄 Setiap heartbeat (~30 menit), LemonAi akan cek otomatis

---
*Setup completed by LemonAi on 2026-02-22*

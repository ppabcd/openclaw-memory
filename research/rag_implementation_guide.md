# Panduan Implementasi RAG di VPS (2026)

Panduan ini menjelaskan langkah-langkah teknis untuk menginstal dan menjalankan sistem Retrieval-Augmented Generation (RAG) pada satu server VPS menggunakan Python, LangChain, dan ChromaDB.

## 1. Persiapan Lingkungan VPS

Pastikan sistem Ubuntu/Linux Anda sudah terupdate dan memiliki Python terinstal.

```bash
# Update sistem
sudo apt update && sudo apt upgrade -y

# Instal Python dan Virtual Environment
sudo apt install python3-pip python3-venv -y
```

## 2. Setup Proyek

Buat direktori kerja dan aktifkan virtual environment untuk menjaga kebersihan dependensi.

```bash
mkdir ~/rag-research
cd ~/rag-research

# Buat virtual environment
python3 -m venv venv
source venv/bin/activate
```

## 3. Instalasi Dependensi Utama

Instal library yang diperlukan untuk pemrosesan dokumen, pembuatan vector, dan database.

```bash
pip install --upgrade pip
pip install langchain langchain-community langchain-chroma
pip install chromadb sentence-transformers pypdf
# Instal provider AI (Pilih salah satu)
pip install langchain-openai # Untuk GPT-4
# atau
pip install langchain-google-genai # Untuk Gemini
```

## 4. Struktur Direktori

Berikut adalah struktur folder yang direkomendasikan:

```text
/rag-research
├── venv/               # Virtual environment
├── data/               # Simpan file PDF/TXT di sini
├── db/                 # Lokasi database Chroma (otomatis dibuat)
└── main.py             # Script utama untuk RAG
```

## 5. Alur Kerja Implementasi (main.py)

Script `main.py` Anda harus melakukan hal berikut:

1.  **Ingestion**: Membaca file dari folder `/data`.
2.  **Splitting**: Membagi teks menjadi potongan kecil (chunks).
3.  **Embedding**: Mengubah teks menjadi representasi angka menggunakan `sentence-transformers`.
4.  **Storage**: Menyimpan vector ke dalam `ChromaDB` di folder `/db`.
5.  **Retrieval**: Mencari potongan teks yang relevan saat ada pertanyaan.
6.  **Generation**: Mengirim konteks + pertanyaan ke LLM (via API) untuk mendapatkan jawaban.

## 6. Tips Performa di VPS

- **RAM**: Minimal 2GB-4GB disarankan jika menggunakan ChromaDB secara lokal.
- **Disk**: Pastikan ada ruang cukup untuk menyimpan database vector jika dokumen Anda berjumlah ribuan.
- **API**: Gunakan API key (Gemini/OpenAI) untuk menghemat beban kerja CPU VPS.

---
*Dokumen ini dibuat oleh LemonAi untuk riset Reza.*

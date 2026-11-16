# Panduan Pembuatan Automation Testing Login (Python + Pytest + Selenium)

Dokumentasi ini menjelaskan standar struktur folder, arsitektur kode (*Page Object Model*), dan langkah-langkah pembuatan skrip *automation testing* untuk fitur **Login** menggunakan **Python**, **Pytest**, dan **Selenium WebDriver**.

---

## 1. Struktur Folder dan File (Page Object Model)

```text
automation/
│
├── config/
│   └── config.py               # Menyimpan URL, kredensial, dan konfigurasi global
│
├── pages/
│   ├── __init__.py
│   ├── base_page.py            # Fungsi dasar Selenium (click, input text, wait, screenshot, dll.)
│   └── login_page.py           # Locator dan aksi khusus untuk halaman Login
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Setup & Teardown browser (Pytest Fixtures & auto-screenshot on failure)
│   └── test_login.py           # Kumpulan skenario test case untuk Login
│
├── reports/                    # Folder output untuk menyimpan hasil report HTML & screenshot
│
├── .env                        # Menyimpan data sensitif (username/password) agar tidak hardcode
├── .env.example                # Template konfigurasi env
├── requirements.txt            # Daftar library Python yang dibutuhkan
└── README.md                   # Dokumentasi utama proyek
```

---

## 2. Persiapan Lingkungan (Setup)

### A. Buat & Aktifkan Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### B. Instal Dependensi
```bash
pip install -r requirements.txt
```

### C. Konfigurasi `.env`
Sesuaikan kredensial dan URL target di file `.env`:
```env
BASE_URL=https://fe-p2p-partnership-portal-dev2.apps.mypaas.telkom.co.id/
VALID_USERNAME=user_anda@email.com
VALID_PASSWORD=PasswordRahasia123!
```

---

## 3. Menjalankan Pengujian

Jalankan seluruh *test case* dan hasilkan laporan dalam format HTML menggunakan perintah berikut:

```bash
pytest tests/test_login.py -v --html=reports/login_report.html --self-contained-html
```

Untuk melihat file laporan:
```bash
open reports/login_report.html
```

Untuk melihat hasil screenshot otomatis:
```bash
open reports/screenshots/
```

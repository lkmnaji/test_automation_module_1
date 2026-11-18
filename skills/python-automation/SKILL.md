---
name: python-automation
description: "Standar dan panduan pembuatan skrip automation testing berbasis Python, Selenium WebDriver, Pytest, dan Page Object Model (POM). Gunakan saat membuat, memodifikasi, menjalankan, atau men-debug test cases web fungsional, form submission, validasi input, auto-screenshot, dan integrasi web quality."
license: MIT
metadata:
  author: automation-team
  version: "1.0"
---

# Python Web Automation Testing Skill

Skill ini mengatur standar arsitektur, pola penulisan kode (*coding style*), dan langkah-langkah pengujian otomasi web (*Web Automation Testing*) menggunakan **Python**, **Selenium WebDriver**, **Pytest**, dan pola desain **Page Object Model (POM)**.

---

## 1. Prinsip Utama & Arsitektur (Page Object Model)

Pemisahan tanggung jawab secara ketat antara **Aksi/Elemen UI (Pages)** dan **Logika Verifikasi (Tests)**:
- **`config/config.py`**: Menyimpan konfigurasi global seperti `BASE_URL`, kredensial pengujian dari `.env`, dan `TIMEOUT`. Jangan pernah meletakkan password langsung di kode (*hardcode*).
- **`pages/base_page.py`**: Berisi wrapper umum fungsi Selenium (`click`, `input_text`, `find_element`, `is_element_present`, `take_screenshot`). Wajib menggunakan **Explicit Wait (`WebDriverWait`)** dan hindari `time.sleep()` yang kaku kecuali untuk demonstrasi UI atau jeda interaksi pengguna.
- **`pages/*_page.py`**: Setiap halaman web memiliki satu representasi class POM yang menyimpan *Locators* dan *Methods* aksi form.
- **`tests/conftest.py`**: Mengelola lifecycle browser (inisialisasi `driver` dan teardown `driver.quit()`), serta hook penangkapan screenshot otomatis saat kegagalan pengujian.
- **`tests/test_*.py`**: Berisi skenario pengujian dengan assertion yang jelas dan deskriptif.

---

## 2. Hirarki Pemilihan Selector (Locator Hierarchy)

Dalam mendefinisikan locator elemen web, utamakan urutan prioritas berikut agar skrip tahan terhadap perubahan tampilan:
1. **Name / ID**: `(By.NAME, "emailOrNIK")` atau `(By.ID, "username")`
2. **CSS Selector dengan Atribut Stabil**: `(By.CSS_SELECTOR, "button[type='submit']")`
3. **Data Test ID (jika ada)**: `(By.CSS_SELECTOR, "[data-testid='btn-submit']")`
4. **XPath Fungsional / Teks**: `(By.XPATH, "//button[contains(text(), 'Login')]")`

Hindari XPath absolut yang panjang dan rapuh seperti `/html/body/div[1]/div[2]/div/form/div[3]/button`.

---

## 3. Penanganan Kasus Khusus UI Frontend

### A. Checkbox dengan Custom Styling (Material-UI / Tailwind)
Elemen `<input type="checkbox">` sering disembunyikan oleh framework CSS modern. Gunakan klik via JavaScript jika terjadi `ElementClickInterceptedException`:
```python
def accept_terms(self):
    checkbox = self.driver.find_element(*self.TERMS_CHECKBOX)
    if not checkbox.is_selected():
        self.driver.execute_script("arguments[0].click();", checkbox)
```

### B. Proteksi Anti-Bot (Google reCAPTCHA)
Bot/Selenium tidak boleh mencoba memecahkan (*bypass/solve*) tantangan reCAPTCHA secara otomatis. Terapkan pola **Semi-Automated (Human-in-the-Loop)**:
1. Skrip otomatis mengisi field username, password, dan mencentang persetujuan.
2. Skrip mendeteksi keberadaan reCAPTCHA dan menunggu hingga tombol submit aktif (maksimal 25-30 detik) saat dicentang secara manual oleh penguji.
3. Begitu tombol submit aktif, skrip langsung melanjutkan klik otomatis.

---

## 4. Standar Pengambilan Screenshot Otomatis

Setiap skrip automation harus memiliki bukti pengujian (*test evidence*):
1. **Success Trigger**: Ambil screenshot segera setelah proses submit berhasil dilakukan.
   ```python
   screenshot_path = page.take_screenshot("login_submit_success")
   ```
2. **Failure Trigger**: Otomatis ditangkap via hook `pytest_runtest_makereport` di `tests/conftest.py` dan dilampirkan ke laporan HTML.
3. Semua file screenshot disimpan di `reports/screenshots/` dengan format nama: `<nama_aksi>_<YYYYMMDD_HHMMSS>.png`.

---

## 5. Cara Menjalankan Pengujian

```bash
# 1. Masuk ke virtual environment
source .venv/bin/activate

# 2. Jalankan seluruh pengujian dengan laporan HTML mandiri
pytest tests/test_login.py -v --html=reports/login_report.html --self-contained-html

# 3. Jalankan skenario interaktif tertentu dengan output terminal langsung
pytest tests/test_login.py -k "test_login_fill_credentials" -v -s
```

---

## 6. Sinergi dengan Web Quality Skills (`.agents/skills/`)

Skill ini bekerja berdampingan dengan paket **`web-quality-skills`**:
- **`python-automation`**: Menangani pengujian fungsional interaksi tombol, form input, dan validasi flow login.
- **`accessibility`**: Mengaudit kepatuhan aksesibilitas elemen form (atribut label, kontras warna, pembaca layar).
- **`performance` & `core-web-vitals`**: Menganalisis kecepatan render form dan responsivitas interaksi pada portal yang diuji.

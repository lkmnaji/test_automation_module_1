import time
import pytest
from pages.login_page import LoginPage
from config.config import Config

class TestLogin:

    def test_portal_load(self, driver):
        """Test Case 1: Memverifikasi portal dan elemen login berhasil dimuat"""
        login_page = LoginPage(driver)
        login_page.open_url(Config.BASE_URL)
        time.sleep(2)
        
        assert "Login" in driver.title or "Partnership" in driver.title, f"Judul halaman tidak sesuai: {driver.title}"
        assert login_page.is_element_present(login_page.USERNAME_INPUT), "Input username/email tidak ditemukan!"
        assert login_page.is_element_present(login_page.PASSWORD_INPUT), "Input password tidak ditemukan!"
        assert login_page.is_element_present(login_page.LOGIN_BUTTON), "Tombol login tidak ditemukan!"

    def test_validation_empty_fields(self, driver):
        """Test Case 2: Validasi ketika input email & password dibiarkan kosong"""
        login_page = LoginPage(driver)
        login_page.open_url(Config.BASE_URL)
        time.sleep(2)
        
        # Fokus lalu keluar field untuk memicu validasi form
        u = login_page.find_element(login_page.USERNAME_INPUT)
        p = login_page.find_element(login_page.PASSWORD_INPUT)
        u.click()
        p.click()
        u.click()
        time.sleep(1)
        
        validation_msg = login_page.get_validation_texts()
        assert "tidak boleh kosong" in validation_msg.lower() or "required" in validation_msg.lower(), (
            f"Validasi field kosong tidak muncul! Output: {validation_msg}"
        )

    def test_validation_invalid_email_format(self, driver):
        """Test Case 3: Validasi format email yang tidak valid"""
        login_page = LoginPage(driver)
        login_page.open_url(Config.BASE_URL)
        time.sleep(2)
        
        login_page.enter_username("bukan_format_email")
        login_page.find_element(login_page.PASSWORD_INPUT).click()
        time.sleep(1)
        
        validation_msg = login_page.get_validation_texts()
        assert "masukkan email dengan benar" in validation_msg.lower() or "invalid" in validation_msg.lower(), (
            f"Validasi format email salah tidak muncul! Output: {validation_msg}"
        )

    def test_login_fill_credentials(self, driver):
        """Test Case 4: Mengisi kredensial valid, checklist ketentuan, dan submit login"""
        login_page = LoginPage(driver)
        login_page.open_url(Config.BASE_URL)
        time.sleep(2)
        
        # 1. Isi email & password dari .env
        login_page.enter_username(Config.VALID_USERNAME)
        login_page.enter_password(Config.VALID_PASSWORD)
        
        # 2. Otomatis checklist kotak "Saya setuju dengan ketentuan penggunaan"
        login_page.accept_terms()
        time.sleep(1)
        
        # Verifikasi nilai input terisi dengan benar di DOM
        email_val = login_page.find_element(login_page.USERNAME_INPUT).get_attribute("value")
        assert email_val == Config.VALID_USERNAME, "Email tidak terisi dengan benar!"
        
        # 3. Penanganan reCAPTCHA & Submit:
        has_recaptcha = login_page.is_element_present(login_page.RECAPTCHA_IFRAME, timeout=3)
        if has_recaptcha:
            print("\n" + "="*70)
            print("[INFO] Checkbox 'Saya setuju dengan ketentuan penggunaan' SUDAH dicentang otomatis.")
            print("[INFO] Deteksi reCAPTCHA aktif. Silakan centang kotak 'I'm not a robot' di browser.")
            print("[INFO] Skrip menunggu hingga reCAPTCHA selesai dicentang...")
            print("="*70)
            
            # Menunggu interaktif hingga tombol submit menjadi aktif (maks 25 detik)
            is_submitted = login_page.wait_for_recaptcha_or_submit(timeout=25)
            if is_submitted:
                print("[INFO] Tombol submit 'Login' berhasil diklik secara otomatis!")
                time.sleep(3)
                # Ambil screenshot saat proses submit login berhasil dijalankan
                screenshot_path = login_page.take_screenshot("login_submit_success")
                print(f"[SUCCESS] Screenshot submit login berhasil disimpan: {screenshot_path}")
            else:
                print("[INFO] Waktu tunggu reCAPTCHA berakhir tanpa submit.")
                # Ambil screenshot kondisi form saat ini
                login_page.take_screenshot("login_waiting_recaptcha")
        else:
            # Jika tidak ada reCAPTCHA, langsung klik login
            login_page.click_login()
            time.sleep(3)
            # Ambil screenshot saat proses submit login berhasil
            screenshot_path = login_page.take_screenshot("login_submit_success")
            print(f"[SUCCESS] Screenshot submit login berhasil disimpan: {screenshot_path}")

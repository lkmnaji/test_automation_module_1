import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators (Mendukung portal Telkom Partnership & generic HTML)
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[name='emailOrNIK'], input[name='username'], #username")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password'], #password")
    TERMS_CHECKBOX = (By.CSS_SELECTOR, "input[name='ketentuan']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], #btn-login")
    RECAPTCHA_IFRAME = (By.CSS_SELECTOR, "iframe[title*='reCAPTCHA']")
    HELPER_TEXTS = (By.CSS_SELECTOR, "[id*='helper-text'], .MuiFormHelperText-root")
    ERROR_ALERT = (By.CSS_SELECTOR, ".MuiAlert-message, .alert-danger, .error-message")
    DASHBOARD_HEADER = (By.XPATH, "//h1 | //header | //*[contains(text(), 'Dashboard') or contains(text(), 'Beranda')]")

    def __init__(self, driver):
        super().__init__(driver)

    def enter_username(self, username):
        self.input_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.input_text(self.PASSWORD_INPUT, password)

    def accept_terms(self):
        """Mencentang checkbox persetujuan penggunaan jika ada di halaman"""
        try:
            checkbox = self.driver.find_element(*self.TERMS_CHECKBOX)
            if not checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", checkbox)
        except Exception:
            # Coba klik label jika input tersembunyi
            try:
                label = self.driver.find_element(By.XPATH, "//label[contains(., 'Saya setuju')]")
                label.click()
            except Exception:
                pass

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def is_login_button_enabled(self):
        btn = self.find_element(self.LOGIN_BUTTON)
        return btn.is_enabled()

    def do_login(self, username, password):
        """Fungsi gabungan untuk melakukan proses input login lengkap"""
        self.enter_username(username)
        self.enter_password(password)
        self.accept_terms()
        time.sleep(1)

    def wait_for_recaptcha_or_submit(self, timeout=10):
        """
        Menunggu reCAPTCHA diselesaikan secara interaktif oleh user atau submit aktif.
        Jika reCAPTCHA selesai dicentang oleh user, tombol login akan otomatis diklik.
        """
        if self.is_element_present(self.RECAPTCHA_IFRAME, timeout=2):
            try:
                # Tunggu hingga tombol submit menjadi aktif (disabled attribute hilang)
                WebDriverWait(self.driver, timeout).until(
                    lambda d: d.find_element(*self.LOGIN_BUTTON).is_enabled()
                )
                self.click_login()
                return True
            except Exception:
                return False
        else:
            self.click_login()
            return True

    def is_dashboard_displayed(self):
        try:
            return self.find_element(self.DASHBOARD_HEADER, timeout=5).is_displayed()
        except Exception:
            return False

    def get_validation_texts(self):
        """Mengambil teks validasi atau pesan error pada form"""
        texts = []
        for el in self.find_elements(self.HELPER_TEXTS):
            t = el.text.strip()
            if t:
                texts.append(t)
        for el in self.find_elements(self.ERROR_ALERT):
            t = el.text.strip()
            if t:
                texts.append(t)
        return " | ".join(texts)

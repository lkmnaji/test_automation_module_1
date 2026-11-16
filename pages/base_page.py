from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from config.config import Config

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.TIMEOUT)

    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except ElementClickInterceptedException:
            # Fallback jika elemen terhalang atau custom styled
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].click();", element)

    def input_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_element(locator).text

    def is_element_present(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def take_screenshot(self, name="screenshot"):
        """Mengambil screenshot layar browser dan menyimpannya di folder reports/screenshots/"""
        import os
        from datetime import datetime
        screenshot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports", "screenshots"))
        os.makedirs(screenshot_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)
        self.driver.save_screenshot(filepath)
        print(f"\n[SCREENSHOT] Berhasil disimpan di: {filepath}")
        return filepath

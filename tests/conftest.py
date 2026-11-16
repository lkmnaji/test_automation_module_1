import os
import shutil
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope="function")
def driver():
    # Setup Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    
    # Deteksi chromedriver lokal yang cocok dengan versi Chrome di sistem
    local_driver_path = os.path.expanduser("~/.cache/selenium/chromedriver/mac-arm64/157.0.8103.51/chromedriver")
    if os.path.exists(local_driver_path):
        service = Service(local_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    elif shutil.which("chromedriver"):
        driver = webdriver.Chrome(options=options)
    else:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    
    # Teardown
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            import os
            from datetime import datetime
            screenshot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports", "screenshots"))
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"failed_{item.name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            driver.save_screenshot(filepath)
            
            # Lampirkan ke pytest-html report jika plugin aktif
            try:
                import pytest_html
                extras.append(pytest_html.extras.image(filepath))
            except Exception:
                pass
    report.extras = extras


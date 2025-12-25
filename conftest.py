import os
from datetime import datetime

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Chrome loglarını azaltmak istersen aç:
    # options.add_experimental_option("excludeSwitches", ["enable-logging"])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Test FAIL olursa reports/ altına otomatik screenshot kaydeder.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            os.makedirs("reports", exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = item.name.replace("/", "_").replace("\\", "_")
            path = os.path.join("reports", f"{name}_{ts}.png")
            try:
                driver.save_screenshot(path)
                print(f"\n[SCREENSHOT] {path}")
            except Exception as e:
                print(f"\n[SCREENSHOT ERROR] {e}")

import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.helpers import wait_front_search_input

DEMO_URL = "https://demo.prestashop.com/#/en/front"


@pytest.mark.regression
def test_search_empty_input_does_not_crash(driver):
    driver.get(DEMO_URL)

    search_input = wait_front_search_input(driver, timeout=80)
    search_input.clear()

    # boş enter
    search_input.send_keys(Keys.ENTER)

    # Beklenen: crash yok. Ya aynı sayfada kalır ya da arama sayfasına gider.
    # Stabil kontrol: arama inputu hâlâ bulunabilir olmalı veya product list container görünmeli.
    wait = WebDriverWait(driver, 30)

    def page_ok(d):
        try:
            # ya input var
            d.find_element(By.CSS_SELECTOR, "input[type='search'], input[name='s']")
            return True
        except Exception:
            pass
        try:
            # ya da ürün listesi container var
            d.find_element(By.ID, "js-product-list")
            return True
        except Exception:
            return False

    wait.until(page_ok)
    assert True

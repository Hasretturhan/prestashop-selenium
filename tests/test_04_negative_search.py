import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.helpers import wait_front_search_input

DEMO_URL = "https://demo.prestashop.com/#/en/front"


@pytest.mark.regression
def test_search_no_result(driver):
    driver.get(DEMO_URL)

    # sağlam arama input bekleme (iframe dahil)
    search_input = wait_front_search_input(driver, timeout=80)

    search_input.clear()
    search_input.send_keys("zzzzzzzzzzzzqwe123")
    search_input.send_keys(Keys.ENTER)

    wait = WebDriverWait(driver, 60)
    wait.until(EC.presence_of_element_located((By.ID, "js-product-list")))

    product_cards = driver.find_elements(
        By.CSS_SELECTOR,
        ".product-miniature, article.product-miniature, .product"
    )

    assert len(product_cards) == 0

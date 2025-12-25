import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.helpers import switch_to_front_office_iframe

DEMO_URL = "https://demo.prestashop.com/#/en/front"


@pytest.mark.regression
def test_search_product(driver):
    driver.get(DEMO_URL)
    switch_to_front_office_iframe(driver)

    wait = WebDriverWait(driver, 50)

    search_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='search'], input[name='s']"))
    )
    search_input.clear()
    search_input.send_keys("mug")
    search_input.submit()

    wait.until(EC.presence_of_element_located((By.ID, "js-product-list")))

    products = driver.find_elements(
        By.CSS_SELECTOR,
        ".product-miniature, article.product-miniature, .product"
    )
    assert len(products) > 0

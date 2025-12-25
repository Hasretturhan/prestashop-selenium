import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEMO_URL = "https://demo.prestashop.com/#/en/front"


@pytest.mark.smoke
def test_smoke_open_front_office(driver):
    driver.get(DEMO_URL)
    wait = WebDriverWait(driver, 40)

    # Demo bazen iframe içinde gelir
    try:
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
        driver.switch_to.frame(iframe)
    except Exception:
        pass

    search = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search'], input[name='s']"))
    )
    assert search.is_displayed()

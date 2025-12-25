import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from pages.helpers import wait_front_search_input, switch_to_front_office_iframe

DEMO_URL = "https://demo.prestashop.com/#/en/front"


@pytest.mark.flaky
def test_add_to_cart_from_search(driver):
    driver.get(DEMO_URL)

    # sağlam search input
    search_input = wait_front_search_input(driver, timeout=80)
    search_input.clear()
    search_input.send_keys("mug")
    search_input.send_keys(Keys.ENTER)

    wait = WebDriverWait(driver, 90)
    wait.until(EC.presence_of_element_located((By.ID, "js-product-list")))

    product_link_css = ".product-miniature a, article.product-miniature a, .product a"
    max_try = 5

    for _ in range(max_try):
        # her turda linkleri yeniden çek (DOM değişiyor)
        links = driver.find_elements(By.CSS_SELECTOR, product_link_css)
        if not links:
            continue

        # her zaman ilk linki tıkla (index kayması -> IndexError engel)
        try:
            links[0].click()
        except StaleElementReferenceException:
            continue
        except Exception:
            # JS click fallback
            driver.execute_script("arguments[0].click();", links[0])

        # ürün sayfası
        title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1, .h1")))
        if not title.text.strip():
            driver.back()
            switch_to_front_office_iframe(driver)
            continue

        add_to_cart_selectors = [
            "button.add-to-cart",
            "button[data-button-action='add-to-cart']",
            ".product-add-to-cart button",
            "form#add-to-cart-or-refresh button[type='submit']",
            ".add-to-cart",
        ]

        clicked = False
        for css in add_to_cart_selectors:
            btns = driver.find_elements(By.CSS_SELECTOR, css)
            if not btns:
                continue

            btn = btns[0]
            disabled = btn.get_attribute("disabled") is not None
            aria_disabled = (btn.get_attribute("aria-disabled") or "").lower() == "true"
            if disabled or aria_disabled:
                continue

            try:
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
                btn.click()
            except Exception:
                driver.execute_script("arguments[0].click();", btn)

            clicked = True
            break

        if not clicked:
            driver.back()
            switch_to_front_office_iframe(driver)
            continue

        # eklendi sinyali: modal iframe içi/dışı
        modal_css = "#blockcart-modal, .modal.show"
        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, modal_css)))
            return
        except Exception:
            pass

        driver.switch_to.default_content()
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, modal_css)))
            return
        except Exception:
            # tekrar listeye dön
            driver.back()
            switch_to_front_office_iframe(driver)
            continue

    assert False, "Could not add to cart within demo variability (tried multiple products)."

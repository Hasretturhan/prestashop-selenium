import pytest
from selenium.webdriver.common.keys import Keys

from pages.helpers import wait_front_search_input, wait_search_result_or_stable_page

DEMO_URL = "https://demo.prestashop.com/#/en/front"


@pytest.mark.boundary
@pytest.mark.regression
@pytest.mark.parametrize(
    "query",
    [
        "a",                 # 1 karakter
        "ğ",                 # TR karakter
        "!" * 5,             # özel karakter
        "x" * 300,           # uzun input
    ],
)
def test_search_boundary_inputs(driver, query):
    driver.get(DEMO_URL)

    search_input = wait_front_search_input(driver, timeout=80)
    search_input.clear()
    search_input.send_keys(query)
    search_input.send_keys(Keys.ENTER)

    # Beklenen: çökme yok → sayfa stabil ya da sonuç alanı geldi
    wait_search_result_or_stable_page(driver, timeout=70)
    assert True


@pytest.mark.security
@pytest.mark.regression
@pytest.mark.parametrize(
    "payload",
    [
        "<script>alert(1)</script>",
        "' OR 1=1 --",
    ],
)
def test_search_security_like_inputs_do_not_crash(driver, payload):
    """
    UI-level security-ish test:
    Bu stringler girilince uygulama crash/blank olmamalı.
    (Gerçek güvenlik testi değildir; input dayanıklılığıdır.)
    """
    driver.get(DEMO_URL)

    search_input = wait_front_search_input(driver, timeout=80)
    search_input.clear()
    search_input.send_keys(payload)
    search_input.send_keys(Keys.ENTER)

    wait_search_result_or_stable_page(driver, timeout=90)
    assert True

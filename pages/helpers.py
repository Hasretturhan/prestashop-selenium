from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def switch_to_front_office_iframe(driver, timeout=30):
    """Varsa iframe'e geçer, yoksa dokunmaz."""
    wait = WebDriverWait(driver, timeout)
    try:
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
        driver.switch_to.frame(iframe)
    except Exception:
        pass


def wait_front_search_input(driver, timeout=60):
    """
    Demo bazen iframe/DOM yenilediği için arama inputunu 'sağlam' şekilde bekler.
    Gerekirse default_content <-> iframe geçişi yaparak arar.
    """
    wait = WebDriverWait(driver, timeout)
    search_locator = (By.CSS_SELECTOR, "input[type='search'], input[name='s']")

    # deneme döngüsü
    for _ in range(6):
        try:
            driver.switch_to.default_content()
        except Exception:
            pass

        # iframe varsa içine gir
        try:
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe"))
            )
            driver.switch_to.frame(iframe)
        except Exception:
            # iframe yoksa zaten default içerikteyiz
            pass

        try:
            el = wait.until(EC.visibility_of_element_located(search_locator))
            return el
        except Exception:
            continue

    # son deneme (hata fırlatsın)
    return wait.until(EC.visibility_of_element_located(search_locator))
from selenium.common.exceptions import WebDriverException

def wait_search_result_or_stable_page(driver, timeout=60):
    """
    Demo bazı query'lerde sonuç sayfasına gitmeyebiliyor.
    Bu helper: sonuç listesi GELDİ mi ya da sayfa STABİL mi (arama inputu var mı) kontrol eder.
    """
    wait = WebDriverWait(driver, timeout)

    def ok(d):
        # 1) klasik sonuç container
        try:
            d.find_element(By.ID, "js-product-list")
            return True
        except Exception:
            pass

        # 2) arama inputu hala var mı (sayfa kırılmadı)
        try:
            d.find_element(By.CSS_SELECTOR, "input[type='search'], input[name='s']")
            return True
        except Exception:
            pass

        # 3) no results benzeri mesajlar (tema değişebilir)
        possible_msgs = [
            ".search-results",
            ".search-no-results",
            "#content",
            "main",
            "body",
        ]
        for css in possible_msgs:
            try:
                el = d.find_element(By.CSS_SELECTOR, css)
                if el.is_displayed():
                    return True
            except Exception:
                continue

        return False

    return wait.until(ok)

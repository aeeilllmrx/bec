from selenium import webdriver
from selenium.webdriver.common.by import By


def download_menu(name, url):
    driver = webdriver.Chrome()
    success = False
    try:
        driver.get(url)
        menu_link = None
        for link in driver.find_elements(By.TAG_NAME, "a"):
            href = link.get_attribute("href")
            if href and "menu" in href.lower():
                menu_link = href
                break
        if not menu_link:
            return None

        driver.get(menu_link)
        driver.find_element(By.TAG_NAME, "body").screenshot(
            "menus/" + name + "_menu.png"
        )
        success = True
    finally:
        driver.quit()

    return success

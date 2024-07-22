from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Improved version - This one contains some other content that fixed bugs on my computer.

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://orteil.dashnet.org/cookieclicker/")

cookie_id = "bigCookie"
cookies_id = "cookies"
product_price_prefix = "productPrice"
product_prefix = "product"

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'English')]"))
)

language = driver.find_element(By.XPATH, "//*[contains(text(), 'English')]")
language.click()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, cookie_id))
)

cookie = driver.find_element(By.ID, cookie_id)

while True:
    cookie.click()
    cookies_count = driver.find_element(By.ID, cookies_id).text.split(" ")[0]
    cookies_count = int(cookies_count.replace(",", ""))

    for i in range(4):
        product_price_element = driver.find_element(By.ID, product_price_prefix + str(i))
        product_price_text = product_price_element.text.replace(",", "")

        if not product_price_text.isdigit():
            continue

        product_price = int(product_price_text)

        if cookies_count >= product_price:
            product = driver.find_element(By.ID, product_prefix + str(i))

            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView();", product)

            # Wait until the product is clickable
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, product_prefix + str(i)))
            )

            # Click using JavaScript
            driver.execute_script("arguments[0].click();", product)
            break

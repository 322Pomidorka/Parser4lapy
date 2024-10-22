import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

URL_BASE = "https://4lapy.ru/catalog/sobaki/korm-sobaki/sukhoy-korm-sobaki/?page="
PAGE = [i for i in range(1, 2)]

driver = webdriver.Chrome()

results = []
for i in PAGE:  # проход по страницам
    urls = []
    driver.get(URL_BASE + str(i))
    elements = driver.find_elements(By.XPATH, "//a[@class='CardProduct_link__Rg5M2']")

    for element in elements:  # добавление в список ссылок на страницы товаров
            urls.append(element.get_attribute("href"))

    for url in urls:  # проход по каждому товару
        driver.get(url)

        # карточка товара --> айди бренд

        name = driver.find_element(By.XPATH, "//*[@id='product_title']").text
        price = driver.find_element(By.XPATH, "//*[@id='product_price']/p").text
        promo_price = price

        id = driver.find_element(By.XPATH,
                                    "//*[@id='product_article_value']").text
        brand = driver.find_element(By.XPATH,
                                    "//*[@id='product_brand_value']/a").text

        try:
            flag = driver.find_element(By.XPATH,
                                    "//*[@id='product_stock_status']").text
        except Exception as ex:
            flag = None
        if not flag:
            results.append(
                {'name': name, 'id': id, 'price': price, 'promo_price': promo_price, 'brand': brand})

driver.close()

df = pd.DataFrame(data=results)
# df.to_excel("result.xlsx", sheet_name="Sheet1")
df.to_csv('out.csv')

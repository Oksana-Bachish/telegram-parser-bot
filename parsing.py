import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

def get_parsing():
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    browser = webdriver.Chrome(options=chrome_options)

    brands_data = {
        'samsung': [],
        'iphone': [],
        'xiaomi': []
    }
    page = 1

    while True:
        print(f'Parsing {page}...')
        url = f'https://www.777555.by/elektronika/telefoniya_i_svyaz/smartfony/page{page}/'

        browser.get(url)

        # Явное ожидание появления карточек
        try:
            WebDriverWait(browser, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".catalog-item"))
            )
        except TimeoutException:
            print(f"На странице {page} карточки не найдены.")
            break

        soup = BeautifulSoup(browser.page_source, 'lxml')
        products = soup.find_all('div', class_='catalog-item')

        for product in products:
            title_tag = product.find('div', class_='catalog-item-title')
            if not title_tag:
                continue

            title_link = title_tag.find_next()
            if not title_link:
                continue

            prod_name = title_link.text.strip().lower()

            if 'samsung' in prod_name:
                brand = 'samsung'
            elif 'iphone' in prod_name:
                brand = 'iphone'
            elif 'xiaomi' in prod_name:
                brand = 'xiaomi'
            else:
                continue

            price = product.find('div', class_='catalog-item-price')
            discount_price = product.find('div', class_='catalog-item-pricemini')

            brands_data[brand].append({
                'link': title_link.get('href'),
                'prod_name': title_link.text.strip(),
                'price': price.text.strip() if price else None,
                'discount_price': discount_price.text.strip() if discount_price else None
            })

        if page > 1:
            if not soup.find('li', class_='next_page').find_next('li', class_='next_page'):
                break
        page += 1

    browser.quit()
    write_json(brands_data)


def write_json(data):
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'json_files')
    os.makedirs(base_path, exist_ok=True)

    for brand, items in data.items():
        file_path = os.path.join(base_path, f'{brand}.json')
        print(f'write_json {file_path}')
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(items, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    get_parsing()

import requests
import configparser
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('config.ini')


CHROME_DRIVER = config['DEFAULT']['CHROME_DRIVER_PATH']


def getProducts():
    products = {}
    browser = webdriver.Chrome()
    browser.get("https://www.jumbo.com.ar/almacen/snacks/snacks")
    time.sleep(1)

    soup = BeautifulSoup(page.content, 'html.parser')
    elem = browser.find_element_by_tag_name("body")
    no_of_pagedowns = 100 #better be safe than sorry

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(5)
        no_of_pagedowns-=1

    return



getProducts()


def a():
    categories = soup.find('div', class_='col-xs-12 col-sm-4 seccion-footer').find_all('a', class_='btn-footer', href=True)

    for category in categories:
        url = category['href']
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        sub_categories = soup.find('div', class_='col-xs-12 col-sm-4 columna-subcategorias').find_all('a', class_='btn-footer', href=True)
        for sub_categorie in sub_categories:
            url = sub_categorie['href']
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            names = soup.find_all('h2', class_='product-item__name')
            prices = soup.find_all('span', class_='product-prices__value product-prices__value--best-price')

            for i in range(0, len(names)):
                products[names[i].text.replace('\n','')] = prices[i].text.replace('$ ','').replace(',','.')

    return products

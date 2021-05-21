import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def getProducts():
    products = {}

    url = 'https://www.jumbo.com.ar/almacen/snacks/snacks'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    categories = soup.find('div', class_='col-xs-12 col-sm-4 seccion-footer').find_all('a', class_='btn-footer', href=True)

    for category in categories:
        url = category['href']
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        sub_categories = soup.find('div', class_='col-xs-12 col-sm-4 columna-subcategorias').find_all('a', class_='btn-footer', href=True)
        for sub_categorie in sub_categories:
            url = sub_categorie['href']+'?PS=99999'
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            names = soup.find_all('h2', class_='product-item__name')
            prices = soup.find_all('span', class_='product-prices__value product-prices__value--best-price')

            for i in range(0, len(names)):
                products[names[i].text.replace('\n','')] = prices[i].text.replace('$ ','').replace(',','.')


    for product,price in products.items():
        print(product,price)

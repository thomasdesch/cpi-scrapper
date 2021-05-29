import requests
import re
import configparser
from Product import Product
from time import sleep
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from math import ceil



config = configparser.ConfigParser()
config.read('config.ini')

class Jumbo:
  def __init__(self):
      pass

  def searchProduct(self, product, limit=-1, cheapest=False, expensive=False):
      products = []
      #load link and open browser
      browser = webdriver.Chrome()
      browser.get(config['SEARCH']['JUMBO']+product)
      sleep(5)

      soup = BeautifulSoup(browser.page_source, 'html.parser')

      number_of_pages = ceil(int(re.findall(r'[0-9]+', soup.find('span', class_='amount').text)[0])/18)
      i = 0
      while i < number_of_pages:
          element = browser.find_element_by_tag_name("body")
          element.send_keys(Keys.END)

          sleep(3)
          i+=1

      soup = BeautifulSoup(browser.page_source, 'html.parser')

      products_names = soup.find_all('a', class_='product-item__name')
      products_brands = soup.findAll('div', class_='product-item__brand')
      products_prices = soup.find_all('div', class_='product-prices__price product-prices__price--regular-price')


      cheapest_product = None
      for i in range(0,len(products_names)):


          p = Product()
          p.name = products_names[i].text.replace('\n','')
          p.price = float(re.findall(r'[0-9]+', products_prices[i].text)[0])
          p.brand = products_brands[i].text
          #p.weight = re.findall(r'[0-9]+', p.name)[0]
          #p.price_per_1000 = ((1000*p.price)/p.weight)
          if cheapest:
              if i==0:
                  cheapest_product = p
              if p.price_per_1000<cheapest_product.price_per_1000:
                  cheapest_product=p
          else:
              products.append(p)

      browser.quit()
      if cheapest:
          return cheapest_product
      else:
          return products


  def getProducts(self):
      products = {}

      url = config['DEFAULT']['JUMBO']
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
                  products[names[i].text.replace('\n','')] = float(prices[i].text.replace('$ ','').replace(',','.'))
      return products


class Dia():
    def __init__(self):
        pass

    def searchProduct(self, product, cheapest=False, Dia_Products_Only = False):
        products = []
        #open browser
        browser = webdriver.Chrome()
        browser.get(config['SEARCH']['DIA']+product)
        sleep(5)
        #finds button to click (to show more products)
        element = browser.find_element_by_class_name("viewMoreProds")
        #clicks until the button dissapears
        while True:
            try:
                ActionChains(browser).click(element).perform()
                sleep(1.5)
            except NoSuchElementException:
                break
            except ElementNotInteractableException:
                break

        html = browser.page_source
        sleep(2)
        #load html source code into BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        #Get all the names, prices
        products_names = soup.find_all('div', class_='product-name')
        products_prices = soup.find_all('span', class_='best-price')
        products_brands = soup.find_all('div', class_='marca')

        cheapest_product = None
        #control variable for finding the cheapest nad Dia product
        j = 0

        for i in range(0, len(products_names)):
            p = Product()
            p.name = products_names[i].find('a').text.replace('\n','')
            p.price = float(products_prices[i].text.replace('$ ','').replace(',','.'))
            p.weight = re.findall(r'[0-9]+', p.name)[0]
            p.price_per_1000 = ((1000*p.price)/p.weight)
            p.brand = products_brands[i].text

            p.name = products_names[i].find('a').text.replace('\n','')

            if Dia_Products_Only:
                if p.brand=='DIA':
                    if cheapest:
                        if j==0:
                            cheapest_product = p
                        if p.price_per_1000<cheapest_product.price_per_1000:
                            cheapest_product=p
                        j+=1
                    else:
                        products.append(p)


            elif cheapest:
                if i==0:
                    cheapest_product = p
                if p.price_per_1000<cheapest_product.price_per_1000:
                    cheapest_product=p

            else:
                products.append(p)
        if cheapest:
            return cheapest_product
        else:
            return products




    def getProducts(self, cheapest=False, expensive=False, Dia_Products_Only = False):
        products = []
        browser = webdriver.Chrome()
        browser.get(config['DEFAULT']['DIA '])
        sleep(5)

        element = browser.find_element_by_class_name("vtex-button__label flex items-center justify-center h-100 ph5")
        products_names = soup.find_all('div', class_='product-name')
        products_prices = soup.find_all('span', class_='best-price')

        for name in products_names:
            name = name.find('h3').find('a').get('title')

        for i in range(0, len(products_names)):
            p = Product()
            p.name(products_names[i].text.replace('\n',''))
            p.price(float(products_prices[i].text.replace('$ ','').replace(',','.')))



        try:
            while True:
                ActionChains(browser).click(browser.find_element_by_class_name("viewMoreProds")).perform()
                sleep(1.5)
        except NoSuchElementException:
            pass
        except ElementNotInteractableException:
            pass

        html = browser.page_source
        sleep(2)
        soup = BeautifulSoup(html, 'html.parser')

        products_names = soup.find_all('div', class_='product-name')
        products_prices = soup.find_all('span', class_='best-price')

        for name in products_names:
            name = name.find('h3').find('a').get('title')

        for i in range(0, len(products_names)):
            products[products_names[i].text.replace('\n','')] = float(products_prices[i].text.replace('$ ','').replace(',','.'))

        return products


class CotoDigital():
    def __init__(self):
        pass



    def searchProduct(self, product: str, limit=-1, cheapest=False, expensive=False):
        products = []
        #load link and open browser
        browser = webdriver.Chrome()
        browser.get(config['SEARCH']['COTO_DIGITAL'])
        sleep(3)
        search_bar = browser.find_element_by_id("atg_store_searchInput")
        search_bar.send_keys(product)
        #Now you can simulate hitting ENTER:
        sleep(5)
        #search_bar.send_keys(Keys.ENTER)
        search_bar.submit()


        soup = BeautifulSoup(browser.page_source, 'html.parser')
        page_count = len(soup.find('div', class_='atg_store_pagination').find_all('li'))-1
        current_page_index = 1
        next_page_url = self._getNextPageURL(soup.find('div', class_='atg_store_pagination').find_all('li', class_=True))
        cheapest_product = None
        print('PAGE COUNT:', page_count)
        while current_page_index < page_count:
            print('PAGE COUNT:', page_count, 'CURRENT PAGE:', current_page_index)
            products_names = soup.find_all('span', class_='span_productName')

            for i in range(0,len(products_names)):
                products_names[i] = products_names[i].find('div', class_="descrip_full").text.replace('\n','')

                #products_brands = soup.findAll('div', class_='product-item__brand')
                products_prices = soup.find_all('div', class_='leftList')
                products_prices_per_1000 = soup.find_all('span', class_='unit')




            for i in range(0,len(products_names)):



                p = Product()

                p.name = products_names[i]
                p.price = float(re.findall(r'[0-9]+', products_prices[i].text)[0])
                #p.brand = products_brands[i].text
                #p.weight = re.findall(r'[0-9]+', p.name)[0]
                p.price_per_1000 = float(products_prices_per_1000[i].text
                .replace('\n','')
                .replace('\t','')
                .replace('$','')
                .replace('.','')
                .replace(',','.')
                .replace('Precio por 1 Kilo escurrido:','')
                .replace('Precio por 1 Kilo :',''))
                p.name = products_names[i]
                if cheapest:
                    if i==0:
                        cheapest_product = p
                    if p.price_per_1000<cheapest_product.price_per_1000:
                        cheapest_product=p
                else:
                    products.append(p)


            browser.get(next_page_url)
            sleep(3)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            current_page_index+=1











        browser.quit()
        if cheapest:
            return cheapest_product
        else:
            return products

    def getProducts(self):
        products = {}
        browser = webdriver.Chrome()
        browser.get(config['DEFAULT']['COTO_DIGITAL'])
        sleep(5)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        products_names = soup.find_all('span', class_='span_productName')
        products_prices = soup.find_all('span', class_='atg_store_newPrice')

        for i in range(0,len(products_names)):
            products_names[i] = products_names[i].find('div').find('div').text.replace('\n','')



        for i in range(0,len(products_prices)):
            temp_price =products_prices[i].text
            temp_price=temp_price.replace('$','').replace(',','.').replace('\n','').replace('\t','').replace('PRECIO CONTADO','')
            products_prices[i] = float(temp_price)

        for i in range(0, len(products_names)):
            products[products_names[i]] = products_prices[i]

        i = 0
        for x,y in products.items():
            print(i,x,y)
            i+=1




        return products




    def _getNextPageURL(self, pages_object):

        for i in range(0, len(pages_object)):
            if pages_object[i]['class'][-1] == 'active':
                return "https://www.cotodigital3.com.ar"+(pages_object[i+1].find('a', href=True)['href'])





        return



class Carrefour():
    def __init__(self):
        pass

    def searchProduct(self, product, cheapest=False):
        products = []
        cheapest_product = None
        #open browser
        browser = webdriver.Chrome()
        browser.get(config['SEARCH']['CARREFOUR'])
        #NEEDS TO MAX WINDOW OR ADD A TRY CATCH FOR THE ID
        sleep(10)
        #gets the total number of pages to get the number of clicks



        search_bar = browser.find_element_by_id("downshift-0-input")
        search_bar.send_keys(product)
        #Now you can simulate hitting ENTER:

        search_bar.send_keys(Keys.ENTER)
        #inputElement.submit()
        sleep(3)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            number_of_pages = soup.find('span', class_='lyracons-search-result-1-x-showingProductsCount b').text.replace('de',',').split(",")

            number_of_pages = ceil(int(number_of_pages[1])/int(number_of_pages[0]))
            #clicks until the button dissapears
            for page_number in range(1,number_of_pages+1):
                if page_number == 1:
                    browser.get(browser.current_url+"&page="+str(page_number))
                else:
                    browser.get(browser.current_url.replace('&page='+str(page_number-1),'&page='+str(page_number)))

                sleep(3)
                element = browser.find_element_by_tag_name("body")
                element.send_keys(Keys.END)
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                products_names = soup.findAll('span', class_='vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body')
        except (AttributeError, IndexError) as e:
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                products_names = soup.findAll('span', class_='vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body')



        for name in products_names:
                print(name.text)


    def getProducts(self, quantity=5):
        products = {}
        browser = webdriver.Chrome()
        browser.get(config['DEFAULT']['CARREFOUR'])
        sleep(10)
        html = browser.page_source

        soup = BeautifulSoup(html, 'html.parser')
        #
        number_of_pages = soup.find('span', class_='lyracons-search-result-1-x-showingProductsCount b').text.replace('de',',').split(",")
        number_of_pages = ceil(int(number_of_pages[1])/int(number_of_pages[0]))

        products_names = soup.findAll('span', class_='vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body')

        for page_number in range(2,number_of_pages):
            browser.get(config['DEFAULT']['CARREFOUR']+"?page="+str(page_number))
            sleep(10)
            html = browser.page_source



        return products

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

def _getNullProduct():
   p = Product()
   p.name = 'N/A'
   p.price = 0
   p.weight = 0
   p.price_per_1000 = 0
   return p

class Jumbo:
  def __init__(self):
      pass



  def searchProduct(self, product : str, limit=-1, category : str = None, cheapest=False, expensive=False):
      products = []
      #load link and open browser
      browser = webdriver.Chrome()

      if category != None:
          browser.get(config['DEFAULT']['JUMBO']+'/'+category+'/'+product)
      else:
          browser.get(config['SEARCH']['JUMBO']+product)


      sleep(5)

      soup = BeautifulSoup(browser.page_source, 'html.parser')


      try:
          number_of_pages = ceil(int(re.findall(r'[0-9]+', soup.find('span', class_='amount').text)[0])/18)
          i = 0
          while i < number_of_pages:
              element = browser.find_element_by_tag_name("body")
              element.send_keys(Keys.END)

              sleep(3)
              i+=1

          #loads new source code
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
      except AttributeError:
          p = Product()
          p.name = 'N/A'
          p.price = 0
          p.weight = 0
          p.price_per_1000 = 0



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

    def searchProduct(self, product, category : str = None,   cheapest=False, Dia_Products_Only = False):
        products = []
        #open browser
        browser = webdriver.Chrome()
        try:
            if category != None:

                browser.get(config['SEARCH']['DIA']+'/'+category+'/'+product)
                sleep(5)
                element = browser.find_element_by_class_name("viewMoreProds")

            else:

                browser.get(config['SEARCH']['DIA']+'/'+product)

                sleep(5)
                element = browser.find_element_by_class_name("viewMoreProds")
        except NoSuchElementException:
            try:

                browser.get(config['SEARCH']['DIA']+'/'+product)
                sleep(5)
                element = browser.find_element_by_class_name("viewMoreProds")
            except NoSuchElementException:
                return _getNullProduct()





        #finds button to click (to show more products)

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
            try:
                p.weight = re.findall(r'(\d+)(?!.*\d)', p.name)[0]
            except IndexError:
                p.weight = 1

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
        browser.quit()
        if cheapest:
            return cheapest_product
        else:
            return products

class Coto():
    def __init__(self):
        pass



    def searchProduct(self, product: str, category : str = None, limit=-1, cheapest=False, expensive=False):
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
        try:
            page_count = len(soup.find('div', class_='atg_store_pagination').find_all('li'))-1
            next_page_url = self._getNextPageURL(soup.find('div', class_='atg_store_pagination').find_all('li', class_=True))
        except AttributeError:
            page_count = 1




        cheapest_product = None
        print('PAGE COUNT:', page_count)
        for page in range(0,page_count):

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




                try:
                    p.price_per_1000 = float(products_prices_per_1000[i].text
                    .replace('\n','')
                    .replace('\t','')
                    .replace('$','')
                    .replace('.','')
                    .replace(',','.')
                    .replace(':','')
                    .replace('Precio por 1 Kilo escurrido','')
                    .replace('Precio por 1 Kilo','')
                    .replace('Precio por 1 Litro','')
                    .replace('Precio por 1 Kilogramo','')
                    .replace('Precio por 1 Kilogramo escurrido','')
                    .replace('gramo escurrido','')
                    .replace('gramo','')
                    .replace('Precio por 100 Mililitros','')
                    .replace('Precio por 100 Gramos','')
                    .replace('escurridos','')
                    .replace('','')) #of course this is not ok but doing the regex is not worth it ValueError:
                except ValueError:
                    p.price_per_1000 = p.price








                p.name = products_names[i]
                if cheapest:
                    if i==0:
                        cheapest_product = p
                    if p.price_per_1000<cheapest_product.price_per_1000:
                        cheapest_product=p
                else:
                    products.append(p)

            if (page+1)<page:
                browser.get(next_page_url)
                sleep(3)
                soup = BeautifulSoup(browser.page_source, 'html.parser')







        browser.quit()
        if cheapest:
            return cheapest_product
        else:
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
        browser.maximize_window()

        sleep(10)




        search_bar = browser.find_element_by_id("downshift-0-input")
        search_bar.send_keys(product)
        #Now you can simulate hitting ENTER:

        search_bar.send_keys(Keys.ENTER)
        #inputElement.submit()
        sleep(3)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        products_names, products_prices_int, products_prices_decimal = [],[],[]
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
                #8 bc doing 1080/300 doesnt work
                for x in range(0,8):
                    browser.execute_script('window.scrollBy(0,300);')
                    sleep(0.3)
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')

                products_names = products_names+soup.find_all('span', class_='vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body')
                products_prices_int = products_prices_int+soup.find_all('span', class_='lyracons-carrefourarg-product-price-1-x-currencyInteger')
                products_prices_decimal = products_prices_decimal+soup.find_all('span', class_='lyracons-carrefourarg-product-price-1-x-currencyFraction')
        #if there is no element to calculate the number of pages
        except (AttributeError, IndexError) as e:
                sleep(5)
                #8 bc doing 1080/300 doesnt work
                for x in range(0,8):
                    browser.execute_script('window.scrollBy(0,300);')
                    sleep(0.3)

                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')

                products_names = soup.find_all('span', class_='vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body')
                products_prices_int = soup.find_all('span', class_='lyracons-carrefourarg-product-price-1-x-currencyInteger')
                products_prices_decimal = soup.find_all('span', class_='lyracons-carrefourarg-product-price-1-x-currencyFraction')

        for i in range(0, len(products_names)):
            p = Product()
            p.name = products_names[i].text
            p.price = int(products_prices_int[i].text)+int(products_prices_decimal[i].text)/100
            products.append(p)

        return products

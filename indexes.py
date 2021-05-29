import pandas as pd
import math

class WrongTypeExeception(Exception):
    pass


def getTotalBasicBasket(bfb, home=1):
    if home==1:
        home = 2.46
        pass
    elif home==2:
        home = 3.09
        pass
    elif home==3:
        home = 3.25
        pass
    else:
        raise WrongTypeExeception('Home must be beetween 1-3')

    pass

#dia y precios cuidados

def getTotalExpenses(arr):
    pass

def getEngelCofficent(total_expenses,food_expenses):
    return food_expenses/total_expenses
    pass

def getBasicFoodBasketProducts(arr):
    df = pd.read_excel (r'Basic_Basket.xlsx')
    pass

def getChepeastProduct(products):
    cheapestProduct = products[0]
    for product in products:
        if product.price<cheapestProduct.price:
            cheapestProduct = product
    return cheapestProduct

def castUnit(raw_unit):
    pass




def getBasicFoodBasketByStore(store, cheapest=False, expensive=False):
    df = pd.read_excel (r'Basic_Basket.xlsx')
    basic_food_basket = {}
    for i in range(0,len(df['Componente'])):
        name = df['Componente'][i]
        unit = float((df['Unidades'][i]).replace('g','').replace('cc',''))/1000        
        products_include = str(df['Productos que se incluyen'][i]).split(",")
        if products_include[0]=='nan':
            if cheapest:
                temp_p = getChepeastProduct(store.searchProduct(name))
                print(temp_p.name, temp_p.price)
                basic_food_basket[name] = temp_p.price_per_1000*unit



            pass
        else:
            product_basket = []
            for p in df['Productos que se incluyen'][i].split(","):
                if cheapest:
                    product_basket.append(getChepeastProduct(store.searchProduct(p)))

            basic_food_basket[name]=product_basket



    pass

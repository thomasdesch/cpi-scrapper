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


def getTotalExpenses(arr):
    pass

def getEngelCofficent(total_expenses,food_expenses):
    return food_expenses/total_expenses
    pass


def getBasicFoodBasketByStore(store, cheapest=False, expensive=False):
    xls = pd.ExcelFile('Basic_Basket.xlsx')

    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    basic_food_basket_categories_df = pd.read_excel(xls, sheet_name=xls.sheet_names[1])


    basic_food_basket = []
    sum_basket = 0
    for i in range(0,len(df['Componente'])):
        category = basic_food_basket_categories_df[store.__class__.__name__][i]

        name = df['Componente'][i]
        unit = float(str((df['Unidades'][i])).replace('g','').replace('cc',''))/1000
        products_include = str(df['Productos que se incluyen'][i]).split(",")
        if products_include[0]=='nan':
            if cheapest:
                p = store.searchProduct(name, cheapest=True, category=category)
                basic_food_basket.append(p)




        else:

            for p_name in df['Productos que se incluyen'][i].split(","):
                if cheapest:
                    print('CURRENT PRODUCT:', p_name)
                    p = store.searchProduct(p_name, cheapest=True)
                    basic_food_basket.append(p)            

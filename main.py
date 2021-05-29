import Stores
from indexes import getBasicFoodBasketByStore






def a():
    print('Select store:')
    print('(1) Carrefour')
    print('(2) Coto')
    print('(3) Dia')
    print('(4) Jumbo')
    print('(0) Go back')
    option = int(input())
    if option == 1:
        product_name = (input('Insert product name\n'))
        print('(1) Search "'+product_name+'"')
        print('(2) Show options')
        print('(3) Go back')
        option = int(input())
        if option == 1:
            Dia = Stores.Dia()
            product = Dia.searchProduct(product_name)
            return

def main():
    print('Select option:')
    print('(1) Search scrap')
    print('(2) Scrap store')
    print('(0) Exit')

    option = int(input())

    while option != 0:
        if option==1:
            a()






if __name__ == '__main__':
    pass

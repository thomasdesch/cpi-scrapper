from Stores import Jumbo, Dia, Coto, Carrefour
from indexes import getBasicFoodBasketByStore


Store = Dia()
#p = Store.searchProduct('carnaza comun','Almacén', cheapest=True)
#print('price $', p.price)
getBasicFoodBasketByStore(Store, cheapest=True)
